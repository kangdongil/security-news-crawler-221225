from datetime import datetime
from urllib.parse import urlparse, parse_qs
from selenium import webdriver
from bs4 import BeautifulSoup
from config.options import options

base_url = "https://www.boannews.com/media"

browser = webdriver.Chrome(options=options)

browser.get(f"{base_url}/list.asp?mkind=1")
soup = BeautifulSoup(browser.page_source, "html.parser")
news = soup.find("div", id="news_area").find_all("div", class_="news_list")
results = []
for new in news:
    anchor = new.find("a")
    idx = parse_qs(urlparse(anchor["href"]).query)["idx"][0]
    title = anchor.text.strip()
    writer, pub_date = new.find("span", class_="news_writer").text.split(" | ")
    pub_date = datetime.strptime(pub_date, "%Y년 %m월 %d일 %H:%M")
    new_data = {
        "idx": idx,
        "link": f"{base_url}/view.asp?idx={idx}",
        "writer": writer.replace(" 기자", ""),
        "pub_date": pub_date.strftime("%Y-%m-%d %H:%M"),
    }
    results.append(new_data)
    print(results)
