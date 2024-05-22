def find_best_words(feedback, word_list, previous_guesses):
    # Initialize sets and dictionaries to track letter constraints
    not_in_word = set()  # Letters not in the word
    in_word_wrong_position = {}  # Letters in the word but wrong position: letter -> positions
    correct_position = {}  # Letters in the correct position: position -> letter
    
    # Process the feedback to populate the above containers
    for position, word_feedback in enumerate(feedback):
        for pos, (letter, status) in enumerate(word_feedback):
            if status == 1:
                not_in_word.add(letter)
            elif status == 2:
                if letter in in_word_wrong_position:
                    in_word_wrong_position[letter].add(pos)
                else:
                    in_word_wrong_position[letter] = {pos}
            elif status == 3:
                correct_position[pos] = letter

    def word_matches_constraints(word):
        # Check against letters that must not be in the word
        if any(letter in not_in_word for letter in word):
            return False
        # Check for letters that are in the correct position
        for pos, letter in correct_position.items():
            if word[pos] != letter:
                return False
        # Check for letters that must be in the word but in different positions
        for letter, positions in in_word_wrong_position.items():
            if letter not in word:
                return False
            if all(word[pos] == letter for pos in positions):
                return False
        return True

    # Filter the word list based on constraints and previous guesses, then return the top 3 matches
    potential_words = []
    for word in word_list:
        if word not in previous_guesses and word_matches_constraints(word):
            potential_words.append(word)
    return potential_words[:3]  # Return the top 3 potential words

