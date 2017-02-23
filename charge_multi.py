import re
import matplotlib.pyplot as plt
import numpy as np
import sys

def read_write(xxx,yyy):
	mesh=open('dumpfile.%d.txt'%xxx)
	N=list()

	for line in mesh:
		line=line.rstrip()
		if re.search('[0-9]+[.][0-9]+ [0-9]+[.][0-9]+ [0-9]+ [0-9]+',line):
			num=line.split()
			N.append(int(num[3]))

	N_timesofvisit=np.asarray(N)
	Qarray=np.zeros(100)
	for i in range(len(N_timesofvisit)):
		for j in range(len(Qarray)):
			if(N_timesofvisit[i]==j): Qarray[j]+=1

	print(sum(Qarray))

	with open('charge.%d.txt'%yyy,'w') as f:
		for i in range(len(Qarray)):
			print('%d =%d\n'%(i,Qarray[i]),file=f)
		##print('total number = %f'%sum(Q), file=f)
	return Qarray

Q0=read_write(0,0)
Q1=read_write(1,1)
Q2=read_write(2,2)
Q3=read_write(3,3)


t=np.arange(100)
plt.plot(t,Q0,'r--',t,Q1,'bs',t,Q2,'g^',t,Q3,'c^')
plt.xscale('linear')
plt.yscale('log')
plt.show()
