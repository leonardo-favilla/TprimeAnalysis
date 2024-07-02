import os
import time
import optparse

usage = 'python weightedselection_v1.py'
parser = optparse.OptionParser(usage)
parser.add_option('-p', '--plot', dest='plot', default = False, action='store_true', help="make histos")
parser.add_option('-s', '--stack', dest='stack', default = False, action='store_true', help="make stack")
parser.add_option('-t', '--tprime', dest='tprime', default = False, action='store_true', help="singal=Tprime")
(opt, args) = parser.parse_args()

pt_met = [150]#[50,100, 150]
dphi= [0.6]#[0.2,0.4,0.6]
dr = [0.8]#[0.8,1.2,1.6]
ptmaxres = [300]#[200,250,300]
ptmaxmix = [500]#[400,500,600]
maxeta = [3]


dryrun = False#True
plot=opt.plot#False#True#
stack =opt.stack#True#False# 
tprime = opt.tprime
if plot:
    for met in pt_met:
        for phi in dphi:
            for r in dr:
                for ptres in ptmaxres:
                    for ptmix in ptmaxmix:
                        #for meta in maxeta:
                        command1= "python3 weightedselection_v1.py -m "+str(met)+" -p "+str(phi)+" -R "+str(r)+" -s "+str(ptres)+" -x "+str(ptmix)+""
                        #command2= "python3 weightedselection_v1.py -m "+str(met)+" -p "+str(phi)+" -R "+str(r)+" -s "+str(ptres)+" -x "+str(ptmix)+""
                        print(command1)
                        if not dryrun:os.popen(command1, "w")
                        #if not dryrun:os.popen(command2, "w")
                            #if not dryrun:time.sleep(600)
if stack:
    for met in pt_met:
        for phi in dphi:
            for r in dr:
                for ptres in ptmaxres:
                    for ptmix in ptmaxmix:
                        for meta in maxeta:
                            command1="python3 weightedselection_stack.py -m "+str(met)+" -p "+str(phi)+" -R "+str(r)+" -s "+str(ptres)+" -x "+str(ptmix)+" -e"+str(meta)
                            command2="python3 weightedselection_stack.py -m "+str(met)+" -p "+str(phi)+" -R "+str(r)+" -s "+str(ptres)+" -x "+str(ptmix)+" -e"+str(meta)+" -z"
                            if tprime:
                                command1=command1+" -t"
                                command2=command2+" -t"
                            print(command2)
                            if not dryrun:os.popen(command1, "w")
                            if not dryrun:os.popen(command2, "w")
