# Assignment 4: Web scraping
In this assignment we will start by working with some regular expression to analyse a text (task 1-4) then we will switch to BeatifulSoup (task 5-10).



### requesting_urls
Sending HTTP reguests:

```python
  $ python3 requesting_urls.py
```
The text can be found in output.txt


### filter_urls
Here we use regular expression to get urls, articles and images from a given html file.
Run:
 ```python
  $ python3 filter_urls.py 
 ```
The resulting clean urls and articles can be found in url.txt and articles.txt respectively.
r"<a\s+[^>]+>" is used to pick out the a tags.
r'href="([^"]+)" is used to pick out the urls.
using '^/' all the relative urls are identified. But while trying to attach the base_url to them I realised for some it does not work. It was the urls with () and ?. I had to attach them separately. I guess the reason for it is because ? and () are signs that have assigned meaning in regular expression.
Then # was clipped.

### collect_dates
In this part, all dates are extracted and returned in a desired format.
Run: 
  
```python
  $ python3 collect_dates.py
``` 
The result can be found in dates.txt
To be able to work with ISO data I returned it separately. It would not work otherwise.
For some reason the suggested method in the assignment4 did not work for me: match = re.sub(rf"({day})\s({month})\s({year})", r"\3/\2/\1", match)
I had to write my own method.

### time_planner
At this part, urls were given and the required data was extracted, put into dataframe and turned to markdown.
Run:
```python
$ python3 time_planner.py
```
### fetch_player_statistics
Using the url of an html page, we extrancted urls for 8 basketball teams and using those urls we found each players personal page and their stats.
```python
$ python3 fetch_player_statistics.py
```
The plots can be found in the folder *NBA_player_statistics*
in find_best_players I used None_points = {"points" : 0.0} to add to those that do not have a data for points. I also had to check again for the existance of page with a table with (ID = Regular_season) because some of the player‘s pages did not have a Regular session table.
os.mkdir(stats_dir) is commented out because after creating the folder for the first time error: directory already exist.
I added the plot_NBA_player_statistics function with some modifications and did not use the plot_best function. They are the same.

## Instalation:
cd into root directory (assignment4 in this case)
To access html body we need to be able to make a request for the html body:
```python
python3 -m pip install requests
```
To be able to use BeautifulSoup:
```python
python3 -m pip install beautifulsoup4
```
Then they can be imported as followed:
```python
from bs4 import BeautifulSoup
import requests
```

### test:
install pytest:
python3 -m pytest -v test/test_package.py
test:
$ pytest

