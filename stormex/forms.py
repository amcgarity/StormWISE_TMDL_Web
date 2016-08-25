from django import forms 

class RunoffForm(forms.Form):
	runoff = forms.FloatField(required=False, label = '')

class SedForm(forms.Form):
	sedimentation = forms.FloatField(required=False, label = '')

class NitForm(forms.Form):
	nitrogen = forms.FloatField(required=False, label = '')	

class PhosForm(forms.Form):
	phosphorous = forms.FloatField(required=False, label = '')		

class r_priority(forms.Form):
	runoff = forms.FloatField(required=False, label = '', 
		widget=forms.NumberInput(attrs={'type':'range', 'step': '1',
			'onchange':'updateTextInput1(this.value);'}),
		min_value=0.0,max_value=10.0)

class s_priority(forms.Form):
	sedimentation = forms.FloatField(required=False, label = '', 
		widget=forms.NumberInput(attrs={'type':'range', 'step': '1',
			'onchange':'updateTextInput2(this.value);'}),
		min_value=0.0,max_value=10.0)

class n_priority(forms.Form):
	nitrogen = forms.FloatField(required=False, label = '', 
		widget=forms.NumberInput(attrs={'type':'range', 'step': '1',
			'onchange':'updateTextInput3(this.value);'}),
		min_value=0.0,max_value=10.0)	

class p_priority(forms.Form):
	phosphorous = forms.FloatField(required=False, label = '', 
		widget=forms.NumberInput(attrs={'type':'range', 'step': '1', 
			'onchange':'updateTextInput4(this.value);'}),
		min_value=0.0,max_value=10.0)	