# ScrapeForCheap.py
# 
# Developed by Issam Abushaban
# Last updated: Septempber 24th 2022
# 
# Objective: Scrape Amazon, Walmart & Ebay for the top result 
# (as assessed by best match, price, and rating when applicable) matching a person's keywords and expected price

# So we can clear the terminal
import os

# Scrape For Cheap functions
from ScrapeForCheapFuncs import *

# Boolean variable to let us know if the user wants to quit
quitTheProgram = False

# Clear Console
os.system('clear')

# Time to ask the user for their input
print("Scrape For Cheap - V0.0.6")
print("A python webscrape by Issam Abushaban\n")
print("THIS SOFTWARE IS INTENDED FOR EDUCATIONAL USE ONLY\n")
print("-------------------------------------")

print("\n\nHello!")
print("\nWelcome to Scrape For Cheap!")

while not quitTheProgram:

    # First we will get the input from the user and clean it up
    # This function will convert that text to a URL text and return it
    keywordString = ask_For_Keyword()

    # Now we need to ask the user for their preferences
    # This function will take the user input and return a double as a price guess
    priceGuess = ask_For_Price_Guess()

    # After we will generate the correct URLs by combining them
    generatedURLs = generate_URLs(keywordString, priceGuess)
    
    # Now we will execute the scraping queiries
    responsesRecieved = get_Request_For_URLs(generatedURLs)

    if (len(responsesRecieved) == 0):
        print("\nThere was a critical error getting the requests.")
        print("We will not be able to execute your request at this time :(")
        print("Please try again later.")
        quitTheProgram = not ask_For_User_Desire_To_Continue()
        continue
    
    # If the queiries were successful we will preform some clean up and interpret the result using Soup!
    digestedResponse = digest_Responses(responsesRecieved)

    # Lastly we will print out the answer to the user!
    print("-------------------------------------")
    print("Here is your answer:\n" + digestedResponse)

    # Ask them if they want to do another!
    quitTheProgram = not ask_For_User_Desire_To_Continue()

print("\nThank you for trying out Scrape For Cheap :D !\n")
raise SystemExit