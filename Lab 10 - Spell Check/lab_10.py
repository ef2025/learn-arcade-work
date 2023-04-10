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

    for line in alice_in_wonderland:
        word_list = split_line(line)
        for line in alice_in_wonderland:
            for word in line:
                # Start at the beginning of the list
                current_list_position = 0

                # Loop until you reach the end of the list, or the value at the
                # current position is equal to the key
                while current_list_position < len(dictionary_list) and dictionary_list[current_list_position] != \
                        word.upper():
                    # Advance to the next item in the list
                    current_list_position += 1

                if current_list_position < len(dictionary_list):
                    print("Line", current_list_position)
                    break
                else:
                    print("The name was not in the list.")
                    break

    # read chapter one line at a time
    # for each line call split line
    # for each word in line, convert to upper and check for presence in dictionary
    # if it is NOT found, print the word and the line number as:

    # Line x possible

    print('---Binary Search---')


if __name__ == '__main__':
    main()
