from kmaps import generate_all_booleans,bool_size
from generateConcepts import generateConcepts
from itertools import combinations
from compatibility import compatibility_check
def sizeFunction_c(c):
    return bool_size(c)


#def getConceptClasses(alphabet,size=9):
    #return generateConcepts.getConcepts(alphabet=alphabet, budget=size)

def getConceptClass_itr(alpahabet,size=9):
    #TODO: I need to decide if i want to remove equal concepts
    # My attempt will be to store all the ids of the concepts found thus far. My hope is that the number of UNIQUE ids will be small
    # We use a set beacuse the full list will be to large.

    concept_ids_found = set()

    for concept in generateConcepts.getConcepts(alpahabet,size):
        concept_id = find_concept_id(concept, alpahabet)
        if concept_id in concept_ids_found:
            continue
        else:
            concept_ids_found.add(concept_id)
            
            yield concept

def generateAllSubsets(alphabet):
    yield []
    for k in alphabet:
        yield k
    for i in range(2,len(alphabet)+1):
        combinations_size_i = combinations(alphabet,i)
        for combination in combinations_size_i:
            yield combination

    
def convert_to_ws(subsets):
    for subset in subsets:
        yield [(subset, "1")]


def find_concept_id(concept,alphabet):
    subsets = generateAllSubsets(alphabet)
    witnessSets = convert_to_ws(subsets)
    final_string = ""
    for witnessSet in witnessSets:
        compatible = compatibility_check(concept, witnessSet, alphabet)
        if compatible:
            final_string += "1"
        else:
            final_string += "0"
    return int(final_string,2)


if __name__ == "__main__":
    print(find_concept_id("A+A'", ["A","B","C","D"]))