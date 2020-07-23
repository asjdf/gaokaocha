import requests
import bs4

r = requests.get("http://gk.eeafj.cn/jsp/scores/gkcj/scores_enter.jsp")
soup = bs4.BeautifulSoup(r.content.decode("utf-8"))
print(r)
print(soup.find(id="findbtn")["value"])