from typing import List

stop_setense_char = '。'
content = ""
k1 = "都像这三个家庭一样地贫穷"
k2 = "丈夫"
content_keyword = k2
import re

sentenses_list = []
numbers_list = []

result_list = []


def read_text():
    result_file = r"D:\outprojects\pdf_retrieval\results\me01a.txt"
    with open(result_file, 'r', encoding="utf-8") as f:
        lines = f.readlines()
        print(len(lines))
        temp_index = 0
        # sentenses_list1 = get_all_keywords_sentense(lines)
        keyword_lines = generate_kwyword_list(lines)

        result = map(lambda value: generate_range_row(value, keyword_lines.index(value), keyword_lines), keyword_lines)
        for r in result:
            start, end, raw_index = r
            if end - start <= 10:  # 认为在10行之内为同一句子
                continue
            # final_result = "".join(lines[start: end]).replace("\n", "")
            # has_key_word = content_keyword in final_result
            page_number = get_page_number(lines[:raw_index + 1])
            final_sentense = get_final_whole_sentense(lines[start: end])
            print(page_number, final_sentense)


def get_page_number(page_lines: List):
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


def get_whole_sentense(part_list: List):
    # end_index = index + default_index
    part_content = "".join(part_list).replace("\n", '')
    print(part_content)
    whole_sentense_pattern = fr"[\s\S]*?{content_keyword}[\s\S]*?{stop_setense_char}$"
    print(whole_sentense_pattern)
    result = re.fullmatch(whole_sentense_pattern, part_content)
    if result is None:
        return "", 0
    else:
        return result, 1


def generate_kwyword_list(page_lines: List):
    keyword_lines = []
    for index, line in enumerate(page_lines):
        if content_keyword in line:
            keyword_lines.append(index)
    return keyword_lines


def get_all_keywords_sentense(page_lines: List) -> List:
    sentenses_list = []
    left_content = "".join(page_lines).replace("\n", '')
    lines = left_content.split(stop_setense_char)
    for index, line in enumerate(lines):
        if content_keyword in line:
            sentense = f"{line}{stop_setense_char}"
            sentenses_list.append(sentense)
    return sentenses_list


def generate_range_row(value, index, keywords_list: List):
    default_value = 6
    start_index = value - default_value
    next_index = index + 1
    if next_index < len(keywords_list):
        end_index = keywords_list[next_index]
    else:
        end_index = keywords_list[index] + default_value
    # print(f"start_index:{start_index} ,end_index: {end_index}, value:{value}, index:{index}, next_index:{next_index}")

    return start_index, end_index, value


def get_final_whole_sentense(range_list: List):
    temp_list = "".join(range_list).replace("\n", "").split(stop_setense_char)
    result = []
    for line in temp_list:
        if content_keyword in line:
            result.append(f"{line}{stop_setense_char}")
    return result[-1] if len(result) > 1 else result[0]


read_text()
