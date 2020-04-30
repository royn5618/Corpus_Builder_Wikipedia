# Corpus_Builder_Wikipedia

This repository is set-up to scrape wikipedia articles. This code leverages the python libraries [Wikipedia](https://pypi.org/project/wikipedia/) and [Beautiful Soup](https://pypi.org/project/beautifulsoup4/) to scrape Wikipedia page contents.

## How to use:

```-topic=<str> -level=<int> -folder=<str>```

-topic : The topic you want to be searched

-level: Level is explained below.

-folder : Storage Folder Name

### What is Level?

This code searches the topic, gets related pages and scrapes them. At level 1, it stops here. If level is 2, it gets the links in these pages and scrapes them as well. Basically, level is the number of times embedded links in the Wikipedia pages will be scraped.

###Samples:

A sample scrape result is provided in the Sample folder.
