from models import State

def all_elements_are_equal(elements, variable):
    return all(element == variable for element in elements)


def get_letters_in_correct_place_index(letter, match_vector):
    letter_correct_place_indexes = []
    for index, value in enumerate(match_vector):
        if value == State.CorrectPlace:
            letter_correct_place_indexes.append((letter, index))

    return letter_correct_place_indexes


def get_letters_in_wrong_place_index(letter, match_vector):
    letter_wrong_place_indexes = []
    for index, value in enumerate(match_vector):
        if value == State.WrongPlace:
            letter_wrong_place_indexes.append((letter, index))

    return letter_wrong_place_indexes


def letter_in_word_in_correct_place(match_vector):
    return State.CorrectPlace in match_vector


def letter_in_word_in_wrong_place(match_vector):
    return State.WrongPlace in match_vector


def filter_words_by_correct_place_letters(words, letters_in_correct_place):
    filtered_words = []
    for word in words:
        word_sum = 0
        for letter, index in letters_in_correct_place:
            if word[index] != letter:
                word_sum += 1
        
        if word_sum == 0:
            filtered_words.append(word)

    return filtered_words


def word_contains_all_letters(word, letters):
    for letter in letters:
        if letter not in word:
            return False
        
    return True


def filter_words_by_wrong_place_letters(words, letters_in_wrong_place):
    filtered_words = []
    
    for word in words:
        letters = [key for key, _ in letters_in_wrong_place]
        
        if not word_contains_all_letters(word, letters):
            continue

        skip_word = False
        for letter, index in letters_in_wrong_place:
            if word[index] == letter:
                skip_word = True
                break
        
        if skip_word:
            continue
        
        filtered_words.append(word)

    return filtered_words
        

def filter_words_ignoring_letters(words, letters_to_ignore):
    filtered_words = []

    for word in words:
        contains_any_letter = False
        for letter in letters_to_ignore:
            if letter in word:
                contains_any_letter = True
                break
        
        if not contains_any_letter:
            filtered_words.append(word)

    return filtered_words


def there_is_not_existing_letters(match_vector):
    return any(element == State.NotExists for element in match_vector)


def get_letters_not_existing_index(letter, match_vector):
    letters_not_existing_index = []

    for index, value in enumerate(match_vector):
        if value == State.NotExists:
            letters_not_existing_index.append((letter, index))

    return letters_not_existing_index


def filter_words_by_notexists_place_letters(words, letters_not_existing):
    filtered_words = []

    for word in words:  
        skip = False
        for letter, index in letters_not_existing:
            if word[index] == letter:
                skip = True
                break
        
        if not skip:
            filtered_words.append(word)

    return filtered_words



def filter_matched_letters(input_words, match_matrix):
    words = input_words[:]

    letters_in_correct_place = []
    letters_in_wrong_place = []
    letters_to_ignore = []
    letters_not_existing = []

    for letter, match_vector in match_matrix.items():

        if all_elements_are_equal(match_vector, State.NotExists):
            letters_to_ignore.append(letter)

        if letter_in_word_in_correct_place(match_vector):
            letters_in_correct_place += get_letters_in_correct_place_index(letter, match_vector)

        if letter_in_word_in_wrong_place(match_vector):
            letters_in_wrong_place += get_letters_in_wrong_place_index(letter, match_vector)

        if there_is_not_existing_letters(match_vector):
            letters_not_existing += get_letters_not_existing_index(letter, match_vector)


    if len(letters_to_ignore) > 0:
        words = filter_words_ignoring_letters(words, letters_to_ignore)

    if len(letters_in_correct_place) > 0:
        words = filter_words_by_correct_place_letters(words, letters_in_correct_place)

    if len(letters_in_wrong_place) > 0:
        words = filter_words_by_wrong_place_letters(words, letters_in_wrong_place)


    if len(letters_not_existing) > 0:
        words = filter_words_by_notexists_place_letters(words, letters_not_existing)

    if len(words) > 0:
        print(f"Success rate: {(1/len(words) * 100):.2f} %")
    else:
        print("There is not more words...")

    return words

