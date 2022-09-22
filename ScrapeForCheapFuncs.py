# ScrapeForCheapFuncs.py
# 
# Developed by Issam Abushaban
# Last updated: Septempber 14th 2022
# 
# Objective: Scrape for Cheap Functions

# For replacing text
from dataclasses import replace
from select import select
from types import TracebackType
from unittest import case
# For transating to URL
from urllib import response
# This is to help us make HTTP request
import requests
# This is to make the text coming from the site more readible
from bs4 import BeautifulSoup 
# So we can convert text to a URL query
import urllib.parse

# So we can connect
headers = { 
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36",
            "sec-ch-ua-platform" : "macOS"
          }

# Walmart URI components
walmartURIPrefix  = "https://www.walmart.com/search?q="
walmartURISuffix1 = "&min_price="
walmartURISuffix2 = "&sort=price_low"

# Ebay URI components
ebayURIPrefix  = "https://www.ebay.com/sch/i.html?_nkw="
ebayURISuffix1 = "&_udlo="
ebayURISuffix2 = "&_sop=15"

# Amazon URI components
amazonURIPrefix  = "https://www.amazon.com/s?k="
amazonURISuffix1 = "&rh=p_36%3A"
amazonURISuffix2 = "-%2Cp_72%3A2661618011&s=price-asc-rank"

# This function requests keywords from the user and returns them as space seperated values
def ask_For_Keyword():
    keywords = ""
    keywordsApproved = False
    
    while not keywordsApproved:
        print("\nWhat would you like to search for today?")
        keywords = input("\nkey words: ").strip()

        #Check keywords
        if keywords == "":
            print("\nPlease enter at least one keyword, and make sure it is space seperated.")
            continue
        else:
            keywordslist = keywords.split()
            keywords = ' '.join(keywordslist)
            
            if keywords == "":
                print("\nPlease enter at least one keyword, and make sure it is space seperated.")
                continue
            
            else:
                keywordsApproved = True

    return urllib.parse.quote(keywords)

# This function requests a price estimate from the user and returns it to the program
def ask_For_Price_Guess():
    price = 0.00
    priceApproved = False
    
    while not priceApproved:
        print("\nWhat is the lowest price you estimate that item could go for?")
        price = input("\n$").strip()
        
        #Check keywords
        try:
            price = float(price)
        except ValueError:
            print("\nPlease enter in a valid price (e.g. $2.00).")
            continue
        
        if price <= 0.00:
            print("\nPlease enter a price greater thank $0.00.")
            continue
        else:
            priceApproved = True

    return price

# This function takes the keywords and price guess of the user and converts them to full URLs
# TODO: Right now priceGuess is not yet incorporated.
def generate_URLs(keywordString, priceGuess):
    
    # amazon has some weird rules!
    amazonKeywordString = keywordString.replace("+","%2B").replace("%20", "+")

    # Min price specifications
    walmartPriceGuess = str(round(priceGuess))
    ebayPriceGuess = "{0:.2f}".format(priceGuess)
    amazonPriceGuess = "{0:.2f}".format(priceGuess)
    amazonPriceGuessParts = amazonPriceGuess.split(".")
    amazonPriceGuess =   amazonPriceGuessParts[0] + amazonPriceGuessParts[1]
    
    # Debugging!
    #print("\nwalmartPriceGuess = " + walmartPriceGuess)
    #print("\nebayPriceGuess = " + ebayPriceGuess)
    #print("\namazonPriceGuess = " + amazonPriceGuess)

    generatedURLs = [
        walmartURIPrefix + keywordString + walmartURISuffix1 + walmartPriceGuess + walmartURISuffix2,
        ebayURIPrefix + keywordString + ebayURISuffix1 + ebayPriceGuess + ebayURISuffix2,
        amazonURIPrefix + amazonKeywordString + amazonURISuffix1 + amazonPriceGuess + amazonURISuffix2
    ]

    return generatedURLs

# This function gets the requests for the urls and returns a list of the Responses
def get_Request_For_URLs(generatedURLs):
    
    # Keep track of the request failures
    numFailures = 0

    # lets make a GET request for each URL
    responsesRecieved = [ requests.get(generatedURLs[0], headers=headers),
                          requests.get(generatedURLs[1], headers=headers),
                          requests.get(generatedURLs[2], headers=headers)
                        ]

    print()

    # Check for request failures
    if (responsesRecieved[0].status_code != 200):
        print(">Walmart Request Failed - Status Code: " + str(responsesRecieved[0].status_code))
        numFailures += 1
    
    if (responsesRecieved[1].status_code != 200):
        print(">Ebay Request Failed - Status Code: " + str(responsesRecieved[1].status_code))
        numFailures += 1

    if (responsesRecieved[2].status_code != 200):
        print(">Amazon Request Failed - Status Code: " + str(responsesRecieved[2].status_code))
        numFailures += 1

    if numFailures > 0:
        responsesRecieved.clear()
    
    return responsesRecieved

# This function...
def digest_Responses(responsesRecieved):
    # Use Beautiful Soup to clean that html!
    soups = [BeautifulSoup(response.content, 'html.parser') for response in responsesRecieved]

    #Debugging Build
    while 1:
        # Walmart Digest
        #walmartMainDiv  = soups[0].find('div[data-stack-index="0"]')
        #walmartSubDiv   = walmartMainDiv.select("section > div")
        #walmartAllItems = walmartSubDiv.select("div > div")
        
        walmartItemTitle = "Item Title"
        walmartItemPrice = "0.00"
        walmartItemShipping =  "0.00"
        walmartItemCost = float(walmartItemPrice) + float(walmartItemShipping)

        # Ebay Digest
        ebayOuterDiv  = soups[1].find('div', id="mainContent").find('div', id="srp-river-results")
        ebayInnerList = ebayOuterDiv.find('ul',class_="srp-results srp-list clearfix")
        ebayItem      = ebayInnerList.select('li[data-view="mi:1686|iid:1"]')
        
        ebayItemTitle = "Item Title"
        ebayItemPrice = "0.00"
        ebayItemShipping =  "0.00"
        ebayItemCost = float(ebayItemPrice) + float(ebayItemShipping)

        # Amazon Digest
        amazonItemTitle = "Item Title"
        amazonItemPrice = "0.00"
        amazonItemShipping =  "0.00"
        amazonItemCost = float(amazonItemPrice) + float(amazonItemShipping)

        # Response Prep
        walmartResponse = "What we found at: Walmart" + "\n"
        walmartResponse += "Item: " + walmartItemTitle + "\n"
        walmartResponse += "Price: $" + walmartItemPrice + "\n"
        walmartResponse += "Shipping: $" + walmartItemShipping + "\n"

        ebayResponse = "What we found at: Ebay" + "\n"
        ebayResponse += "Item: " + ebayItemTitle + "\n"
        ebayResponse += "Price: $" + ebayItemPrice + "\n"
        ebayResponse += "Shipping: $" + ebayItemShipping + "\n"

        amazonResponse = "What we found at: Amazon" + "\n"
        amazonResponse += "Item: " + amazonItemTitle + "\n"
        amazonResponse += "Price: $" + amazonItemPrice + "\n"
        amazonResponse += "Shipping: $" + amazonItemShipping + "\n"

        digestedResponse = "We have determined that the cheapest product is:"
        remainingResponse = "Below you will find detail for the other two sites:"

        # Response Digest
        digestedResponse += "\n"

        if (walmartItemCost <= ebayItemCost and walmartItemCost <= amazonItemCost):
            digestedResponse += walmartResponse + "\n" + remainingResponse
            digestedResponse += ebayResponse + "\n"
            digestedResponse += amazonResponse + "\n"

        elif (ebayItemCost <= walmartItemCost and ebayItemCost <= amazonItemCost):
            digestedResponse += ebayResponse + "\n" + remainingResponse
            digestedResponse += walmartResponse + "\n"
            digestedResponse += amazonResponse + "\n"

        elif (amazonItemCost <= walmartItemCost and amazonItemCost <= ebayItemCost):
            digestedResponse += amazonResponse + "\n" + remainingResponse
            digestedResponse += walmartResponse + "\n"
            digestedResponse += ebayResponse + "\n"

    return digestedResponse

# This function...
def ask_For_User_Desire_To_Continue():
    userDesireToContinue = False
    userInput = ""
    inputApproved = False

    while not inputApproved:
        print("\nWould you like to try again?")
        userInput = input("\nY or N: ").strip()

        #Check Input
        if userInput == "Y" or userInput.capitalize() == "YES":
            userDesireToContinue = True
            inputApproved = True
        elif userInput == "N" or userInput.capitalize() == "NO":
            userDesireToContinue = False
            inputApproved = True
        else : 
            print("\nPlease enter Yes or No.")
            continue

    return userDesireToContinue