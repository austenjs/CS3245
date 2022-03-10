from typing import Dict

class IndexTable:
  '''
  An IndexTable class that is in charge of converting terms (strings) 
  into termIDs (integers) 

  No unique attributes added to this class, using the default 
  constructor in Python. 

  Attributes:
  term_termID_dict(Dict[str, int]): Map a term into a term id
  '''

  def __init__(self):
    self.term_termID_dict = dict()
    self.id = 1

  def get_termID(self, term) -> int:
    '''
    Take a term and return the termID. If it doesn't exist,
    create a new termID.

    Argument:
    term (str): A term ID

    Return:
    A termID
    '''
    if term in self.term_termID_dict:
      return self.term_termID_dict[term]

    # Create new termID
    self.term_termID_dict[term] = self.id
    self.id += 1
    return self.id

  def term_to_termID(self,list_of_terms) -> Dict[str, int]:
    '''
    Take a list of terms and return a dictionary containing the 
    term-termID pair, where the term is the key and the termID
    is the value.

    It updates the term_termID_dict.

    Argument:
      list_of_terms : list of terms from the preprocessed words

    Return:
      Dictionary containing the unique term-termID pairs
    '''
    for term in list_of_terms:
      if term not in self.term_termID_dict:
        self.term_termID_dict[term] = self.id
        self.id += 1 
    
    return self.term_termID_dict

  def get_term_termID_dict(self) -> Dict[str, int]:
    '''
    A getter function to get the term_termID_dict.

    Return:
      Dictionary containing the unique term-termID pairs
    '''
    return self.term_termID_dict
