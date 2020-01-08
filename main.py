import time
import datetime

from scraper import SeleniumScraper
from parser import ComboMatrixParser, InnerTableParser
from writer import JSONWriter

DATETIME_FORMAT = "%Y-%m-%d"

if __name__ == "__main__":
    scraper = SeleniumScraper()
    combo_parser = ComboMatrixParser(timestamp=str(int(time.time())))
    table_parser = InnerTableParser(timestamp=str(int(time.time())))
    output_file_name = "./output/{}.json".format(datetime.datetime.now().strftime(DATETIME_FORMAT))
    json_writer = JSONWriter(filepath=output_file_name)
    htmls = scraper.scrap()
    scraper.driver.quit()
    for url, table_html in htmls.items():
        if 'combOddsTable' in url:
            result = combo_parser.parse_combo_table(table_html)
            json_writer.write(result)
        elif 'wpTable1InnerTable' in url:
            result = table_parser.parse_table(table_html)
            print(result)


