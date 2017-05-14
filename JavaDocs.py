#This is a JavaDoc crawler for methods
#For Example:
#Input = "String indexOf"(without quotes)
#Output = (All links of String.indexOf)

from bs4 import BeautifulSoup
import requests, re, webbrowser,urllib.request
url = 'https://docs.oracle.com/javase/8/docs/api/allclasses-noframe.html'
res = requests.get(url)
flag = False
soup = BeautifulSoup(res.text)
text = ""
print("ClassName MethodName")
inp = input()
flag2 = False
search = inp.split(" ")[0]
methodName = inp.split(" ")[1]
for i in soup.select("a"):
    text = url.replace("allclasses-noframe.html", "") + i["href"]
    m = re.match(".*/(.*)", text)
    if m:

        if str(m.groups()[0]).replace("_", "").replace(".html", "") == search:
            flag = True
            break
if flag:
    f = urllib.request.urlopen(text)
    sp = BeautifulSoup(f)
    for i in sp.select("a"):
        if i.text == methodName:
            flag2 = True
            print("https://docs.oracle.com/javase/8/docs/api/" + i["href"].replace("../", ""))
    if not flag2:
        print("Method Not Found")
else:
    print("Class Not Found")
