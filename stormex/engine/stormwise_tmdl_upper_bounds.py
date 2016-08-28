# -*- coding: utf-8 -*-
"""
Created on Wed Aug  3 19:30:48 2016

@author: arthur
"""

def upper_bounds(inYamlDoc):
        I = inYamlDoc['I']
        J = inYamlDoc['J']
        K = inYamlDoc['K']
        KONJ = inYamlDoc['KONJ']
        cost = inYamlDoc['cost']
        f = inYamlDoc['f']
        area = inYamlDoc['area']
        u = {}  # will be a dictionary of dictionaries
        for i in I:  # generate decision variable dictionary
            jDict = {}
            for j in J: 
                kDict = {}
                if KONJ[j] != None:
                    for k in K:                   
                        if k in KONJ[j]:
                            kDict[k] = cost[k][j]*f[k][j][i]*area[j][i]
                        else:
                            kDict[k] = 0.0
                else:
                    for k in K:
                        kDict[k] = 0.0
                jDict[j] = kDict
            u[i] = jDict
        return u