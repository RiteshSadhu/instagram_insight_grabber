import pandas as pd
account='' #enter name of your account 
account_insight='Insight of {}.txt'.format(account)
with open(account_insight,'r+') as file:
    lines=file.readlines()
    Dframe=pd.read_excel('Insight of {}.xlsx'.format(account),index_col=0)
    for line in lines:
        line=line.strip()
        temp_Dframe=pd.read_excel(line,index_col=0)
        Dframe=Dframe.append(temp_Dframe)
    Dframe.to_excel(account_insight[:account_insight.find('.')]+'.xlsx')
    file.truncate(0)
    pass

account_info='General Information of {}.txt'.format(account)
with open(account_info,'r+') as file:
    lines=file.readlines()
    Dframe=pd.read_excel('General Information of {}.xlsx'.format(account),index_col=0)
    for line in lines:
        line=line.strip()
        temp_Dframe=pd.read_excel(line,index_col=0)
        Dframe=Dframe.append(temp_Dframe)
    Dframe.to_excel(account_info[:account_info.find('.')]+'.xlsx')
    file.truncate(0)
    pass

post_inight='Posts Insights of {}.txt'.format(account)
with open(post_inight,'r+') as file:
    lines=file.readlines()
    Dframe=pd.read_excel('Posts Insights of {}.xlsx'.format(account),index_col=0)
    for line in lines:
        line=line.strip()
        temp_Dframe=pd.read_excel(line,index_col=0)
        Dframe=Dframe.append(temp_Dframe)
    Dframe.to_excel(post_inight[:post_inight.find('.')]+'.xlsx')
    file.truncate(0)
    pass
