import random


def main():
    camel_tiredness = 0
    miles_traveled = 0
    thirst = 0
    natives_distance = -20
    canteen_drinks = 3
    oasis = 0

    print("""Welcome to Camel!
You have stolen a camel to make your way across the great Mobi desert.
The natives want their camel back and are chasing you down! Survive your
desert trek and outrun the natives. \n""")
    done = False

    while not done:
        print("""A. Drink from your canteen.
B. Ahead moderate speed.
C. Ahead full speed.
D. Stop for the night.
E. Status check.
Q. Quit. \n""")
        # quit
        user_input = input("What is your choice? ")
        if user_input.upper() == "Q":
            done = True
            print("Game Over")
        # status check
        elif user_input.upper() == "E":
            print("Miles traveled: ", miles_traveled)
            print("Drinks in canteen: ", canteen_drinks)
            print("The natives are", miles_traveled - natives_distance, "miles behind you. \n")
        # Stop for the night
        elif user_input.upper() == "D":
            camel_tiredness = 0
            print("The camel is happy and energized, with it's fatigue now", camel_tiredness)
            natives_distance += random.randrange(7, 14)
        # Ahead full speed
        elif user_input.upper() == "C":
            miles_traveled += random.randrange(10, 21)
            print("You travelled", miles_traveled, "miles.")
            natives_distance += random.randrange(7, 15)
            thirst += 1
            camel_tiredness += random.randrange(1, 4)
            oasis = random.randrange(1, 21)
        # Ahead moderate speed
        elif user_input.upper() == "B":
            miles_traveled += random.randrange(5, 13)
            print(" You travelled", miles_traveled, "miles.")
            thirst += 1
            camel_tiredness += 1
            natives_distance += random.randrange(7, 14)
            oasis = random.randrange(1, 21)
        # Drink from canteen
        elif user_input.upper() == "A":
            if canteen_drinks == 0:
                print("You are out of water.")
            else:
                canteen_drinks -= 1
                thirst = 0
                print("You feel refreshed! You have", canteen_drinks, "drinks remaining.")

        # Conditions
        # Thirst notification
        if 4 < thirst <= 6 and not done:
            print("You are thirsty.")
        # Died of Thirst
        elif thirst > 6:
            print("You died of thirst!")
            done = True
        # Camel tiredness notification
        if 5 < camel_tiredness <= 8 and not done:
            print("Your camel is getting tired.")
        # Camel death
        elif camel_tiredness > 8:
            print("Your camel is dead.")
            done = True
        # Natives game over
        if natives_distance >= miles_traveled:
            print("The natives caught up to you, and killed you.")
            done = True
        # Native distance warning
        elif miles_traveled - natives_distance <= 15:
            print("The natives are getting close!")
        # Win condition
        if miles_traveled >= 200 and not done:
            print("You escaped the natives and won the game!")
            done = True
        # Oasis check
        if oasis == 20 and not done:
            canteen_drinks += 1
            camel_tiredness = 0
            thirst = 0
            print("You found an oasis! Both you and your camel have a drink, and you refill some of your canteen! \n")


main()
