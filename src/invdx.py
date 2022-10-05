#invdx.py
# An inverted index

import nltk
from nltk import *
from nltk.corpus import wordnet
from nltk import word_tokenize
from nltk.stem.wordnet import WordNetLemmatizer

class InvertedIndex:

        def __init__(self):
                self.index = dict()

        def add(self, word, docid):
                if word in self.index:
                        if docid in self.index[word]:
                                self.index[word][docid] += 1
                        else:
                                self.index[word][docid] = 1
                else:
                        d = dict()
                        d[docid] = 1
                        self.index[word] = d

        #frequency of word in document
        def get_document_frequency(self, word, docid):
                if word in self.index:
                        if docid in self.index[word]:
                                return self.index[word][docid]
                        else:
                                raise LookupError('%s not in document %s' % (str(word), str(docid)))
                else:
                        raise LookupError('%s not in index' % str(word))

        #frequency of word in index, i.e. number of documents that contain word
        def get_index_frequency(self, word):
                if word in self.index:
                        return len(self.index[word])
                else:
                        raise LookupError('%s not in index' % word)


class InvertedIndexForprofile:

        def __init__(self):
                self.index = dict()

        def add(self, word, userid):
                if word in self.index:
                        if userid in self.index[word]:
                                self.index[word][userid] += 1
                        else:
                                self.index[word][userid] = 1
                else:
                        d = dict()
                        d[userid] = 1
                        self.index[word] = d

        #frequency of word in profile
        def get_profile_frequency(self, word, userid):
                if word in self.index:
                        if userid in self.index[word]:
                                return self.index[word][userid]
                        else:
                                # raise LookupError('%s not in document %s' % (str(word), str(userid)))
                                return -1
                else:
                        # raise LookupError('%s not in index' % str(word))
                        return -1


 
class DocumentLengthTable:

        def __init__(self):
                self.table = dict()

        def __len__(self):
                return len(self.table)

        def add(self, docid, length):
                self.table[docid] = length

        def get_length(self, docid):
                if docid in self.table:
                        return self.table[docid]
                else:
                        raise LookupError('%s not found in table' % str(docid))

        def get_average_length(self):
                sum = 0
                for d in self.table:
                        sum += self.table[d]
                return float(sum) / float(len(self.table))

def build_data_structures1(corpus,profile):
        idx = InvertedIndex()
        dlt = DocumentLengthTable()
        idxfp =InvertedIndexForprofile()
        for docid in corpus:

                #build inverted index
                for word in corpus[docid]:
                        idx.add(str(word), str(docid))

                #build document length table
                length = len(corpus[str(docid)])
                dlt.add(docid, length)
        for userid in profile:

                for word in profile[userid]:
                        idxfp.add(str(word),str(userid))

                        
        return idx, dlt ,idxfp 
def build_data_structures(corpus,profile):
        idx = InvertedIndex()
        dlt = DocumentLengthTable()
        # idxfp =InvertedIndex()
        
        idxfp =InvertedIndexForprofile()
        wordnet_lemmatizer = WordNetLemmatizer()
        adjective_tags = ['JJ','JJR','JJS']
        noun_tags = ['NN' ,'NNS' ,'NNP' ,'NNPS']
        verb_tags = ['VB','VBD','VBG','VBN','VBP','VBZ']
        adverb_tags = ['RB','RBR','RBS']
        for docid in corpus:

                #build inverted index
                corpus[docid]=str(corpus[docid]).lower()
                corpus[docid]=word_tokenize(corpus[docid])
                POS_tag = nltk.pos_tag(corpus[docid])
                for word in POS_tag:
                        if word[1] in adjective_tags:
                                word = wordnet_lemmatizer.lemmatize(word[0],wordnet.ADJ)
                        elif word[1] in noun_tags:
                                word = wordnet_lemmatizer.lemmatize(word[0],wordnet.NOUN)
                        elif word[1] in verb_tags:
                                word = wordnet_lemmatizer.lemmatize(word[0],wordnet.VERB)
                        elif word[1] in adverb_tags:
                                word = wordnet_lemmatizer.lemmatize(word[0],wordnet.ADV)
                        else:
                                word=word[0]
                for word in corpus[docid]:
                        word = word.lower()
                        if ( (word != "the") & (word !="a") & (word != "or") & (word != "and") & (word != "an") ) :
                                idx.add(str(word), str(docid))

                #build document length table
                length = len(corpus[str(docid)])
                dlt.add(docid, length)
        for userid in profile:
                profile[userid]=str(profile[userid]).lower()
                profile[userid]=word_tokenize(profile[userid])
                POS_tag = nltk.pos_tag(profile[userid])
                for word in POS_tag:
                        if word[1] in adjective_tags:
                                word = wordnet_lemmatizer.lemmatize(word[0],wordnet.ADJ)
                        elif word[1] in noun_tags:
                                word = wordnet_lemmatizer.lemmatize(word[0],wordnet.NOUN)
                        elif word[1] in verb_tags:
                                word = wordnet_lemmatizer.lemmatize(word[0],wordnet.VERB)
                        elif word[1] in adverb_tags:
                                word = wordnet_lemmatizer.lemmatize(word[0],wordnet.ADV)
                        else:
                                word=word[0]
                        

                for word in profile[userid]:
                        word = word.lower()
                        if ( (word != "the") & (word !="a") & (word != "or") & (word != "and") & (word != "an") ) :
                                idxfp.add(str(word),str(userid))

                        
        return idx, dlt ,idxfp 
