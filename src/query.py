from invdx import build_data_structures, InvertedIndexForUser, InvertedIndex
from rank import score_bm25, score_BM25freq_combine, score_BM25_user
import nltk
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import stopwords

nltk.download("punkt")
lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))

class QueryProcessor:
    def __init__(self, corpus, users):
        self.index, self.u_index, self.dlt = build_data_structures(corpus, users)

    def run_query(self, query):
        query_result = dict()
        for term in query:
            if term in self.index:
                doc_dict = self.index[term]  # retrieve index entry
                for docid, freq in doc_dict.items():  # for each document and its word frequency
                    score = score_bm25(f=freq, qf=1, df=self.index.get_document_frequency(term), N=len(self.dlt),
                                       dl=self.dlt.get_length(docid), avdl=self.dlt.get_average_length())
                    # calculate score
                    if docid in query_result:  # this document has already been scored once
                        query_result[docid] += score
                    else:
                        query_result[docid] = score
        return query_result

    def run_query_with_user(self, query, uid):
        query_result = dict()
        for term in query:
            if term.isalpha():
                if term not in stop_words:
                    lemmatizer.lemmatize(term)
                    if term in self.index:
                        doc_dict = self.index[term]
                        ufreq = self.u_index.get_frequency(term, uid)

                        for docid, freq in doc_dict.items():
                            score = score_BM25_user(f=freq, df=self.index.get_document_frequency(term),
                                                        N=len(self.dlt), dl=self.dlt.get_length(docid),
                                                        avdl=self.dlt.get_average_length(), uf=ufreq)
                            # calculate score
                            if docid in query_result:  # this document has already been scored once
                                query_result[docid] += score
                            else:
                                query_result[docid] = score

        return query_result

    def run_query_with_user_and_df(self, query, uid):
        query_result = dict()
        for term in query:
            if term.isalpha():
                if term not in stop_words:
                    lemmatizer.lemmatize(term)
                    if term in self.index:
                        doc_dict = self.index[term]
                        ufreq = self.index.get_frequency(term, uid)

                        for docid, freq in doc_dict.items():
                            score = score_BM25freq_combine(f=freq, qf=1, df=self.index.get_document_frequency(term),
                                                        N=len(self.dlt), dl=self.dlt.get_length(docid),
                                                        avdl=self.dlt.get_average_length(), uf=ufreq)
                            # calculate score
                            if docid in query_result:  # this document has already been scored once
                                query_result[docid] += score
                            else:
                                query_result[docid] = score

        return query_result