from django.template.loader import get_template
from django.http import HttpResponse
from django.template import Template, Context
from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.contrib import messages 
from forms import *
import os
#from StormWISE_TMDL_Engine.stormwise_tmdl import stormwise
#from StormWISE_TMDL_Engine.stormwise_tmdl import evaluate_solution
from engine.stormwise_tmdl import storm
def test(request):
	messages.info(request,'this works')
	return render(request,'test.html')

def benefits(request):
	os.chdir("/code/stormex/engine")  # Django:  "/code" is the directory of the Django project
	if request.method == 'GET':
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
			ra = ra/10.0 * 693
			sa = sa/10.0 * 844
			na = na/10.0 * 9207
			pa = pa/10.0 * 1168
			ben = [ra,sa,na,pa]
			x = storm('/code/stormex/wingohocking.yaml',ben)
			y = '%.2f' % x['investmentTotal']
			messages.add_message(request, messages.INFO, y)
			array1 = [x['benTotsByBenefit']['1_volume'],
			x['benTotsByBenefit']['2_sediment'],
			x['benTotsByBenefit']['3_nitrogen'],
			x['benTotsByBenefit']['4_phosphorous']]
		else:
			messages.error(request, 'Fill all fields')	
		
	else:
		run = RunoffForm()
		sed = SedForm()
		nit = NitForm()
		phos = PhosForm()	

	return render(request,'benefits.html',
		{'run':run, 'sed':sed, 'nit':nit, 'phos':phos, 'array1':array1})


