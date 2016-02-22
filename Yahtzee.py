"""
Planner for Yahtzee
Simplifications:  only allow discard and roll, only score against upper level
"""

# Used to increase the timeout, if necessary
import codeskulptor
import random
codeskulptor.set_timeout(20)

def gen_all_sequences(outcomes, length):
    """
    Iterative function that enumerates the set of all sequences of
    outcomes of given length.
    """
    
    answer_set = set([()])
    for dummy_idx in range(length):
        temp_set = set()
        for partial_sequence in answer_set:
            for item in outcomes:
                new_sequence = list(partial_sequence)
                new_sequence.append(item)
                temp_set.add(tuple(new_sequence))
        answer_set = temp_set
    return answer_set


def score(hand):
    """
    Compute the maximal score for a Yahtzee hand according to the
    upper section of the Yahtzee score card.

    hand: full yahtzee hand

    Returns an integer score 
    """
    upper_section = []
    for hand_value in range(1, max(hand) + 1):
        upper_section.append(hand.count(hand_value) * hand_value)
    return max(upper_section)


def expected_value(held_dice, num_die_sides, num_free_dice):
    """
    Compute the expected value based on held_dice given that there
    are num_free_dice to be rolled, each with num_die_sides.

    held_dice: dice that you will hold
    num_die_sides: number of sides on each die
    num_free_dice: number of dice to be rolled

    Returns a floating point expected value
    """
    possible_sequences = gen_all_sequences(range(1,num_die_sides + 1), num_free_dice)
    scores = []
    for sequence in possible_sequences:
        scores.append(score(sorted(sequence + held_dice)))
    return float(sum(scores))/len(scores)


def gen_all_holds(hand):
    """
    Generate all possible choices of dice from hand to hold.

    hand: full yahtzee hand

    Returns a set of tuples, where each tuple is dice to hold
    """
    dice_hold = [()]
    for no_dice_hold in range(1, len(hand) + 1):
        temp_result_sub = list(gen_all_sequences(hand,no_dice_hold))
        result_sub = [tuple(sorted(seq)) for seq in temp_result_sub]
        dice_hold += result_sub
    dice_held = []
    
    for seq in dice_hold:
        for val in hand:
            if seq.count(val) > hand.count(val):
                break
        else:
            dice_held.append(seq)
    return set(dice_held)



def strategy(hand, num_die_sides):
    """
    Compute the hold that maximizes the expected value when the
    discarded dice are rolled.

    hand: full yahtzee hand
    num_die_sides: number of sides on each die

    Returns a tuple where the first element is the expected score and
    the second element is a tuple of the dice to hold
    """
    possible_holds = gen_all_holds(hand)
    expected_values = {}
    max_val = 0
    for hold in possible_holds:
        expected_values[hold] = expected_value(hold, num_die_sides, len(hand) - len(hold))
        if expected_values[hold] > max_val:
            max_val = expected_values[hold]
    good_holds = []
    for key in expected_values.keys():
        if expected_values[key] == max_val:
            good_holds.append(key)
    best_hold = good_holds[random.randrange(len(good_holds))]
    
    return (max_val, best_hold)


def run_example():
    """
    Compute the dice to hold and expected score for an example hand
    """
    num_die_sides = 6
    hand = (1, 3, 5)
    #print score(hand)
    #print expected_value((1,3,4), 6, 2)
    print gen_all_holds(hand)
    hand_score, hold = strategy(hand, num_die_sides)
    print hand_score, hold
    #print "Best strategy for hand", hand, "is to hold", hold, "with expected score", hand_score
    
    
#run_example()


#import poc_holds_testsuite
#poc_holds_testsuite.run_suite(gen_all_holds)
                                       
    
    
    



