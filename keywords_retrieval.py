import re
from typing import List

import pandas as pd
from path import Path

from configuration import Configuration
from helpers import load_config, get_results_path


class KeywordsRetrieval:
    def __init__(self):
        self.config: Configuration = load_config()
        self.stop_setense_char = '。'
        self.current_keyword = ""

    def retrieve_keywords(self):
        files: List[Path] = get_results_path().walkfiles(match="*.txt")
        retrieval_result = []
        for num, f in enumerate(files):
            # if num > 2:
            #     break
            file_name = f.name
            lines = f.lines(encoding="utf-8")
            for current_keyword in self.config.keywords:
                keyword_lines = self.generate_kwyword_list(lines, current_keyword)
                result = map(lambda value: self.generate_range_row(value, keyword_lines.index(value), keyword_lines),
                             keyword_lines)

                for r in result:
                    start, end, raw_index = r
                    if end - start <= 10:  # 认为在10行之内为同一句子
                        continue
                    page_number = self.get_page_number(lines[:raw_index + 1])
                    final_sentense = self.get_final_whole_sentense(lines[start: end], current_keyword)
                    item = [final_sentense, page_number, str(file_name), current_keyword, ]
                    print(item)
                    retrieval_result.append(item)
        self.save_excel(retrieval_result)

    def save_excel(self, retrieval_result: List):
        file_name = self.config.excel_file
        df = pd.DataFrame(retrieval_result, columns=["句子", "页码", "文件名", "关键字"])
        df.to_excel(file_name, index=False, engine='xlsxwriter')

    def generate_kwyword_list(self, page_lines: List, content_keyword: str):
        keyword_lines = []
        for index, line in enumerate(page_lines):
            if content_keyword in line:
                keyword_lines.append(index)
        return keyword_lines

    def generate_range_row(self, value, index, keywords_list: List):
        default_value = 6
        start_index = value - default_value
        next_index = index + 1
        if next_index < len(keywords_list):
            end_index = keywords_list[next_index]
        else:
            end_index = keywords_list[index] + default_value
        # print(f"start_index:{start_index} ,end_index: {end_index}, value:{value}, index:{index}, next_index:{next_index}")

        return start_index, end_index, value

    def get_page_number(self, page_lines: List):
        # print("".join(page_lines)[-500:])
        number_pattern = "^\d*\\n$"
        numbers = []
        number_str = ""
        for line in page_lines:
            # print(line)
            result = re.search(number_pattern, line)
            if result is not None:
                numbers.append(result[0].replace("\n", ""))

        if len(numbers) > 1:
            number_str = numbers[-1]
            # print(numbers[-1])
            if len(number_str) >= 2:
                temp_l = list(number_str)
                temp_l.reverse()
                number_str = "".join(temp_l)
                # number_str = number_str[1] + number_str[0]
            # print(number_str)
        return number_str

    def get_final_whole_sentense(self, range_list: List, content_keyword: str):
        temp_list = "".join(range_list).replace("\n", "").split(self.stop_setense_char)
        result = []
        for line in temp_list:
            if content_keyword in line:
                result.append(f"{line}{self.stop_setense_char}")
        if len(result) == 0:
            return ""

        return result[-1] if len(result) > 1 else result[0]


if __name__ == '__main__':
    search = KeywordsRetrieval()
    search.retrieve_keywords()
