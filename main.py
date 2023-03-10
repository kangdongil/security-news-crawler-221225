from time import time
from datetime import datetime
import urllib3
from urllib.parse import urlparse, parse_qs
import requests
from bs4 import BeautifulSoup


base_url = "https://www.boannews.com/media"

start = time()
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
response = requests.get(f"{base_url}/list.asp?mkind=1", verify=False)


soup = BeautifulSoup(response.text, "html.parser")
news = soup.find("div", id="news_area").find_all("div", class_="news_list")
end = time()
results = []
n = 0
for new in news:
    anchor = new.find("a")
    idx = parse_qs(urlparse(anchor["href"]).query)["idx"][0]
    title = anchor.text.strip()
    writer, pub_date = new.find("span", class_="news_writer").text.split(" | ")
    pub_date = datetime.strptime(pub_date, "%Y년 %m월 %d일 %H:%M")

    post_response = requests.get(f"{base_url}/view.asp?idx={idx}", verify=False)
    post_soup = BeautifulSoup(post_response.text, "html.parser")
    news_content = post_soup.find("div", id="news_content")
    content = news_content.text
    new_data = {
        "idx": idx,
        "link": f"{base_url}/view.asp?idx={idx}",
        "title": title,
        "writer": writer.replace(" 기자", ""),
        "pub_date": pub_date.strftime("%Y-%m-%d %H:%M"),
        "content": content,
    }

    results.append(new_data)
    print(n)
    n += 1

for result in results:
    print(result, sep="\n\n")
print(f"{end - start:.4f}초")
