# ScrapeForCheapFuncs.py
# 
# Developed by Issam Abushaban
# Last updated: Septempber 24th 2022
# 
# Objective: Scrape for Cheap Functions

# This is to make the text coming from the site more readible
from bs4 import BeautifulSoup 
# So we can convert text to a URL query
import urllib.parse
# This is to help us make HTTP request and for scraping protection against websites
from scrapfly import ScrapeConfig, ScrapflyClient
# API Credentials (Note you will not get this file from me. 
# You need to create a file called ScrapFlyApi and add the variable apiTestKey = "YOUR API KEY". 
# Make sure to get one from the scrapFly website. You can start with a free account. DO NOT SHARE YOUR Key)
from ScrapFlyApi import apiTestKey

# Start a session
session = ScrapflyClient(key=apiTestKey, max_concurrency=1)

# So we can connect
headers = { 
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36",
            "sec-ch-ua-platform" : "macOS",
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "accept-language": "en-US;en;q=0.9",
            "accept-encoding": "gzip, deflate, br"
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
def generate_URLs(keywordString, priceGuess):
    
    # amazon has some weird rules!
    amazonKeywordString = keywordString.replace("+","%2B").replace("%20", "+")

    # Min price specifications
    walmartPriceGuess = str(round(priceGuess))
    ebayPriceGuess = "{0:.2f}".format(priceGuess)
    amazonPriceGuess = "{0:.2f}".format(priceGuess)
    amazonPriceGuessParts = amazonPriceGuess.split(".")
    amazonPriceGuess =   amazonPriceGuessParts[0] + amazonPriceGuessParts[1]
    
    # Generate The URLS
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

    responsesRecieved = [ 
                          session.scrape(ScrapeConfig(url=generatedURLs[0],headers=headers, asp=True, country="US")),
                          session.scrape(ScrapeConfig(url=generatedURLs[1],headers=headers, asp=True, country="US")),
                          session.scrape(ScrapeConfig(url=generatedURLs[2],headers=headers, asp=True, country="US"))
                        ]

    print()

    # Check for request failures
    if (responsesRecieved[0].status_code != 200):
        print("> Walmart Request Failed - Status Code: " + str(responsesRecieved[0].status_code))
        numFailures += 1

    if (responsesRecieved[1].status_code != 200):
        print("> Ebay Request Failed - Status Code: " + str(responsesRecieved[1].status_code))
        numFailures += 1

    if (responsesRecieved[2].status_code != 200):
        print("> Amazon Request Failed - Status Code: " + str(responsesRecieved[2].status_code))
        numFailures += 1

    if numFailures > 0:
        responsesRecieved.clear()
    
    return responsesRecieved

# This function...
def digest_Responses(responsesRecieved):
    # Use Beautiful Soup to clean that html!
    soups = [BeautifulSoup(response.content, 'html.parser') for response in responsesRecieved]
    
    # Response Prep
    walmartResponse = "\nWhat we found at Walmart" + "\n\n"
    ebayResponse = "\nWhat we found at Ebay" + "\n\n"
    amazonResponse = "\nWhat we found at Amazon" + "\n\n"

    # Walmart Digest ###############################
    try:
        walmartOuterDiv   = soups[0].find('div', id="results-container").next_sibling.find('div')
        walmartInnerList = walmartOuterDiv.contents        
        walmartItemURL = "https://www.walmart.com/" + walmartInnerList[0].find('div').find('div').find('a').get("href")
        walmartItemInfo = walmartInnerList[0].find('div').find('div').find('div').find('div').next_sibling
        walmartItemTitle = walmartItemInfo.contents[1].find('span').text
        walmartItemPrice = walmartItemInfo.select('div[data-automation-id="product-price"]')[0].select('div[aria-hidden="true"]')[0].text
        
        # Now we need to deal with the numbers provided.
        # Walmart prices look like this "$700.00", so let's convert it to 700.00
        walmartItemPrice = walmartItemPrice.replace("$","")

        # Walmart doesn't disclose shipping cost on the first page, but there is a general rule of thumb.
        # Prices above $35 get free shipping.
        if float(walmartItemPrice) >= 35.00:
            walmartItemShipping = "0.00"
        else:
            walmartItemShipping = "TBD at checkout"
        
        walmartItemCost = float(walmartItemPrice)

        walmartResponse += "Item: " + walmartItemTitle + "\n"
        walmartResponse += "Price: $" + walmartItemPrice + "\n"
        walmartResponse += "Shipping: $" + walmartItemShipping + "\n"
        walmartResponse += "Link: " + walmartItemURL + "\n"

    except:
        walmartItemCost = 99999999.99
        walmartResponse += ">Walmart Digest Failed"
    
    # Ebay Digest ##################################
    try:
        ebayOuterDiv  = soups[1].find('div', id="mainContent").find('div', id="srp-river-results")
        ebayInnerList = ebayOuterDiv.find('ul',class_="srp-results srp-list clearfix")
        ebayItemURL = ebayInnerList.select('li[data-view="mi:1686|iid:1"]')[0].find('a', class_="s-item__link").get("href")
        ebayItemInfo  = ebayInnerList.select('li[data-view="mi:1686|iid:1"]')[0].find('div', class_="s-item__info clearfix")
        ebayItemTitle = ebayItemInfo.find('div',class_="s-item__title").find('span').text
        ebayItemPrice = ebayItemInfo.find('div',class_="s-item__details clearfix").find('span', class_="s-item__price").text
        ebayItemShipping = ebayItemInfo.find('div',class_="s-item__details clearfix").find('span', class_="s-item__shipping s-item__logisticsCost").text

        # Now we need to deal with the numbers provided.
        # Ebay prices look like this "$700.00", so let's convert it to 700.00
        ebayItemPrice = ebayItemPrice.replace("$","")

        # Ebay shipping look like this "+$5.00 shipping" or "Free shipping"
        if ebayItemShipping.startswith("Free"):
            ebayItemShipping = "0.00"
        else:
            ebayItemShipping = ebayItemShipping.replace("+","").replace(" shipping","").replace("$","")

        ebayItemCost = float(ebayItemPrice) + float(ebayItemShipping)
    
        ebayResponse += "Item: " + ebayItemTitle + "\n"
        ebayResponse += "Price: $" + ebayItemPrice + "\n"
        ebayResponse += "Shipping: $" + ebayItemShipping + "\n"
        ebayResponse += "Link: " + ebayItemURL + "\n"

    except:
        ebayItemCost = 99999999.99
        ebayResponse += ">Ebay Digest Failed"
    
    # Amazon Digest ################################
    try:
        amazonItemTitle = "Item Title"
        amazonItemPrice = "0.00"
        amazonItemShipping =  "0.00"
        amazonItemCost = float(amazonItemPrice) + float(amazonItemShipping)
        amazonItemURL = responsesRecieved[2].url

        amazonResponse += "Item: " + amazonItemTitle + "\n"
        amazonResponse += "Price: $" + amazonItemPrice + "\n"
        amazonResponse += "Shipping: $" + amazonItemShipping + "\n"
        amazonResponse += "Link: " + amazonItemURL + "\n"
    
    except:
        amazonItemCost = 99999999.99
        amazonResponse += ">Amazon Digest Failed"

    # Completing The Response Digest
    digestedResponse = "\nWe have determined that the cheapest product is:\n"
    remainingResponse = "\nBelow you will find detail for the other two sites:\n"

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