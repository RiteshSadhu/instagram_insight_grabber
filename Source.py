import pandas as pd
from time import sleep, strftime
import urllib.request , json

def w_s_count(string):
    word=1
    senteces=0
    for i in string:
        if i==' ':
            word+=1
        if i=='.':
            senteces+=1
    return [word,senteces]


#Acess Token given from facebook app
access_token=''
# Instagram account ID of acconected to your access token
account_id=''
# Account username of your connected Instagram account 
account=''

#give json files
#general information
with urllib.request.urlopen('https://graph.facebook.com/v6.0/{}/?fields=followers_count%2Cfollows_count%2Cmedia_count%2Cstories&access_token={}'.format(account_id,access_token)) as url:
    general_info=json.loads(url.read().decode())
pass

#account insight
with urllib.request.urlopen('https://graph.facebook.com/v6.0/{}/insights?metric=impressions%2Creach%2Cprofile_views%2Cwebsite_clicks%2Cemail_contacts&period=day&access_token={}'.format(account_id,access_token)) as url:
    account_insight=json.loads(url.read().decode())
pass
account_insight=account_insight['data']

#posts id
posts_id_list=[]
with urllib.request.urlopen('https://graph.facebook.com/v6.0/{}/media?access_token={}'.format(account_id,access_token)) as url:
    posts_id=json.loads(url.read().decode())
pass
for id in posts_id['data']:
    posts_id_list.append(id['id'])

#posts
with urllib.request.urlopen('https://graph.facebook.com/v6.0/{}/media?fields=like_count%2Ccomments_count%2Cmedia_type%2Cid%2Ctimestamp%2Ccaption&access_token={}'.format(account_id,access_token)) as url:
    posts_info=json.loads(url.read().decode())
pass
posts_info=posts_info['data']

#Posts_insight
posts_insight_list=[]
for id in posts_id_list:
    with urllib.request.urlopen("https://graph.facebook.com/v6.0/{}/insights?metric=engagement%2Cimpressions%2Creach%2Csaved&access_token={}".format(id,access_token)) as url:
        post_inight=json.loads(url.read().decode())
        posts_insight_list.append(post_inight['data'])
    pass

#extract data
general_info_dict={'Number of Followers':general_info['followers_count'],
'Number of Following':general_info['follows_count'],
'Number of Media':general_info['media_count'],
'Number of Posts':len(posts_id_list)}
if 'stories' in list(general_info.keys()):
    general_info_dict['Number of Stories']=len(general_info['stories']['data'])
else:
    general_info_dict['Number of Stories']=0


account_insight_dict={'impressions':account_insight[0]['values'][1]['value'],
'Reach':account_insight[1]['values'][1]['value'],
'Profile Views':account_insight[2]['values'][1]['value'],
'Website click':account_insight[3]['values'][1]['value'],
'Email click':account_insight[4]['values'][1]['value']}

posts_dict={'Post Number':[i for i in range(len(posts_id_list),0,-1)],
'Time of creation':[posts_info[i]['timestamp'][:10] for i in range(len(posts_id_list))],
'Title':[posts_info[i]['caption'][:50] for i in range(len(posts_id_list))],
'Number of words':[w_s_count(posts_info[i]['caption'])[0] for i in range(len(posts_id_list))],
'Number of senteces':[w_s_count(posts_info[i]['caption'])[1] for i in range(len(posts_id_list))],
'Likes':[posts_info[i]['like_count'] for i in range(len(posts_id_list))],
'Comments':[posts_info[i]['comments_count'] for i in range(len(posts_id_list))],
'Engagement':[posts_insight_list[i][0]['values'][0]['value'] for i in range(len(posts_id_list))],
'Impressions':[posts_insight_list[i][1]['values'][0]['value'] for i in range(len(posts_id_list))],
'Reach':[posts_insight_list[i][2]['values'][0]['value'] for i in range(len(posts_id_list))],
'Saved':[posts_insight_list[i][3]['values'][0]['value'] for i in range(len(posts_id_list))]}
posts_dict['Person/Seen']=[posts_dict['Impressions'][i]/posts_dict['Reach'][i] for i in range(len(posts_id_list))]


#creat DataFrame
general_info_Dframe=pd.DataFrame(general_info_dict,index=[strftime("%y/%m/%d")])
account_insight_Dframe=pd.DataFrame(account_insight_dict,index=[strftime("%y/%m/%d")])
posts_Dframe=pd.DataFrame(posts_dict,index=[strftime("%y/%m/%d") for i in range(len(posts_id_list))])

#creat csvs
general_info_Dframe.to_excel('General Information of {}_{}.xlsx'.format(account,strftime('%y-%m-%d')))
account_insight_Dframe.to_excel('Insight of {}_{}.xlsx'.format(account,strftime('%y-%m-%d')))
posts_Dframe.to_excel('Posts Insights of {}_{}.xlsx'.format(account,strftime('%y-%m-%d')),encoding = 'utf-8-sig')

#file names
with open ('General Information of zamo_graphic.txt','w') as file:
    file.write('General Information of {}_{}.xlsx\n'.format(account,strftime('%y-%m-%d')))
pass

with open('Insight of zamo_graphic.txt','w') as file:
    file.write('Insight of {}_{}.xlsx'.format(account,strftime('%y-%m-%d')))
pass

with open('Posts Insights of zamo_graphic.txt','w') as file:
    file.write('Posts Insights of {}_{}.xlsx'.format(account,strftime('%y-%m-%d')))
pass
