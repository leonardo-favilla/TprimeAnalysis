import keras
import numpy as np
from datetime import datetime

model = keras.models.load_model("DNN_phase2_test2.h5")
m = np.zeros((20,2))
fj = np.zeros((20,12))
j = np.ones((20, 3, 8))

t0 = datetime.now()
x1 = model.predict({"fatjet":fj, "jet": j,  "top_mass": m}).flatten().tolist()
t1 = datetime.now()
print(x1)
print("time execution = ", t1-t0)
t0 = datetime.now()
x2 = model({"fatjet":fj, "jet": j,  "top_mass": m}).numpy().flatten().tolist()
t1 = datetime.now()
print(x2)
print("time execution = ", t1-t0)
