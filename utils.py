from unidecode import unidecode


def remove_accentuation_from_strings(strings_list):
    treated_list = []
    for string in strings_list:
        normalized_string = unidecode(string)
        normalized_string = normalized_string.replace("-", "").replace(".", "")
        normalized_string = normalized_string.upper()
        treated_list.append(normalized_string)

    return treated_list


def filter_5_chars_string(strings_list):
    filtered_strings = []
  
    for string in strings_list:
        treated_string = string.replace("\n", "").strip()
        if len(treated_string) == 5:
            filtered_strings.append(treated_string)

    return filtered_strings


def remove_line_breaker(strings_list):
    for i in range(len(strings_list)):
        strings_list[i] = strings_list[i].replace("\n", "")