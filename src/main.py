
import matplotlib
import matplotlib.pyplot as plt
from parse import *
from query import QueryProcessor
import operator
from rank import *
recall=0.1
rel=[]
rel.append({1:['1','17'],2:['12','4'],3:['25','28'],4:['32','27'],5:['29','16']})
rel.append({1:['24','1'],2:['12','22'],3:['25','17'],4:['32','30'],5:['29','32']})
rel.append({1:['17','33'],2:['4','34'],3:['25','9'],4:['27','40'],5:['29','39']})
rel.append({1:['13','1'],2:['4','26'],3:['28','27'],4:['30','32'],5:['29','33']})
rel.append({1:['17','34'],2:['12','6'],3:['25','23'],4:['27','24'],5:['16','18']})
rel.append({1:['17','31'],2:['12','34'],3:['25','33'],4:['32','20'],5:['16','22']})
rel.append({1:['1','31'],2:['27','12'],3:['32','24'],4:['33','27'],5:['29','19']})
rel.append({1:['32','1'],2:['33','4'],3:['25','43'],4:['37','27'],5:['44','47']})
rel.append({1:['34','17'],2:['28','4'],3:['24','25'],4:['32','20'],5:['22','29']})
rel.append({1:['5','1'],2:['11','4'],3:['13','25'],4:['28','27'],5:['32','16']})
def text():
        qp = QueryParser(filename="queries.txt")
        cp = CorpusParser(filename="corpus.txt")
        up = ProfileParser(filename="profile.txt")
        qp.parse()
        queries = qp.get_queries()
        print ('Parsing of queries done')
        # print(queries)
        cp.parse()
        corpus = cp.get_corpus()
        print ('Parsing of corpus done')
        up.parse()
        profile = up.get_profile()
        print ('Parsing of user profiles done')
        total_docs=len(corpus)
        total_users=len(profile)
        total_queries=len(queries)
        return queries, corpus,profile,total_docs,total_users,total_queries
def score(queries, corpus,profile,b):
        proc = QueryProcessor(queries, corpus,profile)
        results1 = proc.run1(b=b)
        results2 = proc.run2(b=b)
        results3 = proc.run3(b=b)
        results4 = proc.run4(b=b)
        results5 = proc.run5(b=b)
        results6 = proc.run6(b=b)
        results7 = proc.run7(b=b)
        results8 = proc.run8(b=b)
        # print(results4)
        print('intermediate results are processed ')
        return results1,results2,results3,results4,results5,results6,results7,results8

def retrieve(results1,results2,results3,results4,recall,total_docs,total_users,total_queries):
    qid = 0
    userid = 1
    print("total docs are",total_docs,"total users are",total_users,"total no of queries = ",total_queries)
    limit=int(recall*total_docs)
    ret_q=dict()
    id=0
    ret_u=[]
    ret_qu1=[]
    ret_qu2=[]
    print("the recall limit is ",limit)
    for result in results1:
        id+=1
        sorted_x = sorted(result.items(), key=operator.itemgetter(1))
        sorted_x.reverse()
        # print(sorted_x)
        i=0
        ret1=[]
        for d in sorted_x:
            if(i<limit):
                ret1.append(d[0])
                # print(d[0])
                i+=1
            else:
                break
        ret_q[id]=ret1

    for result in results2:
            sorted_x = sorted (result.items(), key=operator.itemgetter(1))
            sorted_x.reverse()
            r=dict()
            for qid in range(0,total_queries):
                i=0
                ret2=[]
                for d in sorted_x:
                    if(i<limit):
                        ret2.append(d[0])
                        # print(d[0])
                        i+=1
                    else:
                        break
                r[qid+1]=ret2
            ret_u.append(r)
    for result in results3:
            sorted_x = sorted (result.items(), key=operator.itemgetter(1))
            sorted_x.reverse()
            r=dict()
            for qid in range(0,total_queries):
                i=0
                ret2=[]
                for d in sorted_x:
                    if(i<limit):
                        ret2.append(d[0])
                        i+=1
                        # print(d[0])
                    else:
                        break
                r[qid+1]=ret2
            ret_qu1.append(r)
    for result in results4:
            sorted_x = sorted (result.items(), key=operator.itemgetter(1))
            sorted_x.reverse()

            r=dict()
            for qid in range(0,total_queries):
                i=0
                ret2=[]
                for d in sorted_x:
                    if(i<limit):
                        ret2.append(d[0])
                        # print(d[0])
                        i+=1
                    else:
                        break
                r[qid+1]=ret2
            ret_qu2.append(r)
    print('Ranking is done ')
    return ret_q,ret_u,ret_qu1,ret_qu2

def evaluate(recall,ret_q,ret_u,ret_qu1,ret_qu2,rel,total_docs,total_users,total_queries,m):
    t_ret=recall*total_docs
    x=0
    m['map_q'].append(mean_average_precision(total_queries,ret_q,rel[0]))
    for u in range(1,total_users+1):
        x+=mean_average_precision(total_queries,ret_u[u-1],rel[u])
    m['map_u'].append(x/total_users)
    x=0
    for u in range(1,total_users+1):
        x+=mean_average_precision(total_queries,ret_qu1[u-1],rel[u])
    m['map_qu_sc'].append(x/total_users)
    x=0
    for u in range(1,total_users+1):
        x+=mean_average_precision(total_queries,ret_qu2[u-1],rel[u])
    m['map_qu_fc'].append(x/total_users)
    return m
def main():
    m=dict()
    queries, corpus,profile,total_docs,total_users,total_queries=text()

    b=[0.2,0.4,0.6,0.8,1.0]
    m1=dict()
    m1['map_q']=[]
    m1['map_u']=[]
    m1['map_qu_sc']=[]
    m1['map_qu_fc']=[]
    m2['map_q']=[]
    m2['map_u']=[]
    m2['map_qu_sc']=[]
    m2['map_qu_fc']=[]

    for i in range(0,len(b)):
        results1,results2,results3,results4,results5,results6,results7,results8=score( queries, corpus,profile,b[i])

        ret_q_tp,ret_u_tp,ret_qu1_tp,ret_qu2_tp=retrieve(results1,results2,results3,results4,recall,total_docs,total_users,total_queries)
        m1= evaluate(recall,ret_q_tp,ret_u_tp,ret_qu1_tp,ret_qu2_tp,rel,total_docs,total_users,total_queries,m1)

    for i in range(0,len(b)):
        print ("the value of b is", b[i])
        for res in m1:
            print('The corresponding map values are ', m1[res][i])

    print ('Evaluation done')

    plt.plot(m1['map_q'],b,label=str(res))

    plt.legend()
    plt.show()











print("hello")
main()
