This is the README file for A0200704Y-A0200805W's submission
Email(s): e0407685@u.nus.edu, e0407786@u.nus.edu

== Python Version ==

We're using Python Version 3.7.11 for
this assignment.

== General Notes about this assignment ==

The assignment consists of two parts, index construction and query evaulation of free-text queries.

For index construction in the index.py, we are doing the following:
1. Preprocess the files, using the NLTK library, implemented in the Preprocessor class in preprocessor.py
2. Read the documents from a path, using os.listdir
3. Create term-docID pairs for each of the terms for all documents
4. Create postings list and write it to postings.txt
5. Read the postings list to get the line offsets for creating the dictionary
6. Create dictionary of terms using the trie data structure
7. Write the dictionary of terms to the file dictionary.txt

For query evaluation, we have done the following:
1. Load and parse the query 
2. Load the dictionary of terms from dictionary.txt file
3. Evaluate the parsed query using the Vector-Space model

We created a preprocessor.py file to preprocess file using the NLTK module 
We created a memory_indexing.py file to store all the methods related to indexing, which includes:
  - Creating term-docID pairs
  - Creating dictionary trie
  - Creating the postings

We created a queryParser.py file to parse the query 
We created a queryEvaluator.py file to evaluate queries in search.py
We created a utils.py file to store the normalization function

In addition, we experimented with some of the query optimization from lecture 8, in particular heuristic 1a and 3.
These settings could be adjusted in the config.yaml file. However, for accuracy and consistency with HW3 standards, 
these settings are turned to 0 (means that the heuristics are inactive and the query evaluation would be similar to
a program without implementing these heuristics)

Note: Need to install yaml in python to execute this code : pip install pyyaml or pip3 install pyyaml 

Heuristic 1a: High-idf query terms only
Here, we experimented with the cutoff of the idf. We obtained several thresholds for the cutoff:
0.15  : of 
0.185 : the of 
0.19  : the to of 
0.2   : the to of and
0.21  : the to of and in
0.24  : the to of and in a

For our testing for the query speed optimization, we chose the value of 0.19. 

Heuristic 3: Impact-Ordered postings
Here, we set a threshold when computing the value of wf_td. We eventually decided on the value of 0.003 for our testing 
for the query speed optimization.

Results of our testing (averaged across several trials), the speed of the query processing (using our local machine) are as follows:
Heuristic 1a =0 ; Heuristic 3 = 0 (Base case, HW3)    : 2.28 seconds
Heuristic 1a = 0.19; Heuristic 3 = 0.003              : 1.98 seconds

Thus, there's around a 15% improvement in query processing speed. Again, this is just our testing and for HW3, we set these 
hyperparameters to be 0. 

== Files included with this submission ==

1. index.py 
2. search.py
3. preprocessor.py
4. memory_indexing.py
5. queryParser.py
6. queryEvaluator.py
7. utils.py
8. dictionary.txt
9. postings.txt
10. config.yaml
11. requirements.txt
12. README.txt

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
-