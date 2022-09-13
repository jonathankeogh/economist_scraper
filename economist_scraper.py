import requests
from datetime import datetime
from pprint import pprint
import subprocess

url = "https://www.economist.com/"
# get html
result = requests.get(url)
# to string
result = result.text
# split along where economist url is
split_htmls = result.split(url)
# cutoff junk html at end and make full html
urls = [url + split_html.split('"')[0] for split_html in split_htmls]
# Filter for only article urls
articles = list(set(filter(lambda x: '/2022/' in x, urls)))

test_url = articles[0]
print(len(articles))
print(test_url)
test = requests.get(test_url)
test_html = test.text.split('"articleBody":"')[1].split('"')[0]
print(test_html)
download_webpage_cmd = 'wget --no-parent --mirror -p --html-extension --convert-links -e robots=off -P . ' + test_url
delete_js_cmd = "find . -type f -name _app*.js -delete"
for cmd in (download_webpage_cmd, delete_js_cmd):
    subprocess.run(cmd.split())


