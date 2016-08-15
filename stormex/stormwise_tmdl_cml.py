# -*- coding: utf-8 -*-
"""
Created on Sun Aug  7 16:33:12 2016

@author: arthur

provide command line input and output for stormwise_tmdl
"""
def print_output(solutionDict):  
                
    print "Actual Benefit Totals:"      
    for t in sorted(totalsByBenefit):
        print "    %s:  %10.4f %s" % (t,totalsByBenefit[t],'fundamental units')
    
    investTotal = 0.0
    for i in sorted(I):
        for j in sorted(J):
            if KONJ[j] != None:
                for k in sorted(KONJ[j]):
                    spend = x[i][j][k]
                    investTotal += spend
    investTotalMillions = investTotal/1e6
    print "Actual Total Investment Required:   $%10.2f Million" % investTotalMillions
    # Decision Space Output:
    print "\nDecision Space Output:"
    zoneTot = {}
    luTot = {}
    giTot = {}
    for i in sorted(I):  # Compute and output total investments by zone
        zoneTot[i] = 0.0
        for j in sorted(J):
            if KONJ[j] != None:
                for k in sorted(KONJ[j]):
                    zoneTot[i] += x[i][j][k]
        zoneTotMillions = zoneTot[i]/1e6
        print '\nZone:  %s with Total investment in zone =  %10.2f Million (details below)' % (i,zoneTotMillions)
        print '\n%18s' % '',
        for k in sorted(K):
            print "%16s" % k,
        print "%18s" % 'Land Use Total'
        luZoneTot = {}
        for j in sorted(J):  # compute and output total investments by landuse
            print "%-18s" % j,
            luZoneTot[j] = 0.0
            for k in sorted(K):
                if KONJ[j] != None:
                    if k in KONJ[j]:
                        luZoneTot[j] += x[i][j][k]
                        investMillion = x[i][j][k]/1e6
                        print "%18.2f" % investMillion,
                    else:
                        print "%18.2f" % 0.0,
                else:
                    print "%18.2f" % 0.0,
            luZoneTotMillion = luZoneTot[j]/1e6
            print "%18.2f" % luZoneTotMillion
            print ''
            luTot[i] = luZoneTot
        giZoneTot = {}
        for k in sorted(K):
            giZoneTot[k] = 0.0
            for j in sorted(J):
                if KONJ[j] != None:
                    if k in KONJ[j]:
                        giZoneTot[k] += x[i][j][k]
        print "%18s" % "GI Practice Total",
        giTot[i] = giZoneTot
        for k in sorted(K):
            giTotMillion = giZoneTot[k]/1e6
            print "%18.2f" % giTotMillion,
    #print ''
    #print zoneTot
    #print luTot
    #print giTot
    '''

