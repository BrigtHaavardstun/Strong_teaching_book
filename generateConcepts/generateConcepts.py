
import itertools
from itertools import tee

def all_combinations(total, highest=4):
    dp = [[[] for _ in range(total + 1)] for _ in range(highest + 1)]

    # Initialize base cases
    for i in range(highest + 1):
        dp[i][0] = [[]]
        
    for i in range(1, highest + 1):
        for j in range(1, total + 1):
            # Exclude the i
            if j < i:
                dp[i][j] = dp[i-1][j]
            else:
                # Include the i
                dp[i][j] = dp[i-1][j] + [combo + [i] for combo in dp[i][j-i]]

    

    return dp[highest][total]




def getConcepts(alphabet,budget=9):
    yield "T"
    yield "F"
    for total in range(1,budget+1):
        for sizes in all_combinations(total, len(alphabet)):
            for k in iter(recursive_add_teaching_set(sizes,alphabet)):
                yield k
            

def generateAndClauseOfSizeK(alphabet, size):
    boolean_list = (list(itertools.combinations(alphabet, size)))
    boolean_all_bools = []
    for boolean in boolean_list:
        boolean_w_negation = []
        for i in range(pow(2, size)-1,-1,-1): # To have order "deceding", first True,True,True,True, and then True,TrueTrue,False. Finaly False, False,...
            current_config = [bit=="1" for bit in bin(i)[2:].rjust(size, "0")]
            new_boolean = ""
            for b,c in zip(boolean, current_config):
                new_boolean += b
                if not c:
                    new_boolean += "'"

            boolean_w_negation.append(new_boolean)


        boolean_all_bools.extend(boolean_w_negation)   

    return boolean_all_bools


def recursive_add_teaching_set(sizes_to_add, alphabet, generator=None, prev_size=None):

    #figure out which generator should be used now.
    curr_size = sizes_to_add[0]
    if generator is None or prev_size != curr_size:
        generator = iter(generateAndClauseOfSizeK(alphabet=alphabet, size=curr_size))


    # Iterate over all (the rest) boolean expressions 
    while True:     
        try:
            boolean = next(generator)
        except StopIteration:
            break
            
        # If nothing more to add, return this and no recusive call
        if sizes_to_add[1:] == []: 
            yield boolean
            continue


        # As long as we have more to add to the WS.
        # We create an iterator and get all the results from it before moving on to the next boolean formula
        copy_iter, generator = tee(generator,2)
        itr = iter(recursive_add_teaching_set(sizes_to_add[1:],alphabet,copy_iter, curr_size))
        while True:
            try:
                current = next(itr)
                yield boolean + "+" + current
            except StopIteration: 
                break
            


if __name__ == "__main__":
    print("Start test")
    for k in getConcepts(alphabet=["A","B","C","D"],budget=8):
        print(k)