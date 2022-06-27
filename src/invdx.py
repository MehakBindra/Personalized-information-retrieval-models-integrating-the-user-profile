class InvertedIndex:

    def __init__(self):
        self.index = dict()

    def __contains__(self, item):
        return item in self.index

    def __getitem__(self, item):
        return self.index[item]

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

    # frequency of word in document
    def get_frequency(self, word, docid):
        if word in self.index:
            if docid in self.index[word]:
                return self.index[word][docid]
            else:
                return 0
        else:
            return 0

    # frequency of word in index, i.e. number of documents that contain word
    def get_document_frequency(self, word):
        if word in self.index:
            return len(self.index[word])
        else:
            raise LookupError('%s not in index' % word)


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
        for length in self.table.values():
            sum += length
        return float(sum) / float(len(self.table))


class InvertedIndexForUser(object):

    def __init__(self):
        self.index = dict()

    def __contains__(self, item):
        return item in self.index

    def __getitem__(self, item):
        return self.index[item]

    def add(self, word, uid):
        if word in self.index:
            if uid in self.index[word]:
                self.index[word][uid] += 1
            else:
                self.index[word][uid] = 1
        else:
            d = dict()
            d[uid] = 1
            self.index[word] = d

    # frequency of word in document
    def get_frequency(self, word, uid):
        if word in self.index:
            if uid in self.index[word]:
                return self.index[word][uid]
            else:
                raise LookupError('%s not in document %s' % (str(word), str(uid)))
        else:
            raise LookupError('%s not in index' % str(word))

    # frequency of word in index, i.e. number of documents that contain word
    def get_document_frequency(self, word):
        if word in self.index:
            return len(self.index[word])
        else:
            raise LookupError('%s not in index' % word)


def build_data_structures(corpus, users):
    idx = InvertedIndex()
    idx_u = InvertedIndexForUser()
    dlt = DocumentLengthTable()

    for uid in users:
        # build inverted index
        for word in users[uid]:
            idx_u.add(str(word), str(uid))

    for docid in corpus:

        # build inverted index
        for word in corpus[docid]:
            idx.add(str(word), str(docid))

        # build document length table
        length = len(corpus[str(docid)])
        dlt.add(docid, length)
    return idx, idx_u, dlt
