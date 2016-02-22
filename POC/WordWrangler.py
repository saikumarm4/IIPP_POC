"""
Student code for Word Wrangler game
"""

import urllib2
import codeskulptor
import poc_wrangler_provided as provided

WORDFILE = "assets_scrabble_words3.txt"


# Functions to manipulate ordered word lists

def remove_duplicates(list1):
    """
    Eliminate duplicates in a sorted list.

    Returns a new sorted list with the same elements in list1, but
    with no duplicates.

    This function can be iterative.
    """
    temp_list = list(list1)
    idx = 0
    while idx < len(temp_list):
        count = temp_list.count(temp_list[idx])
        if count > 1:
            del temp_list[idx + 1: idx + count]
        idx += 1
    return temp_list

def intersect(list1, list2):
    """
    Compute the intersection of two sorted lists.

    Returns a new sorted list containing only elements that are in
    both list1 and list2.

    This function can be iterative.
    """
    temp_list1, temp_list2 = list(list1), list(list2)
    ans_list = []
    while temp_list1 != [] and temp_list2 != []:
        if temp_list1[0] in temp_list2:
            ans_list.append(temp_list2.pop(temp_list2.index(temp_list1.pop(0))))         
        else:
            temp_list1.pop(0)
    return ans_list

# Functions to perform merge sort

def merge(list1, list2):
    """
    Merge two sorted lists.

    Returns a new sorted list containing all of the elements that
    are in either list1 and list2.

    This function can be iterative.
    """   
    ans_list = []
    list1_idx, list2_idx = 0, 0
    len_list1, len_list2 = len(list1), len(list2)
    
    while list1_idx < len_list1 and list2_idx < len_list2:
        if list1[list1_idx] < list2[list2_idx]:
            ans_list.append(list1[list1_idx])
            list1_idx += 1
        else:
            ans_list.append(list2[list2_idx])
            list2_idx += 1
    if list1_idx < len_list1:
        ans_list += list1[list1_idx: ] 
    else:
        ans_list += list2[list2_idx: ]
    
    return ans_list
                
def merge_sort(list1):
    """
    Sort the elements of list1.

    Return a new sorted list with the same elements as list1.

    This function should be recursive.
    """
    length = len(list1)
    if length <= 1:
        return list1
    else:
        return merge(merge_sort(list1[ : length / 2]), merge_sort(list1[length / 2: ]))

# Function to generate all strings for the word wrangler game

def gen_all_strings(word):
    """
    Generate all strings that can be composed from the letters in word
    in any order.

    Returns a list of all strings that can be formed from the letters
    in word.

    This function should be recursive.
    """
    temp_word = word[:]
    if len(temp_word) == 0:
        return ["", ]
    else:
        first = temp_word[0]
        rest_string = gen_all_strings(temp_word[1: ])
        ans_list = []
        for string in rest_string:
            for idx in range(len(string) + 1):
                temp = list(string)
                temp.insert(idx, first)
                result_str = ""
                for letter in temp:
                    result_str += letter
                ans_list.append(result_str)
        ans_list += rest_string
    return ans_list

# Function to load words from a file

def load_words(filename):
    """
    Load word list from the file named filename.

    Returns a list of strings.
    """
    netfile = urllib2.urlopen(codeskulptor.file2url(filename))
    list_words = []
    for word in netfile.readlines():
        list_words.append(word)
    return list_words

def run():
    """
    Run game.
    """
    words = load_words(WORDFILE)
    wrangler = provided.WordWrangler(words, remove_duplicates, 
                                     intersect, merge_sort, 
                                     gen_all_strings)
    provided.run_game(wrangler)

# Uncomment when you are ready to try the game
#run()
