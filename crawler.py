import re

import pandas as pd
import requests
from bs4 import BeautifulSoup as bs


class Crawler:
  def __init__(self):
    # read tsv from ./admission.tsv
    self.admission = pd.read_csv("admission.csv", sep=",")

  def _crawl_bs4(self, url):
    # crawl the url with bs4, get everything in html
    r = requests.get(url)
    soup = bs(r.text, "html.parser")
    return soup

  def _find_keyword(self, keyword, soup):
    # find the keyword in the html, get all string around the keyword
    string_soup = str(soup)
    # as per recommendation from @freylis, compile once only
    CLEANR = re.compile('<.*?>')
    string_soup = re.sub(CLEANR, '', string_soup)
    indices = [m.start() for m in re.finditer(keyword, string_soup)]

    if len(indices) == 0:
      return []
    else:
      return [string_soup[index - 100: index + 100] for index in indices]

  def return_admission_infos(self, debug=False):
    schools, urls, keywords = self.admission["school"], self.admission["url"], self.admission["keyword"]
    outputs = []
    for school, url, school_keyword in zip(schools, urls, keywords):
      output = {'school': school, 'url': url}
      soup = self._crawl_bs4(url)
      for keyword in school_keyword.split(";"):
        output[keyword] = self._find_keyword(keyword, soup)
      outputs.append(output)

      if debug:
        print(output)

    return outputs


if __name__ == "__main__":
  crawler = Crawler()
  print(crawler.return_admission_infos(True))

  # MIT?
  print(crawler._crawl_bs4("https://www.eecs.mit.edu/academics/graduate-programs/admission-process/graduate-admissions-information-letter/"))
  print(crawler._find_keyword("GRE", crawler._crawl_bs4("https://www.eecs.mit.edu/academics/graduate-programs/admission-process/graduate-admissions-information-letter/")))
