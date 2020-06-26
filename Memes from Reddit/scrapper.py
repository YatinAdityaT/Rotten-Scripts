import os
import re
import praw
import pickle
import requests 
import traceback


reddit = praw.Reddit(client_id=PERSONAL_USE_SCRIPT_14_CHARS,client_secret=SECRET_KEY_27_CHARS, 
                     user_agent=YOUR_APP_NAME,username=YOUR_REDDIT_USER_NAME, 
                     password=YOUR_REDDIT_LOGIN_PASSWORD)

subreddit = reddit.subreddit('PrequelMemes')

def dump_old():
    with open('old.pickle','wb') as f:
        pickle.dump(old,f)



if os.path.exists('old.pickle'):
    with open('old.pickle','rb') as f:
        old = pickle.load(f)
else:
    old = []    
    dump_old()


r = praw.Reddit(client_id=PERSONAL_USE_SCRIPT_14_CHARS,client_secret=SECRET_KEY_27_CHARS, 
                     user_agent=YOUR_APP_NAME,username=YOUR_REDDIT_USER_NAME, 
                     password=YOUR_REDDIT_LOGIN_PASSWORD)
subreddit = r.subreddit('PrequelMemes')
posts = subreddit.top(limit=100)

scrapped = []

for post in posts:
    url = post.url
    if url not in old:
        title = post.title
        extenstion = url.split('.')[-1]
        if len(extenstion)==3:
            title = re.sub('[^A-Z a-z 0-9]+', '', title)
            title+= '.'+extenstion
            scrapped.append([title,url])
            old.append(url)
        else:
            try:
                url = post.media['reddit_video']['fallback_url']
                url = url.split("?")[0]
                title = post.title[:30].rstrip() + ".mp4"
                title = re.sub('[^A-Z .a-z0-9]+', '', title)
                scrapped.append([title,url])
                old.append(url)
            except:
                pass
dump_old()



def download_content(scrapped):
    for title,url in scrapped:
        print(url)
        r = requests.get(url)
        with open(os.path.join("memes",title),"wb") as f:
            f.write(r.content)


download_content(scrapped)