from typing import List,Tuple, Dict
from math import sqrt

class MemoryIndexing:
  '''
  MemoryIndexing class in charge of storing methods for
  in-memory index creation for the documents

  No unique attributes added to this class, using the default 
  constructor in Python.
  '''
  def create_term_docid_pair(self,list_of_terms,doc_id) -> List[Tuple[str,int]]:
    '''
    Take a list of terms from a particular document and the unique 
    doc_id associated with the terms and returns a list of term-
    doc_id pairs stored in a tuple.

    Arguments:
      list_of_terms : list of terms from the particular document.
      doc_id        : the unique document ID.

    Return: 
      List containing the term-docID pairs stored in a tuple.
    '''
    term_docid_pairs = []

    for term in list_of_terms:
      pair = (term,doc_id)
      term_docid_pairs.append(pair)

    return term_docid_pairs


  def create_dictionary_trie(self, list_of_terms, frequency) -> Dict[str, List[int]]:
    '''
    Take a list of terms from a particular document, the
    posting dictionary (to get the doc frequency)  and returns a 
    dictionary that represents the trie-representation of the 
    words inside the list of terms. 

    Arguments:
      list_of_terms : list of terms from the particular document

    
    Return:
      Dictionary representing the trie-representation of the words
      inside the document.
    '''
    root = {}

    for term in list_of_terms:
      current_node = root
      for char in term:
        current_node = current_node.setdefault(char,{})
      current_node['_end_'] = [frequency[term]]
    return root


  def create_posting(self,term_docid_pairs,document_length) -> Dict[str, List[Tuple[int,int]]]:
    '''
    Take a list of term-docID pairs stored in a tuple and returns 
    a dictionary where the key is the term and the value is a list of 
    tuples containing DocID,term frequencies, and document length. 

    Argument:
      term_docid_pairs  : list containing the term-docID pairs stored in a tuple.

    Return:
      Dictionary with term_list-of-docID-term_frequency key-value pairs. 

    Note: If the current node does not have skip pointer, it will be labelled as (..., None, None)
    '''
    posting_dict = dict()
    exist_posting = set()

    for term, doc_id in term_docid_pairs:
      # Duplicate
      if (term, doc_id) in exist_posting:
        posting_dict[term][doc_id] +=1
        continue
      if term not in posting_dict.keys():
        posting_dict[term] = dict()
        posting_dict[term][doc_id] = 1 
      else:
        posting_dict[term][doc_id] = 1
      exist_posting.add((term, doc_id))

    # Turn them into list of tuples
    posting_dict_term_freq = dict()
    for term in posting_dict.keys():
      posting_dict_term_freq[term] = [(doc_id,term_freq,document_length[doc_id]) for doc_id,term_freq in posting_dict[term].items()]

    return posting_dict_term_freq