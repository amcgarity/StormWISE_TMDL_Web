# -*- coding: utf-8 -*-
"""
Created on Wed Aug  3 18:53:23 2016

@author: arthur
"""

from stormwise_tmdl_upper_bounds import upper_bounds
from stormwise_tmdl_benefit_slopes import benefit_slopes

def generate_ampl_dat_file(inYamlDoc):
    ampl = ""   # string containing ampl code to be returned when filled
    upperBounds = upper_bounds(inYamlDoc)
    benefitSlopes = benefit_slopes(inYamlDoc)
    I = inYamlDoc['I']
    J = inYamlDoc['J']
    K = inYamlDoc['K']
    KONJ = inYamlDoc['KONJ']  
    T = inYamlDoc['T']
    sets = ['I','J','K','T'] # I = zone, J = landuse, K = GItype, T = benefit

    for s in sets:  
        ampl = ampl + "set %s := " % s 
        x = inYamlDoc[s]
        for h in sorted(x):
            ampl += "%s " % h
        ampl += ";\n"        
    setsonset = {'KONJ': ('K','J')}
    for s in sorted(setsonset):
        s1 = setsonset[s][1]
        x = inYamlDoc[s1]
        for h in sorted(x):
            ampl = ampl + "set %s[%s] := " % (s,h)
            elements = inYamlDoc[s][h]
            if elements == None:
                value = "" 
                ampl = ampl + "%s;\n" % value 
            else:
                for g in sorted(elements):
                    value = g
                    ampl += "%s " % value
                ampl += " ;\n"
    # process upper bound data:
    ampl += "param u: "
    for k in sorted(K):
        ampl += "%s " % k
    ampl += " :=\n"
    for i in sorted(I):
        for j in sorted(J):
            ampl += "  %s %s" % (i,j)
            if KONJ[j] != None:
                for k in sorted(K):
                    if k in KONJ[j]:
                        ampl += "  %10.2f" % upperBounds[i][j][k]
                    else:
                        ampl += "  %10s" % '.'
            else:
                for k in sorted(K):
                    ampl += "  %10s" % '.'
            ampl += "\n"
    ampl += ";\n"
        
    # process benefit slope data:
    ampl += "param s: "
    for t in sorted(T):
        ampl += "%s " % t
    ampl += " :=\n"
    for i in sorted(I):
        for j in sorted(J):
          
            if KONJ[j] != None:
                for k in sorted(K):
                    if k in KONJ[j]:
                        ampl += "  %s %s %s" % (i,j,k)
                        for t in sorted(T):
                            ampl += "  %15.14f" % benefitSlopes[i][j][k][t]
                        ampl += "\n"
    ampl += ";\n"        
    return ampl
'''
import yaml  
def main(inYamlFile):
    with open(inYamlFile, 'r') as fin:
        inYamlDoc = yaml.load(fin)
        ampl = generate_ampl_dat_file(inYamlDoc)
    with open('stormwise_tmdl.dat', 'w') as fout:     
        fout.write(ampl)
        fout.close()
main('wingohocking.yaml')
'''