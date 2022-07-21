from bs4 import BeautifulSoup
import requests
# BeautifulSoup4 - it works with a parser, eg, lxml parser to retrieve data out of HTML and XML files.
# Requests - allows to send HTTP requests using Python.
# lxml - it is an XML and HTML parser.

# used headers to prevent the Amazon website from blocking me access.
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 '
                  'Safari/537.36',
    "Upgrade-Insecure-Requests": "1",
    "DNT": "1",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate"
}
url = "https://www.amazon.com/gp/bestsellers/books/ref=bsm_nav_pill_print/ref=s9_acss_bw_cg_bsmpill_1c1_w?pf_rd_m=ATVPDKIKX0DER&pf_rd_s=merchandised-search-1&pf_rd_r=JSFR919BB1373W4FETRV&pf_rd_t=101&pf_rd_p=65e3ce24-654c-43fb-a17b-86a554348820&pf_rd_i=16857165011"

amazon_html = requests.get(url, headers=headers)
# created a Beautiful Soup object
amazon = BeautifulSoup(amazon_html.text, 'lxml')

books = amazon.select(".zg-item-immersion")

# the function returns the book names of books with 5 star rating
# the ratings list is outside the scope of the five_star_ratings function because it has to be used in another function.
ratings = []


def five_star_ratings():
    print("BOOK NAMES WITH FIVE STAR RATINGS: ")
    for book_name in books:
        if "a-star-5" in str(book_name):
            for reviews in book_name.select(".p13n-sc-truncate"):
                book_names = reviews.getText().strip()
                ratings.append(book_names)
    print(ratings)

# the prices list is outside the scope of the high_prices function because it has to be used in another function.
prices = []

# this function returns the prices of books with 5 star ratings.
def high_prices():
    print(" ")
    print("BOOK PRICES OF BOOK NAMES WITH FIVE STAR RATINGS: ")
    for book_name in books:
        if "a-star-5" in str(book_name):
            for reviews in book_name.find('span', class_="p13n-sc-price"):
                book_names = reviews.getText().strip()
                # I removed the dollar sign and converted the string to a float so that I can sort the prices in ascending order.
                prices.append(float(book_names.replace('$', '')))

    print(prices)

# this function returns the list of the top 10 expensive books
def combined_list():
    print(" ")
    print("BOOK NAMES AND PRICES OF THE TEN MOST EXPENSIVE BOOKS:")
    # to combine the two lists I had created above, I used the zip function.
    book_name_price = zip(ratings, prices)
    # I then converted the book_name_price to a list by calling the list function
    lis = list(book_name_price)
    # I first tried to sort using sort with no arguments inside but my program crashed
    # so I resorted to using lambda to sort my list of tuples using prices.
    # I used index 1, since 1 is the index of prices in the lists of tuples.
    lis.sort(key=lambda x: x[1])
    # the problem with lambda is that it strictly sorts items from least to most.
    # so I retrieved the last 10 books by slicing the list, since the last 10 books are the ones with the high prices.
    print(lis[-10:])

# defined the main function to order the way the functions defined above should execute so as to avoid the program from
# # returning empty lists.
def main():
    five_star_ratings()
    high_prices()
    combined_list()


main()
