from django.template.loader import get_template
from django.http import HttpResponse
from django.template import Template, Context
from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.contrib import messages 
from forms import *
from stormwise_tmdl import storm

def test(request):
	messages.info(request,'this works')
	return render(request,'test.html')

def benefits(request):
	
	if request.method == 'GET':
		run = RunoffForm(request.GET)
		sed = SedForm(request.GET)
		nit = NitForm(request.GET)
		phos = PhosForm(request.GET)
		if run.is_valid():
			ra = run.cleaned_data['runoff']
		if sed.is_valid():
			sa = sed.cleaned_data['sedimentation']	
		if nit.is_valid():
			na = nit.cleaned_data['nitrogen']	
		if phos.is_valid():
			pa = phos.cleaned_data['phosphorous']
		if ra != None and sa != None and na != None and pa != None:
			ben = [ra,sa,na,pa]
			x = storm('wingohocking.yaml',ben)
			y = '%.2f' % x['investmentTotal']
			messages.add_message(request, messages.INFO, y)
		else:
			messages.error(request, 'Fill all fields')	
		
	else:
		run = RunoffForm()
		sed = SedForm()
		nit = NitForm()
		phos = PhosForm()	

	return render(request,'benefits.html',
		{'run':run, 'sed':sed, 'nit':nit, 'phos':phos})


