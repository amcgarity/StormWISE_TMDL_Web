# -*- coding: utf-8 -*-
"""
Created on Wed Aug  3 19:34:18 2016

@author: arthur
"""

def benefit_slopes(inYamlDoc):
        I = inYamlDoc['I']
        J = inYamlDoc['J']
        K = inYamlDoc['K']
        KONJ = inYamlDoc['KONJ']
        T = inYamlDoc['T']
        cost = inYamlDoc['cost']
        export = inYamlDoc['export']
        eta = inYamlDoc['eta']
        s = {}  # will be a dictionary of dictionaries
        for i in I:  # generate decision variable dictionary
            jDict = {}
            for j in J: 
                kDict = {}
                if KONJ[j] != None:
                    for k in K:                   
                        tDict = {}
                        if k in KONJ[j]:
                            for t in T:
                                tDict[t] = eta[t][k][i]*export[t][j]/cost[k][j]
                        else:
                            for t in T:
                                tDict[t] = 0.0
                        kDict[k] = tDict
                else:
                    for k in K:
                        tDict = {}
                        for t in T:
                            tDict[t] = 0.0
                        kDict[k] = tDict                 
                jDict[j] = kDict
            s[i] = jDict
        return s
