from psutil import users
import requests
from bs4 import BeautifulSoup
import time 
from random import randint
import pandas as pd

############## UNIVERSAL FUNCTIONS ##############

def get_soup(url): #fungsi#
    page = requests.get(url) #page melakukan request untuk mengunjungi page pada url
    soup = BeautifulSoup(page.content) #melakukan scrape pada page melalui fungsi bs
    return soup

############## END OF UNIVERSAL FUNCTIONS ##############

df_link = {
  'companyName': [],
  'numberOfAnime': [],
  'Favorites' : [],
  'animeName': [],
  'animeRate': [],
  'member': []

}

source = 'https://myanimelist.net/company'
soup = get_soup(source)

link_StudioName=[]
companyName=[]
numberOfAnime=[]
list_Favorites=[]
animeName=[]
animeRate=[]
members=[]

studiolist = soup.find_all('td', {'class': 'company'}) #scrape tag td dengan class 'people'
for a in studiolist:
    CompanyHref = a.findChild('a', {'class':'fs14 fw-b'})#scrape tag a dengan class 'fs14 fw-b' atau nama dan tautan
    if CompanyHref is None: #
        continue
    print(CompanyHref) #menunjukkan hasil CompanyHref
    LinkOfStudio = CompanyHref.get('href')# mengambil tag href dari CompanyHref
    if LinkOfStudio == "/anime/producer/1993/Studio_Bind":
        continue
    if LinkOfStudio == "/anime/producer/405/T-Rex":
        continue
    if LinkOfStudio == "/anime/producer/45/Pink_Pineapple":
        continue
    myanimelist = "https://myanimelist.net"
    linkFix =  myanimelist+LinkOfStudio
    print(linkFix)
    link_StudioName.append(linkFix)
    
    soup2 = get_soup(linkFix)
    studioName = soup2.findChild('h1', {'class':'h1'}).getText()
    companyName.append(studioName)
    print(studioName)
    
    favorites=soup2.find_all('span', {'class':'dark_text'})
    favo = favorites[2].getText().split(' ')[-2]
    list_Favorites.append(favo)
    print(favo)

    NameOfAnime = soup2.find_all('div', {'class':'title'})
    for i in NameOfAnime:
        name = i.getText().split('\n')[1]
        animeName.append(name)
        print(name)
        animenumb = len(NameOfAnime)
        print (animenumb)
        numberOfAnime.append(animenumb)
   
    RateOfAnime = soup2.find_all('div', {'class':'stars'})
    for i in RateOfAnime:
       rate = i.getText()
       if rate == "N/A":
           rate = 0
           print(rate)
           animeRate.append(rate)
       else:
           print(rate)
           animeRate.append(rate)

    MemberOfAnime = soup2.find_all('div', {'class':'users'})
    for i in MemberOfAnime:
        member = i.getText()
        members.append(member)
        print(member)


   #menjadikan class ini sebagai parameter studio animasi

df_link['companyName'] = companyName
df_link['numberOfAnime'] = numberOfAnime
df_link['Favorites'] =  list_Favorites
df_link['animeName'] = animeName
df_link['animeRate'] = animeRate
df_link['member'] = members

df_link = pd.DataFrame(df_link)
df_link.to_csv('AnimeListCoba.csv', index=False)