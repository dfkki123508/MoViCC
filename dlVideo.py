import bs4 # unbenutzt
import requests
import pafy
from bs4 import BeautifulSoup

def get_search_url(keywords):
    search_url = "https://www.youtube.com/results?q="
    cc_filter = "&sp=EgIwAVAU"

    # das ganze kann verkürzt werden in einer Zeile:
    # search_url += '+'.join(keywords) + cc_filter
    for keyword in keywords:
        search_url = search_url + keyword  # += ist kürzer
        if keyword is not keywords[len(keywords)-1]:  # letzter Eintrag? Syntax: keywords[-1]
            search_url = search_url + "+"
    search_url = search_url + cc_filter
    print(search_url)
    return search_url

def get_video_links(url):
    html = requests.get(url)
    soup = BeautifulSoup(html.text, 'html.parser')
    a_tags = soup.find_all('a')

    # kürzer: links = [link['href] for link in a_tags if link['href'].startswith('/watch')]
    links = []
    for link in a_tags:
        if link['href'].startswith('/watch'):
            links.append(link['href'])
    print(links)
    return links

def get_download_metadata(link, save_path):
    url = "https://www.youtube.com"+link
    youtube = pafy.new(url)
    author = youtube.author

    video = youtube.getbest(preftype="mp4")
    video.download(quiet=False, filepath=save_path)

    # wieso noch extra parsen?
    # nach dem neusten PEP soll nur noch .format verwendet werden:
    # "{}: {}".format(author, url)
    cc_reference = str("%s: %s" % (author, url))
    #print(cc_reference)
    return cc_reference
