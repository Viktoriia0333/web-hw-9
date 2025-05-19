import requests
from bs4 import BeautifulSoup
import json
from time import sleep

BASE_URL = "http://quotes.toscrape.com"
quotes = []
authors_data = {}
visited_authors = set()


def get_author_details(author_url):
    url = BASE_URL + author_url
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    fullname = soup.find("h3", class_="author-title").text.strip()
    born_date = soup.find("span", class_="author-born-date").text.strip()
    born_location = soup.find("span", class_="author-born-location").text.strip()
    description = soup.find("div", class_="author-description").text.strip()

    return {
        "fullname": fullname,
        "born_date": born_date,
        "born_location": born_location,
        "description": description
    }


def scrape():
    page = 1
    while True:
        url = f"{BASE_URL}/page/{page}/"
        response = requests.get(url)
        if "No quotes found!" in response.text:
            break

        soup = BeautifulSoup(response.text, "html.parser")
        quote_elements = soup.find_all("div", class_="quote")

        for quote_element in quote_elements:
            text = quote_element.find("span", class_="text").text.strip()
            author_name = quote_element.find("small", class_="author").text.strip()
            tags = [tag.text for tag in quote_element.find_all("a", class_="tag")]

            quotes.append({
                "tags": tags,
                "author": author_name,
                "quote": text
            })

            author_link = quote_element.find("a")["href"]
            if author_link not in visited_authors:
                visited_authors.add(author_link)
                author_info = get_author_details(author_link)
                authors_data[author_info["fullname"]] = author_info

        print(f"Page {page} done")
        page += 1
        sleep(0.5)

    with open("quotes.json", "w", encoding="utf-8") as f:
        json.dump(quotes, f, ensure_ascii=False, indent=2)

    with open("authors.json", "w", encoding="utf-8") as f:
        json.dump(list(authors_data.values()), f, ensure_ascii=False, indent=2)

    print("Done! quotes.json and authors.json are saved.")


if __name__ == "__main__":
    scrape()

