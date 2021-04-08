from bs4 import BeautifulSoup
import requests

#use snake_case for naming functions and variables
def scrape_categories():
    source = requests.get("https://www.transtutors.com/").text
    soup = BeautifulSoup(source, "lxml")
    article = soup.find("div", class_="subjectcovered")
    attr = {}               # Don't use name of data structures in variables
                            # Use Blank line to separate new logic block
    
    """
    Dictionary comprehension can be used to perform this task,
    but for better readability standard for loop would be better
    """
    attr = {category.find("div", class_="subject").text: 
            f"https://www.transtutors.com{category.find_all('a')[-1]['href']}" 
            for category in article.find_all("li")}

    # for category in article.find_all("li"):
    #     name = category.find("div", class_="subject").text
    #     link = category.find_all("a")[-1]["href"]
    #     ttlink = f"https://www.transtutors.com{link}"
    #     attr[name] = ttlink

    print(attr)


def main():
    scrape_categories()


if __name__ == "__main__":
    main()