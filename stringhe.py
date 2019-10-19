import os

def processi_testbench(x, y, z):
    res = []
    res.append("\t\t" + x + " <= '1'\n\t\t" + y + " <= '0'\n\t\twait for " + z +" ns\n")
    res.append("\t\t" + x + " <= '0'\n\t\t" + y + " <= '1'\n\t\twait for " + z +" ns\n")
    res.append("\t\t" + x + " <= '1'\n\t\t" + y + " <= '1'\n\t\twait for " + z +" ns\n")
    res.append("\t\t" + x + " <= '0'\n\t\t" + y + " <= '0'\n\t\twait for " + z +" ns\n")
    return res
