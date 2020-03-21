'''
Jay Lin, 3/20/2020
'''
import pygsheets
import pandas as pd
import datetime
import requests
from bs4 import BeautifulSoup
from collections import Counter
from string import punctuation

'''make sure connected to Google Sheets'''
gc = pygsheets.authorize(service_file='/Users/jiaji/Documents/creds.json')
df = pd.DataFrame()

''' Do the word-scraping '''
page = requests.get("https://abcnews.go.com/")
soup = BeautifulSoup(page.content, features="html.parser")
# words within paragraphs
text_p = (''.join(s.findAll(text=True))for s in soup.findAll('p'))
c_p = Counter((x.rstrip(punctuation).lower() for y in text_p for x in y.split()))

# We get the words within divs (may not want or need this)
text_div = (''.join(s.findAll(text=True))for s in soup.findAll('div'))
c_div = Counter((x.rstrip(punctuation).lower() for y in text_div for x in y.split()))

# We sum the two counters and get a list with words count from most to less common
total = c_p + c_div
irrelevant_words = ["–","ampvideo_youtubethe","coveragekeyboard_arrow_up","...ampvideo_youtubethe","agobookmark_bordersharemore_vert","agobookmark_bordersharemore_vertview"," ","","is","as","from","of","to","the","for","a","and","on","in","this","are","at","be","by","has","were","will","with","they"]
for word in irrelevant_words:
    try:
        del total[word] # prune irrelevant words
    except KeyError:
        print(word + " -> Key not found")
list_most_common_words = total.most_common(100)
# for debugging:
print(total.most_common(15))

''' Document current date '''
d = datetime.datetime.today()
print('Current date and time: ', d)

''' Push data into Spreadsheets '''
# create top 100 words column (titled with date)
most_com_words = [a_tuple[0] for a_tuple in list_most_common_words]
df[str(d)] = most_com_words
df['Word Count'] = [a_tuple[1] for a_tuple in list_most_common_words]
# open ss
sh = gc.open('Online News Word Counts')
# select and update sheet
wks = sh[2]
wks.set_dataframe(df,(1,1))



