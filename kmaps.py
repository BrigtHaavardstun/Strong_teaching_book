#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script defines a function to simplify boolean algebra expressions,
inspired by Karnaugh Map.
"""
# Credit: https://github.com/zhcHoward/Kmap/blob/master/Kmap.py


import itertools
from collections import defaultdict
from teachingSets import ALPHABET


class Term:
    def __init__(self, term="", source=None, flag=False):
        if source is None:
            source = set((int(term, 2),))
        self.term = term
        self.source = source
        self.flag = flag
        self.length = len(term)

    @property
    def ones(self):
        """ones counts the number of '1's in the term
        Returns:
            int: the amount of '1's
        """
        return len(list(filter(lambda c: c == "1", self.term)))

    def __eq__(self, other):
        if type(other) != type(self):
            return False
        return self.term == other.term

    def __str__(self):
        return self.term

    def __hash__(self):
        return hash(self.term)

    def __repr__(self):
        return self.__str__()


def diff_terms(term1, term2):
    if term1.length == term2.length:
        diff = 0
        pos = -1

        for idx, (t1, t2) in enumerate(zip(term1.term, term2.term)):
            if diff > 1:
                break
            else:
                if t1 != t2:
                    diff += 1
                    pos = idx

        if diff == 1:
            new_term = "*".join((term1.term[:pos], term2.term[pos + 1:]))
            new_source = term1.source | term2.source
            term1.flag = True
            term2.flag = True

            return Term(new_term, new_source)


def find_prime_implicants(minterms, not_cares):
    table = defaultdict(set)
    for term in minterms + not_cares:
        table[term.ones].add(term)

    prime_implicants = []
    new_implicants = True
    while new_implicants:
        new_implicants = False
        new_table = defaultdict(set)
        for key in sorted(table.keys()):
            # print(f"key == {key}")
            terms1 = table[key]
            terms2 = table[key + 1]
            if terms2:
                for t1, t2 in itertools.product(terms1, terms2):
                    new_term = diff_terms(t1, t2)
                    # print(f"{t1} + {t2} = {new_term}")
                    if not new_term:
                        continue

                    new_table[key].add(new_term)
                    new_implicants = True

            for term in terms1:
                if not term.flag:
                    # print(f"{term} become prime implicant")
                    prime_implicants.append(term)

        table = new_table

    return prime_implicants


def find_essential_prime_implicants(prime_implicants, minterms):
    chart = {}
    for source in itertools.chain.from_iterable((t.source for t in minterms)):
        chart[source] = set()

    for idx, implicant in enumerate(prime_implicants):
        for source in implicant.source:
            if source not in chart:
                continue

            chart[source].add(idx)

    sop = None
    for products in chart.values():
        sop = multiply(sop, products)

    min = float("inf")
    # Len(p) == num of ors + 1.
    
    ids = []

    for p in sop:
        #print("len:", len(p))
        #print(str(p))
        length = len(p)
        if length < min:
            min = length
            ids = [p]
        elif length == min:
            ids.append(p)
    
    ids = sop

    prime_imps =  [[prime_implicants[i] for i in p] for p in ids]
    return prime_imps

def multiply(result, product):
    if not result:
        return set((frozenset((p,)) for p in product))
    else:
        new_result = set()
        for a, b in itertools.product(result, product):
            new_result.add(a | set((b,)))
        return new_result


class Minterms(object):
    """ Minterms stores expressions for 1s and "don't care". """

    def __init__(
        self, minterms=None, not_cares=None,
    ):
        if minterms is None:
            minterms = []
        if not_cares is None:
            not_cares = []

        self.minterms = minterms
        self.not_cares = not_cares

    def simplify(self):
        prime_implicants = find_prime_implicants(self.minterms, self.not_cares)
        result = find_essential_prime_implicants(
            prime_implicants, self.minterms)
        return result


def find_all_minterms(tm, dc,alphabet):
    t_minterms = [Term(term) for term in tm]
    not_cares = [Term(term) for term in dc]
    minterms = Minterms(t_minterms, not_cares)
    res = minterms.simplify()
    index_letter = {}
    for i, l in enumerate(alphabet):
        index_letter[i] = l

    min_all = float("inf")
    minimum_min_term = None

    all_min_terms = []
    for term in res:
        term_formated = []
        size = 0
        for claus in term:
            current = ""
            for i, l in enumerate(str(claus)):
                if l == "*":
                    continue
                elif l == "1":
                    #print(i,l)
                    #print(index_letter)
                    size += 1
                    current += index_letter[i]
                elif l == "0":
                    current += index_letter[i] + "'"
                    size += 1
                else:
                    raise ValueError("Should be 1 or 0")
            
            term_formated.append(current)
        if term_formated == [""]:  # empty term
            return "T"
        if min_all > size:
            min_all = size
            minimum_min_term = "+".join(term_formated)

        all_min_terms.append("+".join(term_formated))
    return minimum_min_term
    #return all_min_terms

def bool_size(bool:str):
    if bool == "T" or bool == "F":
        return 0
    clauses = bool.replace("'","").split("+")
    size = sum([len(x) for x in clauses])
    return size

LIST_OF_ALL_BOOLS = None
from teachingSets import ALPHABET
def generate_all_booleans():
    global LIST_OF_ALL_BOOLS
    if not LIST_OF_ALL_BOOLS is None:
        return LIST_OF_ALL_BOOLS
    nr_letters = len(ALPHABET)
    all_configurations = []
    #for i in range(0, pow(2,pow(2,nr_letters))):
    for i in range(0, pow(2,pow(2,nr_letters))):
        all_configurations.append((bin(i)[2:].rjust(pow(2,nr_letters), "0")))
    
    all_str_terms = [bin(i)[2:].rjust(nr_letters, "0") for i in range(0,pow(2,nr_letters))]

    all_min_bool = []
    for configuration in all_configurations:
        str_term = [term for term,conf in zip(all_str_terms, configuration) if conf=="1"]
        if str_term == []:
            all_min_bool.append("F")
            continue
        all_min_bool.append(find_all_minterms(str_term, []))
    all_min_bool.sort(key=lambda x: str(x))
    all_min_bool.sort(key=lambda x:bool_size(x) )
    LIST_OF_ALL_BOOLS = all_min_bool
    print("\n".join(LIST_OF_ALL_BOOLS[:20]))
    return LIST_OF_ALL_BOOLS
    
def gpt4_generate_all_booleans(alphabet=["A","B","C","D","E","F","G"]):
    nr_letters = len(alphabet)
    all_str_terms = [bin(i)[2:].rjust(nr_letters, "0") for i in range(0,pow(2,nr_letters))]

    for i in range(0, pow(2,pow(2,nr_letters))):
        configuration = (bin(i)[2:].rjust(pow(2,nr_letters), "0"))
        str_term = [term for term,conf in zip(all_str_terms, configuration) if conf=="1"]
        if str_term == []:
            yield "F"
            continue
        yield find_all_minterms(str_term, [], alphabet)

def gpt4_save_to_file():
    # Usage
    alphabet = ["A","B","C","D"]
    with open("all_booleans.txt", "w") as f:
        big_list = []
        for i,bool_val in enumerate(gpt4_generate_all_booleans(alphabet=alphabet)):
            big_list.append(bool_val)
            if i % 10000 == 0:
                print(i)
            if len(big_list) > 700000:
                print("Writing!")
                f.write("\n".join(big_list))
                big_list = []
        if big_list != []:
            f.write("\n".join(big_list))


if __name__ == "__main__":
    gpt4_save_to_file()