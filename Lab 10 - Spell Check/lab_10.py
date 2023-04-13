import re

# This function takes in a line of text and returns
# a list of words in the line.


def split_line(line):
    return re.findall('[A-Za-z]+(?:\'[A-Za-z]+)?', line)


def main():

    # read the dictionary into a list
    # read chapter into a list of lines
    # close both
    """ Read in lines from a file """

    # Open the file for reading, and store a pointer to it in the new
    # variable "file"
    dictionary = open("dictionary.txt")

    # Create an empty list to store our names
    dictionary_list = []

    # Loop through each line in the file like a list
    for dictionary_line in dictionary:
        # Remove any line feed, carriage returns or spaces at the end of the line
        dictionary_line = dictionary_line.strip()

        # Add the name to the list
        dictionary_list.append(dictionary_line)

    dictionary.close()

    # linear search
    print('---Linear Search---')

    # recommend writing in a function
    alice_in_wonderland = open("AliceInWonderLand200.txt")

    line_num = 0

    for line in alice_in_wonderland:
        word_list = split_line(line)
        line_num += 1
        for word in word_list:
            # Start at the beginning of the list
            current_list_position = 0
            if word not in dictionary_list:
                # Loop until you reach the end of the list, or the value at the
                # current position is equal to the key
                while current_list_position < len(dictionary_list) and dictionary_list[current_list_position] != \
                        word.upper():
                    # Advance to the next item in the list
                    current_list_position += 1

                if current_list_position == len(dictionary_list):
                    print("Possible misspelling at Line", line_num, ' for word', word)

    alice_in_wonderland.close()

    # read chapter one line at a time
    # for each line call split line
    # for each word in line, convert to upper and check for presence in dictionary
    # if it is NOT found, print the word and the line number as:

    # Line x possible

    print('---Binary Search---')

    alice_in_wonderland = open("AliceInWonderLand200.txt")
    line_num = 0

    for line in alice_in_wonderland:
        word_list = split_line(line)
        # lower_bound = 0
        # upper_bound = len(line) - 1
        # found = False
        line_num += 1
        for word in word_list:
            # Start at the beginning of the list
            lower_bound = 0
            upper_bound = len(dictionary_list) - 1
            found = False

            if word not in dictionary_list:
                # Loop until you reach the end of the list, or the value at the
                # current position is equal to the key

                # Loop until we find the item, or our upper/lower bounds meet
                while lower_bound <= upper_bound and not found:

                    # Find the middle position
                    middle_pos = (lower_bound + upper_bound) // 2

                    # Figure out if we:
                    # move up the lower bound, or
                    # move down the upper bound, or
                    # we found what we are looking for
                    if dictionary_list[middle_pos] < word.upper():
                        lower_bound = middle_pos + 1
                    elif dictionary_list[middle_pos] > word.upper():
                        upper_bound = middle_pos - 1
                    else:
                        found = True

                if not found:
                    print("Possible misspelling at Line", line_num, ' for word', word)


if __name__ == '__main__':
    main()
