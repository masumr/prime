p=[0]*1000
lis=[]
def sieve():
	for i in range(3,1000,2):
		if p[i]==0: 
			for j in range(i*i,1000,i*2):
				p[j]=1
	lis.append(2)
	for i in range(3,1000,2):
		if p[i]==0:
			lis.append(i)
sieve()
print(lis) 			

