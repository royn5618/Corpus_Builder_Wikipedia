import wikipedia
import argparse
import os
import datetime
from bs4 import BeautifulSoup
from mediawikiapi import MediaWikiAPI
import logging


def main(topic, level, folder_name, logger):
    """
    Function to get content and store in txt file.
    :param folder_name: Name of the folder in which the contents will be stored
    :param topic: Keywords to find pages related to it
    :param level: no of levels to get contents of links
    level 1 (Page A) - Scrape everything - Doesn't visit any link
    level 2 (Page A) - Scrapes everything, gets the links on the page and scrapes the contents of those links

    :return: None
    """
    list_pages = wikipedia.search(topic)
    for i in range(0, level):
        if level > 1 and level != i-1:
            list_pages = create_content(list_pages, folder_name, links_req=True)
        else:
            create_content(list_pages, folder_name, links_req=False)
    logger.info("Process finished at: " + datetime.datetime.now().strftime("%d.%b %Y %H:%M:%S"))


def create_content(list_pages, folder_name, links_req):
    all_links = []
    seen_pages = []
    try:
        seen_pages = os.listdir(folder_name + '/')
    except FileNotFoundError as e:
        logger.info("Novel Scrape")
    for each_page in list_pages:
        try:
            page_wiki_obj = wikipedia.page(each_page)
            if each_page + ".txt" not in seen_pages:
                content = page_wiki_obj.content
                table_contents = get_table_contents(each_page)
                write_to_txt(each_page, content, table_contents, folder_name)
            else:
                logger.info("Seen: " + each_page + ".txt")
            if links_req:
                all_links.append(page_wiki_obj.links)
        except Exception as e:
            logger.error(each_page)
            logger.error(e)
    if links_req and all_links:
        return [each_link for list_of_links in all_links for each_link in list_of_links]
    else:
        return None


def get_table_contents(wiki_page):
    # load page
    mediawikiapi = MediaWikiAPI()
    test_page = mediawikiapi.page(wiki_page)

    # scrape the HTML with BeautifulSoup to find tables
    soup = BeautifulSoup(test_page.html(), 'html.parser')
    tables = soup.findAll("table", {"class": "wikitable"})
    # select target table and apply custom function to export it to pandas
    table_contents = None
    if tables:
        for i in range(0, len(tables)):
            if table_contents:
                table_contents = table_contents + "== Table: " + str(i) + " ==" + "\n"
            else:
                table_contents = "== Table: " + str(i) + " ==" + "\n"
            headers = [th.text.encode("utf-8").decode('utf-8') for th in tables[i].select("tr th")]
            header = ",".join(headers)
            table_contents = table_contents + str(header)
            table_contents = table_contents + '\n'
            for row in tables[0].select("tr + tr"):
                for td in row.find_all("td"):
                    if td.a:
                        try:
                            table_contents = table_contents + td.a['title'] + ","
                        except KeyError as e:
                            pass
                        table_contents = table_contents + str(td.text.encode("utf-8").decode('utf-8')) + ","
                        continue
                    else:
                        table_contents = table_contents + str(td.text.encode("utf-8").decode('utf-8')) + ","
                table_contents = table_contents + '\n'
            table_contents = table_contents + "==============="
    return table_contents


def write_to_txt(page_name, content_to_write, table_content_to_write, folder_name):
    os.makedirs(folder_name, exist_ok=True)
    with open(folder_name + "/" + page_name + '.txt', "w", encoding="utf-8") as text_file:
        text_file.write(content_to_write)
        if table_content_to_write:
            text_file.write("\n")
            text_file.write("\n")
            text_file.write(table_content_to_write)
    logger.info("Content created in folder {} for {}".format(folder_name, page_name))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-topic", type=str)
    parser.add_argument("-level", type=int)
    parser.add_argument("-folder", type=str)
    args = parser.parse_args()
    log_file_name = "log/log_" + datetime.datetime.now().strftime("%d_%b_%Y_%H_%M_%S") + ".log"
    os.makedirs(os.path.dirname(log_file_name), exist_ok=True)
    logging.basicConfig(filename=log_file_name,
                        format="%(levelname)s [%(asctime)s] %(message)s",
                        datefmt="%d-%b-%Y %H:%M:%S",
                        level=logging.INFO)
    logger = logging.getLogger()
    logger.info("Process begun at: " + datetime.datetime.now().strftime("%d.%b %Y %H:%M:%S"))
    main(args.topic, args.level, args.folder, logger)


