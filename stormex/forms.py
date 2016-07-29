from django import forms 

class RunoffForm(forms.Form):
	runoff = forms.FloatField(required=False, label = '')

class SedForm(forms.Form):
	sedimentation = forms.FloatField(required=False, label = '')

class NitForm(forms.Form):
	nitrogen = forms.FloatField(required=False, label = '')	

class PhosForm(forms.Form):
	phosphorous = forms.FloatField(required=False, label = '')		