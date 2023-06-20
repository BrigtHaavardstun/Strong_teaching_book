
from itertools import chain, combinations
ALPHABET = ["A","B","C","D","E","F","G"]

def powerset(iterable, max_size = float("inf")):
    s = list(iterable)
    all_sets = []
    if len(s) >= 0:
        all_sets.append([])
    if len(s) >= 1:
         all_sets.extend(list(s))
    all_sets.extend(list(chain.from_iterable(combinations(s, r) for r in range(2, min(max_size,len(s)+1),1))))
    all_sets = [sorted(["".join(sorted(b)) for b in a])for a in all_sets]
    return all_sets

ALL_TEACHINGSETS = None
def getTeachingsets():
    global ALL_TEACHINGSETS
    if ALL_TEACHINGSETS is not None:
        return ALL_TEACHINGSETS
    allTeachingsets = []
    k = 13
    for set in powerset(powerset(ALPHABET),k):
        for i in range(pow(2,len(set))):
            test = bin(i)[2:].rjust(len(set),"0") #We itterate over all bit string and set each element in TS to corresponding value
            allTeachingsets.append(list(zip(set,test)))
    ALL_TEACHINGSETS = allTeachingsets
    return ALL_TEACHINGSETS

def sizeFunction_w(TS):
    return sum([len(example) for (example,trueFalse) in TS ])



if __name__ == "__main__":
    prev = 0
    for k in sorted(getTeachingsets(),key=sizeFunction_w):
        #print(k)
        curr = sizeFunction_w(k)
        if curr < prev:
            print(k)
            break
        prev = curr

    print("\n".join(list(map(str, sorted(getTeachingsets(),key=sizeFunction_w)))[:30]))

