import json
from math import log
from math import sqrt
from . import stemmer
from operator import itemgetter


def precal_index_info(index):
    N = 10000
    doc_len = {}
    idf = {}
    for word in index:
        idf[word] = log(N/len(index[word]), 2)
        for d in index[word]:
            if d[0] not in doc_len:
               doc_len[d[0]] = 0
            doc_len[d[0]] += idf[word] * d[1] * idf[word] * d[1]
    for doc in doc_len:
        doc_len[doc] = sqrt(doc_len[doc])
    return doc_len, idf


def preprocess_query(q, p):
    freq = {}
    for i in range(len(q)):
        q[i] = q[i].lower()
        q[i] = p.stem(q[i], 0, len(q[i])-1)
        if q[i] not in freq:
            freq[q[i]] = 0
        freq[q[i]] += 1
    return freq



def get_query_result(query):
    index = json.load(open("inverted_index.json"))
    document_len, idf = precal_index_info(index)
    ps = stemmer.PorterStemmer()

    query = query.strip().split()
    query = preprocess_query(query, ps)
    ranklist = {}
    query_len = 0.0
    for t in query:
        if t not in idf:
            continue
        w = query[t] * idf[t]
        query_len += w*w
        for d in index[t]:
            if d[0] not in ranklist:
                ranklist[d[0]] = 0.0
            ranklist[d[0]] += w*idf[t]*d[1]
    query_len = sqrt(query_len)
    for d in ranklist:
        ranklist[d] = ranklist[d] / (query_len * document_len[d])

    return sorted(ranklist.items(), key = itemgetter(1), reverse=True)
