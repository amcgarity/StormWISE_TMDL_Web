def make_dat(bens):
	vol = bens[0]
	sed = bens[1]
	nit = bens[2]
	phos = bens[3]
	ampl = "data;\n"
	ampl+= "param Bmin :=\n"
	ampl+= "1_volume   %.f\n" % vol
	ampl+= "2_sediment   %.f\n" % sed
	ampl+= "3_nitrogen   %.f\n" % nit
	ampl+= "4_phosphorous   %.f\n" % phos
	ampl+= ";\nmodel;"
	return ampl