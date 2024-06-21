# Solution of Advent of Code 2023 (https://adventofcode.com/2023/)
# Author: Monika Rosinska
# Date: 19. 6. 2024

# The instructions for the tasks are simplified. For the whole assignment please visit the site, as it is not allowed to
#   copy parts of the event. The same applies to input examples.

import numpy as np
import regex as re
from typing import Dict, List
from functools import reduce


# ####################### TASK 1 A #######################
# Task: On each line, the desired value can be found by combining the first digit and the last digit (in that order)
#       to form a single two-digit number. What is the sum of all the desired values in whole document?
def task_01_a():
    val_sum = 0
    with open("inputs/input_01.txt", 'r') as file:
        for line in file:
            digits = [char for char in line if char.isdigit()]
            if digits:
                val_sum += int(digits[0] + digits[-1])
    print(f"The sum of all calibration values is {val_sum}.")


# ####################### TASK 1 B #######################
# Task: DTTO, but the digits can be spelled out and can overlap (e.g. eightwo).
def task_01_b():
    spelled_digits_map = {
        "zero": "0",
        "one": "1",
        "two": "2",
        "three": "3",
        "four": "4",
        "five": "5",
        "six": "6",
        "seven": "7",
        "eight": "8",
        "nine": "9"
    }
    val_sum = 0
    with open("inputs/input_01.txt", 'r') as file:
        for line in file:
            digits = []
            for idx, char in enumerate(line):
                if char.isdigit():
                    digits.append(char)
                else:
                    for digit in spelled_digits_map:
                        if line[idx:].startswith(digit):
                            digits.append(spelled_digits_map.get(digit))
                            break
            if digits:
                val_sum += int(digits[0] + digits[-1])
    print(f"The sum of all calibration values is {val_sum}.")


# ####################### TASK 2 A #######################
# Task: In a bag there are red, green and blue cubes. In each game, several times random cubes are chosen, with known
#       count of each colour. Which games use maximum 12 red cubes, 13 green cubes and 14 blue cubes? What is the sum
#       of the IDs of those games?
def task_02_a():
    red_count = 12
    green_count = 13
    blue_count = 14

    id_sum = 0
    with open("inputs/input_02.txt", 'r') as file:
        for idx, line in enumerate(file):
            line = line.split(": ")[1]  # get rid of "Game x:" prefix
            selections = line.split("; ")  # get individual rounds of the game (or the selections of cubes)
            game_ok = True
            for selection in selections:  # check each round of the game
                # round contains list of cubes in random order, does not have to contain each colour
                # try to find the colour, remove the colon and at last position, there should be a number;
                #   if there is no number, the colour is not present in the round and the count is 0
                red = (selection.split(" red")[0]).split(", ")[-1]
                red = int(red) if red.isdigit() else 0

                green = (selection.split(" green")[0]).split(", ")[-1]
                green = int(green) if green.isdigit() else 0

                blue = (selection.split(" blue")[0]).split(", ")[-1]
                blue = int(blue) if blue.isdigit() else 0

                if red > red_count or green > green_count or blue > blue_count:
                    game_ok = False
                    break
            if game_ok:
                id_sum += idx + 1
    print(f"The sum of indexes is {id_sum}.")


# ####################### TASK 2 B #######################
# Task: DTTO, but find the minimum set of cubes that must have been present in each game.
#       What is the sum of the power of these counts?
def task_02_b():
    sum_of_power = 0
    with open("inputs/input_02.txt", 'r') as file:
        for line in file:
            line = line.split(": ")[1]  # get rid of "Game x:" prefix
            selections = line.split("; ")  # get individual rounds of the game (or the selections of cubes)
            reds = 0
            blues = 0
            greens = 0

            for selection in selections:  # check each round of the game
                # round contains list of cubes in random order, does not have to contain each colour
                # try to find the colour, remove the colon and at last position, there should be a number;
                #   if there is no number, the colour is not present in the round and the count is 0
                red = (selection.split(" red")[0]).split(", ")[-1]
                red = int(red) if red.isdigit() else 0
                reds = max(red, reds)

                green = (selection.split(" green")[0]).split(", ")[-1]
                green = int(green) if green.isdigit() else 0
                greens = max(green, greens)

                blue = (selection.split(" blue")[0]).split(", ")[-1]
                blue = int(blue) if blue.isdigit() else 0
                blues = max(blue, blues)

            sum_of_power += reds * greens * blues
    print(f"Sum of powers of needed cubes is {sum_of_power}.")


# ####################### TASK 3 A  #######################
# Task: In a file containing numbers and symbols, find numbers adjacent to a symbol (except '.'), even diagonally.
#       What is the sum of all the numbers?

# returns true if the given character is a valid symbol (in context of the task); using ASCII table
def is_character(char):
    if ord(char) == ord('.') or char.isdigit():
        return False
    if ord('!') <= ord(char) <= ord('/'):
        return True
    if ord(':') <= ord(char) <= ord('@'):
        return True
    if ord('[') <= ord(char) <= ord('`'):
        return True
    return False


# returns list of numbers in given text
def find_numbers(text):
    pattern = r'\b\d+\b'
    matches = re.finditer(pattern, text)
    return [(match.group(), match.start()) for match in matches]


# returns unique code of number using the number, the line index and its position in the line
def code_number(number, number_idx, line_idx):
    return f"{line_idx}_{number_idx}_{number}"


# returns sum of the numbers in the line adjacent to some symbol, and updated list of used numbers
# char_idxs - list of indexes on which some symbol is
# text - the string (line) the numbers should be searched in
# line_idx - index of the text line; needed for the number coding
# used_numbers - list of numbers already used, using code_number format
def get_subsum(char_idxs, text, line_idx, used_numbers):
    subsum = 0
    numbers = find_numbers(text)
    for number, number_idx in numbers:
        # each number must be used only once
        if code_number(number, number_idx, line_idx) in used_numbers:
            continue

        # get interval of positions, on which a symbol can be present (it must touch the number at least diagonally)
        interval = [number_idx - 1, number_idx + len(number)]

        for position in char_idxs:  # for each given character
            if interval[0] <= position <= interval[1]:
                subsum += int(number)
                used_numbers.add(code_number(number, number_idx, line_idx))
                break
            if position > interval[1]:
                break

    return subsum, used_numbers


def task_03_a():
    total_sum = 0
    used_numbers = set()
    previous_line = ""
    previous_line_char_idxs = []

    with open("inputs/input_03.txt", 'r') as file:
        for line_idx, line in enumerate(file):
            char_idxs = [idx for idx, char in enumerate(line) if is_character(char)]

            # find the numbers (their sum) for the current symbols and current line, for the current symbols and
            #   previous line and for the previous line symbols and current line
            #   (the first two are computations for the current line - the current text line and the line above;
            #   the last one is catch-up for the previous line to get numbers in line under the symbols)
            subsum_1, used_numbers = get_subsum(char_idxs, line, line_idx, used_numbers)
            subsum_2, used_numbers = get_subsum(char_idxs, previous_line, line_idx - 1, used_numbers)
            subsum_3, used_numbers = get_subsum(previous_line_char_idxs, line, line_idx, used_numbers)

            total_sum = total_sum + subsum_1 + subsum_2 + subsum_3

            previous_line = line
            previous_line_char_idxs = char_idxs

    print(f"The sum of the numbers is {total_sum}.")


# ####################### TASK 3 B #######################
# Task: DTTO, find stars with exactly two adjacent numbers and get these numbers. The desired value of the star is
#       a multiplication of these two numbers. What is the sum of all the values?

# returns list of numbers adjacent to the star
# star_idx - position of the star
# text - the string where to search for the numbers
def get_star_numbers(star_idx, text):
    star_numbers = []
    numbers = find_numbers(text)
    for number, number_idx in numbers:
        # get interval of positions, on which a symbol can be present (it must touch the number at least diagonally)
        interval = [number_idx - 1, number_idx + len(number)]

        if interval[0] <= star_idx <= interval[1]:
            star_numbers.append(number)
            continue
        if star_idx < interval[0]:
            break

    return list(star_numbers)


def task_03_a():
    prev_previous_line = ""
    previous_line = ""
    total_sum = 0

    with open("inputs/input_03.txt", 'r') as file:
        previous_line = file.readline().strip()  # get first line and store it as previous line

        for line_idx, line in enumerate(file, start=2):
            star_idxs = [match.start() for match in re.finditer(r'\*', previous_line)] # get stars in previous line

            # the stars in previous line are considered; prev_previous_line is line above the stars, current line
            #   is line under the stars
            for star in star_idxs:
                numbers_prev_prev_line = get_star_numbers(star, prev_previous_line)
                numbers_star_line = get_star_numbers(star, previous_line)
                numbers_current_line = get_star_numbers(star, line)

                # concatenate the list of numbers and if there are exactly two numbers, multiply them and add to sum
                number_list = numbers_prev_prev_line + numbers_star_line + numbers_current_line
                if len(number_list) == 2:
                    total_sum += int(number_list[0]) * int(number_list[1])

            prev_previous_line = previous_line
            previous_line = line

        # process last line (the same process as above)
        star_idxs = [match.start() for match in re.finditer(r'\*', previous_line)]
        for star in star_idxs:
            numbers_prev_prev_line = get_star_numbers(star, prev_previous_line)
            numbers_star_line = get_star_numbers(star, previous_line)

            number_list = numbers_prev_prev_line + numbers_star_line + numbers_current_line
            if len(number_list) == 2:
                total_sum += int(number_list[0]) * int(number_list[1])

        print(f"The sum of products of gears is {total_sum}.")

task_03_a()

