# StormWISE_TMDL model Cost minimization with multiple benefits as constraints 
# In this model file, parameters s and u are calculated outside of AMPL, such
# as by the stormwise_tmdl.py program.

set I;	# drainage zones
set J; 	# land-use categories
set K;	# bmp/lid categories
set KONJ{J} within K; # bmp/lid categories that are deployed on each land-use 
set T;	# benefit categories

param Bmin{T}; # default 0.0;		# lower bounds for benefits in standard units
param s{I,j in J,KONJ[j],T}; #benefit slopes
param u{I,j in J,KONJ[j]};   # calculated upper spending limits

var x{i in I,j in J,k in KONJ[j]} >= 0 <= u[i,j,k];	# amout to invest - Decision Variables

minimize investment: sum{i in I, j in J, k in KONJ[j]} x[i,j,k];

subject to benefits{t in T}: sum{i in I, j in J, k in KONJ[j]} s[i,j,k,t]*x[i,j,k] >= Bmin[t];
