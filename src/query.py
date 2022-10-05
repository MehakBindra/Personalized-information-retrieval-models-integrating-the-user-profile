

from invdx import *
from rank import *
import nltk
from nltk import *
from nltk.corpus import wordnet
from nltk.stem.wordnet import WordNetLemmatizer 
# from rank import score_BM25
# from rank import score_BM25S
# from rank import score_BM25score_combine
# from rank import score_BM25freq_combine
import operator

b=0.75

alpha_3=0.5

class QueryProcessor:
        def __init__(self, queries, corpus,profile):
                self.queries = queries
                self.profile = profile 
                self.index, self.dlt ,self.indexfp = build_data_structures(corpus,profile)
                self.index1, self.dlt1 ,self.indexfp1 = build_data_structures1(corpus,profile)


        def run1(self,b):
                results = []
                for query in self.queries:
                        results.append(self.run_query1(query,b))
                return results

        def run2(self,b):
                results = []
                for userid in self.profile:
                        for query in self.queries:
                                results.append(self.run_query2(userid,b))
                return results
        
        def run3(self,b):
                results=[]
                for userid in self.profile:
                        for query in self.queries:
                                results.append(self.run_query3(query,userid,b))
                return results
        
        def run4(self,b):
                results = []
                for userid in self.profile:
                        for query in self.queries:
                                results.append(self.run_query4(query,userid,b))
                return results

        def run5(self,b):
                results = []
                for query in self.queries:
                        results.append(self.run_query5(query,b))
                return results

        def run6(self,b):
                results = []
                for userid in self.profile:
                        for query in self.queries:
                                results.append(self.run_query6(userid,b))
                return results
        
        def run7(self,b):
                results = []
                for userid in self.profile:
                        for query in self.queries:
                                results.append(self.run_query7(query,userid,b))
                return results
        
        def run8(self,b):
                results = []
                for userid in self.profile:
                        for query in self.queries:
                                results.append(self.run_query8(query,userid,b))
                return results


        def run_query1(self, query,b):
                query_result = dict()
                wordnet_lemmatizer = WordNetLemmatizer()
                adjective_tags = ['JJ','JJR','JJS']
                noun_tags = ['NN' ,'NNS' ,'NNP' ,'NNPS']
                verb_tags = ['VB','VBD','VBG','VBN','VBP','VBZ']
                adverb_tags = ['RB','RBR','RBS']
                
                for term in query:
                        query=str(query).lower()
                        POS_tag = nltk.pos_tag(query)
                        for word in POS_tag:
                                if word[1] in adjective_tags:
                                        term = wordnet_lemmatizer.lemmatize(word[0],wordnet.ADJ)
                                elif word[1] in noun_tags:
                                        term = wordnet_lemmatizer.lemmatize(word[0],wordnet.NOUN)
                                elif word[1] in verb_tags:
                                        term = wordnet_lemmatizer.lemmatize(word[0],wordnet.VERB)
                                elif word[1] in adverb_tags:
                                        term = wordnet_lemmatizer.lemmatize(word[0],wordnet.ADV)
                                else:
                                        term=word[0]
                       
                        if term in self.index.index:
                                doc_dict = self.index.index[term] # retrieve index entry
                                for docid in doc_dict:
                                        freq=self.index.get_document_frequency(term,docid) #for each document and its word frequency
                                        score = score_BM25(qf=query.count(term),inf=self.index.get_index_frequency(term), df=freq, N=len(self.dlt),
                                                                           dl=self.dlt.get_length(docid), avdl=self.dlt.get_average_length(),b=b) # calculate score
                                        if docid in query_result: #this document has already been scored once
                                                query_result[docid]+= score
                                        else:
                                                 query_result[docid]= score
                                                
                return query_result

        def run_query5(self, query,b):
            query_result = dict()
            
            for term in query:
                    if term in self.index1.index:
                            doc_dict = self.index1.index[term] # retrieve index entry
                            for docid in doc_dict:
                                    freq=self.index1.get_document_frequency(term,docid) #for each document and its word frequency
                                    score = score_BM25(qf=query.count(term),inf=self.index1.get_index_frequency(term), df=freq, N=len(self.dlt),
                                                                       dl=self.dlt.get_length(docid), avdl=self.dlt.get_average_length(),b=b) # calculate score
                                    if docid in query_result: #this document has already been scored once
                                            query_result[docid]+= score
                                    else:
                                             query_result[docid]= score
                                            
            return query_result


        def run_query2(self,userid,b):
                query_result = dict()
                wordnet_lemmatizer = WordNetLemmatizer()
                adjective_tags = ['JJ','JJR','JJS']
                noun_tags = ['NN' ,'NNS' ,'NNP' ,'NNPS']
                verb_tags = ['VB','VBD','VBG','VBN','VBP','VBZ']
                adverb_tags = ['RB','RBR','RBS']
                
                for term in self.profile[userid]:
                        POS_tag = nltk.pos_tag(self.profile[userid])
                        for word in POS_tag:
                                if word[1] in adjective_tags:
                                        term = wordnet_lemmatizer.lemmatize(word[0],wordnet.ADJ)
                                elif word[1] in noun_tags:
                                        term = wordnet_lemmatizer.lemmatize(word[0],wordnet.NOUN)
                                elif word[1] in verb_tags:
                                        term = wordnet_lemmatizer.lemmatize(word[0],wordnet.VERB)
                                elif word[1] in adverb_tags:
                                        term = wordnet_lemmatizer.lemmatize(word[0],wordnet.ADV)
                                else:
                                        term=word[0]
                       
                        if term in self.index.index:
                                doc_dict = self.index.index[term] # retrieve index entry
                                for docid in doc_dict: #for each document and its word frequency
                                        freq=self.index.get_document_frequency(term,docid)
                                        score = score_BM25S_profile( df=freq, inf=self.index.get_index_frequency(term), N=len(self.dlt),dl=self.dlt.get_length(docid), avdl=self.dlt.get_average_length(),uf=self.indexfp.get_profile_frequency(term,userid),b=b) # calculate score
                                        if docid in query_result: #this document has already been scored once
                                                query_result[docid]+= score
                                        else:
                                                 query_result[docid]= score
                                                
                return query_result
        def run_query6(self,userid,b):
                query_result = dict()
                for term in self.profile[userid]:
                        if term in self.index1.index:
                                doc_dict = self.index1.index[term] # retrieve index entry
                                for docid in doc_dict: #for each document and its word frequency
                                        freq=self.index1.get_document_frequency(term,docid)
                                        score = score_BM25S_profile( df=freq, inf=self.index1.get_index_frequency(term), N=len(self.dlt),dl=self.dlt.get_length(docid), avdl=self.dlt.get_average_length(),uf=self.indexfp1.get_profile_frequency(term,userid),b=b) # calculate score
                                        if docid in query_result: #this document has already been scored once
                                                query_result[docid]+= score
                                        else:
                                                 query_result[docid]= score
                                                
                return query_result

        def run_query3(self, query,userid,b):
                query_result = dict()
                wordnet_lemmatizer = WordNetLemmatizer()
                adjective_tags = ['JJ','JJR','JJS']
                noun_tags = ['NN' ,'NNS' ,'NNP' ,'NNPS']
                verb_tags = ['VB','VBD','VBG','VBN','VBP','VBZ']
                adverb_tags = ['RB','RBR','RBS']
                
                for term in query:
                        query=str(query).lower()
                        # query=word_tokenize(query)
                        POS_tag = nltk.pos_tag(query)
                        for word in POS_tag:
                                if word[1] in adjective_tags:
                                        term = wordnet_lemmatizer.lemmatize(word[0],wordnet.ADJ)
                                elif word[1] in noun_tags:
                                        term = wordnet_lemmatizer.lemmatize(word[0],wordnet.NOUN)
                                elif word[1] in verb_tags:
                                        term = wordnet_lemmatizer.lemmatize(word[0],wordnet.VERB)
                                elif word[1] in adverb_tags:
                                        term = wordnet_lemmatizer.lemmatize(word[0],wordnet.ADV)
                                else:
                                        term=word[0]
                       
                        if term in self.index.index:
                                doc_dict = self.index.index[term] # retrieve index entry
                                for docid in doc_dict: #for each document and its word frequency
                                        freq=self.index.get_document_frequency(term,docid)
                                        score = score_BM25(qf=query.count(term),inf=self.index.get_index_frequency(term), df=freq, N=len(self.dlt),
                                                                           dl=self.dlt.get_length(docid), avdl=self.dlt.get_average_length(),b=b) # calculate score
                                        if docid in query_result: #this document has already been scored once
                                                query_result[docid]+= score
                                        else:
                                                 query_result[docid]= score
                for term in self.profile[userid]:
                        POS_tag = nltk.pos_tag(str(self.profile[userid]).lower())
                        for word in POS_tag:
                                if word[1] in adjective_tags:
                                        term = wordnet_lemmatizer.lemmatize(word[0],wordnet.ADJ)
                                elif word[1] in noun_tags:
                                        term = wordnet_lemmatizer.lemmatize(word[0],wordnet.NOUN)
                                elif word[1] in verb_tags:
                                        term = wordnet_lemmatizer.lemmatize(word[0],wordnet.VERB)
                                elif word[1] in adverb_tags:
                                        term = wordnet_lemmatizer.lemmatize(word[0],wordnet.ADV)
                                else:
                                        term=word[0]
                       
                        if term in self.index.index:
                                doc_dict = self.index.index[term] # retrieve index entry
                                for docid in doc_dict: #for each document and its word frequency
                                        freq=self.index.get_document_frequency(term,docid)
                                        score = score_BM25S_profile( df=freq, inf=self.index.get_index_frequency(term), N=len(self.dlt),dl=self.dlt.get_length(docid), avdl=self.dlt.get_average_length(),uf=self.indexfp.get_profile_frequency(term,userid),b=b) # calculate score
                                        if docid in query_result: #this document has already been scored once
                                                query_result[docid]+= alpha_3*score
                                        else:
                                                 query_result[docid]= alpha_3*score
                
                                                
                return query_result
        def run_query7(self, query,userid,b):
                query_result = dict()

                for term in query:
                        if term in self.index1.index:
                                doc_dict = self.index1.index[term] # retrieve index entry
                                for docid in doc_dict: #for each document and its word frequency
                                        freq=self.index1.get_document_frequency(term,docid)
                                        score = score_BM25(qf=query.count(term),inf=self.index1.get_index_frequency(term), df=freq, N=len(self.dlt),
                                                                           dl=self.dlt.get_length(docid), avdl=self.dlt.get_average_length(),b=b) # calculate score
                                        if docid in query_result: #this document has already been scored once
                                                query_result[docid]+= score
                                        else:
                                                 query_result[docid]= score
                for term in self.profile[userid]:
                        if term in self.index.index:
                                doc_dict = self.index.index[term] # retrieve index entry
                                for docid in doc_dict: #for each document and its word frequency
                                        freq=self.index.get_document_frequency(term,docid)
                                        score = score_BM25S_profile( df=freq, inf=self.index.get_index_frequency(term), N=len(self.dlt),dl=self.dlt.get_length(docid), avdl=self.dlt.get_average_length(),uf=self.indexfp.get_profile_frequency(term,userid),b=b) # calculate score
                                        if docid in query_result: #this document has already been scored once
                                                query_result[docid]+= alpha_3*score
                                        else:
                                                 query_result[docid]= alpha_3*score
                
                                                
                return query_result

        def run_query4(self, query,userid,b):
                query_result = dict()
                wordnet_lemmatizer = WordNetLemmatizer()
                adjective_tags = ['JJ','JJR','JJS']
                noun_tags = ['NN' ,'NNS' ,'NNP' ,'NNPS']
                verb_tags = ['VB','VBD','VBG','VBN','VBP','VBZ']
                adverb_tags = ['RB','RBR','RBS']
                
                for term in query:
                        query=str(query).lower()
                        POS_tag = nltk.pos_tag(query)
                        for word in POS_tag:
                                if word[1] in adjective_tags:
                                        term = wordnet_lemmatizer.lemmatize(word[0],wordnet.ADJ)
                                elif word[1] in noun_tags:
                                        term = wordnet_lemmatizer.lemmatize(word[0],wordnet.NOUN)
                                elif word[1] in verb_tags:
                                        term = wordnet_lemmatizer.lemmatize(word[0],wordnet.VERB)
                                elif word[1] in adverb_tags:
                                        term = wordnet_lemmatizer.lemmatize(word[0],wordnet.ADV)
                                else:
                                        term=word[0]
                       
                        if(term in self.profile[userid]):
                            if term in self.index.index:
                                doc_dict = self.index.index[term] # retrieve index entry
                                for docid in doc_dict: #for each document and its word frequency
                                        freq=self.index.get_document_frequency(term,docid)
                                        score = score_BM25freq_combine(qf=query.count(term),inf=self.index.get_index_frequency(term), df=freq, N=len(self.dlt),
                                                                           dl=self.dlt.get_length(docid), avdl=self.dlt.get_average_length(),uf=self.indexfp.get_profile_frequency(term,userid),b=b) # calculate score
                                        if docid in query_result: #this document has already been scored once
                                                query_result[docid]+= score
                                        else:
                                                 query_result[docid]= score
                                                
                return query_result
        
        def run_query8(self, query,userid,b):
                query_result = dict()
                for term in query:
                    if(term in self.profile[userid]):
                        if term in self.index1.index:
                                doc_dict = self.index1.index[term] # retrieve index entry
                                for docid in doc_dict: #for each document and its word frequency
                                        freq=self.index1.get_document_frequency(term,docid)
                                        score = score_BM25freq_combine(qf=query.count(term),inf=self.index1.get_index_frequency(term), df=freq, N=len(self.dlt),
                                                                           dl=self.dlt.get_length(docid), avdl=self.dlt.get_average_length(),uf=self.indexfp1.get_profile_frequency(term,userid),b=b) # calculate score
                                        if docid in query_result: #this document has already been scored once
                                                query_result[docid]+= score
                                        else:
                                                 query_result[docid]= score
                                                
                return query_result
