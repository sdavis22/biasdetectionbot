from credentials import *
from time import sleep
import tweepy
import scraper

#Fox News, FoxLA, CBSNews, CBSLA, ABC, NBCNews, AP
follow_list = ['15012486', '1367531', '9648652', '28785486', '24928809', '14173315', '51241574']
auth = tweepy.OAuthHandler(consumer_key, consumer_key_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

class Listener(tweepy.StreamListener):
    def on_status(self, status):
        if status.is_quote_status:
            return
        if status.id in follow_list:
            result = scraper.check_article(status)
            if result[0]:
                #Could be a single word or a wordlist
                if isinstance(result[1], str):
                    print(status.entities['urls'])
                    update = "@" + status.user.screen_name
                    update += " this article used some coded language. "
                    update += "The word " + result[1] + " is widely considered to be "
                    update += "dated in the criminal justice community. "
                    update += "https://twitter.com/i/web/status/" + status.id_str
                    print(update)
                else:
                    print(status.entities['urls'])
                    update = "@" + status.user.screen_name
                    update += " this article used some coded language. "
                    update += "The phrase " + result[1][0] + " " + result[1][1] " is widely considered to be "
                    update += "dated in the criminal justice community. "
                    update += "https://twitter.com/i/web/status/" + status.id_str
                    print(update)
                new_status = api.update_status(update)
                api.retweet(new_status.id)

    def on_error(self, status_code):
        print(status_code)
        return False    

def run_bot():
    listener = Listener()
    stream = tweepy.Stream(auth, listener=listener, tweet_mode="extended")
    #Currently streams for @FOXLA, @FOXNews, and @CBSNews
    stream.filter(follow=follow_list)

run_bot()
#print("@" + status.user.screen_name)
