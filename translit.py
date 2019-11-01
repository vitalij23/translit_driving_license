import re

# http://www.consultant.ru/document/cons_doc_LAW_28295/3d53b063c117e5309f5e1d78aaead678fb642834/
# Приказ МВД N 782
special_rules = {  # Е Ё  И
    'Е': {'YE': {'at_start': None, 'after': 'ЬЪАЕЁИЙОЫЭЮЯ'}},
    'Ё': {'E': {'after': 'ЧШЩЖ'},
          'YO': {'at_start': None, 'after': 'ЬЪАЕЁИЙОЫЭЮЯ'},
          'YE': {'after': 'БВГДЗКЛМНПРСТФХЦ'},
          },
    'И': {'YI': {'after': 'Ь'}}

}
mapping = (
    u'АБВГДE' + 'З' + 'ИЙКЛМНОПРСТУФ' + 'ЪЫЬЭ',#ЕЁЖ  #И  #ХЦЧШЩ  #ЮЯ",
    u'ABVGDE' + 'Z' + 'IYKLMNOPRSTUF' + '\'Y\'e',
)

multi_mapping = {  # Ж ХЦЧШЩ ЮЯ
    u"Ж": u"ZH",
    u"Х": u"KH",
    u"Ц": u"TS",
    u"Ч": u"CH",
    u"Ш": u"SH",
    u"Щ": u"SHCH",
    u"Ю": u"YU",
    u"Я": u"YA",
}


def translit(rustr: str) -> str:
    """
    Водительское удостоверение. Предположительно Приказ МВД N 782
    :param rustr:
    :return: latin
    """
    new_line = rustr
    # special_rules
    for rus_char, letters_dict in special_rules.items():
        for eng_char, rules in letters_dict.items():
            for rul, support in rules.items():
                if rul == 'at_start':
                    if new_line[0] == rus_char:
                        new_line = eng_char + new_line[1:]

                if rul == 'after':
                    for _ in range(len(new_line)):
                        for i, c in enumerate(new_line):
                            if c == rus_char and i > 0 and new_line[i-1] in support:
                                new_line = new_line[:i] + eng_char + new_line[i+1:]
                                break

    # mapping
    for i, c in enumerate(mapping[0]):
        new_line = re.sub(c, mapping[1][i], new_line)

    # multi_mapping
    for c, repl in multi_mapping.items():
        new_line = re.sub(c, repl, new_line)

    return new_line


if __name__ == '__main__':  # test
    if translit('ЕАЛЬИСЬEEЬEЯ') != 'YEAL\'YIS\'EE\'EYA':
        print("fail1")

    if translit('СЕРГЕЕВИЧ') != 'SЕRGЕYEVICH':
        print("fail2")

    if translit('ИГОРЬ') != 'IGOR\'':
        print("fail3")
#
# registry.register(ExampleLanguagePack)
#
# print(get_available_language_codes())
#
# # ['el', 'hy', 'ka', 'ru', 'example']
#
# print(translit('АЛЬИСЯ', 'example'))

