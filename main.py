import sys
import json
import heapq
import re
from collections import Counter

class Newsela:
    def __init__(self, question_data, names, excluded_words):
        self.names = set(names) # special names/phrases
        self.question_data = [(self.sanitize(question['text'].lower()), question['percent_correct']) for question in question_data] # list of tuples (list of str, int) eg. [([list of words], percent_correct), ([list of words], percent_correct), ... ]
        self.excluded_words = set(excluded_words) # words to ignore
    
    def sanitize(self, text):
        """
        Takes a sentence string and returns a list of words of that string without punctuation. 
        Keeps any special names with punctuation eg. U.S. and S.C. Johnson
        Parameters
        ----------
        text : str

        Returns
        _______
        list of str
        """
        sanitized_list = []

        # get the special names/phrases
        for name in self.names:
            if name.lower() in text:
                sanitized_list.append(name.lower())
                text = text.replace(name.lower(), ' ')

        # remove any punctuation
        text = re.sub(r'[^A-Za-z0-9 ]+', ' ', text).replace('blockquote', '')

        for word in text.split():
            sanitized_list.append(word)
        return sanitized_list
    
    def get_word_count(self, question_text_list):
        """
        Returns a dictionary with words as the key and frequency as the value

        Parameters
        ----------
        question_text_list: list of str
        """
        filtered_text = []
        for text in question_text_list:
            for word in text:
                if word not in self.excluded_words:
                     filtered_text.append(word)
        word_count = dict(Counter(filtered_text))
        return word_count

    def get_top_k(self, word_count, k):
        """
        Returns top k frequent words in the word_count dictionary in descending order

        Parameters
        ----------
        word_count: dict (key: str, value: int)
        k: int
        """
        heap = []
        heapq.heapify(heap)
        for word, count in word_count.items():
            if len(heap) < k:
                heapq.heappush(heap, (count, word))
            else:
                heapq.heappushpop(heap, (count, word))
        
        return sorted(heap, reverse=True)

    def analyze(self, poor_percent, good_percent, top_k):
        """
        Prints out the top top_k frequent words for well performed and poor performed questions.
        Well performed questions are questions where the percent correct is greater than good_percent.
        Poor performed questions are questions where the percent correct is less than or equal too poor_percent.

        Paramters
        ---------
        poor_percent: float
        good_percent: float
        top_k: int
        """
        poor = []
        good = []

        for text, percent_correct in self.question_data:
            if percent_correct <= poor_percent:
                poor.append(text)
            if percent_correct > good_percent:
                good.append(text)

        poor_count = self.get_word_count(poor)
        good_count = self.get_word_count(good)
        top_k_poor = self.get_top_k(poor_count, top_k)
        top_k_good = self.get_top_k(good_count, top_k)

        print('Top words in well performed questions: (percent_correct > ' + str(good_percent) + ')' + '\n')
        print(top_k_good)
        print('\n')
        print('Top words in poor performed questions: (percent_correct <= ' + str(poor_percent) + ')' + '\n')
        print(top_k_poor)
        print('\n')

        

            


if __name__ == '__main__':
    f = open('quiz_question_data_(1).json')
    data = json.load(f)
    
    names = ['S.C. Johnson', 'meekerorum', 'T. rex', 'tyrannosaurus rex', 'u.s.', 'united states', 'america']
    excluded_words = ['after', 'before', 'using', 'many', 'want', 'been', 'its', 'those', 'option', 'let', 'into', 'much', 'being', 'now', 'use', 'gives', 'each', 'way', 'two', 'she', 'said', 't', 's', 'the', 'of', 'that', 'from', 'to', 'a', 'in', 'is', 'which', 'sentence', 'what', 'and', 'for', 'not', 'are', 'why', 'does', 'on', 'select', 'following', 'has', 'as', 'it', 'up', 'if', 'than', 'do', 'paragraph', 'best', 'all', 'except', 'section', 'article', 'word', 'shows', 'how', 'idea', 'author', 'by', 'an', 'this', 'sentences', 'be', 'between', 'with', 'about', 'can', 'their', 'or', 'was', 'text', 'most', 'above', 'contains', 'have', 'include', 'his', 'explains', 'provides', 'will', 'at', 'make', 'he', 'so', 'get', 'but', 'her', 'we', 'may', 'had', 'they', 'did', 'no', 'one', 'you', 'work']
    
    newsela = Newsela(data, names, excluded_words)
    newsela.analyze(float(sys.argv[1]), float(sys.argv[2]), int(sys.argv[3]))
    
    f.close()