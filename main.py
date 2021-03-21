import requests
from bs4 import BeautifulSoup
from IPython.display import Image, display

URL_SITE = "https://www.biobiochile.cl"


def get_soup(url: str) -> BeautifulSoup:
    response = requests.get(url)
    return BeautifulSoup(response.text, "lxml")


def get_full_url(link: str) -> str:
    return link if link.find("https") != -1 else URL_SITE + link


def get_sections(soup: BeautifulSoup) -> list[str]:
    link_sections = soup.find("div", attrs={"class": "nav-container"}) \
        .find("ul", attrs={"class": "categories-nav"}) \
        .find_all("a", attrs={"class": "nav-link"})
    return [get_full_url(link.get("href")) for link in link_sections]


def get_sub_sections(sections: list[str]):
    links = []
    for section_url in sections:
        soup = get_soup(section_url)
        articles = soup.find_all("div", attrs={"class": "article-text-container"})
        for article in articles:
            aTag = article.find("a")
            if aTag is not None and aTag.get("href") is not None and aTag.get("href").find("https") != -1:
                links.append(aTag.get("href"))
    return links

def get_metadata(link: str):
    soup = get_soup(link)
    title = soup.find("h1", attrs={"class": "post-title"}).text.strip()
    author = soup.find("span", attrs={"class": "autor"}).find("a").text
    create_at = soup.find("div", attrs={"class": "post-date"}).text

    return {
        "title": title,
        "author": author,
        "create_at": create_at
    }

def get_iamges(link: str):
    soup = get_soup(link)
    image = soup.find("figure").find("img")
    if image is not None:
        img_req = requests.get(image.get("src"))
        return Image(img_req)
    return None

soup = get_soup(URL_SITE)
links = get_sections(soup)
links_sub_sections = get_sub_sections(links)
author_data = get_metadata(links_sub_sections[0])
img = get_iamges(links_sub_sections[0])
