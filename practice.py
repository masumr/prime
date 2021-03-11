p=[0]*1000
lis=[]
#sieve function

def sieve():
	for i in range(3,1000,2):
		if p[i]==0: 
			for j in range(i*i,1000,i*2):
				p[j]=1
	lis.append(2)
	for i in range(3,1000,2):
		if p[i]==0:
			lis.append(i)


#Coprime funcion

def coprime(n):
	ans=n
	for i in range(len(lis)):
		if lis[i]*lis[i]>n:
			break
		if n%lis[i]==0:
			while n%lis[i]==0:
				n/=lis[i]
			ans-=ans/lis[i]
	if n>1:
		ans-=ans/lis[i]
	return ans


sieve()
n=int(input("Enter find coprime number: ")
print(f'Coprime of {n}= {coprime(n)}')		

