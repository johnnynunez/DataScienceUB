import sys


class Sequence(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def size(self):
        """
        Returns the size of the sequence.
        """
        return len(self.x)

    def __len__(self):
        return len(self.x)

    def copy_sequence(self):
        """
        Performs a deep copy of the sequence
        """
        s = Sequence(self.x[:], self.y[:])
        return s

    def update_from_sequence(self, new_y):
        """
        Returns a new sequence equal to the previous but with y set to newy
        """
        s = Sequence(self.x, new_y)
        return s

    def to_words(self, sequence_list=False, only_tag_translation=False):
        assert sequence_list, "no sequence_list as been given therefore we do not know the \
                               mapping from integers to words or tags"

        if only_tag_translation:
            rep = ""
            for i, xi in enumerate(self.x):
                yi = self.y[i]
                rep += "%s/%s " % (xi,
                                   sequence_list.y_dict.get_label_name(yi))
        else:
            rep = ""
            for i, xi in enumerate(self.x):
                yi = self.y[i]
                rep += "%s/%s " % (sequence_list.x_dict.get_label_name(xi),
                                   sequence_list.y_dict.get_label_name(yi))
        return rep

    def __str__(self):
        rep = ""
        for i, xi in enumerate(self.x):
            yi = self.y[i]
            rep += "%s/%s " % (xi,
                               yi)
        return rep

    def __repr__(self):
        rep = ""
        for i, xi in enumerate(self.x):
            yi = self.y[i]
            rep += "%s/%s " % (xi,
                               yi)
        return rep


class UnicodeSequence(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def size(self):
        """
        Returns the size of the sequence.
        """
        return len(self.x)

    def __len__(self):
        return len(self.x)

    def copy_sequence(self):
        """
        Performs a deep copy of the sequence
        """
        s = Sequence(self.x[:], self.y[:])
        return s

    def update_from_sequence(self, new_y):
        """
        Returns a new sequence equal to the previous but with y set to newy
        """
        s = Sequence(self.x, new_y)
        return s

    def printseq(self):
        rep = unicode("")
        for i, xi in enumerate(self.x):
            yi = self.y[i]
            rep += xi + "/" + yi + " "
        print(rep)

    #def __repr__(self):
    #    rep = unicode("")
    #    for i, xi in enumerate(self.x):
    #        yi = self.y[i]
    #        rep += xi + unicode("/") + yi + unicode(" ")
    #    return rep
