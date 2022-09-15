import requests
from datetime import datetime
from pprint import pprint
import subprocess



def economist_article_scraper():

    url = "https://www.economist.com/"
    # Pull html of homepage
    result = requests.get(url)
    result = result.text

    # Split up the html so that the start of each string is the links on the front page
    split_htmls = result.split(url)

    # Clean up
    all_urls = [url + split_html.split('"')[0] for split_html in split_htmls]

    # Filter for only article urls (those with dates in them)
    articles = list(set(filter(lambda x: '/2022/' in x, all_urls)))

    # Now we will format each article so that we can arrange them by date and section
    formatted_articles = []
    for article_url in articles:
        # Raw html for article page
        an_article = requests.get(article_url).text

        # Format out the date, section from url
        splitted_data = article_url.split('/')
        section = splitted_data[3]
        date = datetime.strptime(splitted_data[4] + splitted_data[5] + splitted_data[6], '%Y%m%d')

        article_title = an_article.split('"title":')[1].split('"')[1].split('|')[0]
        section = section.split('-')
        if len(section) > 1:
            temp_string = ''
            for a_word in section:
                temp_string += a_word.capitalize() + ' '
            section = temp_string
        else:
            section = section[0].capitalize()

        print('scraped: ', section, article_title, article_url)

        # Pull out article body incase we need it (?)
        article_body = an_article.split('"articleBody":"')[1].split('"')[0]

        # Aggregate into dict
        article_data = {
            'body': article_body,
            'title': article_title,
            'section': section,
            'date': date,
        }

        formatted_articles.append(article_data)

    exit()

    test_url = articles[0]
    print(len(articles))
    print(test_url)
    test = requests.get(test_url)
    print(test.text.split('"title":"')[1].split(' | ')[0])
    # test_html = test.text.split('"articleBody":"')[1].split('"')[0]
    # print(test_html)
    # download_webpage_cmd = 'wget --no-parent --mirror -p --html-extension --convert-links -e robots=off -P . ' + test_url
    # delete_js_cmd = "find . -type f -name _app*.js -delete"
    # ready_articles = "find . -type f -name *.html"
    # list_of_files = subprocess.Popen(ready_articles.split(), stdout=subprocess.PIPE).communicate()[0]
    # print(list_of_files)
    # exit()
    # for cmd in (download_webpage_cmd, delete_js_cmd):
    #     list_of_files = subprocess.Popen(ready_articles.split(), stdout=subprocess.PIPE).communicate()[0]
    #     subprocess.run(cmd.split())

if __name__ == '__main__':
    economist_article_scraper()
