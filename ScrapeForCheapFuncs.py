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
walmartURIPrefix = "https://www.walmart.com/search?q="
walmartURISuffix = "&sort=price_low"

# Ebay URI components
ebayURIPrefix = "https://www.ebay.com/sch/i.html?_nkw="
ebayURISuffix = "&_sop=15"

# Amazon URI components
amazonURIPrefix = "https://www.amazon.com/s?k="
amazonURISuffix = "&rh=p_72%3A2661618011&s=price-asc-rank"

# This function requests keywords from the user and returns them as space seperated values
def ask_For_Keyword():
    keywords = ""
    keywordsApproved = False
    
    while not keywordsApproved:
        print("What would you like to search for today?\n")
        keywords = input().strip()
        
        #Check keywords
        if keywords == "":
            print("Please enter at least one keyword, and make sure it is space seperated.\n")
            continue
        else:
            keywordslist = keywords.split()
            keywords = ' '.join(keywordslist)
            
            if keywords == "":
                print("Please enter at least one keyword, and make sure it is space seperated.\n")
                continue
            
            else:
                keywordsApproved = True

    return urllib.parse.quote(keywords)

# This function requests a price estimate from the user and returns it to the program
def ask_For_Price_Guess():
    price = 0.00
    priceApproved = False
    
    while not priceApproved:
        print("What is the lowest price you estimate that item could go for?\n")
        price = input("$").strip()
        
        #Check keywords
        if not price.isfloat:
            print("\nPlease enter in a valid price (e.g. $2.00).")
            continue
        elif float(price) <= 0.00:
            print("\nPlease enter a price greater thank $0.00.")
            continue
        else:
            priceApproved = True

    return price

# This function takes the keywords and price guess of the user and converts them to full URLs
# TODO: Right now priceGuess is not yet incorporated.
def generate_URLs(keywordString, priceGuess):

    return [
            walmartURIPrefix + keywordString + walmartURISuffix,
            ebayURIPrefix + keywordString + ebayURISuffix,
            amazonURIPrefix + keywordString + amazonURISuffix
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