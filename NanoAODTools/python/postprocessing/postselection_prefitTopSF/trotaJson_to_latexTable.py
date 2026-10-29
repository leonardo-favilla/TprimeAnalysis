#!/usr/bin/env python3
"""Generate LaTeX tables from Trota scale-factor JSON files.

Supported JSON structures
------------------------
{
  "Mixed": {
    "Tight": {
      "topmatched": {
        "pass": {"value": [...], "error": [...]},
        "fail": {"value": [...], "error": [...]}
      }
    },
    "Loose": {...},
    "LooseButNotTight": {...}
  },
  "Resolved": {...},
  "Merged": {...}
}

For the new structure, the era is inferred from the filename (for example
TrotaScaleFactors_2023_Mixed.json -> 2023) unless --era is provided.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Iterable

DEFAULT_CATEGORIES      = ["Resolved", "Mixed", "Merged"]
DEFAULT_MATCHING_ORDER  = ["topmatched", "nonmatched", "other"]
DEFAULT_CHANNELS        = ["pass", "fail"]
DEFAULT_BIN_LABELS      = ["[0,200[", "[200,400[", "[400,600[", "[600,1000)", "[0,400[", "[400,1000)"]   # event categories of extract_ScaleFactors.py
LATEX_NL                = r"\\"
FILENAME_PREFIX         = "TrotaScaleFactors_"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Convert a Trota scale-factor JSON into LaTeX tables."
    )
    parser.add_argument("input_json", help="Path to the input JSON file")
    parser.add_argument(
        "-o",
        "--output",
        help="Optional output .tex file. If omitted, print to stdout.",
    )
    parser.add_argument(
        "--categories",
        default=",".join(DEFAULT_CATEGORIES),
        help=(
            "Comma-separated category names to export. "
            f"Default: {','.join(DEFAULT_CATEGORIES)}"
        ),
    )
    parser.add_argument(
        "--working-points",
        help=(
            "Optional comma-separated list of working points to export. "
            "By default, all working points found in the JSON are exported."
        ),
    )
    parser.add_argument(
        "--bin-labels",
        default=";".join(DEFAULT_BIN_LABELS),
        help=(
            "Semicolon-separated pT bin labels. Must match the number of values in each "
            "channel. Example: [0,200[;[200,400[;[400,600[;[600,1000)"
        ),
    )
    parser.add_argument(
        "--precision",
        type=int,
        default=6,
        help="Number of digits after the decimal point. Default: 6",
    )
    parser.add_argument(
        "--era",
        help=(
            "Optional era label. For the new structure it overrides the era inferred from "
            "the filename."
        ),
    )
    parser.add_argument(
        "--standalone",
        action="store_true",
        help="Wrap the output in a minimal standalone LaTeX document.",
    )
    return parser.parse_args()


def latex_escape(text: str) -> str:
    replacements = {
        "\\": r"\textbackslash{}",
        "&": r"\&",
        "%": r"\%",
        "$": r"\$",
        "#": r"\#",
        "_": r"\_",
        "{": r"\{",
        "}": r"\}",
        "~": r"\textasciitilde{}",
        "^": r"\textasciicircum{}",
    }
    return "".join(replacements.get(ch, ch) for ch in text)


def normalize_csv(raw: str | None) -> list[str]:
    if not raw:
        return []
    items = [item.strip() for item in raw.split(",") if item.strip()]
    return items


def normalize_bin_labels(raw: str) -> list[str]:
    labels = [item.strip() for item in raw.split(";") if item.strip()]
    if not labels:
        raise ValueError("No bin labels were provided.")
    return labels


def format_float(value: float, precision: int) -> str:
    return f"{value:.{precision}f}"


def sanitize_label_component(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", text.lower()).strip("_")


def infer_era_from_filename(input_path: Path) -> str:
    stem = input_path.stem
    if stem.startswith(FILENAME_PREFIX) and len(stem) > len(FILENAME_PREFIX):
        return stem[len(FILENAME_PREFIX) :].split("_")[0]   # TrotaScaleFactors_<era>_<TopCategory>.json -> <era>
    return stem


def is_channel_payload(obj: object) -> bool:
    return isinstance(obj, dict) and any(key in obj for key in DEFAULT_CHANNELS)


def is_matching_payload(obj: object) -> bool:
    if not isinstance(obj, dict):
        return False
    return any(is_channel_payload(value) for value in obj.values())


def resolve_name(requested: str, available: Iterable[str]) -> str | None:
    mapping = {name.lower(): name for name in available}
    return mapping.get(requested.lower())


def ordered_matching_items(matching_map: dict[str, object]) -> list[tuple[str, dict]]:
    ordered: list[tuple[str, dict]] = []
    used: set[str] = set()

    for name in DEFAULT_MATCHING_ORDER:
        if name in matching_map and isinstance(matching_map[name], dict):
            ordered.append((name, matching_map[name]))
            used.add(name)

    for name, payload in matching_map.items():
        if name not in used and isinstance(payload, dict):
            ordered.append((name, payload))

    return ordered


def build_table(
    era: str,
    category: str,
    working_point: str,
    matching_map: dict[str, object],
    bin_labels: list[str],
    precision: int,
) -> str:
    lines: list[str] = []
    title = f"{era} {category} {working_point}" if working_point else f"{era} {category}"
    caption = (
        f"Trota scale factors for the {working_point} working point in the {era} {category} category."
        if working_point
        else f"Trota scale factors for the {era} {category} category."
    )

    label_parts = [
        "tab",
        "trota",
        "sf",
        sanitize_label_component(era),
        sanitize_label_component(category),
    ]
    if working_point:
        label_parts.append(sanitize_label_component(working_point))
    label = "_".join(part for part in label_parts if part)

    lines.append(r"\begin{table}[htbp]")
    lines.append(r"\centering")
    lines.append(r"\begin{tabular}{llccc}")
    lines.append(r"\hline")
    lines.append(rf"\multicolumn{{5}}{{c}}{{{latex_escape(title)}}} {LATEX_NL}")
    lines.append(r"\hline")
    lines.append(rf"Matching & Channel & $p_T$ bin & Value & Error {LATEX_NL}")
    lines.append(r"\hline")
    lines.append("")

    matching_items = ordered_matching_items(matching_map)
    for match_index, (matching, matching_data) in enumerate(matching_items):
        total_rows = 0
        for channel in DEFAULT_CHANNELS:
            payload = matching_data.get(channel)
            if isinstance(payload, dict):
                total_rows += len(payload.get("value", []))

        if total_rows == 0:
            continue

        first_row_of_matching = True
        for channel_index, channel in enumerate(DEFAULT_CHANNELS):
            channel_payload = matching_data.get(channel)
            if not isinstance(channel_payload, dict):
                continue

            values = channel_payload.get("value", [])
            errors = channel_payload.get("error", [])
            if len(values) != len(errors):
                raise ValueError(
                    f"Mismatch in '{era}/{category}/{working_point}/{matching}/{channel}': "
                    f"{len(values)} values but {len(errors)} errors."
                )
            if len(values) != len(bin_labels):
                raise ValueError(
                    f"Mismatch in '{era}/{category}/{working_point}/{matching}/{channel}': "
                    f"{len(values)} entries but {len(bin_labels)} bin labels."
                )

            channel_rows = len(values)
            for row_index, (bin_label, value, error) in enumerate(zip(bin_labels, values, errors)):
                parts: list[str] = []
                if first_row_of_matching:
                    parts.append(rf"\multirow{{{total_rows}}}{{*}}{{{latex_escape(matching)}}}")
                    first_row_of_matching = False
                else:
                    parts.append("")

                if row_index == 0:
                    parts.append(rf"\multirow{{{channel_rows}}}{{*}}{{{latex_escape(channel)}}}")
                else:
                    parts.append("")

                parts.extend(
                    [
                        bin_label,
                        format_float(float(value), precision),
                        format_float(float(error), precision),
                    ]
                )
                lines.append(" & ".join(parts) + f" {LATEX_NL}")

            has_later_channel = any(
                isinstance(matching_data.get(next_ch), dict)
                for next_ch in DEFAULT_CHANNELS[channel_index + 1 :]
            )
            if has_later_channel:
                lines.append(r"\cdashline{2-5}")

        if match_index < len(matching_items) - 1:
            lines.append(r"\hline")
            lines.append("")

    lines.append(r"\hline")
    lines.append(r"\end{tabular}")
    lines.append(rf"\caption{{{latex_escape(caption)}}}")
    lines.append(rf"\label{{{label}}}")
    lines.append(r"\end{table}")
    return "\n".join(lines)


def build_document(body: str) -> str:
    return "\n".join(
        [
            r"\documentclass{article}",
            r"\usepackage{multirow}",
            r"\usepackage{arydshln}",
            r"\begin{document}",
            body,
            r"\end{document}",
        ]
    )


def extract_tables_from_old_structure(
    data: dict[str, object],
    categories_requested: list[str],
    bin_labels: list[str],
    precision: int,
) -> tuple[list[str], list[str]]:
    tables: list[str] = []
    warnings: list[str] = []

    for era, era_payload in data.items():
        if not isinstance(era_payload, dict):
            warnings.append(f"Skipping '{era}' because its content is not a dictionary.")
            continue

        for category_req in categories_requested:
            category_name = resolve_name(category_req, era_payload.keys())
            if category_name is None:
                warnings.append(f"Requested category '{category_req}' was not found under era '{era}'.")
                continue

            category_payload = era_payload.get(category_name)
            if not isinstance(category_payload, dict):
                warnings.append(
                    f"Skipping '{era}/{category_name}' because its content is not a dictionary."
                )
                continue

            if not is_matching_payload(category_payload):
                warnings.append(
                    f"Skipping '{era}/{category_name}' because it does not look like a matching map."
                )
                continue

            tables.append(
                build_table(
                    era=str(era),
                    category=category_name,
                    working_point="",
                    matching_map=category_payload,
                    bin_labels=bin_labels,
                    precision=precision,
                )
            )

    return tables, warnings


def extract_tables_from_new_structure(
    data: dict[str, object],
    categories_requested: list[str],
    working_points_requested: list[str],
    bin_labels: list[str],
    precision: int,
    era: str,
) -> tuple[list[str], list[str]]:
    tables: list[str] = []
    warnings: list[str] = []

    for category_req in categories_requested:
        category_name = resolve_name(category_req, data.keys())
        if category_name is None:
            warnings.append(f"Requested category '{category_req}' was not found.")
            continue

        category_payload = data.get(category_name)
        if not isinstance(category_payload, dict):
            warnings.append(f"Skipping '{category_name}' because its content is not a dictionary.")
            continue

        available_wps = list(category_payload.keys())
        if working_points_requested:
            wp_names: list[str] = []
            for wp_req in working_points_requested:
                wp_name = resolve_name(wp_req, available_wps)
                if wp_name is None:
                    warnings.append(
                        f"Requested working point '{wp_req}' was not found under category '{category_name}'."
                    )
                else:
                    wp_names.append(wp_name)
        else:
            wp_names = available_wps

        for wp_name in wp_names:
            wp_payload = category_payload.get(wp_name)
            if not isinstance(wp_payload, dict):
                warnings.append(
                    f"Skipping '{category_name}/{wp_name}' because its content is not a dictionary."
                )
                continue
            if not is_matching_payload(wp_payload):
                warnings.append(
                    f"Skipping '{category_name}/{wp_name}' because it does not look like a matching map."
                )
                continue

            tables.append(
                build_table(
                    era=era,
                    category=category_name,
                    working_point=wp_name,
                    matching_map=wp_payload,
                    bin_labels=bin_labels,
                    precision=precision,
                )
            )

    return tables, warnings


def detect_structure(data: dict[str, object]) -> str:
    if not data:
        raise ValueError("The JSON file is empty.")

    first_value = next(iter(data.values()))
    if not isinstance(first_value, dict):
        raise ValueError("Top-level JSON values must be dictionaries.")

    if is_matching_payload(first_value):
        raise ValueError("Unsupported JSON shape: top-level matching map found.")

    nested_values = list(first_value.values())
    if nested_values and any(is_channel_payload(value) for value in nested_values):
        return "old"
    if nested_values and any(is_matching_payload(value) for value in nested_values):
        return "new"

    # Fallback: if top-level keys look like years, assume old structure.
    if all(re.fullmatch(r"\d{4}", str(key)) for key in data):
        return "old"

    raise ValueError("Could not determine whether the JSON uses the old or new structure.")


def main() -> int:
    args = parse_args()
    input_path = Path(args.input_json)

    try:
        data = json.loads(input_path.read_text())
    except FileNotFoundError:
        print(f"Error: file not found: {input_path}", file=sys.stderr)
        return 1
    except json.JSONDecodeError as exc:
        print(f"Error: invalid JSON: {exc}", file=sys.stderr)
        return 1

    if not isinstance(data, dict):
        print("Error: the top-level JSON object must be a dictionary.", file=sys.stderr)
        return 1

    try:
        categories_requested = normalize_csv(args.categories)
        if not categories_requested:
            raise ValueError("No categories were provided.")
        working_points_requested = normalize_csv(args.working_points)
        bin_labels = normalize_bin_labels(args.bin_labels)
        structure = detect_structure(data)
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    try:
        if structure == "old":
            tables, warnings = extract_tables_from_old_structure(
                data=data,
                categories_requested=categories_requested,
                bin_labels=bin_labels,
                precision=args.precision,
            )
        else:
            era = args.era or infer_era_from_filename(input_path)
            tables, warnings = extract_tables_from_new_structure(
                data=data,
                categories_requested=categories_requested,
                working_points_requested=working_points_requested,
                bin_labels=bin_labels,
                precision=args.precision,
                era=era,
            )
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    if not tables:
        print("Error: no tables were produced.", file=sys.stderr)
        for warning in warnings:
            print(f"Warning: {warning}", file=sys.stderr)
        return 1

    output_text = "\n\n".join(tables)
    if args.standalone:
        output_text = build_document(output_text)

    if args.output:
        Path(args.output).write_text(output_text)
    else:
        print(output_text)

    for warning in warnings:
        print(f"Warning: {warning}", file=sys.stderr)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
