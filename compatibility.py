

def compatibility_check(c,w, alphabet):
    if c == "T":
        return all(trueOrFalse=="1" for (c,trueOrFalse) in w)
    if c == "F":
        return all(trueOrFalse=="0" for (c,trueOrFalse) in w)
    # Make the boolean expression checkable
    clauses = c.split("+")
    
    # Our concept needs to match the witness set for all of its examples
    compatible_for_all = True
    for (example,trueOrFalse) in w: 
        bool_dict = {}
        for letter in example:
            bool_dict[letter] = True
        for letter in alphabet:
            if letter not in bool_dict:
                bool_dict[letter] = False
        

        # We check if any of the clauses match the current example
        current_compatibal = False
        for clause in clauses:
            this_clause_eval = True
            for i in range(len(clause)):
                if clause[i] == "'":
                    continue
                if i+1 < len(clause) and clause[i+1] == "'":
                    this_clause_eval = this_clause_eval and not bool_dict[clause[i]]

                else:
                    this_clause_eval = this_clause_eval and  bool_dict[clause[i]]

            current_compatibal = current_compatibal or this_clause_eval
            if current_compatibal:
                break
        if trueOrFalse == "1":
            trueOrFalse = True
        elif trueOrFalse == "0":
            trueOrFalse = False
        compatible_for_all = compatible_for_all and current_compatibal == trueOrFalse
        if not compatible_for_all:
            break
    
    return compatible_for_all


        


if __name__ == "__main__":
    boolean_expr = "AB+C'D"
    witness = [("AD",1),("ABCD",1)]
    print(compatibility_check(boolean_expr, witness))
