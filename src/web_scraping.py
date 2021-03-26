from bs4 import BeautifulSoup
import requests
import custom_func as cf
import pandas as pd
from tqdm import tqdm

path_references = "..\\references\\"
list_businesses = cf.load_obj("businesses_api", path_references)

user_agent = (
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US;"
    " rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7"
)
headers = {
    "User-Agent": user_agent,
}

for b in tqdm(range(0, len(list_businesses))):
    url = list_businesses[b]["url"]

    # Schedule
    while True:
        try:
            response = requests.get(url, headers=headers)
            html = response.content
            html_list = pd.read_html(html)
            break
        except ValueError as e:
            if str(e) == "No tables found":
                pass
            elif str(e) == "No tables found matching pattern '.+'":
                break
    if html_list:
        df_schedule = html_list[0].rename(columns={0: "day", 1: "time"})
        del df_schedule[2]
        list_businesses[b]["schedule"] = df_schedule

    # Offer delivery
    soup = BeautifulSoup(html, "html.parser")
    sections = soup.find_all("section")
    spans = sections[0].find_all("span")
    list_businesses[b]["delivery"] = "no"
    if spans:
        if spans[0].get_text() == "Updated services":
            for i in range(0, len(spans)):
                if spans[i].get_text() == "Delivery":
                    list_businesses[b]["delivery"] = "yes"
                    continue

cf.save_obj(list_businesses, "businesses_updated", "..\\references\\")
