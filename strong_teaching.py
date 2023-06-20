


from generatingTeachingSets.teachingSetGenerator import getWitnessSet # [(val,0/1)]
from teachingSets import sizeFunction_w
from ConceptClass import sizeFunction_c, getConceptClass_itr
from compatibility import compatibility_check
from itertools import tee



def run():
    filename= "TeachingBook.csv"
    with open(filename, "w") as f:
        f.write("")

    teachingBook = {}
    alphabet = ["A","B","C","D","E"]

    #print("Generating all concepts...")
    #all_concepts = sorted(getConceptClasses(), key=sizeFunction_c)
    #print("done!")
    #print("Generating all witnessSets...")
    #all_teachingsets = sorted(getTeachingsets(),key = sizeFunction_w)
    #print("done!")
    set_of_used_concepts = set() # We store a set of all concepts ids found. We use a set beacuse all numbers would be to large.
    first_non_used_concept_generator = getConceptClass_itr(alphabet,size=7) # We want this to point to the latest non used concept.
    all_below_used = 0
    teaching_book_w = {}

    for i,w in enumerate(getWitnessSet(alphabet,budget=500)):
        #TODO: Check if first_non_used_concept_generator is empty
        orginal_iterator, copy_iterator = tee(first_non_used_concept_generator, 2) #Create two unique iterators
        first_non_used_concept_generator = orginal_iterator # Set one of the copies to the orignal.
        concept_number = all_below_used # Counter to keep track of current concept
        no_more = True
        while True: 
            boolean = None
            try:
                boolean = next(copy_iterator)
                no_more = False
            except StopIteration:
                break

            
            #c = boolean
            current_concept_number = concept_number
            concept_number += 1
            if current_concept_number in set_of_used_concepts:
                continue
            
            if compatibility_check(boolean,w, alphabet):
                set_of_used_concepts.add(current_concept_number)

                while all_below_used in set_of_used_concepts:
                    set_of_used_concepts.remove(all_below_used) # Keep the set small, remove as we go
                    all_below_used += 1  
                    try: 
                        next(first_non_used_concept_generator) #Keep this aligned with all_below_used
                    except StopIteration:
                        break
                    
               
                teachingBook[boolean] = w
                teaching_book_w[i]= boolean

                #if len(teachingBook) % 100 == 0:
                #        print(len(teachingBook), len(set_of_used_concepts), boolean,w)
                break

                    
        if no_more:
            break
        with open(filename, "a") as f:
            if i in teaching_book_w: # Check if the teaching set found a boolean concept compaitibl
                c = teaching_book_w[i]
                f.write(f"{c}, {w},{sizeFunction_c(c)},{sizeFunction_w(w)}\n")
    
                

if __name__ == "__main__":
    run()
    """
    ALPHABET = ["A","B"]

    
    iter_1 = iter([1,4,3,2,5,6])
    iter_2 = iter([3,2,1,4,5,6])


    all_below = 0
    set_of_found_ceoncepts = set()
    generator_first_non_used = iter_2
    for w in iter_1:
        orginal_iterator, copy_iterator = tee(generator_first_non_used, 2) #Create two unique iterators
        generator_first_non_used = orginal_iterator # Set one of the copies to the orignal.
        concept_number = all_below # Counter to keep track of current concept

        while True: 
            concept = None
            try:
                concept = next(copy_iterator)
            except:
                break
        

            if concept_number in set_of_found_ceoncepts:
                concept_number += 1
                print("We avoid these?")
                continue
            
            print(concept,concept_number)
            current_concept_number = concept_number
            concept_number += 1 
            if concept == w:
                set_of_found_ceoncepts.add(current_concept_number)
            

                while all_below in set_of_found_ceoncepts:
                    set_of_found_ceoncepts.remove(all_below) # Keep the set small, remove as we go
                    all_below += 1   

                    try: 
                        next(generator_first_non_used) #Keep this aligned with all_below_used
                    except:
                        break
                break


        """
                  
