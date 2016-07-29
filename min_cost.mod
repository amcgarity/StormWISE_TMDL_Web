# StormWISE model Cost minimization with multiple benefits as constraints - April 2010
set I;	# drainage zones
set J; 	# land-use categories
set K;	# bmp/lid categories
set KONJ{J} within K; # bmp/lid categories that are deployed on each land-use 
set T;	# benefit categories

param Bmin{T}; # default 0.0;		# lower bounds for benefits in converted units
param convert{T}; # conversion factors for benefits
param cost{j in J,KONJ[j]}; 	# marginal bmp/lid cost per unit of area treated 
param eta{I,K,T};	# BMP removal efficiency for load reduction benefits
param scale{T};   	# scale factors for benefits - may include unit conversions or fraction of runoff
#param runoff{J};	# runoff by land use in cm
#param emc{J,T};		# event mean concentrations (mg/L)
#param export{j in J,t in T} = scale[t]*runoff[j]*emc[j,t];	# calculated export coefficient
param export{J,T};
param f{I,j in J,KONJ[j]};		# treatment fraction
param area{I,J};	# area in zone i having land-use j
param s{i in I,j in J,k in KONJ[j],t in T} = eta[i,k,t]*export[j,t]/cost[j,k];	# calculated benefit slopes
param u{i in I,j in J,k in KONJ[j]} = cost[j,k]*f[i,j,k]*area[i,j];				# calculated upper spending limits

var x{i in I,j in J,k in KONJ[j]} >= 0 <= u[i,j,k];	# amout to invest - Decision Variables

minimize investment: sum{i in I, j in J, k in KONJ[j]} x[i,j,k];

subject to benefits{t in T}: sum{i in I, j in J, k in KONJ[j]} s[i,j,k,t]*x[i,j,k] >= Bmin[t]/convert[t];
