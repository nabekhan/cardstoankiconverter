## Convert cards to anki
# Notes:
# Question: Solution container (contains "photo question" (image), "image question" (text)
# and options -> list of selectors or hint)

# Feedback: results container collected (contains message (text answer) and class text containing
# td with feedback summary)

# Steps: 1) Login into cards, retrieve selected deck, click "Play Sequentially" 2) Retrieve data
# 3) Answer question to move onto the next question

# Second library to use list and export data to anki

# library
from retrievecard import importcards
from deckgen import deckgen


def main(username="", password="", bypasswarnings=False):
    if not username:
        username = input("Please enter your username for uofc cards:\n")
    if not password:
        password = input("Please enter your password for uofc cards:\n")
    if not bypasswarnings:
        warning = input("This script will autocomplete your cards deck in order to reveal all associated"
                        " cards. \nI suggest you go through the cards deck by yourself before converting it"
                        " into an anki deck. \nPlease type I UNDERSTAND to proceed:\n")
    else:
        warning = "I UNDERSTAND"
    if warning == "I UNDERSTAND":
        deckname = input("Please enter the cards deck name you wish to convert: \n") # ex: "Get to know SAWH"
        cards = importcards(deckname, username, password)
        deckgen(cards, deckname)

        # import csv
        # with open(deckname+'.csv', 'w', newline='') as f:
        #     writer = csv.writer(f)
        #     writer.writerows(cards)
    else:
        print("Ending . . .")
        exit()

if __name__ == "__main__":
    main()