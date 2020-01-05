from bs4 import BeautifulSoup

class ComboMatrixParser:

    def __init__(self, timestamp):
        self.codec = 'lxml'
        self.timestamp = timestamp

    def parse_combo_table(self, html):
        result = {}
        soup = BeautifulSoup(html, self.codec)
        a_elements = soup.find_all('a')
        combos = [(x['href'].strip('javascript:processQuickBet(').strip(')').replace("'", ''), x.text) for x in
                  a_elements]
        for combo in combos:
            path = [x.strip() for x in combo[0].split(',')]
            self.assign(result, path+[self.timestamp], float(combo[1]))
        return result

    def assign(self, dictionary, path_elements, value):
        target = path_elements.pop(0)
        if not dictionary.get(target):
            dictionary[target] = {}
        if path_elements:
            self.assign(dictionary[target], path_elements, value)
        else:
            dictionary[target] = value
