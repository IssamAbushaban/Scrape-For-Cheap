# ScrapeForCheap.py
# 
# Developed by Issam Abushaban
# Last updated: Septempber 13th 2022
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
print("Scrape For Cheap - V0.0.2")
print("A python webscrape by Issam Abushaban\n\n")

print("Hello!\n")
print("Welcome to Scrape For Cheap!\n")

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
    requestsGotten = get_Request_For_URLs(generatedURLs)
    
    # Keep track of the request failures
    numFailures = 0

    # Check for request failures
    if (len(requestsGotten) == 0):
        numFailures = 3
        print("\nThere was a critical error getting the requests.")

    else:
        if (requestsGotten[1].status_code != 200):
            print("Walmart Request Failed - Status Code: " + str(requestsGotten[1].status_code))
            numFailures += 1
        
        if (requestsGotten[2].status_code != 200):
            print("Ebay Request Failed - Status Code: " + str(requestsGotten[2].status_code))
            numFailures += 1

        if (requestsGotten[3].status_code != 200):
            print("Amazon Request Failed - Status Code: " + str(requestsGotten[3].status_code))
            numFailures += 1

    if numFailures > 0:
        print("\nDue to failures we will not be able to execute your request at this time :(\n")
        print("Please try again soon later.\n")

    else:
        # If the queiries were successful we will preform some clean up and interpret the result using Soup!
        digestedResponse = digest_Requests(requestsGotten)

        # Lastly we will print out the answer to the user!
        print("\nHere is your answer: " + digestedResponse + "\n")

    # Ask them if they want to do another!
    quitTheProgram = not ask_For_User_Desire_To_Continue()

print("Thank you for trying out Scrape For Cheap :D !\n")
raise SystemExit