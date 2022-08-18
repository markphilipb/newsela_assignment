# Newsela Assignment
## About
The solution I wrote will print out the top k most frequent words for both poor and well performed questions. 
The solution will take 3 arguments: two percents (`poor_percent` and `good_percent`) and a number `k`. Questions with `percent_correct` lower than or equal to `poor_percent` is considered poor and 
questions with `percent_correct` greather than `good_percent` is considered well performed. The solution also has the ability to exclude any irrelevant words as well as include any special words/phrases.

## Running the code
*Note: These instructions were performed on a Mac and assuming the user has python installed. Performing the instructions on Windows should be similar*

On a terminal, navigate to the **newsela_assignment** directory. You can execute the code by running main.py with 3 command 
line arguments such as: `python main.py poor_percent good_percent k` 
*(make sure to replace `poor_percent` and `good_percent` with a float less than 1 and k with an integer)*.

ex. `python main.py .5 .5 100`

## File structure
The code is contained in `main.py` and the analysis/response is contained in `response.txt`

## Extra
### Editing words to exclude and names to include
The solution by default will exclude many irrelevant words. The list of words to exclude can be found in `main.py` on line 118 called `excluded_words`.
The solution will also include any special names/phrases such as 'S.C. Johnson' or 'united states'. The list of names to include can be found in 'main.py' on line 117 called `names`
