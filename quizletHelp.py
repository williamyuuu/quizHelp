import requests
from bs4 import BeautifulSoup
import re

headers = {"User-Agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'}

def readFrom(filename):
    f = open(filename + ".html", "r")
    return f.read()

def writeTo(filename, input):
    f = open(filename + ".txt", "w")
    f.write(input)
    f.close()


def search(query):
    # print(f"finding query of {query}")
    try:
        from googlesearch import search
    except ImportError:
        print("No module named 'google' found")

        # to search

    for j in search(query + " quizlet", tld="com", num=1, stop=1, pause=2):
        return j

def find_answer(URL, query):
    # print(f"finding answer for {query} at {URL}")

    page = requests.get(URL, headers=headers)
    soup = BeautifulSoup(page.content, "html.parser")
    soup = BeautifulSoup(soup.prettify(), "html.parser")
    #print(soup)

    for i in range(len((soup.findAll("div", {"class": "SetPageTerms-term"})))):
        text = (soup.findAll("div", {"class": "SetPageTerms-term"})[i]).text
        text = re.sub(r"\n", "", text)
        text = re.sub(r"\s{3,}", " || ", text.strip())
        # print(query)

        # print(text)
        x = re.search(query, text, re.IGNORECASE)
        if x:
            print(text)

def one():
    query = input("Enter question: ")
    find_question = ' '.join(query.split()[2:5])
    url = search(query)
    find_answer(url, find_question)

def main():
    source = readFrom("quiz")
    soup = BeautifulSoup(source, "html.parser")

    for x in range(10):
        info = (soup.findAll("textarea", {"name": "question_text"})[x]).text
        info = re.sub(r"<.*?>", "", info)
        query = info
        find_question = ' '.join(query.split()[2:5])
        # print("main question", x)
        url = search(query)
        find_answer(url, find_question)


if __name__ == "__main__":
    #main()
    one()
