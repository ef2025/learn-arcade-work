class Room:
    def __init__(self, description, north, east, south, west):
        self.description = description
        self.north = north
        self.east = east
        self.south = south
        self.west = west


def main():
    room_list = []
    current_room = 0
    next_room = 0
    done = False

    # Room list (description, north, east, south, west)
    room = Room("\nYou are in the second bedroom. The sheets are worn, and dust has settled on the dresser. "
                " There is a door to the east.", None, 1, None, None)
    room_list.append(room)

    room = Room("\nYou are in the south hall, there doors to the east, west, and a connected hall to the north.",
                4, 2, None, 0)
    room_list.append(room)

    room = Room("\nYou are in the dining room. The food on the table exudes a nostalgic smell. There are doors to the"
                " west and north.", 3, None, None, 1)
    room_list.append(room)

    room = Room("\nYou are in the kitchen. There is fresh food on the stove, but the one who made it is nowhere to"
                " be found. There are doors to the west and south.", None, None, 2, 4)
    room_list.append(room)

    room = Room("\nYou are in the north hall, there are doors to the east, west, a connected hall to the south and a "
                " balcony to the north.", 6, 3, 1, 5)
    room_list.append(room)

    room = Room("\nYou are in the first bedroom. The bed was recently made, but by who? "
                " There is a door to the east.", None, 4, None, None)
    room_list.append(room)

    room = Room("\nYou are on the balcony. You can see a faint glow over the mountain where the city is."
                " There is a hall to the south.", None, None, 4, None)
    room_list.append(room)

    while not done:
        print(room_list[current_room].description)
        direction = input("Which way would you like to go? (n s e w or q to quit) ").lower()
        if direction[0] == 'n':
            next_room = room_list[current_room].north

        elif direction[0] == 's':
            next_room = room_list[current_room].south

        elif direction[0] == 'e':
            next_room = room_list[current_room].east

        elif direction[0] == 'w':
            next_room = room_list[current_room].west

        elif direction[0] == 'q':
            print("Thank you for playing!")
            done = True

        else:
            print("Please pick a valid direction.")
            continue

        # check for valid choice
        if next_room is None and not done:
            print("You can't go that way!")
            continue

        # if all is well, set new room
        current_room = next_room


main()
