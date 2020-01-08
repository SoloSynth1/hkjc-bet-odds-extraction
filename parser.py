import json
from bs4 import BeautifulSoup


class Parser:

    def __init__(self, timestamp):
        self.codec = 'lxml'
        self.timestamp = timestamp

    def reorganize_path_elements(self, path_elements):
        odd_type, race_number, combination = path_elements
        return [race_number, odd_type, combination]

    def assign(self, dictionary, path_elements, value):
        target = path_elements.pop(0)
        if not dictionary.get(target):
            dictionary[target] = {}
        if path_elements:
            self.assign(dictionary[target], path_elements, value)
        else:
            dictionary[target] = value

    def extract_elements(self, a_elements, lstrip_str, rstrip_str):
        return [(x['href'].strip(lstrip_str).strip(rstrip_str).replace("'", ''), x.text) for x in a_elements]

    def write_combos_to_result(self, result, combos):
        for combo in combos:
            path = [x.strip() for x in combo[0].split(',')]
            path = self.reorganize_path_elements(path)
            self.assign(result, path+[self.timestamp], float(combo[1]))
        return result

class ComboMatrixParser(Parser):

    def __init__(self, timestamp):
        super().__init__(timestamp)

    def parse_combo_table(self, html):
        result = {}
        soup = BeautifulSoup(html, self.codec)
        a_elements = soup.find_all('a')

        combos = self.extract_elements(a_elements, 'javascript:processQuickBet(', ')')

        result = self.write_combos_to_result(result, combos)

        return result

class InnerTableParser(Parser):

    def __init__(self, timestamp):
        super().__init__(timestamp)

    def parse_table(self, html):
        result = {}
        soup = BeautifulSoup(html, self.codec)
        a_elements = soup.find_all('a')

        def filter_elements(a_elements, criteria):
            return [a_element for a_element in a_elements if criteria in a_element['href']]

        a_horse_elements = filter_elements(a_elements, 'goHorseRecord')
        a_win_elements = filter_elements(a_elements, "processQuickBet('WIN'")
        a_pla_elements = filter_elements(a_elements, "processQuickBet('PLA'")

        horses = self.extract_elements(a_horse_elements, 'javascript:goHorseRecord2(', ');')
        wins = self.extract_elements(a_win_elements, 'javascript:processQuickBet(', ')')
        plas = self.extract_elements(a_pla_elements, 'javascript:processQuickBet(', ')')

        for win in wins:
            _, race_no ,horse_no = [x.strip() for x in win[0].split(",")]

        result = self.write_combos_to_result(result, wins)
        result = self.write_combos_to_result(result, plas)

        return result
