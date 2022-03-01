This is the README file for A0200704Y-A0200805W's submission
Email(s): e0407685@u.nus.edu, e0407786@u.nus.edu

== Python Version ==

We're using Python Version 3.7.11 for
this assignment.

== General Notes about this assignment ==

The assignment consists of two parts, index construction and query evaulation of Boolean queries.

For index construction in index.py file, we are doing the following:
1. Preprocess the files, using the NLTK library, implemented in the Preprocessor class in preprocessor.py
2. Read the documents from a path, using os.listdir
3. Convert all the terms to termIDs (for BSBI index construction)
4. Index construction through the BSBI method
5. Create postings list
6. Create skip pointers on the postings list
7. Create dictionary of terms using the trie data structure
8. Write the dictionary of terms to the file dictionary.txt

For query evaluation, we have done the following:
1. Load and parse the query using the Shunting Yard Algorithm, in the QueryParser class in queryParser.py 
2. Load the dictionary of terms from dictionary.txt file
3. Evaluate the parsed query

We created a preprocessor.py file to preprocess file using the NLTK module 
We created a memory_indexing file to store all the methods related to indexing, which includes:
  - Creating term-docID pairs
  - Creating dictionary trie
  - Creating the postings
  - Creating skip pointers in the indexing steps
We created an index_table.py file to create a dictionary to link the terms to termIDs
We created a bsbi.py for the index construction using the BSBI method

We created a queryParser.py file to parse the query using the Shunting Yard Algorithm
We created a queryEvaluator.py file to evaluate queries in search.py

== Files included with this submission ==

1. index.py 
2. search.py
3. preprocessor.py
4. memory_indexing.py
5. bsbi.py
6. index_table.py
7. queryParser.py
8. queryEvaluator.py
9. dictionary.txt
10. postings.txt
11. README.txt

== Statement of individual work ==

Please put a "x" (without the double quotes) into the bracket of the appropriate statement.

[x] We, A0200704Y-A0200805W, certify that I/we have followed the CS 3245 Information
Retrieval class guidelines for homework assignments.  In particular, I/we
expressly vow that I/we have followed the Facebook rule in discussing
with others in doing the assignment and did not take notes (digital or
printed) from the discussions.  

[ ] I/We, A0000000X, did not follow the class rules regarding homework
assignment, because of the following reason: -

We suggest that we should be graded as follows: -

== References ==

<Please list any websites and/or people you consulted with for this
assignment and state their role>
