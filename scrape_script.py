import os
from tqdm import tqdm
import pandas as pd
from bs4 import BeautifulSoup
import requests


def scrape_categories():
    source = requests.get("https://www.transtutors.com/").text
    soup = BeautifulSoup(source, "lxml")
    article = soup.find("div", class_="subjectcovered")
    attr = {}

    attr = {
        category.find(
            "div", class_="subject"
        ).text: f"https://www.transtutors.com{category.find_all('a')[-1]['href']}"
        for category in article.find_all("li")
    }
    return attr


def scrape_question(categ, page_link):

    source = requests.get(page_link).text
    soup = BeautifulSoup(source, "lxml")

    check_pages = soup.find("div", class_="prevnxt")
    last_page = check_pages.find("a", class_="nxt")["href"]
    total_pages = last_page.split("/")[-2]

    for i in range(int(total_pages)+1):
        source = requests.get(page_link+str(i)).text
        soup = BeautifulSoup(source, "lxml")
        questions = soup.find("ul", class_="inner-topics-covered")
        lt = []

        for li in tqdm(questions.find_all("li")):
            attr = {}
            link = li.find("a")["href"]
            q_page = requests.get(link).text
            soup1 = BeautifulSoup(q_page, "lxml")
            q_box = soup1.find("div", class_="question-box")
            attr["Category"] = categ
            attr["Date"] = q_box.find("div", class_="postedDate").text.strip()
            attr["Question"] = q_box.find(
                "div", class_="discription").text.strip()
            lt.append(attr)

        df = pd.DataFrame(lt)
        if os.path.isfile('data.csv'):
            df.to_csv("data.csv", index=False, mode='a', header=False, encoding="UTF-8")
        else:
            df.to_csv("data.csv", index=False, encoding="UTF-8")


def main():
    attr = scrape_categories()

    for key in attr:
        scrape_question(key, attr[key])


if __name__ == "__main__":
    main()
