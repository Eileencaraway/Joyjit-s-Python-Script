import urllib
from BeautifulSoup import *

url=raw_input("Enter the url-")
html=urllib.urlopen(url).read()
soup=BeautifulSoup(html)

tags=soup('span')
summ=list()
for tag in tags:
    a= tag.contents[0]
    summ.append(int(a))

print sum(summ)
