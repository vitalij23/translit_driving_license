import re


class RulesOld:
    """Предположительно Приказ МВД N 782
    http://www.consultant.ru/document/cons_doc_LAW_28295/3d53b063c117e5309f5e1d78aaead678fb642834/
    """
    # old
    special_rules = {  # Е Ё  И
        'Е': {'YE': {'at_start': None, 'after': 'ЬЪАЕЁИЙОЫЭЮЯ'}},
        'Ё': {'E': {'after': 'ЧШЩЖ'},
              'YO': {'at_start': None, 'after': 'ЬЪАЕЁИЙОЫЭЮЯ'},
              'YE': {'after': 'БВГДЗКЛМНПРСТФХЦ'},
              },
        'И': {'YI': {'after': 'Ь'}}

    }
    mapping = (
        u'АБВГДЕ' + 'З' + 'ИЙКЛМНОПРСТУФ' + 'ЪЫЬЭ',  # ЕЁЖ  #И  #ХЦЧШЩ  #ЮЯ",
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


class RulesNew:
    """ Приказ МВД N 995 (2015-н/в)
     http://www.consultant.ru/document/cons_doc_LAW_195687/3197806174c701185ffd8e8986a24173958def21/"""
    special_rules = {  # Е Ё  И
        # 'Е': {'YE': {'at_start': None, 'after': 'ЬЪ'}}, #АЕЁИЙОЫЭЮЯ
        # 'Ё': {'E': {'after': 'ЧШЩЖ'},
        #       'YO': {'at_start': None, 'after': 'ЬЪАЕЁИЙОЫЭЮЯ'},
        #       'YE': {'after': 'БВГДЗКЛМНПРСТФХЦ'},
        #       },
        # 'И': {'YI': {'after': 'Ь'}}

    }
    mapping = (
        u'АБВГДЕ' + 'З' + 'ИЙКЛМНОПРСТУФ' + 'ЫЬЭ',#ЕЁЖ  #И  #ХЦЧШЩ  #ЮЯ",
        u'ABVGDE' + 'Z' + 'IIKLMNOPRSTUF' + 'Y\'e',
    )

    multi_mapping = {  # Ж ХЦЧШЩ ЮЯ
        u"Ж": u"ZH",
        u"Х": u"KH",
        u"Ц": u"TS",
        u"Ч": u"CH",
        u"Ш": u"SH",
        u"Щ": u"SHCH",
        u"Ю": u"IU",  #?
        u"Я": u"IA",  # /mnt/hit4/hit4user/PycharmProjects/cnn/samples/vodit_udostav/0/76-208-0.png
        u'Ъ': u'IE'
    }


def translit(rustr: str, rules) -> str:
    """
    Водительское удостоверение.

    :param rustr:
    :return: latin
    """

    special_rules = rules.special_rules
    mapping = rules.mapping
    multi_mapping = rules.multi_mapping

    new_line = rustr
    #special_rules
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


def check(rus, lat, p3=False) -> bool:
    # TODO: сделать сложный регекс чтобы исключить названия с АРЕСП и КОБЛАНКА
    # rus = re.sub(' +', '', rus)
    # lat = re.sub(' +', '', lat)
    if p3:
        tr_old = translit(rus, RulesOld)
        tr_new = translit(rus, RulesNew)
        tr2_old = re.sub(r'RESP\.?', 'RESPUBLICA',
                      tr_old)  # new /mnt/hit4/hit4user/PycharmProjects/cnn/samples/vodit_udostav/0/31-329-0.png
        tr2_old = re.sub(r'OBL\.?', "OBLAST'",
                      tr2_old)  # new  /mnt/hit4/hit4user/PycharmProjects/cnn/samples/vodit_udostav/0/37-168-0.png
        tr2_new = re.sub(r'RESP\.?', 'RESPUBLIKA', tr_new)
        tr2_new = re.sub(r'OBL\.?', " OBLAST'", tr2_new)
        # we don't know the difference between old and new
        if tr_old == lat or tr_new == lat or tr2_old == lat or tr2_new == lat:
            return True

    elif translit(rus, RulesOld) == lat or translit(rus, RulesNew) == lat:
        return True
    return False


if __name__ == '__main__':  # test
    if translit('ЕАЛЬИСЬEEЬEЯ', RulesOld) != "YEAL'YIS'EE'EYA":  # Приказ МВД N 782
        print("fail1")

    if translit('СЕРГЕЕВИЧ', RulesOld) != 'SERGEYEVICH':  # /mnt/hit4/hit4user/PycharmProjects/cnn/samples/vodit_udostav/0/45-287-0.png
        print("fail2")

    if translit('ИГОРЬ', RulesOld) != "IGOR'" and translit('ИГОРЬ', RulesNew) != "IGOR'":
        print("fail3")

    if translit('РЕСП. ДАГЕСТАН', RulesOld) != 'RESP. DAGESTAN':
        print('fail4')

    if translit('САГИНБАЕВ', RulesNew) != 'SAGINBAEV': # new /mnt/hit4/hit4user/PycharmProjects/cnn/samples/passport_and_vod/0/2019080115-2-0.png
        print('fail5')

    if translit('ЕВГЕНЬЕВИЧ', RulesOld) != "YEVGEN'YEVICH":  # 'YEVGEN'YEVICH' old # /mnt/hit4/hit4user/PycharmProjects/cnn/samples/vodit_udostav/0/7-408-6.png
        print('fail6')

    if translit('АНАТОЛЬЕВИЧ', RulesNew) != "ANATOL'EVICH":  # new /mnt/hit4/hit4user/PycharmProjects/cnn/samples/passport_and_vod/0/30-161-10.png
        print('fail7')

    if not check('ЧЕЛЯБИНСКАЯ ОБЛ.', 'CHELYABINSKAYA OBL.',
                 p3=True):  # /mnt/hit4/hit4user/PycharmProjects/cnn/samples/vodit_udostav/0/45-176-0.png
        print('fail8')

    if not check('ЧЕЛЯБИНСКАЯ ОБЛ', "CHELYABINSKAYA OBLAST'",
                 p3=True):  # /mnt/hit4/hit4user/PycharmProjects/cnn/samples/vodit_udostav/0/45-176-0.png
        print('fail9')

    if not check('РЕСП ДАГЕСТАН', "RESPUBLIKA DAGESTAN",
                 p3=True):  # /mnt/hit4/hit4user/PycharmProjects/cnn/samples/vodit_udostav/0/45-446-0.png
        print('fail10')

    if not check('УКРАИНА', 'UKRAINA',
                 p3=True):  # /mnt/hit4/hit4user/PycharmProjects/cnn/samples/passport_and_vod/0/29-327-0.png
        print('fail11')

    print(translit('ХУССЕЙН', RulesNew))
    print('KHUSSEIN')
    print(check('ХУССЕЙН', 'KHUSSEIN'))
