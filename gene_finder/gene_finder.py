# -*- coding: utf-8 -*-
"""
Created on Sun Feb  2 11:24:42 2014

@author: Stephanie Northway

"""

import random
import re

# from load import load_seq
from amino_acids import aa_table

STOP_CODONS = filter(lambda key: aa_table[key] == '|', aa_table.keys())  # list of stop codons
START_CODON = 'ATG'  # nottttt worth it


def shuffle_string(s):
    """ Shuffles the characters in the input string
        NOTE: this is a helper function, you do not have to modify this in any way """
    return ''.join(random.sample(s, len(s)))


def get_complement(nucleotide):
    """ Returns the complementary nucleotide

        nucleotide: a nucleotide (A, C, G, or T) represented as a string
        returns: the complementary nucleotide
    >>> get_complement('A')
    'T'
    >>> get_complement('C')
    'G'
    """
    complements = {'A': 'T', 'T': 'A', 'G': 'C', 'C': 'G'}
    return complements[nucleotide]


def get_sequence_complement(dna):
    """ Returns the complement of the sequence.
        dna: a DNA sequence
        returns: the complement of the sequence

    >>> get_sequence_complement("ATGCATGAATGTAGATAGATGTGCCC")
    'TACGTACTTACATCTATCTACACGGG'
    """
    return ''.join(get_complement(c) for c in dna)


def get_reverse_complement(dna):
    """ Computes the reverse complementary sequence of DNA for the specfied DNA
        sequence

        dna: a DNA sequence represented as a string
        returns: the reverse complementary DNA sequence represented as a string
    >>> get_reverse_complement("ATGCCCGCTTT")
    'AAAGCGGGCAT'
    >>> get_reverse_complement("CCGCGTTCA")
    'TGAACGCGG'
    """
    return get_sequence_complement(dna[::-1])


def rest_of_ORF(dna):
    """ Takes a DNA sequence that is assumed to begin with a start codon and returns
        the sequence up to but not including the first in frame stop codon.  If there
        is no in frame stop codon, returns the whole string.

        dna: a DNA sequence
        returns: the open reading frame represented as a string
    >>> rest_of_ORF("ATGTGAA")
    'ATG'
    >>> rest_of_ORF("ATGAGATAGG")
    'ATGAGA'
    >>> rest_of_ORF("ATGGGGGGGG")
    'ATGGGGGGGG'
    >>> rest_of_ORF("ATGCATGAATGTAGATAG")
    'ATGCATGAATGTAGA'
    """
    post_start = dna[3:]  # get string after start codon
    # find the stop codons used in this sequence
    stops = filter(lambda sc: post_start.find(sc) > -1, STOP_CODONS)
    # if there are any stop codons, find their indices and return the ORF up to the minimum stop codon index
    if len(stops):
        # get stop indices at multiples of 3
        stop_indices = []
        for sc in stops:
            stop_indices.extend([m.start() for m in re.finditer(sc, dna) if m.start() % 3 == 0])
        # return dna up to first legit stop codon
        if len(stop_indices):
            return dna[:min(stop_indices)]
    # if no stop codons, return the original sequence
    return dna


def find_all_ORFs_oneframe(dna):
    """ Finds all non-nested open reading frames in the given DNA sequence and returns
        them as a list.  This function should only find ORFs that are in the default
        frame of the sequence (i.e. they start on indices that are multiples of 3).
        By non-nested we mean that if an ORF occurs entirely within
        another ORF, it should not be included in the returned list of ORFs.

        dna: a DNA sequence
        returns: a list of non-nested ORFs
    >>> find_all_ORFs_oneframe("ATGCATGAATGTAGATAGATGTGCCC")
    ['ATGCATGAATGTAGA', 'ATGTGCCC']
    >>> find_all_ORFs_oneframe("ATGCATGAAATGGGGTAGTGTCCCATG")
    ['ATGCATGAAATGGGG', 'ATG']
    >>> find_all_ORFs_oneframe("ATGCCCGGGCCCTAGCCCATGTAGCCCCCCATGATGTTTTAGCCC")
    ['ATGCCCGGGCCC', 'ATG', 'ATGATGTTT']
    """
    # find indices of start codons
    # re.finditer returns an iterator over all non-overlapping matches in the string
    start_indices = [m.start() for m in re.finditer(START_CODON, dna) if m.start() % 3 == 0]

    substrings = []

    if len(start_indices):
        i = 0
        current_index = 0
        while i < len(start_indices):
            if start_indices[i] >= current_index:
                orf = rest_of_ORF(dna[start_indices[i]:])
                substrings.append(orf)
                current_index = start_indices[i] + len(orf)
            i += 1
    return substrings


def find_all_ORFs(dna):
    """ Finds all non-nested open reading frames in the given DNA sequence in all 3
        possible frames and returns them as a list.  By non-nested we mean that if an
        ORF occurs entirely within another ORF and they are both in the same frame,
        it should not be included in the returned list of ORFs.

        dna: a DNA sequence
        returns: a list of non-nested ORFs

    >>> find_all_ORFs("ATGCATGAATGTAG")
    ['ATGCATGAATGTAG', 'ATGAATGTAG', 'ATG']
    """
    all_orfs = []
    for i in range(3):
        all_orfs.extend(find_all_ORFs_oneframe(dna[i:]))
    return all_orfs


def find_all_ORFs_both_strands(dna):
    """ Finds all non-nested open reading frames in the given DNA sequence on both
        strands.

        dna: a DNA sequence
        returns: a list of non-nested ORFs
    >>> find_all_ORFs_both_strands("ATGCGAATGTAGCATCAAA")
    ['ATGCGAATG', 'ATGCTACATTCGCAT']
    """
    all_orfs = []
    all_orfs.extend(find_all_ORFs(dna))
    all_orfs.extend(find_all_ORFs(get_reverse_complement(dna)))
    return all_orfs


def longest_ORF(dna):
    """ Finds the longest ORF on both strands of the specified DNA and returns it
        as a string
    >>> longest_ORF("ATGCGAATGTAGCATCAAA")
    'ATGCTACATTCGCAT'
    """
    return max(find_all_ORFs_both_strands(dna), key=len)


def longest_ORF_noncoding(dna, num_trials):
    """ Computes the maximum length of the longest ORF over num_trials shuffles
        of the specfied DNA sequence

        dna: a DNA sequence
        num_trials: the number of random shuffles
        returns: the maximum length longest ORF
        """
    longest_orfs = []
    for n in num_trials:
        shuffled = shuffle_string(dna)
        longest_orfs.append(longest_ORF(shuffled))

    return longest_ORF(longest_orfs)


def coding_strand_to_AA(dna):
    """ Computes the Protein encoded by a sequence of DNA.  This function
        does not check for start and stop codons (it assumes that the input
        DNA sequence represents an protein coding region).

        dna: a DNA sequence represented as a string
        returns: a string containing the sequence of amino acids encoded by the
                 the input DNA fragment

        >>> coding_strand_to_AA("ATGCGA")
        'MR'
        >>> coding_strand_to_AA("ATGCCCGCTTT")
        'MPA'
    """
    codons = [dna[i:i+3] for i in range(len(dna)) if i % 3 == 0 and i + 3 <= len(dna)]
    return ''.join([aa_table[c] for c in codons])


def gene_finder(dna, threshold):
    """ Returns the amino acid sequences coded by all genes that have an ORF
        larger than the specified threshold.
        dna: a DNA sequence
        returns: a list of all amino acid sequences coded by the sequence dna.
    """
    orfs = find_all_ORFs_both_strands(dna)
    valid_genes = filter(lambda x: len(x) > threshold, orfs)
    return [coding_strand_to_AA(gene) for gene in valid_genes]

if __name__ == "__main__":
    import doctest
    doctest.testmod()
