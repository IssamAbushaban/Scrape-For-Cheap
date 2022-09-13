# Web Scraping Ideation

Scraper takes a search term and looks for the cheapest product matching the key words on three sites:

- Walmart
- Ebay
- Amazon

This means I will need to examine each of these to learn how they operate.

Let’s research how each of these sites structure their URIs.

## Walmart

- Searching for “Blue Cat Hat” produces the following:
    - [https://www.walmart.com/search?q=Blue+Cat+Hat](https://www.walmart.com/search?q=Blue+Cat+Hat)
    - https://www.walmart.com/search?q=[keywords parsed by +]
- For the price is lowest on Walmart this happens:
    - [https://www.walmart.com/search?q=Blue+Cat+Hat&sort=price_low](https://www.walmart.com/search?q=Blue+Cat+Hat&sort=price_low)
    - &sort=price_low

## Ebay

- Searching for “Blue Cat Hat” produces the following:
    - [https://www.ebay.com/sch/i.html?_nkw=Blue+Cat+Hat](https://www.ebay.com/sch/i.html?_nkw=Blue+Cat+Hat)
    - https://www.ebay.com/sch/i.html?_nkw=[keywords parsed by +]
- For the price is lowest on Ebay this happens:
    - [https://www.ebay.com/sch/i.html?_nkw=Blue+Cat+Hat&_sop=15](https://www.ebay.com/sch/i.html?_nkw=Blue+Cat+Hat&_sop=15)
    - &_sop=15

## Amazon

- Searching for “Blue Cat Hat” produces the following:
    - [https://www.amazon.com/s?k=Blue+Cat+Hat](https://www.amazon.com/s?k=Blue+Cat+Hat)
    - https://www.amazon.com/s?k=[parsed by + Keywords]
- For the price is lowest on Amazon this happens:
    - [https://www.amazon.com/s?k=Blue+Cat+Hat&s=price-asc-rank](https://www.amazon.com/s?k=Blue+Cat+Hat&s=price-asc-rank)
    - &s=price-asc-rank
- If we add in the highest rating filter
    - [https://www.amazon.com/s?k=Blue+Cat+Hat&rh=p_72%3A2661618011&s=price-asc-rank](https://www.amazon.com/s?k=Blue+Cat+Hat&rh=p_72%3A2661618011&s=price-asc-rank)
    - &rh=p_72%3A2661618011&s=price-asc-rank