from poly import poly
from poly import can_not_div_Error
from poly import egcd
import random
class ntru:
	def __init__(self,N,p,q,Fp = None,Fq = None,g = None,private_key = None,public_key = None):
		self.N = N
		self.p = p
		self.q = q
		self.private_key = private_key
		self.public_key = public_key 
		self.Fp = Fp
		self.Fq = Fq
		self.g = g
		P = [0] * (N + 1) 
		P[0] = -1
		P[N] = 1
		self.P = poly(P) 

	def _randpoly(self,one = None,_one = None):
		if one == None and _one == None:
			tot = random.randint(2,self.N - 1)
			one = random.randint(0,tot)
			_one = tot - one
		r =[0] * self.N
		while one != 0 or _one != 0:
			pos = random.randint(0,self.N - 1)
			if r[pos] is 0:
				if one > 0:
					r[pos] = 1
					one -= 1
				elif _one > 0:
					r[pos] = -1
					_one -= 1
		return poly(r)

	def randpoly_private(self):
		if self.N == 107:
			return self._randpoly(15,14)
		elif self.N == 503:
			return self._randpoly(216,215)
		else :
			return self._randpoly()

	def randpoly_g(self):
		if self.N == 107:
			return self._randpoly(12,12)
		elif self.N == 503:
			return self._randpoly(72,72)
		else:
			return self._randpoly()

	def randpoly_phi(self):
		if self.N == 107:
			return self._randpoly(5,5)
		elif self.N == 503:
			return self._randpoly(5,5)
		else:
			return self._randpoly()		
	def get_public(self):
		#self.public_key = 
		pass
	def createKey_pair(self):
		N = self.N
		q = self.q
		p = self.p
		self.private_key = self.randpoly_private()
		self.g = self.randpoly_g()
		while self.g.is_z():
			self.g = self.randpoly_g()
		tmp = q
		k = 0
		while tmp != 0:
			tmp = tmp // 2
			k += 1
		k -= 1
		while True:
			try:
				self.Fq = self.private_key.inv(N,2,k)
				self.Fp = self.private_key.inv(N,p,1)
				if (self.Fq is not False) and (self.Fp is not False):
					break
				self.private_key = self.randpoly_private()
			except can_not_div_Error:
				self.private_key = self.randpoly_private()	

		h = self.Fq.StarMult(self.g,N,q)
		self.public_key = h
		return (h,self.private_key)
	def encrypto(self,m):
		phi = self.randpoly_phi()
		phi = poly([-1,1,0,0,0,-1,1])
		c = phi.StarMult(self.public_key,self.N,self.q)
		c.expend(self.N)
		m.expend(self.N)
		for i in range(0,self.N):
			c.coe[i] = self.p * c.coe[i] + m.coe[i] 
			c.coe[i] %= self.q
		return c
	def decrypto(self,m):
		a = self.private_key.StarMult(m,self.N,self.q)
		for i in range(0,len(a.coe)):
			if a.coe[i] < 0:
				a.coe[i] += self.q
			if a.coe[i] > self.q / 2:
				a.coe[i] = a.coe[i] - self.q
		M = a.StarMult(self.Fp,self.N,self.p).polydiv(self.P,self.p)[1]
		return M
"""
TEST
"""

NTRU = ntru(97,3,32,Fp=poly([-1,0,1,1]),public_key=poly([1,2,0,-2,-1]),private_key=poly([-1,1,0,0,1]))
NTRU.createKey_pair()
m = NTRU.encrypto(poly([1,2,1,1,1,0,0,1,1])) #
M = NTRU.decrypto(m)
print(M.coe)