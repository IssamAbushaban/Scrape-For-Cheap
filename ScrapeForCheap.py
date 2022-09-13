# ScrapeForCheap.py
# 
# Developed by Issam Abushaban
# Last updated: Septempber 13th 2022
# 
# Objective: Scrape Amazon, Walmart & Ebay for the top result (as assessed by best match, price, and rating when applicable) matching a person's keywords and expected price

# So we can clear the terminal
import os
# This is to help us make HTTP request
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

# Clear Console
os.system('clear')

# Time to ask the user for their input
print("Scrape For Cheap - V0.0.1")
print("A python webscrape by Issam Abushaban\n\n")

print("Hello!\n")
print("Welcome to Scrape For Cheap!\n")

def requestKeywordInput():
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

print(requestKeywordInput())
