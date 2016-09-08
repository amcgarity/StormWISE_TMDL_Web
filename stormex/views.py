from django.template.loader import get_template
from django.http import HttpResponse
from django.template import Template, Context
from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.contrib import messages 
from forms import *
import os
# additional imports taken from stormwise_tmdl_cml:
import yaml
from copy import deepcopy
from StormWISE_TMDL_Engine.stormwise_tmdl import stormwise
from StormWISE_TMDL_Engine.stormwise_tmdl import evaluate_solution
from StormWISE_TMDL_Engine.stormwise_tmdl_benefits_and_bounds import benefit_slopes
from StormWISE_TMDL_Engine.stormwise_tmdl_benefits_and_bounds import upper_bounds
from StormWISE_TMDL_Engine.stormwise_tmdl_benefits_and_bounds import convert_benefit_units
from StormWISE_TMDL_Engine.stormwise_tmdl_benefits_and_bounds import format_and_convert_benefit_dict
from Arts_Python_Tools.tools import multiply_dict_by_constant
from Arts_Python_Tools.tools import format_dict_as_strings

amplPath = "/var/lib/ampl/ampl"

#from engine.stormwise_tmdl import storm 
def test(request):
    messages.info(request,'this works')
    return render(request,'test.html')
    
def benefits(request):
    try:
        inYamlFile = "wingohocking.yaml"
        with open(inYamlFile, 'r') as fin:
            inYamlDoc = yaml.load(fin)
    except IOError:
        print "\n SORRY:  the file %s can not be found" % inYamlFile
        return
    try:
        with open('convert_benefits.yaml', 'r') as fin:
            convertBenefits = yaml.load(fin)
    except IOError:
        print "\n SORRY:  the file %s can not be found" % 'convert_benefits.yaml' 
        return   
    benefitUnits = convertBenefits['benefitUnits']
    benefitConvertUnits = convertBenefits['benefitConvertUnits']

    #os.chdir("/code/StormWISE_TMDL_Engine")  # all file input and output now in this directory

    if request.method == 'GET':
        benefitDict = {}
        run = r_priority(request.GET)
        sed = s_priority(request.GET)
        nit = n_priority(request.GET)
        phos = p_priority(request.GET)
        array1 = [0,0,0,0]
        ben = [0,0,0,0]
        if run.is_valid():
            ra = run.cleaned_data['runoff']
            
        if sed.is_valid():
            sa = sed.cleaned_data['sedimentation']  
            
        if nit.is_valid():
            na = nit.cleaned_data['nitrogen']
                
        if phos.is_valid():
            pa = phos.cleaned_data['phosphorous']
            
        if ra != None and sa != None and na != None and pa != None:
            #ra = ra/10.0 * 693
            #sa = sa/10.0 * 844
            #na = na/10.0 * 9207
            #pa = pa/10.0 * 1168
            #ben = [ra,sa,na,pa]
            benefitDict = {}
            tDict = {}
            tDict['1_volume'] = ra/benefitConvertUnits['1_volume']
            tDict['2_sediment'] = ra/benefitConvertUnits['2_sediment']
            tDict['3_nitrogen'] = ra/benefitConvertUnits['3_nitrogen']
            tDict['4_phosphorous'] = ra/benefitConvertUnits['4_phosphorous']
            benefitDict['benefitLowerBounds'] = tDict
            #os.chdir("/code/StormWISE_TMDL_Engine")  # all file input and output now in this directory
            decisions = stormwise(amplPath,inYamlDoc,benefitDict)
            s = benefit_slopes(inYamlDoc)
            solutionDict = evaluate_solution(decisions,s,inYamlDoc)

            x = solutionDict['benTotsByBenefit']
            #x = storm('/code/stormex/wingohocking.yaml',ben)
            #y = '%.2f' % x['investmentTotal']
            y = '%.2f' % solutionDict['investmentTotal']
            messages.add_message(request, messages.INFO, y)
            array1 = [x['1_volume'],
            x['2_sediment'],
            x['3_nitrogen'],
            x['4_phosphorous']]
        else:
            messages.error(request, 'Fill all fields')  
        
    else:
        run = RunoffForm()
        sed = SedForm()
        nit = NitForm()
        phos = PhosForm()   

    return render(request,'benefits.html',
        {'run':run, 'sed':sed, 'nit':nit, 'phos':phos, 'array1':array1})


