import re
from urllib.parse import urljoin

## -- Task 2 -- ##


def find_urls(
    html: str,
    base_url: str = "https://en.wikipedia.org",
    output: str = None,
) -> set:
    """Find all the url links in a html text using regex
    Arguments:
        html (str): html string to parse
    Returns:
        urls (set) : set with all the urls found in html text
    """
    # create and compile regular expression(s) 

    urls = re.compile(r"<a\s+[^>]+>", flags=re.IGNORECASE)
    # 1. find all the anchor tags, then
    # 2. find the urls href attributes
    href_pat = re.compile(r'href="([^"]+)"|(?:href="([^"]+)")', flags=re.IGNORECASE)
    href_set = set()
    for url in urls.findall(html):
        match = href_pat.search(url)
        if match:
            if re.search('^/', match.group(1)):
                if re.search('\?', match.group(1)) or re.search('\(', match.group(1)):
                    match3 = base_url + match.group(1)
                    href_set.add(match3)
                else:
                    href_set.add(re.sub(match.group(1), (base_url+match.group(1)),match.group(1)))
            elif re.search('#', match.group(1)):
                match2 = re.search('#', match.group(1))
                if len(match.group(1)[:match2.start()])!= 0:
                    href_set.add(match.group(1)[:match2.start()])
            else:
                href_set.add(match.group(1))
    # Write to file if requested
    if output:
        print(f"Writing to: {output}")
        f = open(output, "w")
        for i in href_set:
            f.write(str(i))
            f.write('\n')
        f.close()
    return href_set


def find_articles(html: str, output:str = None) -> set:
    """Finds all the wiki articles inside a html text. Make call to find urls, and filter
    arguments:
        - text (str) : the html text to parse
    returns:
        - (set) : a set with urls to all the articles found
    """
    urls = find_urls(html)
    pattern = re.compile(pattern = r'^https?:\/\/[a-z]{2}\.wikipedia\.[a-z]{2,3}/wiki/[^:]+$', flags=re.IGNORECASE)
    articles = set()
    for url in urls:
        match = pattern.search(url)
        if match:
            articles.add(match.group(0))
        
    # Write to file if wanted
    if output:
        print(f"Writing to: {output}")
        f = open(output, "w")
        for i in articles:
            f.write(str(i))
            f.write('\n')
        f.close()
    return articles


## Regex example
def find_img_src(html: str):
    """Find all src attributes of img tags in an HTML string

    Args:
        html (str): A string containing some HTML.

    Returns:
        src_set (set): A set of strings containing image URLs

    The set contains every found src attibute of an img tag in the given HTML.
    """
    # img_pat finds all the <img alt="..." src="..."> snippets
    # this finds <img and collects everything up to the closing '>'
    img_pat = re.compile(r"<img[^>]+>", flags=re.IGNORECASE)
    # src finds the text between quotes of the `src` attribute
    src_pat = re.compile(r'src="([^"]+)"', flags=re.IGNORECASE)
    src_set = set()
    # first, find all the img tags
    for img_tag in img_pat.findall(html):
        # then, find the src attribute of the img, if any
        match = src_pat.search(img_tag)
        if match:
            src_set.add(match.group(1))
    return src_set
