# Program for Renaming Friends Episodes
# This Program gets the Episodes name from imdb, and renames the ones present on your computer. 
# This Program expects The Episode to already be in order, and just need to get the proper names.
import re,os
import requests
from bs4 import BeautifulSoup

for x in range(1,11):
    url = "http://www.imdb.com/title/tt0108778/episodes?season=" + str(x) + "&ref_=tt_eps_sn_" + str(x)
    soup = BeautifulSoup(requests.get(url).text)
    path = r"F:/TV Shows/Friends/S0" + str(x) + "/"
    if x == 10:
        path = r"F:/TV Shows/Friends/S" + str(x) + "/"
    ep = 0
    for i in soup.find_all('strong'):
        ep+=1
        if str(i).startswith("<strong>Season"):
            break
        else:
            f = str(i).replace("<strong>", "")
            f = str(f).replace("</strong>", "")
            m = re.search('.*title="(.*?)"', f)
            print(m.groups()[0])
            if m:
                r = path + "1 (" + str(ep) + ").mkv"
                os.rename(r, path + str(ep) + " ." + str(m.groups()[0]).replace(":", "").replace("...", "").replace(".","") + ".mkv")
