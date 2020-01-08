from selenium import webdriver


class SeleniumScraper:

    def __init__(self):
        self.TARGETS = {
            "https://bet.hkjc.com/racing/pages/odds_wpq.aspx?lang=ch": [
                'combOddsTableQIN',
                'combOddsTableQPL',
                'wpTable1InnerTable'
            ],
            # The table inside is the same as the 'wpTable1InnerTable' from the page 'odds_wpq.aspx'
            # "https://bet.hkjc.com/racing/pages/odds_qtt.aspx?lang=ch": [
            #     'wpTable1InnerTable'
            # ]
        }
        self.BROWSER_DRIVER_PATH = "./driver/chromedriver"
        self.TABLE_IDS = []
        self.driver = webdriver.Chrome(self.BROWSER_DRIVER_PATH)

    def __del__(self):
        self.driver.quit()

    def scrap(self):
        result = {}
        for target_url, id_list in self.TARGETS.items():
            self.driver.get(target_url)
            for id in id_list:
                result["{}.{}".format(target_url, id)] = self.driver.find_element_by_id(id).get_attribute('innerHTML')
        return result
