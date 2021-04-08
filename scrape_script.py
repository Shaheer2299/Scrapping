from bs4 import BeautifulSoup
import requests

source = requests.get("https://www.transtutors.com/").text

soup = BeautifulSoup(source, "lxml")


article = soup.find("div", class_="subjectcovered")

Dict = {}
for category in article.find_all("li"):

    name = category.find("div", class_="subject").text

    link = category.find_all("a")[-1]["href"]
    ttlink = f"https://www.transtutors.com{link}"
    Dict[name] = ttlink


print(Dict)