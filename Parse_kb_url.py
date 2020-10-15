#!/usr/local/lib/python2.7
# -*- coding: utf-8 -*-
# vim:fileencoding=utf-8
__author__ = 'PykhovaOlga'

import re

from bs4 import BeautifulSoup as bs
from authorization_v2 import auth


class PARSING():
    def __init__(self):
        self.session = auth()

    def parse_block_cods(self, look_for_url):
        result = {}
        response = self.session.post(look_for_url, headers={'Accept-Encoding': 'identity'})
        soup = bs(response.content, 'html.parser')
        divs = soup.find_all('div', attrs={'class': 'code panel pdl conf-macro output-block'})
        i = 0
        for div in divs:
            result[i] = div.text
            i += 1
        return result

    def writing_to_file(self, result, path_to_file):
        with open(path_to_file, 'w') as local_log:
            for val in result.values():
                try:
                    local_log.write((val).encode('utf-8'))
                    local_log.write("\n\n\n")
                except Exception as ex:
                    print(ex)
                    local_log.write('Error Writing'+"\n\n\n")

if __name__ == '__main__':
    parse = PARSING()
    PATH_PREF = '/opt/noc/lib/boba/data/'

    try:
        base_url = 'https://kb.ertelecom.ru/pages/viewpage.action?pageId=127291067#id-%D0%A6%D0%B5%D0%BD%D1%82%D1%80%D0%B0%D0%BB%D0%B8%D0%B7%D0%B0%D1%86%D0%B8%D1%8F%D1%81%D0%B5%D1%80%D0%B2%D0%B5%D1%80%D0%BE%D0%B2%D0%B2%D0%B8%D0%B4%D0%B5%D0%BE%D0%BD%D0%B0%D0%B1%D0%BB%D1%8E%D0%B4%D0%B5%D0%BD%D0%B8%D1%8F.-1.IP-filter'
        result = parse.parse_block_cods(base_url)
        prefixes_file = PATH_PREF + 'prefixes_msa190_00001'
        parse.writing_to_file(result, prefixes_file)
    except Exception as ex:
        print(ex)

    try:
        acl_url = 'https://kb.ertelecom.ru/pages/viewpage.action?pageId=128476926#id-1.3.5%D0%90%D0%B3%D1%80%D0%B5%D0%B3%D0%B0%D1%86%D0%B8%D1%8F:%D0%BA%D0%BE%D0%BC%D0%BC%D1%83%D1%82%D0%B0%D1%82%D0%BE%D1%80%D1%8BHuawei6320-1.3.1.7ACL'
        result_2 = parse.parse_block_cods(acl_url)
        result_acl = {}
        for num_block, code_block in result_2.items():
            if re.search('(acl number \d+\s+rule)', code_block) is not None:
                result_acl[num_block] = code_block
        acl_file = PATH_PREF + 'acl_msa5839_00003'
        parse.writing_to_file(result_acl, acl_file)
    except Exception as ex:
        print(ex)


    # MSA-6105
    try:
        alcatel_url = 'https://kb.ertelecom.ru/pages/viewpage.action?spaceKey=concept&title=6.3.1+Alcatel+SR7750'
        result = parse.parse_block_cods(alcatel_url)
        alcatel_file_name = PATH_PREF + 'alcatel_msa6105_0001'
        parse.writing_to_file(result, alcatel_file_name)
    except Exception as ex:
        print(ex)

