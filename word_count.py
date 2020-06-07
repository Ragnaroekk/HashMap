# word_count.py
# ===================================================
# Implement a word counter that counts the number of
# occurrences of all the words in a file. The word
# counter will return the top X words, as indicated
# by the user.
# ===================================================

import re
from hash_map import HashMap

"""
This is the regular expression used to capture words. It could probably be endlessly
tweaked to catch more words, but this provides a standard we can test against, so don't
modify it for your assignment submission.
"""
rgx = re.compile("(\w[\w']*\w|\w)")

def hash_function_2(key):
    """
    This is a hash function that can be used for the hashmap.
    """

    hash = 0
    index = 0
    for i in key:
        hash = hash + (index + 1) * ord(i)
        index = index + 1
    return hash

def top_words(source, number):
    """
    Takes a plain text file and counts the number of occurrences of case insensitive words.
    Returns the top `number` of words in a list of tuples of the form (word, count).

    Args:
        source: the file name containing the text
        number: the number of top results to return (e.g. 5 would return the 5 most common words)
    Returns:
        A list of tuples of the form (word, count), sorted by most common word. (e.g. [("a", 23), ("the", 20), ("it", 10)])
    """

    keys = set()

    ht = HashMap(2500,hash_function_2)

    count = 1

    # This block of code will read a file one word as a time and
    # put the word in `w`. It should be left as starter code.
    with open(source) as f:
        for line in f:
            words = rgx.findall(line)
            for w in words:
                if ht.contains_key(w.lower()):
                    value = ht.get(w.lower())
                    value += 1
                    ht.put(w.lower(), value)
                else:
                    ht.put(w.lower(), 1)

    result = sort_function(ht, number)

    return result

def sort_function(hash_map, number):
    """
    Sorts the hash map by most common words and returns a tuple of the
    top x most common where x is the number passed in.
    With help from https://stackoverflow.com/
    :param hash_map: Hashmap that has the data to sort
    :param number: number of top results to return
    :return: A tuple of the most common number of items
    """
    temp_list = []

    # per assignment guidelines:
    # "Variables in the HashMap()class are not private.You are allowed to access and change their values directly.
    # You do not need to write any getter or setter methods for the HashMap() class."
    # also, we are not to change the init method, but we are accessing a private variable here

    for linked_list in hash_map._buckets:
        if linked_list.head is not None:
            curr = linked_list.head
            while curr is not None:
                node = (curr.key, curr.value)
                temp_list.append(node)
                curr = curr.next
    temp_list.sort(key=lambda tup: tup[1])
    temp_list.reverse()

    result = []
    for i in range(number):
        result.append(temp_list[i])

    return result



# print(top_words("test.txt", 5))  # COMMENT THIS OUT WHEN SUBMITTING TO GRADESCOPE