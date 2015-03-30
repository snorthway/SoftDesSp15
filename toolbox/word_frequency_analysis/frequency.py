""" Analyzes the word frequencies in a book downloaded from
    Project Gutenberg """

import string
from collections import Counter

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

def get_word_list(file_name):
    """ Reads the specified project Gutenberg book.  Header comments,
        punctuation, and whitespace are stripped away.  The function
        returns a list of the words used in the book as a list.
        All words are converted to lower case.
    """
    # Read the file
    f = open(file_name, 'r')
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

def get_top_n_words(word_list, n):
    """ Takes a list of words as input and returns a list of the n most frequently
        occurring words ordered from most to least frequently occurring.
        word_list: a list of words (assumed to all be in lower case with no
                    punctuation
        n: the number of words to return
        returns: a list of n most frequently occurring words ordered from most
                 frequently to least frequentlyoccurring
    """
    c = Counter(word_list)
    return c.most_common(n)

if __name__ == '__main__':
    print get_top_n_words(get_word_list('pg32325.txt'), 10)