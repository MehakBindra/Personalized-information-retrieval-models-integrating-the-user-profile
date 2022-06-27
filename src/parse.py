import re
import nltk
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import stopwords

nltk.download("punkt")
nltk.download("stopwords")
nltk.download('wordnet')

lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))


class CorpusParser:

    def __init__(self, filename):
        self.filename = filename
        self.regex = re.compile('^#\s*\d+')
        self.corpus = dict()

    def parse(self):
        with open(self.filename) as f:
            s = ''.join(f.readlines())
        blobs = s.split('#')[1:]
        for x in blobs:
            text = x.split()
            final_text = []
            docid = text.pop(0)
            for word in text:
                if word.isalpha():
                    if word not in stop_words:
                        lemmatizer.lemmatize(word)
                        final_text.append(word)

            self.corpus[docid] = final_text

    def get_corpus(self):
        return self.corpus


class QueryParser:

    def __init__(self):
        pass

    @staticmethod
    def parse(query):
        parsed_query = query.rstrip().split()
        return parsed_query


class UserParser:

    def __init__(self, filename):
        self.filename = filename
        self.regex = re.compile('^#\s*\d+')
        self.users = dict()

    def parse(self):
        with open(self.filename) as f:
            s = ''.join(f.readlines())
        blobs = s.split('#')[1:]
        for x in blobs:
            text = x.split()
            final_text = []
            userid = text.pop(0)
            for word in text:
                if word.isalpha():
                    if word not in stop_words:
                        lemmatizer.lemmatize(word)
                        final_text.append(word)

            self.users[userid] = final_text

    def get_users(self):
        return self.users
