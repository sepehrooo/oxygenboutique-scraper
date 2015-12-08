# oxygenboutique-scraper
oxygenboutique.com python scraper. (Lyst challenge)

This scraper is written with Python and Scrapy framework.
To use it, install Scrapy, create a scrapy project named oxygenboutique.com, replace the items.py and add oxygen.py
then run this code in your terminal:
scrapy crawl oxygenboutique.com -o result.json -t json

Some information about my code:
About products' gender, all oxygenboutique's products are for ladies, so I'm returning all products gender as "F". But it is possible to write a code to guess the gender by product name and description if necessary.
For guessing products' colors I have scraped colorhexa.com/color-names with Scrapy.

A sample output is items.json.

Thanks for checking my code :)