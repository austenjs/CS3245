from typing import List,Tuple, Dict

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


  def create_dictionary_trie(self,list_of_terms,posting_dictionary) -> Dict[str, List[int,int]]:
    '''
    Take a list of terms from a particular document, the
    posting dictionary (to get the doc frequency), and the index
    table to map the term to termIDs and returns a 
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
      current_node['_end_'] = [term,len(posting_dictionary[term])] 
    '''
    if it founds the end marker, get the key pointer to the postings list and the document frequency
    '''
    return root


  def create_posting(self,termid_docid_pairs,) -> Dict[int, List[int]]:
    '''
    Take a list of term-docID pairs stored in a tuple and the index
    table that maps the terms to termIDs and returns a dictionary
    where the key is the term and the value is a list that contains 
    the different docIDs that contains the term.

    Argument:
      term_docid_pairs  : list containing the term-docID pairs stored in a tuple.

    Return:
      Dictionary with term_list-of-docIDs key-value pairs. 
    '''
    posting_dict = dict()
    exist_posting = set()

    for term_id, doc_id in termid_docid_pairs:
      # Duplicate
      if (term_id, doc_id) in exist_posting:
        continue
      if term_id not in posting_dict.keys():
        posting_dict[term_id] = [doc_id]
      else:
        posting_dict[term_id].append(doc_id)
      exist_posting.add((term_id, doc_id))

    return posting_dict