#proof of concept of minimal repilica

import hashlib
import json
from typing import Any, Dict, List, Optional

import random
import time

def hex2bin(hexN):
	scale = 16
	num_of_bits = 256
	return bin(int(hexN, scale))[2:].zfill(num_of_bits)

def hamdist(str1, str2):
	diffs = 0
	bstr1 = hex2bin(str1)
	bstr2 = hex2bin(str2)
	for ch1, ch2 in zip(str1, str2):
		if ch1 != ch2: 
			diffs += 1
	return diffs 

def hash(block: Dict[str, Any]) -> str:
	# hashing 
	block_string = json.dumps(block, sort_keys=True).encode()
	return hashlib.sha256(block_string).hexdigest()

def valid_state(proof: str, state: Dict[str, Any]) -> bool:
	"""
	Validates the state
	:param proof: hash in the database
	:param state: account info
	:return: True if correct, False if not.
	"""
	state_hash = hash(state)
	return state_hash == proof

def sortedIndex(str1, strArray2):
	#n = int(random.uniform(1,len(strArray2)))
	s = [hamdist(str1, str2) for str2 in strArray2]
	idx = [i[0] for i in sorted(enumerate(s),key=lambda x:x[1])]
	return idx[0]

def new_state(a, t, spin, spx):
	state = {
		'account': '',
		'timestamp': 0,
		'spin': 0,
		'spx': 0,
	}
	state['account']= a
	state['timestamp']=t
	state['spin'] = spin
	state['spx'] = spx
	return state

class Node:
	def __init__(self):
		self.l = None
		self.r = None

class Trie:
	#implementataion of a binary trie
	def __init__(self):
		self.root = None

	def getRoot(self):
		return self.root

	def add(self, val):
		if(self.root == None):
			self.root = Node()
		self._add(val, self.root)

	def _add(self, val, node):
		if (len(val)>0):
			if(val[0] == '0'):
				if(node.l == None):
					node.l = Node()
				self._add(val[1:], node.l)
			elif(val[0] == '1'):
				if(node.r == None):
					node.r = Node()
				self._add(val[1:], node.r)

	def find(self, val):
		if (self.root != None):
			return self._find(val, self.root)
		else:
			return False
	def _find(self, val, node):
		if(len(val)==0):
			if(node.l == None and node.r == None):
				return True
			else:
				return False
		elif(val[0] == '0' and node.l != None):
			return self._find(val[1:], node.l)
		elif(val[0] == '1' and node.r != None):
			return self._find(val[1:], node.r)
		else:
			return False

	def deleteTrie(self):
	# garbage collector will do this for us. 
		self.root = None

	def delete(self, val):
		if (self.root != None):
			return self._delete(val, self.root, None, 0)
		else:
			return F
	def _delete(self, val, node, parent, lr):
		if len(val)>0:
			if (val[0]=='0'):
				return self._delete(val[1:], node.l, node, 0)
			if (val[0]=='1'):
				return self._delete(val[1:], node.r, node, 1)
			if (node.l==None and node.r==None):
				if (lr==0):
					parent.l = None
				else:
					parent.r = None
				return
		elif (node.l==None and node.r==None):
			if (lr==0):
				parent.l = None
			else:
				parent.r = None
			return True
		else:
			return False


trie = Trie()


nb = 1667
# visa process 1167 transactions per second on average
# http://www.altcointoday.com/bitcoin-ethereum-vs-visa-paypal-transactions-per-second/
accounts = [hashlib.sha256(str(random.uniform(1,100000000)).encode()).hexdigest() for i in range(nb)]
spins = [random.uniform(1,100000000) for i in range(nb)]
spxs = [random.uniform(1,100000000) for i in range(nb)] 

state_list = [new_state(accounts[i], 1, spins[i], spxs[i]) for i in range(nb)]
hash_list = [hash(st) for st in state_list]

accounts2 = [hashlib.sha256(str(random.uniform(1,100000000)).encode()).hexdigest() for i in range(nb)]
spins2 = [random.uniform(1,10000000) for i in range(nb)]
spxs2 = [random.uniform(1,10000000) for i in range(nb)] 

state_list2 = [new_state(accounts2[i], 1, spins2[i], spxs2[i]) for i in range(nb)]
hash_list2 = [hash(st) for st in state_list2]

current_milli_time = lambda: int(round(time.time() * 1000))

start = current_milli_time()
for x in hash_list:
	trie.add(hex2bin(x))
end = current_milli_time()
print("add " + str(end - start))

start = current_milli_time()
for x in hash_list2:
	trie.add(hex2bin(x))
end = current_milli_time()
print("add " + str(end - start))

start = current_milli_time()
for x in hash_list:
	s = trie.find(hex2bin(x))
	if (s==False):
		print(x)
end = current_milli_time()
print("find true " + str(end - start))

start = current_milli_time()
for x in hash_list2:
	s = trie.find(hex2bin(x))
	if (s==False):
	 	print(x)
end = current_milli_time()
print("find false " + str(end - start))

start = current_milli_time()
for i in range(int(nb/2)):
	s = trie.delete(hex2bin(hash_list[i]))
end = current_milli_time()
print("delete half " + str(end - start))

start = current_milli_time()
n = 0
for i in range(nb):
	x = hash_list[i]
	s = trie.find(hex2bin(x))
	if (s==False):
		n += 1
print(str(n) + ' false' )		
end = current_milli_time()
print("find false " + str(end - start))
