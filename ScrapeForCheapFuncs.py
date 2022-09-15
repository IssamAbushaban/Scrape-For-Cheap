# ScrapeForCheapFuncs.py
# 
# Developed by Issam Abushaban
# Last updated: Septempber 14th 2022
# 
# Objective: Scrape for Cheap Functions

# This is to help us make HTTP request
from urllib import response
import requests
# This is to make the text coming from the site more readible
from bs4 import BeautifulSoup 
# So we can convert text to a URL query
import urllib.parse

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

    walmartPriceGuess = str(round(priceGuess))
    ebayPriceGuess = "{0:.2f}".format(priceGuess)
    amazonPriceGuess = "{0:.2f}".format(priceGuess)

    amazonPriceGuessParts = amazonPriceGuess.split(".")
    amazonPriceGuess =   amazonPriceGuessParts[0] + amazonPriceGuessParts[1]
    
    # Debugging!
    #print("\nwalmartPriceGuess = " + walmartPriceGuess)
    #print("\nebayPriceGuess = " + ebayPriceGuess)
    #print("\namazonPriceGuess = " + amazonPriceGuess)

    return [
            walmartURIPrefix + keywordString + walmartURISuffix1 + walmartPriceGuess + walmartURISuffix2,
            ebayURIPrefix + keywordString + ebayURISuffix1 + ebayPriceGuess + ebayURISuffix2,
            amazonURIPrefix + keywordString + amazonURISuffix1 + amazonPriceGuess + amazonURISuffix2
            ]

# This function...
def get_Request_For_URLs(generatedURLs):
    return []

# This function...
def digest_Requests(requestsGotten):
    return []

# This function...
def ask_For_User_Desire_To_Continue():
    return False