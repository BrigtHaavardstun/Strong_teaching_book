import itertools


def generateAndClauseOfSizeK(alphabet, size, negation=True):
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
        

def generateSubsetOfSizeK(alphabet,size):
    boolean_list = (list(itertools.combinations(alphabet, size)))
    return boolean_list

if __name__ == '__main__':
    for i in range(1,6):
        for bool in generateAndClauseOfSizeK(["A","B","C","D","E"],i):
            print(bool)

