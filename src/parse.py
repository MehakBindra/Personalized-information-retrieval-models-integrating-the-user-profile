
import re


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
			# x=x[2:]
			text = x.split()
			docid=text[0]
			# docid = text.pop(0)
			self.corpus[docid] = text[1:]

	def get_corpus(self):
		return self.corpus


class QueryParser:

	def __init__(self, filename):
		self.filename = filename
		self.queries = []

	def parse(self):
		with open(self.filename) as f:
			lines = ''.join(f.readlines())
		self.queries = [x.rstrip().split() for x in lines.split('\n')[:-1]]

	def get_queries(self):
		return self.queries


class ProfileParser:

        def __init__(self,filename):
                self.filename = filename
                self.profile=dict()

        def parse(self):
                i=1;
                with open(self.filename,encoding="utf8") as f:
                        p=''.join(f.readlines())
                for x in p.split('),('):
                        text = x.split(',')
                        userid = i
                        i +=1
                        self.profile[userid]=text

        def get_profile(self):
                return self.profile

