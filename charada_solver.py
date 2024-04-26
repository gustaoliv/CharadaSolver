import utils
import string
from models import State
from word_solver import filter_matched_letters, all_elements_are_equal
from selenium import webdriver
from time import sleep
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import random
import time
from itertools import product
from unidecode import unidecode


main_url     = "https://charada.vercel.app/"
initial_word = "AUREO"

NUMBER_OF_LINES = 6
NUMBER_OF_COLUMNS = 5
AMOUNT_SOLVES = 100

def type_word_and_press_enter(driver: webdriver.Chrome, word):
    actions = ActionChains(driver)
    actions.send_keys(word)
    for char in word:
        actions.send_keys(char)
        actions.pause(0.5)

    actions.send_keys(Keys.RETURN)
    actions.pause(0.5)
    actions.perform()
    time.sleep(1)


def updated_match_matrix_from_line(driver: webdriver.Chrome, input_match_matrix, line_index):
    match_matrix = input_match_matrix.copy()

    line_elements = driver.find_elements(By.XPATH, ".//div[@class='flex-grow'][1]/div[@class='flex justify-center mb-1']")
    if line_elements == None or len(line_elements) != NUMBER_OF_LINES:
        raise Exception("Could not get the correct line elements")
    
    current_line = line_elements[line_index]
    current_line_columns_elements = current_line.find_elements(By.XPATH, ".//div")
    if current_line_columns_elements == None or len(current_line_columns_elements) != NUMBER_OF_COLUMNS:
        raise Exception("Could not get the correct column elements")

    for index, column_element in enumerate(current_line_columns_elements):
        letter = unidecode(column_element.text)
        column_class = column_element.get_attribute("class")
        if not letter or not column_class:
            raise Exception("Empty values treating some column")
        
        if "border-green" in column_class:
            match_matrix[letter][index] = State.CorrectPlace
        elif "border-yellow" in column_class:
            match_matrix[letter][index] = State.WrongPlace
        else:
            if all_elements_are_equal(match_matrix[letter], State.NotTested):
                match_matrix[letter] = [State.NotExists,] * NUMBER_OF_COLUMNS
            else:
                match_matrix[letter][index] = State.NotExists

    return match_matrix


def select_word_from_list(filtered_words):
    return random.choice(filtered_words)


def clear_input(driver: webdriver.Chrome):
    actions = ActionChains(driver)
    for i in range(NUMBER_OF_COLUMNS):
        actions.send_keys(Keys.BACKSPACE)
    actions.perform()


def get_expected_word(driver: webdriver.Chrome):
    word_elements = driver.find_elements(By.XPATH, ".//h3[contains(@id, 'headlessui-dialog-title-')]")
    if word_elements == None:
        raise Exception("Could not find the word expected element")

    word_element = word_elements[-1]
    splited_word = word_element.text.split(":")
    if len(splited_word) == 2:
        return splited_word[1]
    else:
        return word_element.text


def restart_game(driver: webdriver.Chrome):
    new_game_button = driver.find_element(By.XPATH, ".//button[contains(text(), 'Novo Jogo')]")
    if new_game_button == None:
        raise Exception("Could not find the new game button")
    
    new_game_button.click()


def generate_random_words(match_matrix, filtered_words):
    print("Generating random words")

    available_letters = []

    for letter, match_vector in match_matrix.items():
        if all_elements_are_equal(match_vector, State.NotExists):
            continue

        available_letters.append(letter)

    all_combinations = product(available_letters, repeat=5)

    five_letters_words = filter(lambda x: len(x) == 5, all_combinations)

    five_letters_words = [''.join(comb) for comb in five_letters_words]

    for c in five_letters_words:
        filtered_words.append(c)
    

def solve():
    amount_success = 0

    driver = webdriver.Chrome()
    driver.get(main_url)

    for i in range(AMOUNT_SOLVES):
        file  = open("treated_words.txt", encoding = "UTF-8")
        words = file.readlines()

        print("\n\n")
        print("-" * 50)
        print(f"Loaded {len(words)} words...")
        

        # Input treatment and initializing control
        # words = utils.remove_accentuation_from_strings(all_lines)
        # words = utils.filter_5_chars_string(words)
        # words = list(set(words))

        # new_file = open("treated_words.txt", encoding = "UTF-8", mode="w")
        # new_file.writelines(line + '\n' for line in words)
        
        utils.remove_line_breaker(words)
        letters = list(str(letter) for letter in string.ascii_uppercase)
        match_matrix = {letter:[State.NotTested,] * NUMBER_OF_COLUMNS for letter in letters}
        
        filtered_words = words.copy()
        
        for line_index in range(NUMBER_OF_LINES):
            if line_index == 0:
                type_word_and_press_enter(driver, initial_word)
                filtered_words.remove(initial_word)
            else:
                stop = False
                while(True):
                    filtered_words = filter_matched_letters(filtered_words, match_matrix)

                    if len(filtered_words) == 0:
                        generate_random_words(match_matrix, filtered_words)
                        filtered_words = filter_matched_letters(filtered_words, match_matrix)

                    
                    selected_word = select_word_from_list(filtered_words)
                    type_word_and_press_enter(driver, selected_word)
                    filtered_words.remove(selected_word)

                    if "Parabéns você acertou!" in driver.page_source:
                        print(f"Success ===> {selected_word}")
                        amount_success += 1
                        stop = True
                        break
                    elif "Não foi dessa vez!" in driver.page_source:
                        print(f"Fail ===> The word was {get_expected_word(driver)}")
                        stop = True
                        break
                    
                    if "Palavra não encontrada" not in driver.page_source:
                        break

                    clear_input(driver)

                if stop:
                    break

            match_matrix = updated_match_matrix_from_line(driver, match_matrix, line_index)

        
        restart_game(driver)


    print(f"Success rate: {amount_success}/{AMOUNT_SOLVES}")

    

    