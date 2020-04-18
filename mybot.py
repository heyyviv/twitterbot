import tweepy
import time
import requests
import json

CONSUMER_KEY='xxxxx'#key
CONSUMER_SECRET='xxxxx'#sectetkey
ACCESS_KEY='xxxx'#acesskey
ACCESS_SECRET='xxxxx'#secret accesskey

auth=tweepy.OAuthHandler(CONSUMER_KEY,CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY,ACCESS_SECRET)
api=tweepy.API(auth)
#mentions=api.mentions_timeline()
#"dict_keys(['_api', '_json', 'created_at', 'id', 'id_str', 'text', 'truncated', 'entities', 'source', 'source_url'," \
#" 'in_reply_to_status_id', 'in_reply_to_status_id_str', 'in_reply_to_user_id', 'in_reply_to_user_id_str', " \
#"'in_reply_to_screen_name', 'author', 'user', 'geo', 'coordinates', 'place', 'contributors', 'is_quote_status', " \
#"'retweet_count', 'favorite_count', 'favorited', 'retweeted', 'lang'])"
FILE_NAME='last_seen.txt'


def see_last_seen(fname):
    last_seen=open(fname,'r')
    last_id=int(last_seen.read().strip())
    last_seen.close()
    return last_id



def store_last_seen(fname,last_id):
    last_seen=open(fname,'w')
    last_seen.write(str(last_id))
    last_seen.close()
    return


#main function
def reply_to_tweet():
    #replying to mention tweet
    last_seen_id=see_last_seen(FILE_NAME)
    mentions=api.mentions_timeline(last_seen_id,tweet_mode='extended')
    for mention in reversed(mentions):
        last_seen_id=mention.id
        store_last_seen(FILE_NAME,last_seen_id)
        if '@username' in mention.full_text.lower():
            print("tweeting",flush=True)
            api.update_status('@'+mention.user.screen_name+"Thanks buddy ",mention.id)
    #tweet to twitter account
    url = "https://api.ratesapi.io/api/latest?base=USD"

    payload = {}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload)
    if(response.ok==True):
        tt = response.json()
        kk = tt['rates']
        beatles = 'Base is USD    INR:' + str(kk['INR']) + '  JPY:' + str(kk['JPY']) + ' EUR:' + str(
                kk['EUR']) + ' AUD:' + str(kk['AUD'])
        heyy = str(tt['date'])
        try:
            api.update_status(status=beatles+'at :'+heyy+ ' #economy')
        except tweepy.TweepError as error:
            if error.api_code == 187:
                # Do something special
                print('someting is wrong')
        else:
             pass



while(True):
    reply_to_tweet()
    time.sleep(7200)
