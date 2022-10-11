import codecs
import gzip
from skseq.sequences.label_dictionary import *
from skseq.sequences.sequence import *
from skseq.sequences.sequence_list import *
from os.path import dirname
import numpy as np

class PostagCorpus(object):
    """
    Reads a Dataset and saves as attributes of the instanciated corpus

    word_dict: dict
    A dictionary with the words in the data

    tag_dict: dict
    A dictionary containing all tags (states) in the observed sequences
    """
    def __init__(self):
        """
        Reads a Dataset and saves as attributes of the instanciated corpus

        word_dict: dict
        A dictionary with the words in the data

        tag_dict: dict
        A dictionary containing all tags (states) in the observed sequences
        """

        # Word dictionary.
        self.word_dict = LabelDictionary()

        # POS tag dictionary.
        # Initialize noun to be tag zero so that it the default tag.
        self.tag_dict = LabelDictionary()

        # Initialize sequence list.
        self.sequence_list = SequenceList(self.word_dict, self.tag_dict)


    def read_sequence_list_conll(self, train_file,
                                 mapping_file=("%s/en-ptb.map"
                                               % dirname(__file__)),
                                 max_sent_len=100,
                                 max_nr_sent=100000):
        """
        Reads data from the conll dataset
        """

        # Build mapping of postags:
        mapping = {}
        if mapping_file is not None:
            for line in open(mapping_file):
                coarse, fine = line.strip().split("\t")
                mapping[coarse.lower()] = fine.lower()

        instance_list = self.read_conll_instances(train_file,
                                                  max_sent_len,
                                                  max_nr_sent,
                                                  mapping)

        seq_list = SequenceList(self.word_dict, self.tag_dict)

        for sent_x, sent_y in instance_list:
            seq_list.add_sequence(sent_x, sent_y,  self.word_dict, self.tag_dict)

        return seq_list


    def read_conll_instances(self, file, max_sent_len, max_nr_sent, mapping):
        """
        Reads data from the conll dataset
        """

        if file.endswith("gz"):
            zf = gzip.open(file, 'rb')
            reader = codecs.getreader("utf-8")
            contents = reader(zf)
        else:
            contents = codecs.open(file, "r", "utf-8")

        nr_sent = 0
        instances = []
        ex_x = []
        ex_y = []
        nr_types = len(self.word_dict)
        nr_pos = len(self.tag_dict)
        for line in contents:
            toks = line.split()
            if len(toks) < 2:
                # print "sent n %i size %i"%(nr_sent,len(ex_x))
                if len(ex_x) < max_sent_len and len(ex_x) > 1:
                    # print "accept"
                    nr_sent += 1
                    instances.append([ex_x, ex_y])
                # else:
                #     if(len(ex_x) <= 1):
                #         print "refusing sentence of len 1"
                if nr_sent >= max_nr_sent:
                    break
                ex_x = []
                ex_y = []
            else:
                pos = toks[4]
                word = toks[1]
                pos = pos.lower()
                if pos not in mapping:
                    mapping[pos] = "noun"
                    print("unknown tag %s", pos)
                pos = mapping[pos]
                if word not in self.word_dict:
                    self.word_dict.add(word)
                if pos not in self.tag_dict:
                    self.tag_dict.add(pos)
                ex_x.append(word)
                ex_y.append(pos)
                # ex_x.append(self.word_dict[word])
                # ex_y.append(self.tag_dict[pos])
        return instances

    # Dumps a corpus into a file
    def save_corpus(self, dir):
        """
        Saves the corpus in the given directory
        """

        if not os.path.isdir(dir + "/"):
            os.mkdir(dir + "/")
        word_fn = codecs.open(dir + "word.dic", "w", "utf-8")
        for word_id, word in enumerate(self.int_to_word):
            word_fn.write("%i\t%s\n" % (word_id, word))
        word_fn.close()
        tag_fn = open(dir + "tag.dic", "w")
        for tag_id, tag in enumerate(self.int_to_tag):
            tag_fn.write("%i\t%s\n" % (tag_id, tag))
        tag_fn.close()
        word_count_fn = open(dir + "word.count", "w")
        for word_id, counts in self.word_counts.iteritems():
            word_count_fn.write("%i\t%s\n" % (word_id, counts))
        word_count_fn.close()
        self.sequence_list.save(dir + "sequence_list")

    # Loads a corpus from a file
    def load_corpus(self, dir):
        """
        Loads the corpus form the given directory
        """
        word_fn = codecs.open(dir + "word.dic", "r", "utf-8")
        for line in word_fn:
            word_nr, word = line.strip().split("\t")
            self.int_to_word.append(word)
            self.word_dict[word] = int(word_nr)
        word_fn.close()
        tag_fn = open(dir + "tag.dic", "r")
        for line in tag_fn:
            tag_nr, tag = line.strip().split("\t")
            if tag not in self.tag_dict:
                self.int_to_tag.append(tag)
                self.tag_dict[tag] = int(tag_nr)
        tag_fn.close()
        word_count_fn = open(dir + "word.count", "r")
        for line in word_count_fn:
            word_nr, word_count = line.strip().split("\t")
            self.word_counts[int(word_nr)] = int(word_count)
        word_count_fn.close()
        self.sequence_list.load(dir + "sequence_list")

        # Read a text file in conll format and return a sequence list



    def read_sequence_list_conll2002(self,
                                     train_file,
                                     min_sent_len=3,
                                     max_sent_len=100000,
                                     max_nr_sent=100000):
        """
        Reads the data form the conll2002 dataset of spanish named entity recognition
        """

        instance_list = self.read_conll2002_instances(train_file,
                                                      min_sent_len,
                                                      max_sent_len,
                                                      max_nr_sent,
                                                      )

        seq_list = SequenceList(self.word_dict, self.tag_dict)

        for sent_x, sent_y in instance_list:
            seq_list.add_sequence(sent_x, sent_y,  self.word_dict, self.tag_dict)

        return seq_list


    def read_conll2002_instances(self, file, min_sent_len, max_sent_len, max_nr_sent):
        """
        Reads the data form the conll2002 dataset of spanish named entity recognition
        """
        aux = codecs.open(file, encoding='latin-1')
        lines = []
        for line in aux:
            lines.append(line)

        data = []
        acum = []
        for line in lines:
            acum.append(line)
            if line == '\n':
                if len(acum) >= min_sent_len:
                    data.append(acum[0:-1])
                acum = []

        instances = []
        for d in data:
            x = []
            y = []
            for line in d:
                word = line.split()[0]
                tag = line.split()[2]

                if word not in self.word_dict:
                    self.word_dict.add(word)
                if tag not in self.tag_dict:
                    self.tag_dict.add(tag)

                x.append(word)
                y.append(tag)

            instances.append([x, y])

        return instances



    def read_sequence_list_train_BR(self,
                                    train_file_path="./Portugues_data/train-BR.tsv",
                                    min_sent_len=3,
                                    max_sent_len=100000,
                                    max_nr_sent=100000):
        """
        Reads the data form the train-BR dataset custom dataset tagged in vlex
        """

        instance_list = self.read_train_BR_instances( train_file_path,
                                                      min_sent_len,
                                                      max_sent_len,
                                                      max_nr_sent,
                                                      )

        seq_list = SequenceList(self.word_dict, self.tag_dict)

        for sent_x, sent_y in instance_list:
            seq_list.add_sequence(sent_x, sent_y,  self.word_dict, self.tag_dict)

        return seq_list


    def read_train_BR_instances(self, file_path, min_sent_len, max_sent_len, max_nr_sent):
        """
        Reads the data form the train-BR dataset custom dataset tagged in vlex
        """
        file = codecs.open(file_path, encoding='latin-1')
        
        data = []
        for line in file:
            data.append(line)

        sequences = []
        sequence = []
        for word in data:
            if ".\tO" in word[0:3]:
                sequence.append(word)
                sequences.append(sequence)
                sequence=[]
            else:
                sequence.append(word)

        instances = []
        for d in sequences:
            x = []
            y = []

            for word_tag in d:
                word, tag = word_tag.split("\t")
                tag = tag.split("\n")[0]

                if word not in self.word_dict:
                    self.word_dict.add(word)
                if tag not in self.tag_dict:
                    self.tag_dict.add(tag)

                x.append(word)
                y.append(tag)

            instances.append([x, y])

        return instances











## Hack don't look at the code below

class PostagUnicodeCorpus(object):

    def __init__(self):
        # POS tag dictionary.
        # Initialize noun to be tag zero so that it the default tag.
        self.tag_dict = LabelDictionary(['noun'])

        # Initialize sequence list.
        self.sequence_list = SequenceUnicodeList(self.tag_dict)

    # Read a text file in conll format and return a sequence list
    def read_sequence_list_conll2002(self,
                                 train_file,
                                 min_sent_len=3,
                                 max_sent_len=100000,
                                 max_nr_sent=100000):

        instance_list = self.read_conll2002_instances(train_file,
                                                      min_sent_len,
                                                      max_sent_len,
                                                      max_nr_sent,
                                                      )

        seq_list = SequenceUnicodeList(instance_list)

        for sent_x, sent_y in instance_list:
            seq_list.add_sequence(sent_x, sent_y)

        return seq_list

    def read_conll2002_instances(self, file, min_sent_len, max_sent_len, max_nr_sent):

        aux = codecs.open(file, encoding='latin-1')
        lines = []
        for line in aux:
            lines.append(line)

        data = []
        acum = []
        for line in lines:
            acum.append(line)
            if line == '\n':
                if len(acum) >= min_sent_len:
                    data.append(acum[0:-1])
                acum = []

        instances = []
        for d in data:
            x = []
            y = []
            for line in d:
                x.append(line.split()[0])
                y.append(line.split()[2])

            instances.append([x,y])

        return instances
