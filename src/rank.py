__author__ = 'Nick Hirakawa'

from math import log

k1 = 1.2
k3 = 100
b = 0.75
alpha = 0.5


# N = no of documents
# n = no of terms

def score_bm25(f, qf, df, N, dl, avdl):
    K = compute_k(dl, avdl)
    second = log((N - df + 0.5) / (df + 0.5))
    first = ((k1 + 1) * f) / (K + f)
    third = ((k3 + 1) * qf) / (k3 + qf)
    return first * second * third


def compute_k(dl, avdl):
    return k1 * ((1 - b) + b * (float(dl) / float(avdl)))


def score_BM25_user(f, df, N, dl, avdl, uf):
    K = compute_k(dl, avdl)
    second = log((N - df + 0.5) / (df + 0.5))
    first = ((k1 + 1) * f) / (K + f)
    third = ((k3 + 1) * uf) / (k3 + uf)
    return first * second * third


def score_BM25freq_combine(f, qf, df, N, dl, avdl, uf):
    K = compute_k(dl, avdl)
    second = log((N - df + 0.5) / (df + 0.5))
    first = ((k1 + 1) * f) / (K + f)
    third = ((k3 + 1) * qf + alpha * uf) / (k3 + qf + alpha * uf)
    x = first * second * third
    return x


def p_at_k(k, rel, ret):
    count = 0
    for i in range(0, k):
        for j in range(0, len(rel)):
            if ret[i] == rel[j]:
                count += 1
    return count / k


def mean_average_precision(ret, rel):
    total_p = 0
    if len(ret) != 0:
        for j in range(0, len(ret)):
            total_p += p_at_k(j + 1, rel, ret)
        average_p = total_p / len(ret)
    return average_p


