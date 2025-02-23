import math

def VS(R, S, NR, P):
    return (R*math.log10(S+1)*math.log10(NR+1)*(NR/S+1))/P

def CER(D, P):
    return D/P

def ACS(R, S, NR, P, D, M):
    return (R*math.log10(NR+1)/(M+1))*math.log10(S+1)*(1/(math.log10(P+10)))*(D/10)