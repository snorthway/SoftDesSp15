""" Evaluate the performance of various DNA proessing algorithms """

from random import randint
import time
import matplotlib.pyplot as plt

def generate_random_dna(n):
    """ Generate a random DNA sequence of length n """
    dna_list = []
    nucleotides = ['A','C','G','T']
    for i in range(n):
        r = randint(0,3)
        dna_list.append(nucleotides[r])
    return "".join(dna_list)

def get_complement(c):
    """ Returns the complimentary nucleotide to c """
    if c == 'A':
        return 'T'
    if c == 'C':
        return 'G'
    if c == 'G':
        return 'C'
    if c == 'T':
        return 'A'

def reverse_complement_1(dna):
    """ Method 2 for computing the reverse complementary sequence of DNA
        for the specfied DNA sequence
    
        dna: a DNA sequence represented as a string
        returns: the reverse complementary DNA sequence represented as a string
    >>> reverse_complement_1("ATGCCCGCTTT")
    'AAAGCGGGCAT'
    >>> reverse_complement_1("CCGCGTTCA")
    'TGAACGCGG'
    """
    return_val = ""
    for c in dna:
        return_val = get_complement(c) + return_val 
    return return_val

def reverse_complement_2(dna):
    """ Method 1 for Computing the reverse complementary sequence of DNA
        for the specfied DNA sequence
    
        dna: a DNA sequence represented as a string
        returns: the reverse complementary DNA sequence represented as a string
    >>> reverse_complement_2("ATGCCCGCTTT")
    'AAAGCGGGCAT'
    >>> reverse_complement_2("CCGCGTTCA")
    'TGAACGCGG'
    """
    return_val = []
    for c in reversed(dna):
        return_val.append(get_complement(c))
    return "".join(return_val)

if __name__ == '__main__':
    dna_length = range(50, 5000, 50)
    times_1 = []
    times_2 = []
    # import doctest
    # doctest.testmod()
    for l in dna_length:
        dna = generate_random_dna(l)
        start_time = time.time()
        rev_complement = reverse_complement_1(dna)
        stop_time = time.time()

        times_1.append(stop_time - start_time)

        dna = generate_random_dna(l)
        start_time = time.time()
        rev_complement = reverse_complement_2(dna)
        stop_time = time.time()

        times_2.append(stop_time - start_time)

    plt.plot(dna_length, times_1, 'b', label="alg 1")
    plt.plot(dna_length, times_2, 'r', label="alg 2")
    plt.xlabel('Length of DNA sequence')
    plt.ylabel('Time to run')
    plt.legend(loc='best')
    plt.show()