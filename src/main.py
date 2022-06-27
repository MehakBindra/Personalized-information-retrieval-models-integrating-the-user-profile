from parse import *
from query import QueryProcessor
import operator
from rank import mean_average_precision

rel = [2442, 2266, 2243, ]
def main():
    cp = CorpusParser(filename='../text/corpus.txt')
    qp = QueryParser()
    up = UserParser(filename='../text/users.txt')
    cp.parse()
    up.parse()
    uid = input("Enter user id between 1 to 7:")
    query = input("Enter query :")
    parsed_query = qp.parse(str(query))
    corpus = cp.get_corpus()
    users = up.get_users()
    proc = QueryProcessor(corpus, users)
    result = proc.run_query(parsed_query)
    sorted_x = sorted(result.items(), key=operator.itemgetter(1))
    sorted_x.reverse()
    if len(sorted_x) != 0:
        print(' '.join(corpus.get(sorted_x[0][0])))
    else:
        print ("no document matches the search")

    user_result = proc.run_query_with_user(parsed_query, str(uid))
    user_sorted_x = sorted(user_result.items(), key=operator.itemgetter(1))
    user_sorted_x.reverse()
    if len(user_sorted_x) != 0:
        print(' '.join(corpus.get(user_sorted_x[0][0])))
    else:
        print ("no document matches the search for this user")

    user_result1 = proc.run_query_with_user_and_df(parsed_query, str(uid))
    user_sorted_x1 = sorted(user_result1.items(), key=operator.itemgetter(1))
    user_sorted_x1.reverse()
    if len(user_sorted_x1) != 0:
        print(' '.join(corpus.get(user_sorted_x1[0][0])))
    else:
        print ("no document matches the search for this user")

    ret_q, ret_u, ret_qu = retrieve(result, user_result, user_result1, len(cp.get_corpus()))
    m = evaluate(ret_q, ret_u, ret_qu, rel)
    print(m)


def evaluate(ret_q, ret_u, ret_qu, real):
    m = dict()

    m['map_q'] = mean_average_precision(ret_q, real)
    m['map_u'] = mean_average_precision(ret_u, real)
    m['map_qu_fc'] = mean_average_precision(ret_qu, real)
    return m


def retrieve(results1, results2, results3, total_docs):
    print("total docs are", total_docs)
    limit = int(0.1 * total_docs)

    print("the recall limit is ", limit)

    sorted_x = sorted(results1.items(), key=operator.itemgetter(1))
    sorted_x.reverse()
    i = 0
    ret1 = []
    for d in sorted_x:
        if i < limit:
            ret1.append(d[0])
            i += 1
        else:
            break

    sorted_x = sorted(results2.items(), key=operator.itemgetter(1))
    sorted_x.reverse()
    i = 0
    ret2 = []
    for d in sorted_x:
        if i < limit:
            ret2.append(d[0])
            i += 1
        else:
            break

    sorted_x = sorted(results3.items(), key=operator.itemgetter(1))
    sorted_x.reverse()
    i = 0
    ret3 = []
    for d in sorted_x:
        if i < limit:
            ret3.append(d[0])
            i += 1
        else:
            break

    print('Ranking is done ')
    return ret1, ret2, ret3


if __name__ == '__main__':
    main()
