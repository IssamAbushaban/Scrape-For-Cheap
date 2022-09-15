# Web Scraping Ideation

Scraper takes a search term and looks for the cheapest product matching the key words on three sites:

- **`Walmart`**
- **`Ebay`**
- **`Amazon`**

This means I will need to examine each of these to learn how they operate.

Let’s research how each of these sites structure their URIs.

## Walmart

- Searching for “Blue Cat Hat” produces the following:
    - [`https://www.walmart.com/search?q=Blue+Cat+Hat`](https://www.walmart.com/search?q=Blue+Cat+Hat)
        - https://www.walmart.com/search?q=[keywords parsed by +]
- For the price is lowest and at least $10.02, we can't do that. walmart seems to ignore decimals and then the item search is invalid. Therefore we have to round to an integer. Let's do $10. On Walmart this happens:
    - [`https://www.walmart.com/search?q=Blue+Cat+Hat&min_price=10&sort=price_low`](https://www.walmart.com/search?q=Blue+Cat+Hat&min_price=10&sort=price_low)
        - &sort=price_low
        - &min_price=10

- Now if we focus on the html that will get us the values we want, we will notice that they are all housed in this `div`:
    
    ![Untitled](Web%20Scraping%20Ideation/Untitled.png)
    

- The code snippet is below:
    
    ```html
    <div class="flex flex-wrap w-100 flex-grow-0 flex-shrink-0 ph2 pr0-xl pl4-xl mt0-xl mt3">...
    
    	<div class="mb1 ph1 pa0-xl bb b--near-white w-25">...
    		
    		<div data-item-id="5TU4LT2EOU9Z" class="sans-serif mid-gray relative flex flex-column w-100 hide-child-opacity">...
    		
    		</div>
    	
    	</div>
    
    </div>
    ```
    

- The most notable part of the code above are the following:
    - mb1 ph1 pa0-xl bb b--near-white w-25
    
    This is because the other items seem to be specific to the item displayed whereas this part represents the class that this item is. It should always be the first one of its class on the page so we can search for the class. We can also make use of it’s parent with the class (it only shows up once):
    
    - flex flex-wrap w-100 flex-grow-0 flex-shrink-0 ph2 pr0-xl pl4-xl mt0-xl mt3
- The rest of the following code snippets are contained within that inner `div`.
    - The following code snippet contains the name of the seller of the product:
        
        ```html
        <div class="b f6 black mr1 mt2 mb1 lh-copy">Surpdew</div>
        ```
        
    - The following code snippet contains the title of the product:
        
        ```html
        <span class="w_BO" style="-webkit-line-clamp: 3; padding-bottom: 0em; margin-bottom: 0em;"><span data-automation-id="product-title" class="f6 f5-l normal dark-gray mb0 mt1 lh-title">Pet Accessories Clearance Bibs Pet Saliva Towel Halloween With Costume Puppy Decor Hats For Small Cat Dog Blue</span></span>
        ```
        

- The following code snippet contains the price and shipping cost of the product:
    
    ```html
    <div data-automation-id="product-price" class="flex flex-wrap justify-start items-center lh-title mb2 mb1-m"><div class="b black f5 mr1 mr2-xl lh-copy f4-l" aria-hidden="true">$3.62</div><span class="w_BR">current price $3.62</span><div class="f7 f6-l gray mr1 strike" aria-hidden="true">$7.39</div><span class="w_BR">was $7.39</span><div class="f7 f6-l gray">+$3.49 shipping</div></div>
    ```
    

## Ebay

- Searching for “Blue Cat Hat” produces the following:
    - [`https://www.ebay.com/sch/i.html?_nkw=Blue+Cat+Hat`](https://www.ebay.com/sch/i.html?_nkw=Blue+Cat+Hat)
        - https://www.ebay.com/sch/i.html?_nkw=[keywords parsed by +]
- For the price is lowest and at least $10.02 on Ebay this happens:
    - [`https://www.ebay.com/sch/i.html?_nkw=Blue+Cat+Hat&_udlo=10&_sop=15`](https://www.ebay.com/sch/i.html?_nkw=Blue+Cat+Hat&_udlo=10.02&_sop=15)
        - &_sop=15
        - &_udlo=10.02

- Now if we focus on the html that will get us the values we want, we will notice that they are all housed in this `div`:
    
    ![Untitled](Web%20Scraping%20Ideation/Untitled%201.png)
    

- The code snippet is below:
    
    ```html
    <li class="s-item s-item__pl-on-bottom" data-view="mi:1686|iid:1" data-gr4="2" data-gr3="2" data-gr2="2">...</li>
    ```
    

- The most notable parts of the code above are the following:
    - data-view="mi:1686|iid:1"
    - data-gr4="2"
    - data-gr3="2"
    - data-gr2="2"
    
    This is because the other items seem to be specific to the item displayed whereas these represent where it is on the page. Note: data-gr#="1" seems to be the header where it says “Result”. It seems to be generated always as the first result.
    
- The rest of the following code snippets are contained within that `div`.
    - The following code snippet contains the name of the seller of the product:
        
        ```html
        <h5 class="s-line-clamp-1"><span class="a-size-base-plus a-color-base">Moonker</span></h5>
        
        ```
        

- The following code snippet contains the title of the product:
    
    ```html
    <div class="s-item__title"><span role="heading" aria-level="3">Plain Beanie Cat Ears Bunny Cuffed Warm Ski Winter Knitted Cap Hat Fashion Cute</span></div>
    ```
    

- The following code snippet contains the price of the product:
    
    ```html
    <div class="s-item__detail s-item__detail--primary"><span class="s-item__price">$4.89</span></div>
    ```
    
- Lastly, the following code snippet contains the shipping cost of the product:
    
    ```html
    <div class="s-item__details clearfix"><div class="s-item__detail s-item__detail--primary"><span class="s-item__price">$1.39</span></div><div class="s-item__detail s-item__detail--primary"><span class="s-item__trending-price">Was: <span class="clipped">Previous Price</span><span class="STRIKETHROUGH">$1.99</span></span>&ensp;&ensp;<span class="s-item__discount s-item__discount"><span class="BOLD">30% off</span></span></div><div class="s-item__detail s-item__detail--primary"><span class="s-item__purchase-options s-item__purchaseOptions">or Best Offer</span></div><div class="s-item__detail s-item__detail--primary"><span class="s-item__shipping s-item__logisticsCost">+$5.99 shipping</span></div><div class="s-item__detail s-item__detail--primary"><span> <span aria-labelledby="s-8lmo782" class="s-8lmo782_s-8mql657" role="group"><span aria-hidden="true">&ZeroWidthSpace;<wbr>Sponsored</span></span></span><span class="s-item__space_bar"></span></div></div>
    ```
    
    - Note if the product has no shipping the price is alone.

## Amazon

- Searching for “Blue Cat Hat” produces the following:
    - [`https://www.amazon.com/s?k=Blue+Cat+Hat`](https://www.amazon.com/s?k=Blue+Cat+Hat)
        - https://www.amazon.com/s?k=[parsed by + Keywords]
- For the price is lowest and at least $10 on Amazon this happens:
    - [`https://www.amazon.com/s?k=Blue+Cat+Hat&rh=p_36%3A1000-&s=price-asc-rank`](https://www.amazon.com/s?k=Blue+Cat+Hat&rh=p_36%3A1000-&s=price-asc-rank)
        - &s=price-asc-rank
        - &rh=p_36%3A1002-
            - Interesting that the 10.02 is hidden here &rh=p_36%3A *1002* -
- If we add in the highest rating filter
    - [`https://www.amazon.com/s?k=Blue+Cat+Hat&rh=p_36%3A1002-%2Cp_72%3A2661618011&s=price-asc-rank`](https://www.amazon.com/s?k=Blue+Cat+Hat&rh=p_36%3A1002-%2Cp_72%3A2661618011&s=price-asc-rank)
    - It combines with the at least $10 piece!
        - &rh=p_36%3A1002-%2Cp_72%3A2661618011

- Now if we focus on the html that will get us the values we want, we will notice that they are all housed in this `div`:
    ![Untitled](Web%20Scraping%20Ideation/Untitled%202.png)
    
- The code snippet is below:
    
    ```html
    <div data-asin="B07F3M4V77" data-index="2" data-uuid="4cc87241-b461-4c5a-ba7a-d3d161645a14" data-component-type="s-search-result" class="sg-col-4-of-12 s-result-item s-asin sg-col-4-of-16 sg-col s-widget-spacing-small sg-col-4-of-20" data-component-id="12" data-cel-widget="search_result_2">...</div>
    ```
    

- The most notable parts of the code above are the following:
    - data-index="2"
    - data-cel-widget="search_result_2"
    
    This is because the other items seem to be specific to the item displayed whereas these represent where it is on the page. Note: search_result_1 seems to be the header where it says “Result”. It seems to be generated always as the first result.
    
- The rest of the following code snippets are contained within that `div`.
    - The following code snippet contains the name of the seller of the product:
        
        ```html
        <h5 class="s-line-clamp-1"><span class="a-size-base-plus a-color-base">Moonker</span></h5>
        
        ```
        

- The following code snippet contains the title of the product:
    
    ```html
    <h2 class="a-size-mini a-spacing-none a-color-base s-line-clamp-2"><a class="a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal" href="/Toddler-Girls-Summer-Bucket-Protection/dp/B07F3M4V77/ref=sr_1_1?keywords=Blue+Cat+Hat&amp;qid=1663019396&amp;refinements=p_72%3A2661618011&amp;sr=8-1"><span class="a-size-base-plus a-color-base a-text-normal">Baby Sun Hat,Kids Toddler Boy Girls Cat Ears Summer Straw Hat Bucket Sun Protection Cap</span> </a> </h2>
    ```
    

- The following code snippet contains the price of the product:
    
    ```html
    <a class="a-size-base a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal" href="/Toddler-Girls-Summer-Bucket-Protection/dp/B07F3M4V77/ref=sr_1_1?keywords=Blue+Cat+Hat&amp;qid=1663019396&amp;refinements=p_72%3A2661618011&amp;sr=8-1"><span class="a-price" data-a-size="xl" data-a-color="base"><span class="a-offscreen">$2.99</span><span aria-hidden="true"><span class="a-price-symbol">$</span><span class="a-price-whole">2<span class="a-price-decimal">.</span></span><span class="a-price-fraction">99</span></span></span> </a>
    ```
    
- Lastly, the following code snippet contains the shipping cost of the product:
    
    ```html
    <div class="a-row a-size-base a-color-secondary s-align-children-center"><span aria-label="$6.99 shipping"><span class="a-color-base">$6.99 shipping</span></span></div>
    ```