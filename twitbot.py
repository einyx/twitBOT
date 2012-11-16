LATESTFILE = 'latest_prcd.txt'
LOGFILE = 'log_prcd.txt'
import sys
import twitter
import aiml
import os, time
os.chdir('/Users/einyx/twitBOT')
bot=aiml.Kernel()  
bot.learn("alice/*.aiml")  



api = twitter.Api(consumer_key='',
consumer_secret='',
access_token_key='',
access_token_secret='')

if os.path.exists(LATESTFILE):
    fp = open(LATESTFILE)
    lastid = fp.read().strip()
    fp.close()

    if lastid == '':
        lastid = 0
else:
    lastid = 0

fp = open(LOGFILE)
alreadyMessaged = fp.readlines()
fp.close()
for i in range(len(alreadyMessaged)):
    if alreadyMessaged[i].strip() == '':
        continue

    alreadyMessaged[i] = alreadyMessaged[i].split('|')[1]
alreadyMessaged.append('prcd1') 

results = api.GetSearch('music', since_id=lastid)

if len(results) == 0:
    print 'Nothing to reply to. Quitting.'
    sys.exit()
repliedTo = []

for statusObj in results:
    postTime = time.mktime(time.strptime(statusObj.created_at[:-6], '%a, %d %b %Y %H:%M:%S'))

    if time.time() - (24*60*60) < postTime and statusObj.user.screen_name not in alreadyMessaged and '@prcd1' not in statusObj.text.lower():
        if [True for x in alreadyMessaged if ('@' + x).lower() in statusObj.text.lower()]:
            print 'Skipping because it\'s a mention: @%s - %s' % (statusObj.user.screen_name.encode('ascii', 'replace'), statusObj.text.encode('ascii', 'replace'))
            continue

        try:
            print 'Posting in reply to @%s: %s' % (statusObj.user.screen_name.encode('ascii', 'replace'), statusObj.text.encode('ascii', 'replace'))
            # try to get the string into unicode
            post = unicode(statusObj.text) # probably an error here?
            reply = bot.respond(post)
            api.PostUpdate((reply), in_reply_to_status_id=statusObj.id)
            repliedTo.append( (statusObj.id, statusObj.user.screen_name, statusObj.text.encode('utf-8', 'replace')) )
            time.sleep(1)
        except Exception:
            print "Unexpected error:", sys.exc_info()[0:2]


fp = open(LATESTFILE, 'w')
fp.write(str(max([x.id for x in results])))
fp.close()

fp = open(LOGFILE, 'a')
fp.write('\n'.join(['%s|%s|%s' % (x[0], x[1], x[2]) for x in repliedTo]) + '\n')
fp.write('\n')
fp.close()
