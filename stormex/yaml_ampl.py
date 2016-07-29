# -*- coding: utf-8 -*-

	
def yaml_to_ampl(doc):
    sets = ['I','J','K','T'] # I = zone, J = landuse, K = GItype, T = benefit
    ampl = ""
    for s in sets:  
        ampl = ampl + "set %s := " % s 
        x = doc[s]
        for h in sorted(x):
            ampl += "%s " % h
        ampl += ";\n"        
    setsonset = {'KONJ': ('K','J')}
    for s in sorted(setsonset):
        s1 = setsonset[s][1]
        x = doc[s1]
        for h in sorted(x):
            ampl = ampl + "set %s[%s] := " % (s,h)
            elements = doc[s][h]
            if elements == None:
                value = "" 
                ampl = ampl + "%s;\n" % value 
            else:
                for g in sorted(elements):
                    value = g
                    ampl += "%s " % value
                ampl += " ;\n"
    params_1d = {'convert': 'T'}
    for p in sorted(params_1d):
        ampl = ampl + "param %s :=\n" % p
        s = params_1d[p]
        x = list(doc[s])
        for h in sorted(x):
            value = doc[p][h]
            if value == None:
                value = '.'  # Ampl data file notation for null value
            ampl = ampl + "    %s %s\n" % (h,value)
        ampl = ampl + ";\n"
    params_2d = {'cost': ('J','K'),   # specify (row,column)
                 'export': ('J','T'),
                 'area': ('I','J'),}
    for p in sorted(params_2d):
        ampl = ampl + "param %s :" % p
        s = params_2d[p]
        s0 = s[0] # rows set
        s1 = s[1] # columns set
        x = list(doc[s1])  # contains column names
        for h in sorted(x):
            ampl = ampl + " %s" % h
        ampl = ampl + " :=\n"
        y = list(doc[s0])  # contains row names
        for g in sorted(y):
            ampl = ampl + "    %s " % g
            for h in sorted(x):
                value = doc[p][h][g]
                if value == None:
                    value = '.'  # Ampl data file notation for null value
                ampl = ampl + " %s" % value
            ampl = ampl + "\n"
        ampl = ampl + ";\n"
    params_3d = {'eta': ('I','K','T'),
                 'f': ('I','J','K')}
    for p in sorted(params_3d):
        ampl = ampl + "param %s :=\n" % p
        s = params_3d[p]
        s0 = s[0] # rows set
        s1 = s[1] # columns set
        s2 = s[2] # layers set
        z = list(doc[s2])  # contains layer names
        y = list(doc[s1])  # contains row names
        x = list(doc[s0])  # contains column names
        for e in sorted(z):
            ampl = ampl + "    [*,*,%s]:" % e
            for g in sorted(y):
                ampl = ampl +  " %s" % g
            ampl = ampl + " :=\n"
            #print doc['eta']['1_volume']['1_bioswale']['1_headwaters']

            for h in sorted(x):
                ampl = ampl + "    %s" % h
                for g in sorted(y):
                    value = doc[p][e][g][h]
                    if value == None:
                        value = '.' # Ampl data file notation for null value
                    ampl = ampl + " %s" % value
            ampl = ampl + "\n"
        ampl = ampl + ";\n"
    return ampl
'''
def main():
    with open('wingohocking.yaml', 'r') as f:
        doc = yaml.load(f)
        yaml_to_ampl(doc)
        docString = yaml.dump(doc, default_flow_style=True)
        doc2 = yaml.load(docString)
        yaml_to_ampl(doc2)
        #print docString

main()
'''


