# -*- coding: utf-8 -*-
"""
markov.py

A tool to turn Project Gutenberg books into hours of fun.
Not that reading isn't already hours of fun.

Last updated February 24, 2015

@author: Stephanie Northway

"""
import string
import pickle
import random
from collections import Counter


FRAME_LENGTH = 2


def remove_chars(s, *chars):
    """
    Because WHY ISN'T THIS A STRING FUNCTION

    s: string to remove characters from
    *chars: sequence of characters to remove
    returns: s minus the unwanted characters
    """
    for c in chars:
        s = s.replace(c, '')
    return s


def process_pg_file(filepath):
    """
    Processes a Project Gutenberg book into a list of words and punctuation.

    filepath: the location of the file containing a Project Gutenberg book
    returns: the book, as a list of words
    """
    # Read the file
    f = open(filepath, 'r')
    lines = f.readlines()

    # Find the beginning and end of the actual book
    start_line = 0
    end_line = -1
    while lines[start_line].find('START OF THIS PROJECT GUTENBERG EBOOK') == -1:
        start_line += 1
    while lines[end_line].find('END OF THIS PROJECT GUTENBERG EBOOK') == -1:
        end_line -= 1

    # Return a list of all the words
    lines = lines[start_line+1:end_line]
    words = []
    unwanted_chars = ['_', '\\', '"']

    for l in lines:
        # line_words = l.strip(string.whitespace).replace('_', '').replace('\\', '').replace('"', '').lower().split(' ')
        l = remove_chars(l, *unwanted_chars)

        line_words = l.lower().split(' ')

        for w in line_words:
            # If a word ends in punctuation (that isn't an apostrophe), separate it.
            if len(w) > 1 and w[-1] in string.punctuation and w[-1] != "'":
                words.append(w[:-1])
                words.append(w[-1])
            else:
                if w.find('--') != -1:
                    words.extend([w.split('--')[0], '--', w.split('--')[1]])
                else:
                    words.append(w)
    # take out all the gosh dang empty strings
    return filter(lambda w: w != '', words)


def create_reference(word_list):
    """
    Takes in a book as a list of words, returns a dictionary with prefixes as keys
    and a Counter object with the frequency of 'next words' as values.

    word_list: book represented as a list of words and punctuation
    returns: crazy huge dictionary
    """
    reference_dict = {}
    for i in range(len(word_list)-FRAME_LENGTH):
        frame = tuple(word_list[i:i+FRAME_LENGTH])
        print frame
        if frame not in reference_dict.keys():
            reference_dict[frame] = Counter()
        try:
            reference_dict[frame].update([word_list[i+FRAME_LENGTH]])
        except Exception, e:
            print e

    return reference_dict


def store_reference(reference_dict, filepath='testPickle.p'):
    """
    Pickles the reference dictionary for future use.

    reference_dict: the painstakingly generated dictionary mapping ngrams to their following words
    filepath: where to save the .p file
    """
    with open(filepath, 'wb') as f:
        pickle.dump(reference_dict, f, pickle.HIGHEST_PROTOCOL)


def load_reference(filepath='testPickle.p'):
    """
    Loads a reference dictionary from a .p file.

    filepath: the file from which to load the thing
    returns: the unpickled reference dictionary
    """
    with open(filepath, 'rb') as f:
        unpickled = pickle.load(f)
    return unpickled


def generate_next_word(counter):
    """
    Given a Counter object, return a word based on the weights.
    Right now this is really really stupid, because it just makes it a list again.

    counter: collections.Counter object
    returns: a random key from counter weighted by the counts
    """
    l = []
    for key, value in counter.iteritems():
        l.extend([key]*value)
    return random.choice(l)


def generate_text(reference_dict, sentences=5):
    """
    Given a reference dictionary, return some number of sentences.

    reference_dict: a dictionary of the form {2-tuple: Counter}
    sentences: optional parameter for how many sentences you want, default 5
    """
    frame = random.choice(reference_dict.keys())
    words = list(frame)
    stop_chars = ['.', '?', '!']
    stops = 0
    while stops < sentences:
        next = generate_next_word(reference_dict[frame])
        words.append(next)
        frame = tuple(words[-FRAME_LENGTH:])
        if next in stop_chars:
            stops += 1

    wordstring = ' '.join(words)
    for p in remove_chars(string.punctuation, '('):
        wordstring = wordstring.replace(' '+p, p)
    return wordstring


def mash_references(r1, r2):
    """
    Given two reference dictionaries, returns a combination of them

    r1: a reference dictionary
    r2: a different reference dictionary
    returns: the union of r1 and r2
    """
    mashup = {}
    keys = set(r1.keys() + r2.keys())
    for k in keys:
        if r1.get(k) is not None:
            if r2.get(k) is not None:
                mashup[k] = r1.get(k) + r2.get(k)
            else:
                mashup[k] = r1[k]
        else:
            mashup[k] = r2[k]

    return mashup

if __name__ == '__main__':
    # huck_finn = load_reference(filepath='huck_finn.p')
    # critique = load_reference(filepath='critique_of_pure_reason.p')
    # huck_finn_of_pure_reason = mash_references(huck_finn, critique)
    print generate_text(load_reference('huck_finn_of_pure_reason.p'), sentences=3)
