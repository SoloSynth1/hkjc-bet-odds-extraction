import time
import datetime

from scraper import SeleniumScraper
from parser import ComboMatrixParser
from writer import ComboWriter

DATETIME_FORMAT = "%Y-%m-%d"

if __name__ == "__main__":
    scraper = SeleniumScraper()
    combo_parser = ComboMatrixParser(timestamp=str(int(time.time())))
    output_file_name = "./output/{}.json".format(datetime.datetime.now().strftime(DATETIME_FORMAT))
    combo_writer = ComboWriter(filepath=output_file_name)
    htmls = scraper.scrap()
    scraper.driver.quit()
    for url, table_html in htmls.items():
        if 'combOddsTable' in url:
            result = combo_parser.parse_combo_table(table_html)
            combo_writer.write(result)


