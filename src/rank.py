

from math import log

k1 = 1.2
k3 = 100
# b = 0.75
R = 0.0
alpha=0.5

def score_BM25(qf, inf, df, N, dl, avdl,b):
	K = compute_K(dl, avdl,b)
	second = log(  (N-inf + 0.5) / (inf + 0.5) ) 
	first = ((k1 + 1) * df) / (K + df)
	third = ((k3+1) * qf) / (k3 + qf)
	return first * second * third


def compute_K(dl, avdl,b):
	return k1 * ((1-b) + b * (float(dl)/float(avdl)) )


def score_BM25S_profile(inf, df, N, dl, avdl,uf,b):
	K = compute_K(dl, avdl,b)
	second = log(  (N-inf + 0.5) / (inf + 0.5) ) 
	first = ((k1 + 1) * df) / (K + df)
	third = ((k3+1) * uf) / (k3 + uf)
	return first * second * third



def score_BM25freq_combine(qf, inf, df, N, dl, avdl,uf,b):
	K = compute_K(dl, avdl,b)
	second = log(  (N-inf + 0.5) / (inf + 0.5) ) 
	first = ((k1 + 1) * df) / (K + df)
	third = ((k3+1) * qf + alpha * uf) / (k3 + qf + alpha * uf)
	x=first * second * third
	return x 
def p_at_k(k,rel,ret):
	count=0
	for i in range(0,k):
		for j in range(0,len(rel)):
			if(ret[i]==rel[j]):
				count+=1
	return count/k
def mean_average_precision(total_queries,ret,rel):
	total_p=0
	total_average_p=0
	for i in range(0,total_queries):
		for j in range(0,len(ret[i+1])):	
			total_p+=p_at_k(j+1,rel[i+1],ret[i+1])
		average_p=total_p/5
		total_average_p+=average_p
	mean_average_p=total_average_p/total_queries
	return mean_average_p


