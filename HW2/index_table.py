from typing import Dict
import preprocessor

class IndexTable:
  '''
  An IndexTable class that is in charge of converting terms (strings) 
  into termIDs (integers) 

  No unique attributes added to this class, using the default 
  constructor in Python. 
  '''

  def term_to_termID(self,list_of_terms) -> Dict[str:int]:
    '''
    Take a list of terms and return a dictionary containing the 
    term-termID pair, where the term is the key and the termID
    is the value.

    Argument:
      list_of_terms : list of terms from the preprocessed words

    Return:
      Dictionary containing the unique term-termID pairs
    '''
    term_termID_pair = dict()
    id = 1

    for term in list_of_terms:
      if term not in term_termID_pair.keys():
        term_termID_pair[term] = id
      id +=1 
    
    return term_termID_pair
