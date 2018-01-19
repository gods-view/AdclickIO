# encoding=utf-8
import random

def toInt(v):
	try:
		return int(v)
	except Exception,e:
		return 0;
	
def toFloat(v):
	try:
		return float(v)
	except Exception,e:
		return 0;

def randomList(seq, num):
	return random.sample(seq, num) 


def toBind(s):
	ss=bin(s).replace('0b','')
	return int(ss)
	

def getORvalue(flag_value,step):
	flag=step | int(flag_value)
	return flag
	
def getANDvalue(flag_value,step):
	flag=step & int(flag_value)
	return flag


def convert_n_bytes(n, b):
    bits = b*8
    return (n + 2**(bits-1)) % 2**bits - 2**(bits-1)

def convert_4_bytes(n):
    return convert_n_bytes(n, 4)

def getHashCode(s):
    h = 0
    n = len(s)
    for i, c in enumerate(s):
        h = h + ord(c)*31**(n-1-i)
    return convert_4_bytes(h)

#print getORvalue(2, 6)
#print getANDvalue(8,16)
'''
dest = {}
for i in range(2*num):
	v = random.choice(seq)
	if not dest.has_key(v):
		dest[v] = 1
		if len(dest) == num:
			break
		
return dest.keys()
'''