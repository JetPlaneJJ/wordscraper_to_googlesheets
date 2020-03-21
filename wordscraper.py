'''
Jay Lin, 3/20/2020
'''
import datetime
import requests
from bs4 import BeautifulSoup
from collections import Counter
from string import punctuation

page = requests.get("https://news.google.com/?hl=en-US&gl=US&ceid=US:en")
soup = BeautifulSoup(page.content, features="html.parser")
# words within paragraphs
text_p = (''.join(s.findAll(text=True))for s in soup.findAll('p'))
c_p = Counter((x.rstrip(punctuation).lower() for y in text_p for x in y.split()))

# We get the words within divs
text_div = (''.join(s.findAll(text=True))for s in soup.findAll('div'))
c_div = Counter((x.rstrip(punctuation).lower() for y in text_div for x in y.split()))

# We sum the two counters and get a list with words count from most to less common
total = c_div + c_p
irrelevant_words = ["the","for","a","and","on","in","this","are","at","be","by","has","were","will","with","they"]
for word in irrelevant_words:
    try:
        del total[word] # prune irrelevant words
    except KeyError:
        print("Key not found")
list_most_common_words = total.most_common()
print(total.most_common(15))

d = datetime.datetime.today()
print('Current date and time: ', d)
