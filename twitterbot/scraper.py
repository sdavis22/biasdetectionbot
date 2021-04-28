from bs4 import BeautifulSoup
import string
import ssl
import urllib.request
from textblob import TextBlob
ssl._create_default_https_context = ssl._create_unverified_context

crime_words = ["sentenced", "suspect", "police", "killed", "robbed", "robbery", 
"prosecutor", "prosecutors", "defendants", "defendant", "convicted", "shooting", "crime", "arrested",
"crimes", "suspects", "shootings"]

problem_words = ["criminal", "felon", "ghetto", "addict", "deviant",
"thug", "junkie", "psycho", "alien", "felons", "aliens", "thugs", "junkies", "illegals",
"criminals", "convicts"]

problem_digrams = [["violent", "criminal"], ["violent", "felon"], ["illegal", "alien"], ["illegal", "aliens"],
["violent", "criminals"], ["violent", "felons"], ["mentally", "ill"], ["drug", "addict"], ["drug", "abuser"],
["illegal", "immigrants"], ["illegal", "immigrant"]]

#Input: String of article text
#Output: Article text with removed punctuation
def remove_punctuation(text):
  if isinstance(text, str):
    no_punct = "".join([c for c in text if c not in string.punctuation])
    return no_punct

#Checks article text against common crime words
#Returns true if we predict the article is about crime, false if not
def validate_crime(text):
    text_no_punct = remove_punctuation(text)
    for word in text_no_punct.split():
        for word1 in crime_words:
            if word.lower() == word1:
                return True
    return False

def check_noun(blob, word):
    blob_parts = blob.tags
    for pair in blob_parts:
        if pair[0].lower() == word:
            if pair[1] == 'NNS' or pair[1] == 'NN':
                return True
            else:
                return False
    return False

#Same as above method, but checks against problematic words
# Returns True and the word found, or False and None            
def check_problematic(text):
    blob = TextBlob(text)
    subjective = blob.sentiment.subjectivity
    polarity = blob.sentiment.polarity
    if subjective > 0.33 or polarity < 0:
        for word in blob.words:
            for word1 in problem_words:
                if word.lower() == word1:
                    if word1 == 'criminal' or word1 == 'felon' or word1 == 'criminals':
                        if check_noun(blob, word1):
                            return True, word1
                    else:    
                        return True, word1
        for digram in blob.ngrams(2):
            for digram1 in problem_digrams:
                if digram[0].lower() == digram1[0] and digram[1].lower() == digram1[1]:
                    return True, digram1
    return False, None

#Given a link, returns the article text
#we also pass in the news organization, for different scraping protocols
def get_article_text(link, org):
    if org == "CBSLA":
        article_text_noheaders = ''
        html = urllib.request.urlopen(link).read().decode()
        soup = BeautifulSoup(html, "html.parser")
        article = soup.find("div", class_="main-story-wrapper")
        article_text = article.findAll("p")
        for p in article_text:
            article_text_noheaders += p.text.strip() + " "
        article_text_noheaders.strip()
        if validate_crime(article_text_noheaders):
            return article_text_noheaders
        else:
            print(article_text_noheaders)
            return None
    elif org == "AP":
        article_text_noheaders = ''
        html = urllib.request.urlopen(link).read().decode()
        soup = BeautifulSoup(html, "html.parser")
        article = soup.find(class_="Article")
        article_text = article.findAll("p")
        for p in article_text:
            article_text_noheaders += p.text.strip() + " "
        article_text_noheaders.strip()
        if validate_crime(article_text_noheaders):
            return article_text_noheaders
        else:
            print(article_text_noheaders)
            return article_text_noheaders
    else:
        article_text_noheaders = ''
        html = urllib.request.urlopen(link).read().decode()
        soup = BeautifulSoup(html, "html.parser")
        article = soup.find("article")
        article_text = article.findAll("p")
        for p in article_text:
            article_text_noheaders += p.text.strip() + " "
        article_text_noheaders.strip()
        if validate_crime(article_text_noheaders):
            return article_text_noheaders
        else:
            print(article_text_noheaders)
            return None

#Wrapper method for scraping from a tweet
#Input: Tweepy Status
#Output: False if no link/problematic language found
#True if we find a link, read the text, and find coded language
def check_article(status):
    #get link from tweet if exists
    link = ''
    if status.entities['urls'] is not None:
        if len(status.entities['urls']) > 0:
            link = status.entities['urls'][0]['expanded_url']
            org = status.user.screen_name
        else:
            return False, None
    else:
        return False, None
    text = get_article_text(link, org)
    if text is not None:
        return check_problematic(text)
