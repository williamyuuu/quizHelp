import requests
from bs4 import BeautifulSoup
import re
from termcolor import colored


headers = {"User-Agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'}


# reads HTML file, used to read source_page.html
def readFrom(filename):
    f = open(filename + ".html", "r")
    return f.read()


# googles query for quizlet url and returns first link
def search(query):
    try:
        from googlesearch import search
    except ImportError:
        print("No module named 'google' found")

    for j in search(query + " quizlet", tld="com", num=1, stop=1, pause=2):
        return j


# purge articles and punctuations
def purge(word):
    word = re.sub(r"\bthe\b", "", word, flags=re.IGNORECASE)
    word = re.sub(r"\ba\b", "", word, flags=re.IGNORECASE)
    word = re.sub(r"\ban\b", "", word, flags=re.IGNORECASE)
    word = re.sub(r"\.", "", word)
    word = re.sub(r",", "", word)
    word = re.sub(r"!", "", word)
    word = re.sub(r"\?", "", word)
    word = re.sub(r"-", " ", word)

    return word


# searches for the best match to your query and returns
def find_best_match(query, text, high, output):
    query = purge(query)
    text_purged = purge(text)
    query_list = query.split()

    count = 0
    # searches individual words from query to quizlet page
    for x in range(len(query_list)):
        ans = re.search(query_list[x], text_purged, re.IGNORECASE)

        # adds one match if individual word matches quizlet question
        if ans:
            count = count + 1

    # if quizlet question matches query better, replaces the best match output
    if count > high:
        high = count
        output = text

    # returns the best match info
    return high, output


# formats output by splitting answer from question displayed on quizlet page
def display_f_output(output, query, x):

    output = re.sub(r"\s{2,}", " || ", output.strip())
    quizlet = output.split("||")
    answer = colored(quizlet[1], "green", attrs=["bold"])
    question = quizlet[0].split()

    # match question portion to query, unmatched will be colored red
    for i in range(len(question)):
        ans = re.search(question[i], query, re.IGNORECASE)

        # if not match, makes it red
        if not ans:
            question[i] = colored(question[i], "red", attrs=["underline"])

    # combine the output and display
    question = " ".join(question)
    print(f"{[x+1]} {question} : {answer}")


# finds quizlet questions in url and matches to query
def find_answer(url, query, x):
    page = requests.get(url, headers=headers)
    page = re.sub(r"<br>", "", str(page.content))
    soup = BeautifulSoup(page, "html.parser")
    soup = BeautifulSoup(soup.prettify(), "html.parser")

    high = 0
    output = ""

    # searches all the questions on quizlet page, returns best output
    for i in range(len((soup.findAll("div", {"class": "SetPageTerms-term"})))):
        text = (soup.findAll("div", {"class": "SetPageTerms-term"})[i]).text
        text = re.sub(r"\n", "", text)
        text = re.sub(r"\\", "", text)
        high, output = find_best_match(query, text, high, output)

    display_f_output(output, query, x)


# type in query option
def type_in():
    max = input("How many questions:")
    for x in range(int(max)):
        query = input("Enter question: ")
        url = search(query)
        find_answer(url, query, x)


# reads off source_page.html for queries
def source():
    source = readFrom("source_page")
    soup = BeautifulSoup(source, "html.parser")

    for x in range(10):
        query = (soup.findAll("textarea", {"name": "question_text"})[x]).text
        url = search(query)
        find_answer(url, query, x)


if __name__ == "__main__":
    answer = input("input or source:")

    if answer == "input":
        type_in()
    elif answer == "source":
        source()
    else:
        # example of colored terminal print
        print(colored("unidentified", "red"))
