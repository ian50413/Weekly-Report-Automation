# -*- coding: utf-8 -*-
"""
Created on Fri Mar 10 11:08:25 2023

@author: ian.chen25
"""

import pandas as pd

colnames=['Year', 'Month', 'DayOfMonth', '2WeekNum', 'Date', 'CustId', 'UserName', 'Country', 'Currency', 'Company_Turnover', 'Company_Winlost'
          , 'Market', 'Product', 'Type', 'IsVIP', 'Brand']

Year = 2023
Month = 3
Day = 7
big_player_limit = 5

vnd_df = pd.read_csv('VND_for_python.csv', names=colnames, header=None)
vnd_for_dau = pd.read_csv('VND_for_python.csv', names=colnames, header=None)
vnd_df.dtypes
#Add YearMonth column
vnd_df['YearMonth'] = vnd_df['Year'].astype(str) + '-' + vnd_df['Month'].astype(str)

#Time Stamp filter
#vnd_df = vnd_df[vnd_df['Year'].between(1,7)]
#vnd_df = vnd_df[vnd_df['Month'].between(1,7)]
vnd_df = vnd_df[vnd_df['DayOfMonth'].between(1,Day)]


#%%
target_mau_summary = {}
#MAU by Year-Month these three years
mau = vnd_df.groupby(['Year','Month'])['CustId'].nunique().reset_index()
mau = mau.rename(columns={'CustId':'MAU'})
mau['PCT_Change'] = mau['MAU'].pct_change().round(4)*100
target_mau = mau[mau['Year'] == Year]
target_mau = target_mau[target_mau['Month'].between(Month-1, Month)].reset_index(drop=True)
target_mau_summary['target_mau'] = target_mau

#MAU by BET & TOP
brand_mau = vnd_df.groupby(['Brand','Year','Month'])['CustId'].nunique().reset_index()
brand_mau = brand_mau.rename(columns={'CustId':'MAU'})
brand_mau['PCT_Change'] = brand_mau['MAU'].pct_change().round(4)*100
target_brand_mau = brand_mau[brand_mau['Year'] == Year]
target_brand_mau = target_brand_mau[target_brand_mau['Month'].between(Month-1, Month)].reset_index(drop=True)
target_mau_summary['target_brand_mau'] = target_brand_mau

#MAU by Market
market_mau = vnd_df.groupby(['Market','Year','Month'])['CustId'].nunique().reset_index()
market_mau = market_mau.rename(columns={'CustId':'MAU'})
market_mau['PCT_Change'] = market_mau['MAU'].pct_change().round(4)*100
target_market_mau = market_mau[market_mau['Year'] == Year]
target_market_mau = target_market_mau[target_market_mau['Month'].between(Month-1, Month)].reset_index(drop=True)
target_mau_summary['target_market_mau'] = target_market_mau

#MAU by PlayerType
pt_mau = vnd_df.groupby(['Type','Year','Month'])['CustId'].nunique().reset_index()
pt_mau = pt_mau.rename(columns={'CustId':'MAU'})
pt_mau['PCT_Change'] = pt_mau['MAU'].pct_change().round(4)*100
target_pt_mau = pt_mau[pt_mau['Year'] == Year]
target_pt_mau = target_pt_mau[target_pt_mau['Month'].between(Month-1, Month)].reset_index(drop=True)
target_mau_summary['target_pt_mau'] = target_pt_mau

#MAU by Product
pd_mau = vnd_df.groupby(['Product','Year','Month'])['CustId'].nunique().reset_index()
pd_mau = pd_mau.rename(columns={'CustId':'MAU'})
pd_mau['PCT_Change'] = pd_mau['MAU'].pct_change().round(4)*100
target_pd_mau = pd_mau[pd_mau['Year'] == Year]
target_pd_mau = target_pd_mau[target_pd_mau['Month'].between(Month-1, Month)].reset_index(drop=True)
target_mau_summary['target_pd_mau'] = target_pd_mau

#MAU by Product & Player Type
pd_pt_mau = vnd_df.groupby(['Product','Type','Year','Month'])['CustId'].nunique().reset_index()
pd_pt_mau = pd_pt_mau.rename(columns={'CustId':'MAU'})
pd_pt_mau['PCT_Change'] = pd_pt_mau['MAU'].pct_change().round(4)*100
target_pd_pt_mau = pd_pt_mau[pd_pt_mau['Year'] == Year]
target_pd_pt_mau = target_pd_pt_mau[target_pd_pt_mau['Month'].between(Month-1, Month)].reset_index(drop=True)
target_mau_summary['target_pd_pt_mau'] = target_pd_pt_mau

#%%
target_winning_summary = {}
#Winning, Turnover by Year-Month these three years
winning_turnover = vnd_df.groupby(['Year','Month'])['Company_Winlost', 'Company_Turnover'].sum().reset_index()
winning_turnover = winning_turnover.rename(columns={'Company_Winlost':'Winlost'})
winning_turnover = winning_turnover.rename(columns={'Company_Turnover':'Turnover'})
winning_turnover['Winlost'] = winning_turnover['Winlost']#.round(2).astype(int)
winning_turnover['Turnover'] = winning_turnover['Turnover']#.round(2).astype(int)
winning_turnover['Winning_PCT_Change'] = winning_turnover['Winlost'].pct_change().round(4)*100
winning_turnover['Turnover_PCT_Change'] = winning_turnover['Turnover'].pct_change().round(4)*100
target_winning_turnover = winning_turnover[winning_turnover['Year'] == Year]
target_winning_turnover = target_winning_turnover[target_winning_turnover['Month'].between(Month-1, Month)].reset_index(drop=True)
target_winning_turnover = target_winning_turnover[['Year','Month','Winlost','Winning_PCT_Change','Turnover','Turnover_PCT_Change']]
target_winning_summary['target_winning_turnover'] = target_winning_turnover

#Product Margin
margin = vnd_df[vnd_df['Year'] == Year]
margin = margin[margin['Month'].between(Month-1,Month)]
margin = margin.groupby(['Product','Year','Month'])['Company_Winlost','Company_Turnover'].sum().reset_index()
margin['Company_Winlost'] = margin['Company_Winlost'].round(2).astype(int)
margin['Company_Turnover'] = margin['Company_Turnover'].round(2).astype(int)
margin['Winlost_PCT_change'] = margin['Company_Winlost'].pct_change().round(4)*100
margin['Turnover_PCT_change'] = margin['Company_Turnover'].pct_change().round(4)*100
margin['Margin'] = (margin['Company_Winlost'] / margin['Company_Turnover']).round(3)*100
target_margin = margin.reset_index(drop=True)
target_winning_summary['target_margin'] = target_margin
#margin = margin.pivot(index='Product', columns=('Year','Month'), values='Margin')
#margin = margin.fillna(0)

# Get big player list for current month
big_player_limit = 5

big_player = vnd_df[vnd_df['Year'] == Year]
big_player = big_player[big_player['Month'].between(Month-1,Month)]
big_player = big_player.groupby(['YearMonth','UserName'])['Company_Winlost'].sum().reset_index()
big_player = big_player.pivot(index='UserName', columns='YearMonth', values='Company_Winlost')
big_player = big_player.fillna(0)
big_player['diff'] = (big_player.iloc[:,1] - big_player.iloc[:,0]).round(2)
# big_player = big_player.reset_index()
#big_player['Company_Winlost'] = big_player['Company_Winlost'].round().astype(int)
#big_player['diff'] = big_player['diff'].round(2)
co_lose_most = big_player['diff'].nsmallest(big_player_limit).index.values.tolist()
co_win_most = big_player['diff'].nlargest(big_player_limit).index.values.tolist()
outlier_bigplayer = co_lose_most + co_win_most
big_player_check = big_player.reset_index()
big_player_check = big_player_check[['UserName','diff']]
big_player_check = big_player_check[big_player_check['UserName'].isin(outlier_bigplayer)]
big_player_check = big_player_check.reset_index(drop=True)
target_winning_summary['outlier_bigplayer'] = outlier_bigplayer
target_winning_summary['big_player_check'] = big_player_check


"""
#Margin without big players current month (exclude top/bottom 5)
ex_margin = vnd_df[vnd_df['Year'] == Year]
ex_margin = ex_margin[ex_margin['Month'] == Month]
ex_margin = ex_margin[~ex_margin['UserName'].isin(outlier_bigplayer)]  # remove big player current month
ex_margin = ex_margin.groupby(['Product','Year','Month'])['Company_Winlost','Company_Turnover'].sum().reset_index()
#ex_margin['Company_Winlost'] = ex_margin['Company_Winlost'].round(2)  # .astype(int)
#ex_margin['Company_Turnover'] = ex_margin['Company_Turnover'].round(2)  # .astype(int)
ex_margin['Margin'] = (ex_margin['Company_Winlost'] / ex_margin['Company_Turnover']).round(3)*100
target_exclude_margin = ex_margin.reset_index(drop=True)
#ex_margin = ex_margin.pivot(index='Product', columns=('Year','Month'), values='Margin')
#ex_margin = ex_margin.fillna(0)
"""
    
#Get every products big player and calculate margin excluding big player
product_list = ['Sport', 'Casino', 'Game', 'ESport']

target_product_bp = {}
for i in product_list:
    target_product_bp[f"{i}_big_player"] = vnd_df[vnd_df['Year'] == Year]
    target_product_bp[f"{i}_big_player"] = target_product_bp[f"{i}_big_player"][target_product_bp[f"{i}_big_player"]['Month'].between(Month-1,Month)]
    target_product_bp[f"{i}_big_player"] = target_product_bp[f"{i}_big_player"][target_product_bp[f"{i}_big_player"]['Product'] == i]
    target_product_bp[f"{i}_big_player"] = target_product_bp[f"{i}_big_player"].groupby(['YearMonth','UserName'])['Company_Winlost'].sum().reset_index()
    target_product_bp[f"{i}_big_player"] = target_product_bp[f"{i}_big_player"].pivot(index='UserName', columns='YearMonth', values='Company_Winlost')
    target_product_bp[f"{i}_big_player"] = target_product_bp[f"{i}_big_player"].fillna(0)
    target_product_bp[f"{i}_big_player"]['diff'] = (target_product_bp[f"{i}_big_player"].iloc[:,1] - target_product_bp[f"{i}_big_player"].iloc[:,0]).round(2)
    co_lose_most = target_product_bp[f"{i}_big_player"]['diff'].nsmallest(big_player_limit).index.values.tolist()
    co_win_most = target_product_bp[f"{i}_big_player"]['diff'].nlargest(big_player_limit).index.values.tolist()
    target_product_bp[f"target_{i}_outlier_bigplayer"] = co_lose_most + co_win_most
    target_product_bp[f"{i}_big_player_check"] = target_product_bp[f"{i}_big_player"].reset_index()
    target_product_bp[f"target_{i}_big_player_check"] = target_product_bp[f"{i}_big_player_check"][target_product_bp[f"{i}_big_player_check"]['UserName'].isin(target_product_bp[f"target_{i}_outlier_bigplayer"])].reset_index(drop=True)
    
    target_product_bp[f"target_{i}_ex_margin"] = vnd_df[vnd_df['Year'] == Year]
    target_product_bp[f"target_{i}_ex_margin"] = target_product_bp[f"target_{i}_ex_margin"][target_product_bp[f"target_{i}_ex_margin"]['Month'] == Month]
    target_product_bp[f"target_{i}_ex_margin"] = target_product_bp[f"target_{i}_ex_margin"][target_product_bp[f"target_{i}_ex_margin"]['Product'] == i]
    target_product_bp[f"target_{i}_ex_margin"] = target_product_bp[f"target_{i}_ex_margin"][~target_product_bp[f"target_{i}_ex_margin"]['UserName'].isin(target_product_bp[f"target_{i}_outlier_bigplayer"])]  # remove big player current month
    target_product_bp[f"target_{i}_ex_margin"] = target_product_bp[f"target_{i}_ex_margin"].groupby(['Product','Year','Month'])['Company_Winlost','Company_Turnover'].sum().reset_index()
    target_product_bp[f"target_{i}_ex_margin"]['Company_Winlost'] = target_product_bp[f"target_{i}_ex_margin"]['Company_Winlost'].round(2).astype(int)
    target_product_bp[f"target_{i}_ex_margin"]['Company_Turnover'] = target_product_bp[f"target_{i}_ex_margin"]['Company_Turnover'].round(2).astype(int)
    target_product_bp[f"target_{i}_ex_margin"]['Margin'] = (target_product_bp[f"target_{i}_ex_margin"]['Company_Winlost'] / target_product_bp[f"target_{i}_ex_margin"]['Company_Turnover']).round(3)*100
    target_product_bp[f"target_{i}_ex_margin"] = target_product_bp[f"target_{i}_ex_margin"].reset_index(drop=True)
#%%
#Statement Generate
    #df.loc[df['column_name'] == some_value]
    #df.loc[(df['column_name'] >= A) & (df['column_name'] <= B)]
#MAU statement
print(f"{vnd_df.iloc[0]['Currency']} market MAU situation as below: ")
result_market = target_mau_summary['target_market_mau'].loc[(target_mau_summary['target_market_mau']['Year'] == Year)
                                           &(target_mau_summary['target_market_mau']['Month'] == Month)]
print(f"{result_market.iloc[0]['Market']} changed {result_market.iloc[0]['PCT_Change']} % in {result_market.iloc[0]['Year']} {result_market.iloc[0]['Month']}.")
print(f"{result_market.iloc[1]['Market']} changed {result_market.iloc[1]['PCT_Change']} % in {result_market.iloc[1]['Year']} {result_market.iloc[1]['Month']}.")

result_brand = target_mau_summary['target_brand_mau'].loc[(target_mau_summary['target_brand_mau']['Year'] == Year)
                                           &(target_mau_summary['target_brand_mau']['Month'] == Month)]
print(f"{result_brand.iloc[0]['Brand']} changed {result_brand.iloc[0]['PCT_Change']} % in {result_brand.iloc[0]['Year']} {result_brand.iloc[0]['Month']}.")
print(f"{result_brand.iloc[1]['Brand']} changed {result_brand.iloc[1]['PCT_Change']} % in {result_brand.iloc[1]['Year']} {result_brand.iloc[1]['Month']}.")

result_mau = target_mau_summary['target_mau'].round(2)
print(f"MAU last month is {result_mau.iloc[0]['MAU'].astype(int)} compare with this month {result_mau.iloc[1]['MAU'].astype(int)} changed {result_mau.iloc[1]['PCT_Change']}%.")

result_pt_mau = target_mau_summary['target_pt_mau'].round(2)
print(f"{result_pt_mau.iloc[0]['Type']} MAU last month is {result_pt_mau.iloc[0]['MAU']} compare with this month {result_pt_mau.iloc[1]['MAU']} changed {result_pt_mau.iloc[1]['PCT_Change']}%.")
print(f"{result_pt_mau.iloc[2]['Type']} MAU last month is {result_pt_mau.iloc[2]['MAU']} compare with this month {result_pt_mau.iloc[3]['MAU']} changed {result_pt_mau.iloc[3]['PCT_Change']}%.")
print(f"{result_pt_mau.iloc[4]['Type']} MAU last month is {result_pt_mau.iloc[4]['MAU']} compare with this month {result_pt_mau.iloc[5]['MAU']} changed {result_pt_mau.iloc[5]['PCT_Change']}%.")
print("\n")
#Winning Statement
print(f"{vnd_df.iloc[0]['Currency']} market Winning situation as below: ")
result_winning = target_winning_summary['target_winning_turnover']
print(f"Winning last month is {result_winning.iloc[0]['Winlost'].round(0).astype(int)} compare with this month {result_winning.iloc[1]['Winlost'].round(0).astype(int)} changed {result_winning.iloc[1]['Winning_PCT_Change']}%.")
print(f"Turnover last month is {result_winning.iloc[0]['Turnover'].round(0).astype(int)} compare with this month {result_winning.iloc[1]['Turnover'].round(0).astype(int)} changed {result_winning.iloc[1]['Turnover_PCT_Change']}%.")
winning_change = (result_winning.iloc[1]['Winlost'] - result_winning.iloc[0]['Winlost']).round(0).astype(int)
print(f"Winning change {winning_change}.")

result_big_player = target_winning_summary['big_player_check']
result_product = target_winning_summary['target_margin']
if (result_winning.iloc[1]['Winlost'].astype(int) - result_winning.iloc[0]['Winlost'].astype(int)) <= 0:
    result_big_player_negative = result_big_player[result_big_player['diff'] < 0 ].sort_values(by='diff', ascending=True).reset_index(drop=True)
    accum_winlost = 0
    print(f"{result_big_player_negative['UserName'].values} are top {big_player_limit} losing big player.")
    print(f"{result_big_player_negative['diff'].values} are top {big_player_limit} losing big player's winlost.")
    for i in result_big_player_negative.index:
        accum_winlost += result_big_player_negative.iloc[i]['diff']
        print(f"{i+1} top players account for {((accum_winlost/winning_change)*100).round(2)}% of winlost.")
        
elif (result_winning.iloc[1]['Winlost'].astype(int) - result_winning.iloc[0]['Winlost'].astype(int)) > 0:
    result_big_player_positive = result_big_player[result_big_player['diff'] > 0 ].sort_values(by='diff', ascending=False).reset_index(drop=True)
    accum_winlost = 0
    print(f"{result_big_player_positive['UserName'].values} are top {big_player_limit} winning big player.")
    print(f"{result_big_player_positive['diff'].values} are top {big_player_limit} winning big player's winlost.")

    for i in result_big_player_positive.index:
        accum_winlost += result_big_player_positive.iloc[i]['diff']
        print(f"{i+1} top players account for {((accum_winlost/winning_change)*100).round(2)}% of winlost.")
casino_winning_change = result_product.iloc[1]['Company_Winlost'] - result_product.iloc[0]['Company_Winlost']
games_winning_change = result_product.iloc[5]['Company_Winlost'] - result_product.iloc[4]['Company_Winlost']
sports_winning_change = result_product.iloc[7]['Company_Winlost'] - result_product.iloc[6]['Company_Winlost']
esports_winning_change = result_product.iloc[3]['Company_Winlost'] - result_product.iloc[2]['Company_Winlost']
print(f"Sports winlost last month is {result_product.iloc[6]['Company_Winlost']} compare with this month {result_product.iloc[7]['Company_Winlost']} change {sports_winning_change}.")
print(f"Games winlost last month is {result_product.iloc[4]['Company_Winlost']} compare with this month {result_product.iloc[5]['Company_Winlost']} change {games_winning_change}.")
print(f"Casino winlost last month is {result_product.iloc[0]['Company_Winlost']} compare with this month {result_product.iloc[1]['Company_Winlost']} change {casino_winning_change}.")
print(f"ESport winlost last month is {result_product.iloc[2]['Company_Winlost']} compare with this month {result_product.iloc[3]['Company_Winlost']} change {esports_winning_change}.")
print(f"Sports account for {((sports_winning_change/winning_change)*100).round(2)}% of winlost.")
print(f"Games account for {((games_winning_change/winning_change)*100).round(2)}% of winlost.")
print(f"Casino account for {((casino_winning_change/winning_change)*100).round(2)}% of winlost.")
print(f"ESports account for {((esports_winning_change/winning_change)*100).round(2)}% of winlost.")
#Product Margin Situation
result_product['Margin'] = result_product['Margin'].round(2)
print(f"Sports Winlost change {result_product.iloc[7]['Winlost_PCT_change'].round(2)}%, Turoverover change {result_product.iloc[7]['Turnover_PCT_change'].round(2)}%")
print(f"Sports margin last month is {result_product.iloc[6]['Margin']} compare with this month {result_product.iloc[7]['Margin']} change {(result_product.iloc[7]['Margin']-result_product.iloc[6]['Margin']).round(2)}.")
print(f"Sports margin exclude top & bottom {big_player_limit} big player is {target_product_bp['target_Sport_ex_margin'].iloc[0]['Margin'].round(2)}.")
print(f"Games Winlost change {result_product.iloc[5]['Winlost_PCT_change'].round(2)}%, Turoverover change {result_product.iloc[5]['Turnover_PCT_change'].round(2)}%")
print(f"Games margin last month is {result_product.iloc[4]['Margin']} compare with this month {result_product.iloc[5]['Margin']} change {(result_product.iloc[5]['Margin']-result_product.iloc[4]['Margin']).round(2)}.")
print(f"Games margin exclude top & bottom {big_player_limit} big player is {target_product_bp['target_Game_ex_margin'].iloc[0]['Margin'].round(2)}.")
print(f"Casino Winlost change {result_product.iloc[1]['Winlost_PCT_change'].round(2)}%, Turoverover change {result_product.iloc[1]['Turnover_PCT_change'].round(2)}%")
print(f"Casino margin last month is {result_product.iloc[0]['Margin']} compare with this month {result_product.iloc[1]['Margin']} change {(result_product.iloc[1]['Margin']-result_product.iloc[0]['Margin']).round(2)}.")
print(f"Casino margin exclude top & bottom {big_player_limit} big player is {target_product_bp['target_Casino_ex_margin'].iloc[0]['Margin'].round(2)}.")
print(f"ESport Winlost change {result_product.iloc[3]['Winlost_PCT_change'].round(2)}%, Turoverover change {result_product.iloc[3]['Turnover_PCT_change'].round(2)}%")
print(f"ESport margin last month is {result_product.iloc[2]['Margin']} compare with this month {result_product.iloc[3]['Margin']} change {(result_product.iloc[3]['Margin']-result_product.iloc[2]['Margin']).round(2)}.")
print(f"Esport margin exclude top & bottom {big_player_limit} big player is {target_product_bp['target_ESport_ex_margin'].iloc[0]['Margin'].round(2)}.")

#%%
#Get chart data for slides
target_slides_summary = {}
#1. Active player by Year Month these two years
target_slides_summary['mau'] = vnd_df.groupby(['Year','Month'])['CustId'].nunique().reset_index()
target_slides_summary['mau'] = target_slides_summary['mau'].rename(columns={'CustId':'MAU'})
target_slides_summary['mau'].to_excel(r'C:\Users\ian.chen25\Desktop\Titansoft\PROBATION\0217_VND_Weekly\Weekly Report VND New Sturcture/mau.xlsx', index = None, header=True)

#2. Winning by Year Month these two years
target_slides_summary['winning_turnover'] = vnd_df.groupby(['Year','Month'])['Company_Winlost', 'Company_Turnover'].sum().reset_index()
target_slides_summary['winning_turnover'] = target_slides_summary['winning_turnover'].rename(columns={'Company_Winlost':'Winning'})
target_slides_summary['winning_turnover'] = target_slides_summary['winning_turnover'].rename(columns={'Company_Turnover':'Turnover'})
target_slides_summary['winning_turnover']['Winning'] = target_slides_summary['winning_turnover']['Winning'].round(0).astype(int)
target_slides_summary['winning_turnover']['Turnover'] = target_slides_summary['winning_turnover']['Turnover'].round(0).astype(int)
target_slides_summary['winning_turnover'].to_excel(r'C:\Users\ian.chen25\Desktop\Titansoft\PROBATION\0217_VND_Weekly\Weekly Report VND New Sturcture/winnning_turnover.xlsx', index = None, header=True)

#3. DAU these two months
target_slides_summary['dau'] = vnd_for_dau.groupby(['Year','Month','DayOfMonth'])['CustId'].nunique().reset_index()
target_slides_summary['dau'] = target_slides_summary['dau'][target_slides_summary['dau']['Year'] == 2023]
target_slides_summary['dau'] = target_slides_summary['dau'][target_slides_summary['dau']['Month'].between(2,3)]
target_slides_summary['dau'] = target_slides_summary['dau'].rename(columns={'CustId':'DAU'})
target_slides_summary['dau'].to_excel(r'C:\Users\ian.chen25\Desktop\Titansoft\PROBATION\0217_VND_Weekly\Weekly Report VND New Sturcture/dau.xlsx', index = None, header=True)

#4. MAU by player type these two years
target_slides_summary['mau_player_type'] = vnd_df.groupby(['Type','Year','Month'])['CustId'].nunique().reset_index()
target_slides_summary['mau_player_type'] = target_slides_summary['mau_player_type'].rename(columns={'CustId':'MAU'})
target_slides_summary['mau_player_type'].to_excel(r'C:\Users\ian.chen25\Desktop\Titansoft\PROBATION\0217_VND_Weekly\Weekly Report VND New Sturcture/mau_player_type.xlsx', index = None, header=True)

#5.Winning by product these two years
target_slides_summary['winning_turnover_product'] = vnd_df.groupby(['Product','Year','Month'])['Company_Winlost', 'Company_Turnover'].sum().reset_index()
target_slides_summary['winning_turnover_product'] = target_slides_summary['winning_turnover_product'][target_slides_summary['winning_turnover_product']['Product'] != 'ESport']
target_slides_summary['winning_turnover_product'] = target_slides_summary['winning_turnover_product'].rename(columns={'Company_Winlost':'Winning'})
target_slides_summary['winning_turnover_product'] = target_slides_summary['winning_turnover_product'].rename(columns={'Company_Turnover':'Turnover'})
target_slides_summary['winning_turnover_product']['Winning'] = target_slides_summary['winning_turnover_product']['Winning'].round(0).astype(int)
target_slides_summary['winning_turnover_product']['Turnover'] = target_slides_summary['winning_turnover_product']['Turnover'].round(0).astype(int)
target_slides_summary['winning_turnover_product'].to_excel(r'C:\Users\ian.chen25\Desktop\Titansoft\PROBATION\0217_VND_Weekly\Weekly Report VND New Sturcture/winnning_turnover_product.xlsx', index = None, header=True)

#6. Margin by product these two years
target_slides_summary['product_margin'] = vnd_df.groupby(['Product','Year','Month'])['Company_Winlost','Company_Turnover'].sum().reset_index()
target_slides_summary['product_margin'] = target_slides_summary['product_margin'][target_slides_summary['product_margin']['Product'] != 'ESport']
target_slides_summary['product_margin']['Company_Winlost'] = target_slides_summary['product_margin']['Company_Winlost'].round(2).astype(int)
target_slides_summary['product_margin']['Company_Turnover'] = target_slides_summary['product_margin']['Company_Turnover'].round(2).astype(int)
target_slides_summary['product_margin']['Winlost_PCT_change'] = target_slides_summary['product_margin']['Company_Winlost'].pct_change().round(4)*100
target_slides_summary['product_margin']['Turnover_PCT_change'] = target_slides_summary['product_margin']['Company_Turnover'].pct_change().round(4)*100
target_slides_summary['product_margin']['Margin'] = (target_slides_summary['product_margin']['Company_Winlost'] / target_slides_summary['product_margin']['Company_Turnover']).round(3)*100
target_slides_summary['product_margin'] = target_slides_summary['product_margin'].reset_index(drop=True)
target_slides_summary['product_margin'].to_excel(r'C:\Users\ian.chen25\Desktop\Titansoft\PROBATION\0217_VND_Weekly\Weekly Report VND New Sturcture/product_margin.xlsx', index = None, header=True)


















