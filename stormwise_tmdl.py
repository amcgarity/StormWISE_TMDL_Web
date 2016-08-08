# -*- coding: utf-8 -*-
"""
stormwise_tmdl.py
takes a stormwise input file in YAML format
computes benefit slopes and investment upper bounds
outputs an AMPL dat file
and then runs AMPL on the dat file to generate stormwise_tmdl output
"""
import yaml
from subprocess import call
from stormwise_tmdl_ampl import generate_ampl_dat_file
from stormwise_tmdl_upper_bounds import upper_bounds
from stormwise_tmdl_benefit_slopes import benefit_slopes

def stormwise(inYamlDoc):
    ampl = generate_ampl_dat_file(inYamlDoc)
    # store the structure of the problem as found in the YAML file
    with open('stormwise_tmdl.dat', 'w') as fout:     
        fout.write(ampl)
        fout.close()
    call(["/Applications/amplide.macosx64/ampl","stormwise_tmdl.run"])
    with open('stormwise_tmdl.yaml', 'r') as fin:
        solution = yaml.load(fin)
        x = solution['x']
        I = inYamlDoc['I']
        J = inYamlDoc['J']
        K = inYamlDoc['K']
        KONJ = inYamlDoc['KONJ']
        # generate decision variable dictionary filling in zeros where necessary
        decisions = {}
        for i in I:  
            jDict = {}
            for j in J: 
                kDict = {}
                if KONJ[j] != None:
                    for k in K:                   
                        if k in KONJ[j]:
                            kDict[k] = x[i][j][k]
                        else:
                            kDict[k] = 0.0
                else:
                    for k in K:
                        kDict[k] = 0.0
                jDict[j] = kDict
            decisions[i] = jDict
        return decisions




def evaluate_solution(decisions,s,inYamlDoc):
    solutionDict = {}
    solutionDict['decisions'] = decisions
    I = inYamlDoc['I']
    J = inYamlDoc['J']
    K = inYamlDoc['K']
    T = inYamlDoc['T']

    '''
    benefitUnits = {'1_volume': 'Million Gallons', '2_sediment': 'Tons',
                    '3_nitrogen': 'Pounds', '4_phosphorous': 'Pounds'}        
    '''
    benefits = {}
    totalsByBenefit = {}
    totalsByBenefitByZone = {}
    totalsByBenefitByLanduse = {}
    totalsByBenefitByGi = {}
    benefitsByZoneByLanduseByGi = {}
    totalsByBenefitByZoneByLanduse = {}
    totalsByBenefitByZoneByGi = {}
    totalsByBenefitByLanduseByGi = {}

# Individual BENEFITS BY ZONE BY LANDUSE BY GI BY BENEFIT CATEGORY:    
    #print "Individual benefits by zone by landuse by GI by benefit category (I,J,K,T):"
    for i in sorted(I):
        jDict = {}
        for j in sorted(J):
            kDict = {}
            for k in sorted(K):
                tDict = {}
                for t in sorted(T):
                    tDict[t] = s[i][j][k][t]*decisions[i][j][k] #individual benefit
                kDict[k] = tDict
            jDict[j] = kDict
        benefits[i] = jDict
    #benefitsYaml = yaml.dump(benefits)
    #print benefitsYaml
    solutionDict['benefits'] = benefits
# INDIVIDUAL BENEFITS BY BENEFIT CATEGORY BY ZONE BY LANDUSE BY GI:   
    #print "Individual benefits by benefit category by zone by landuse by GI (T,I,J,K)" 
    for t in sorted(T):
        iDict = {}
        for i in sorted(I):
            jDict = {}
            for j in sorted(J):
                kDict = {}
                for k in sorted(K):
                    kDict[k] =  benefits[i][j][k][t]
                jDict[j] = kDict
            iDict[i] = jDict
        benefitsByZoneByLanduseByGi[t] = iDict
    #totsYaml = yaml.dump(benefitsByZoneByLanduseByGi)
    #print totsYaml     
    solutionDict['benefitsByZoneByLanduseByGi'] = benefitsByZoneByLanduseByGi
# TOTALS BY BENEFIT CATEGORY:   
    #print "Total benefits by benefit category (T):" 
    for t in sorted(T):
        tot_t = 0.0
        for i in sorted(I):
            for j in sorted(J):
                for k in sorted(K):
                    value = benefits[i][j][k][t]
                    tot_t += value                    
        totalsByBenefit[t] = tot_t
    solutionDict['totalsByBenefit'] = totalsByBenefit
#   TOTALS BY BENEFIT CATEGORY BY ZONE:
    #print "Total benefits by benefit category by zone (T,I):"
    for t in sorted(T):
        iDict = {}
        for i in sorted(I):
            tot_ti = 0.0
            for j in sorted(J):
                for k in sorted(K):
                    tot_ti += benefits[i][j][k][t]
            iDict[i] = tot_ti
        totalsByBenefitByZone[t] = iDict
    solutionDict['totalsByBenefitByZone'] = totalsByBenefitByZone
    #totsYaml = yaml.dump(totalsByBenefitByZone)
    #print totsYaml
# TOTALS BY BENEFIT CATEGORY BY LANDUSE:
    #print "Total benefits by benefit category by landuse (T,J):"
    for t in sorted(T):
        jDict = {}
        for j in sorted(J):
            tot_tj = 0.0
            for i in sorted(I):
                for k in sorted(K):
                    tot_tj += benefits[i][j][k][t]
            jDict[j] = tot_tj
        totalsByBenefitByLanduse[t] = jDict
    solutionDict['totalsByBenefitByLanduse'] = totalsByBenefitByLanduse
    #totsYaml = yaml.dump(totalsByBenefitByLanduse)
    #print totsYaml 
# TOTALS BY BENEFIT CATEGORY BY GI:
    #print "Total benefits by benefit category by gi technology (T,K):"    
    for t in sorted(T):
        kDict = {}
        for k in sorted(K):
            tot_tk = 0.0
            for i in sorted(I):
                for j in sorted(J):
                    tot_tk += benefits[i][j][k][t]
            kDict[k] = tot_tk
        totalsByBenefitByGi[t] = kDict
    solutionDict['totalsByBenefitByGi'] = totalsByBenefitByGi
    #totsYaml = yaml.dump(totalsByBenefitByGi)
    #print totsYaml 

    
# TOTALS BY BENEFIT BY ZONE BY LANDUSE:
    #print "Total benefits by benefit category by zone by landuse (T,I,J):"
    for t in sorted(T):
        iDict = {}
        for i in sorted(I):
            jDict = {}
            for j in sorted(J):
                tot_k = 0.0
                for k in sorted(K):
                    tot_k += benefits[i][j][k][t]
                jDict[j] = tot_k
            iDict[i] = jDict
        totalsByBenefitByZoneByLanduse[t] = iDict
    solutionDict['totalsByBenefitByZoneByLanduse'] = totalsByBenefitByZoneByLanduse
    #totsYaml = yaml.dump(totalsByBenefitByZoneByLanduse)
    #print totsYaml 
            
# TOTALS BY BENEFIT BY ZONE BY GI:
    #print "Total benefits by benefit category by zone by gi technology (T,I,K)"
    for t in sorted(T):
        iDict = {}
        for i in sorted(I):
            kDict = {}
            for k in sorted(K):
                tot_j = 0.0
                for j in sorted(J):
                    tot_j += benefits[i][j][k][t]
                kDict[k] = tot_j
            iDict[i] = kDict
        totalsByBenefitByZoneByGi[t] = iDict
    solutionDict['totalsByBenefitByZoneByGi'] = totalsByBenefitByZoneByGi
    #totsYaml = yaml.dump(totalsByBenefitByZoneByGi)
    #print totsYaml 

# TOTALS BY BENEFIT BY LANDUSE BY GI:
    #print "Total benefits by benefit category by landuse by gi technology (T,J,K):"
    for t in sorted(T):
        jDict = {}
        for j in sorted(J):
            kDict = {}
            for k in sorted(K):
                tot_i = 0.0
                for i in sorted(I):
                    tot_i += benefits[i][j][k][t]
                kDict[k] = tot_i
            #print "j = %s" % j
            jDict[j] = kDict
        totalsByBenefitByLanduseByGi[t] = jDict
    solutionDict['totalsByBenefitByLanduseByGi'] = totalsByBenefitByLanduseByGi
    #totsYaml = yaml.dump(totalsByBenefitByLanduseByGi)
    #print totsYaml 
    '''
# Check overall totals for consistency:
    print "totalsByBenefit:"
    totsYaml = yaml.dump(totalsByBenefit)
    print totsYaml
    
    
    print "\nsumation of benefits:"     
    tot = {}
    for t in T:
        tot[t] = 0.0
    for i in I:
        for j in J:
            for k in K:
                for t in T:
                    tot[t] += benefits[i][j][k][t]
    for t in sorted(T):
        print "%s: %15.7f" % (t,tot[t])

    print "\nsummation of benefitsByZoneByLanduseByGi:"     
    tot = {}
    for t in T:
        tot[t] = 0.0
        for i in I:
            for j in J:
                for k in K:
                    tot[t] += benefitsByZoneByLanduseByGi[t][i][j][k]
    for t in sorted(T):
        print "%s: %15.7f" % (t,tot[t])

    print "\nsummation of totalsByBenefitByZone:"     
    tot = {}
    for t in T:
        tot[t] = 0.0
        for i in I:
            tot[t] += totalsByBenefitByZone[t][i]
    for t in sorted(T):
        print "%s: %15.7f" % (t,tot[t])

    print "\nsummation of totalsByBenefitByLanduse:"     
    tot = {}
    for t in T:
        tot[t] = 0.0
        for j in J:
            tot[t] += totalsByBenefitByLanduse[t][j]
    for t in sorted(T):
        print "%s: %15.7f" % (t,tot[t])

    print "\nsummation of totalsByBenefitByGi:"     
    tot = {}
    for t in T:
        tot[t] = 0.0
        for k in K:
            tot[t] += totalsByBenefitByGi[t][k]
    for t in sorted(T):
        print "%s: %15.7f" % (t,tot[t])   

    print "\nsummation of totalsByBenefitByZoneByLanduse:"     
    tot = {}
    for t in T:
        tot[t] = 0.0
        for i in I:
            for j in J:
                tot[t] += totalsByBenefitByZoneByLanduse[t][i][j]
    for t in sorted(T):
        print "%s: %15.7f" % (t,tot[t])  

    print "\nsummation of totalsByBenefitByZoneByGi:"     
    tot = {}
    for t in T:
        tot[t] = 0.0
        for i in I:
            for k in K:
                tot[t] += totalsByBenefitByZoneByGi[t][i][k]
    for t in sorted(T):
        print "%s: %15.7f" % (t,tot[t])  

    print "\nsummation of totalsByBenefitByLanduseByGi:"     
    tot = {}
    for t in T:
        tot[t] = 0.0
        for j in J:
            for k in K:
                tot[t] += totalsByBenefitByLanduseByGi[t][j][k]
    for t in sorted(T):
        print "%s: %15.7f" % (t,tot[t])  
    '''

    solutionStr = yaml.dump(solutionDict)
    print "\n\nsolutionStr printout:"
    print solutionStr
    return(solutionDict)  
          
def main(inYamlFile):
    with open(inYamlFile, 'r') as fin:
        inYamlDoc = yaml.load(fin)
    decisions = stormwise(inYamlDoc)
    print "\nDECISIONS:"
    print yaml.dump(decisions)
    s = benefit_slopes(inYamlDoc)
    evaluate_solution(decisions,s,inYamlDoc)
#    u = upper_bounds(inYamlDoc)
#    evaluate_solution(inYamlDoc,u)


#    print "\nUPPER BOUNDS:"
#    print yaml.dump(u)
#    print "\nBENEFIT SLOPES:"
#    print yaml.dump(s)


main('wingohocking.yaml')

