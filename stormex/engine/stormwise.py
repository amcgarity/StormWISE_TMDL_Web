# -*- coding: utf-8 -*-
"""
stormwise.py
takes a stormwise input file in YAML format
converts it to an AMPL dat file
and then runs AMPL on the dat file to generate stormwise output
"""
import yaml
from subprocess import call
from yaml_ampl import yaml_to_ampl
from ben_dat import make_dat
def storm(bens):
    ampl_ben = make_dat(bens)
    with open('benefits.dat', 'w') as outfile:
        outfile.write(ampl_ben)
        outfile.close()
    with open('wingohocking.yaml', 'r') as fin:
        doc = yaml.load(fin)
        ampl = yaml_to_ampl(doc)
        # store the structure of the problem as found in the YAML file
        I = doc['I']
        J = doc['J']
        K = doc['K']
        KONJ = doc['KONJ']
        KONJ2 = doc['KONJ2']
        T = doc['T']
        convert = doc['convert']
    with open('wingohocking.dat', 'w') as fout:     
        fout.write(ampl)
        fout.close()
    call(["/var/lib/ampl/ampl","min_cost.run"])
    with open('min_cost.yaml', 'r') as fin:
        solution = yaml.load(fin)
        x = solution['x']
        u = solution['u']
        s = solution['s']
        
        # PRINT OUT RESULTS TO CONSOLE:
        benefitUnits = {'1_volume': 'Million Gallons', '2_sediment': 'Tons',
                        '3_nitrogen': 'Pounds', '4_phosphorous': 'Pounds'}        
        print ""
        maxBenefitTotal = {}
        for t in T:
            maxtot = 0.0
            for i in sorted(I):
                for j in sorted(J):
                    if KONJ[j] != None:
                        for k in sorted(KONJ[j]):
                            spend = u[i][j][k]
                            maxtot += convert[t]*s[i][j][k][t]*spend
            maxBenefitTotal[t] = maxtot
        print "Maximum Benefit Totals:"      
        for t in sorted(maxBenefitTotal):
            print "    %s:  %10.4f %s" % (t,maxBenefitTotal[t],benefitUnits[t])

        maxInvestTotal = 0.0
        for i in sorted(I):
            for j in sorted(J):
                if KONJ[j] != None:
                    for k in sorted(KONJ[j]):
                        spend = u[i][j][k]
                        maxInvestTotal += spend
        maxInvestMillions = maxInvestTotal/1e6
        print "Maximum Total Investment Required:   $%10.2f Million" % maxInvestMillions


        print ""
        benefitTotal = {}
        for t in T:
            tot = 0.0
            for i in sorted(I):
                for j in sorted(J):
                    if KONJ[j] != None:
                        for k in sorted(KONJ[j]):
                            spend = x[i][j][k]
                            tot += convert[t]*s[i][j][k][t]*spend
            benefitTotal[t] = tot
        print "Actual Benefit Totals:"      
        for t in sorted(benefitTotal):
            print "    %s:  %10.4f %s" % (t,benefitTotal[t],benefitUnits[t])
        
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
        for i in sorted(I):  # Compute and output total investments by zone
            zoneTot = 0.0
            for j in sorted(J):
                if KONJ[j] != None:
                    for k in sorted(KONJ[j]):
                        zoneTot += x[i][j][k]
            zoneTotMillions = zoneTot/1e6
            print '\nZone:  %s with Total investment in zone =  %10.2f Million (details below)' % (i,zoneTotMillions)
            print '\n%18s' % '',
            for k in sorted(K):
                print "%16s" % k,
            print "%18s" % 'Land Use Total'
            #giLuTotalMillion = {}
            for j in sorted(J):  # compute and output total investments by landuse
                #giLuTotalMillion[j] = 0.0
                print "%-18s" % j,
                giTot = 0.0
                for k in sorted(K):
                    if KONJ[j] != None:
                        if k in KONJ[j]:
                            giTot += x[i][j][k]
                            investMillion = x[i][j][k]/1e6
                            #giLuTotalMillion[j] += investMillion
                            print "%18.2f" % investMillion,
                        else:
                            print "%18.2f" % 0.0,
                    else:
                        print "%18.2f" % 0.0,
                giTotMillion = giTot/1e6
                print "%18.2f" % giTotMillion
                print ''

    return investTotalMillions

