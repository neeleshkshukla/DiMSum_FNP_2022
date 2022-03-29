#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import pickle


import traceback

bad_file = ["7796.txt","14018.txt","23372.txt","4842.txt","11692.txt","2633.txt","132.txt","18103.txt","9588.txt","11736.txt","6586.txt"]


# needs to be number increasing
# remove page-page
def remove_slash(lst):
    for i in range(1, len(lst) - 1):
        if lst[i] == "–" and lst[i + 1].isalpha() and lst[i - 1].isalpha():
            return lst[0:i] + lst[i + 2:]
        if lst[i] == "-" and lst[i + 1].isalpha() and lst[i - 1].isalpha():
            return lst[0:i] + lst[i + 2:]
    return lst


def clean_number(str):
    ans = ""
    for i in str:
        if i.isdigit():
            ans += i
    return ans


def remove_number(str1, pos_num):
    line = str1.split(" ")
    line = [i for i in line if i != ""]
    line = remove_slash(line)
    if (pos_num == 0):
        for i in range(0, len(line)):
            if (not line[i].isnumeric()) and any(c.isalpha() for c in line[i]):
                # if (not line[i].isnumeric()):
                return " ".join(line[i:]).replace(".", ""), clean_number(line[pos_num])
    else:
        for i in range(len(line) - 1, -1, -1):
            if (not line[i].isnumeric()) and any(c.isalpha() for c in line[i]):
                # if (not line[i].isnumeric()):
                return " ".join(line[0:i + 1]).replace(".", ""), clean_number(line[pos_num])


# if start with content, search with less requirement
def process_tolerant(num, lst):
    index = num
    toc = []
    toc_page = []
    sub_dir = 0
    bad_line = 0
    pos_num = None
    for i in range(min(10, len(lst) - index - 1)):
        index += 1
        if_start, pos_num = toc_start(lst[index])
        if (if_start):
            break
        elif i == 9:
            return None, 0, 0
    while (sub_dir <= 5 and index < len(lst)):
        status, _ = toc_form_check(lst[index], pos_num)
        if (status):
            sub_dir = 0
            content, number = remove_number(lst[index], pos_num)
            toc.append(content)
            toc_page.append(number)
        else:
            sub_dir += 1
            bad_line += 1
            # toc.append(lst[index])
        index += 1
    if (index - num - bad_line > 3):
        # return toc[0:len(toc)-sub_dir]
        return toc, index - sub_dir - 1, toc_page
    else:
        return None, 0, 0


# search continuous appearing numbers
def process(num, lst, pos_num):
    index = num
    toc = []
    toc_page = []
    sub_dir = 0
    bad_line = 0
    prev_page = -1
    while (sub_dir <= 5 and index < len(lst)):
        if "contents" in lst[index].lower() and toc_page != [] and len(toc_page) < 2:
            toc_page.pop()
            toc.pop()
            index += 1
            continue
        status, cur_page = toc_form_check(lst[index], pos_num)
        if (status):
            if (cur_page >= prev_page):
                prev_page = cur_page
                sub_dir = 0
                content, number = remove_number(lst[index], pos_num)
                toc.append(content)
                toc_page.append(number)
            else:
                sub_dir += 1
                bad_line += 1
        else:
            sub_dir += 1
            bad_line += 1
            # toc.append(lst[index])
        index += 1
    if (index - num - bad_line > 5):
        # return toc[0:len(toc)-sub_dir]
        return toc, index - sub_dir - 1, toc_page
    else:
        return None, 0, 0


# check if satify the format of ToC
def toc_form_check(str, pos_num=None):
    # str1 = re.sub(r'[^\w\s]','',str)
    str1 = str.replace(".", "")
    str1 = str1.replace("•", "")
    line = str1.split(" ")
    line = [i for i in line if i != ""]
    line = remove_slash(line)
    if line == []:
        return False, 0
    alpha = 0
    number = 0
    for word in line:
        if word.isalpha():
            alpha += 1
        if word.isnumeric():
            number += 1
    # if alpha==len(line)-1 and number ==1 and alpha >0 and len(line)<10 and line[pos_num].isnumeric():
    if number >= 1 and alpha >= 1 and len(line) < 15 and line[pos_num].isnumeric():
        try:
            if int(line[pos_num]) < 150 and int(line[pos_num]) > 0:
                return True, int(line[pos_num])
        except:
            return False, 0
    return False, 0


# Check if looks like start of ToC
def toc_start(str):
    str = re.sub(r'[^\w\s]', '', str)
    line = str.split(" ")
    line = [i for i in line if i != ""]
    line = remove_slash(line)
    if line == []:
        return False, None
    alpha = 0
    number = 0
    for word in line:
        if word.isalpha():
            alpha += 1
        if word.isnumeric():
            number += 1
    num_pos = None
    if line[0].isnumeric():
        num_pos = 0
    elif line[-1].isnumeric():
        num_pos = -1
    else:
        return False, None
    # if alpha==len(line)-1 and number ==1 and alpha >0 and len(line)<10:
    if number >= 1 and alpha >= 1 and len(line) < 15:
        try:
            val = int(line[num_pos])
            if (val < 50):
                return True, num_pos
        except:
            return False, None
    return False, None


def split_page(key, lst, start_pos, page_hint):
    prev_pos = start_pos

    key_index = 0
    page_pos = []
    count = start_pos

    while (count < len(lst) - 100 and key_index < len(key)):
        if key[key_index].lower() in lst[count].lower():
            # if match(key[key_index].lower(),lst[count].lower()):
            # if page_pos!=[] and page_pos[-1]!=None and count <= page_pos[-1]+5:
            if page_pos != [] and page_pos[-1] != None and count <= page_pos[-1] + int(page_hint[key_index]) - int(
                    page_hint[key_index - 1]):
                page_pos.pop()
                key_index -= 1
            else:
                prev_pos = count
                page_pos.append(count)
                key_index += 1
        count += 1

        if page_pos != [] and page_pos[0] != None:
            diff = page_pos[0]
        else:
            diff = start_pos

        if (key_index < len(key) and key_index > 0 and (
                count > (len(lst) - diff) * int(page_hint[key_index]) * 1.2 / int(page_hint[-1]))):
            count = prev_pos
            page_pos.append(None)
            key_index += 1
        elif (count == len(lst) - 100 and key_index < len(key)):
            count = prev_pos
            page_pos.append(None)
            key_index += 1

    return page_pos


def split_page_without_pagehint(key, lst, start_pos):
    prev_pos = start_pos

    key_index = 0
    page_pos = []
    count = start_pos
    while (count < len(lst) - 100 and key_index < len(key)):
        if key[key_index].lower() in lst[count].lower():
            # if match(key[key_index].lower(),lst[count].lower()):
            # if page_pos!=[] and page_pos[-1]!=None and count <= page_pos[-1]+5:
            if page_pos != [] and page_pos[-1] != None and count <= page_pos[-1] + 2:
                page_pos.pop()
                key_index -= 1
            else:
                prev_pos = count
                page_pos.append(count)
                key_index += 1
        count += 1

        if (count == len(lst) - 100 and key_index < len(key)):
            count = prev_pos
            # count = start_pos
            page_pos.append(None)
            key_index += 1

    return page_pos


def search_page_helper(key, lst, start_pos):
    prev_pos = start_pos

    key_index = 0
    page_pos = []
    count = start_pos

    while (count < len(lst) - 100 and key_index < len(key)):
        if key[key_index] in lst[count].lower().split(" "):

            if page_pos != [] and page_pos[-1] != None and count <= page_pos[-1] + int(key[key_index]) - int(
                    key[key_index - 1]):
                page_pos.pop()
                key_index -= 1
            else:
                prev_pos = count
                page_pos.append(count)
                key_index += 1

        count += 1

        if (key_index < len(key) and (count > len(lst) * int(key[key_index]) * 1.2 / int(key[-1]))):
            count = prev_pos
            # count = start_pos
            page_pos.append(None)
            key_index += 1
        elif (key_index < len(key) and count == len(lst) - 100):
            count = prev_pos
            # count = start_pos
            page_pos.append(None)
            key_index += 1

    return page_pos


def remove_zero(lst):
    new_lst = []
    for i in lst:
        if i[0] == "0":
            new_lst.append(i[1:])
        else:
            new_lst.append(i)
    return new_lst


def search_page(key, lst, start_pos):
    ori = search_page_helper(key, lst, start_pos)
    clean = search_page_helper(remove_zero(key), lst, start_pos)
    num = 0
    for i in ori:
        if i == None:
            num += 1
    num1 = 0
    for i in clean:
        if i == None:
            num1 += 1
    if num > num1:
        return clean
    else:
        return ori


def match(str1, str2):
    lst1 = str1.lower().split(" ")
    lst2 = str2.lower().split(" ")
    find = 0
    unfind = 0
    for i in lst1:
        if i in lst2:
            find += 1
        else:
            unfind += 1
    if unfind == 1 or unfind == 0:
        return True
    else:
        return False


def find_next(pos, lst, end):
    for i in range(pos, len(lst)):
        if lst[i] != None:
            return lst[i]
    return end


def weak_search(key, page_pos, lst, start_pos):
    prev = start_pos
    next_page = 0
    for i in range(len(page_pos)):
        if page_pos[i] == None:
            next_page = find_next(i, page_pos, len(lst))
            for index in range(prev + 2, next_page):
                if match(key[i], lst[index]):
                    page_pos[i] = index
                    prev = index
                    break
        else:
            prev = page_pos[i]
    return page_pos

def find_next_with_index(pos,lst,end):
    for i in range(pos,len(lst)):
        if lst[i]!=None:
            return lst[i],i
    return end,len(lst)

def split_into_half(lst,file,start_pos):
    prev = None
    next_page = 0
    for i in range(len(lst)):
        if lst[i] == None:
            next_page,index = find_next_with_index(i,lst,len(file))
            if prev!= None:
                for j in range(i,index):
                    lst[j] = int((next_page -  prev)*(j-i+1) / (index-i+1) + prev)
            else:
                for j in range(i,index):
                    lst[j] = int((next_page-start_pos)*(j-i) / (index-i) + start_pos)
        else:
            prev = lst[i]
    return lst


# see which searching method is better
def see_which_one_better_title(pages_search_by_number, pages_search_by_title, tmp_file, key, start_pos):
    exist_page = 0
    for i in range(0, min(6, len(pages_search_by_title))):
        if pages_search_by_title[i] != None:
            exist_page += 1
    if exist_page > 4:
        return True
    exist_number = 0
    for i in range(0, min(6, len(pages_search_by_number))):
        if pages_search_by_number[i] != None:
            exist_number += 1
    if exist_page <= 3 and exist_number > 4:
        return False
    pages_search_by_number = split_into_half(pages_search_by_number, tmp_file, start_pos)
    pages_search_by_title = split_into_half(pages_search_by_title, tmp_file, start_pos)

    max_diff_number = 0
    bad_times = 0
    for i in range(1, min(6, len(pages_search_by_number))):
        val = pages_search_by_number[i] - pages_search_by_number[i - 1]
        if val < 3:
            bad_times += 1
        if bad_times > 1:
            return True
        if ((int(key[i]) - int(key[i - 1])) == 0):
            continue
        val = val / (int(key[i]) - int(key[i - 1]))
        if val > max_diff_number:
            max_diff_number = val

    max_diff_title = 0
    bad_times = 0
    for i in range(1, min(6, len(pages_search_by_title))):
        val = pages_search_by_title[i] - pages_search_by_title[i - 1]
        if val < 3:
            bad_times += 1
        if bad_times > 1:
            return False
        if ((int(key[i]) - int(key[i - 1])) == 0):
            continue
        val = val / (int(key[i]) - int(key[i - 1]))
        if val > max_diff_title:
            max_diff_title = val
    return max_diff_title < max_diff_number * 1.2


def see_which_one_better(pages_search_by_number, pages_search_by_title, tmp_file, key, start_pos):
    exist_number = 0
    for i in range(0, min(6, len(pages_search_by_number))):
        if pages_search_by_number[i] != None:
            exist_number += 1
    exist_page = 0
    for i in range(0, min(6, len(pages_search_by_title))):
        if pages_search_by_title[i] != None:
            exist_page += 1
    if exist_page <= 3 and exist_number > 4:
        return True
    elif exist_page > 4 and exist_number <= 3:
        return False
    pages_search_by_number = split_into_half(pages_search_by_number, tmp_file, start_pos)
    pages_search_by_title = split_into_half(pages_search_by_title, tmp_file, start_pos)

    max_diff_number = 0
    bad_times = 0
    for i in range(1, min(6, len(pages_search_by_number))):
        val = pages_search_by_number[i] - pages_search_by_number[i - 1]
        if val < 3:
            bad_times += 1
        if bad_times > 1:
            return False
        if ((int(key[i]) - int(key[i - 1])) == 0):
            continue
        val = val / (int(key[i]) - int(key[i - 1]))
        if val > max_diff_number:
            max_diff_number = val

    max_diff_title = 0
    bad_times = 0
    for i in range(1, min(6, len(pages_search_by_title))):
        val = pages_search_by_title[i] - pages_search_by_title[i - 1]
        if val < 3:
            bad_times += 1
        if bad_times > 1:
            return True
        if ((int(key[i]) - int(key[i - 1])) == 0):
            continue
        val = val / (int(key[i]) - int(key[i - 1]))
        if val > max_diff_title:
            max_diff_title = val
    return max_diff_number < max_diff_title * 1.2


def page_exist(toc_page):
    for i in toc_page:
        if i == "":
            return False
    return True


def extract_toc(dir_path, annual_report_dir):
    directory = os.path.join(dir_path, annual_report_dir)
    num_file = 0
    exist_toc = 0

    file_toc_loc = {}
    file_toc_len = {}

    print(len([name for name in os.listdir(directory)]))

    # for file has ToC
    for file in os.listdir(directory):
        try:
            if num_file % 300 == 0:
                print("Processing File Number: ", num_file)
            file_id = file.split('.')[0]
            if file in bad_file:
                continue
            if ".DS_Store" in file:
                continue
            tmp_file = []
            contents = []

            with open(os.path.join(directory, file), "r", encoding='utf-8') as f:
                for line in f:
                    line = line.replace("\n", "").replace("\t", " ").replace("\xa0", " ")
                    tmp_file.append(line)
            # I assume that toc will appear in either start or end of the file--> not true
            # contain keywords "content"
            count = 0
            find = 0
            toc = None
            while (count < len(tmp_file)):
                if_start, pos = toc_start(tmp_file[count])
                if if_start:
                    toc, start_pos, toc_page = process(count, tmp_file, pos)
                    if (toc):
                        find = 1
                        contents.append(toc)
                        exist_toc += 1
                        break
                count += 1
            count = 0
            while (count < len(tmp_file) and find == 0):
                if "contents" in tmp_file[count].lower():
                    toc, start_pos, toc_page = process_tolerant(count, tmp_file)
                    if (toc):
                        find = 1
                        contents.append(toc)
                        exist_toc += 1
                        break
                count += 1
            if (find == 0):
                print('TOC not found in: ', file)
            else:
                if (page_exist(toc_page)):
                    pages_search_by_number = search_page(toc_page, tmp_file, start_pos)
                    # print(pages_search_by_number)
                    pages_search_by_title = split_page(toc, tmp_file, start_pos, toc_page)
                    # print(pages_search_by_title)
                    pages_search_by_title = weak_search(toc, pages_search_by_title, tmp_file, start_pos)
                    # print(pages_search_by_title)
                    ans = see_which_one_better(pages_search_by_number, pages_search_by_title, tmp_file, toc_page,
                                               start_pos)
                    # print(ans)
                    if (ans):
                        previ = 0
                        nexti = 0
                        for i in range(len(pages_search_by_number)):
                            if pages_search_by_number[i] == None and pages_search_by_title[i] != None:
                                nexti = find_next(i, pages_search_by_number, len(tmp_file))
                                if (previ < pages_search_by_title[i] and nexti > pages_search_by_title[i]):
                                    pages_search_by_number[i] = pages_search_by_title[i]
                            else:
                                if pages_search_by_number[i] != None:
                                    previ = pages_search_by_number[i]

                        pages = pages_search_by_number
                    else:
                        pages = pages_search_by_title
                else:
                    pages_search_by_title = split_page_without_pagehint(toc, tmp_file, start_pos)
                    pages = weak_search(toc, pages_search_by_title, tmp_file)
                pages = split_into_half(pages, tmp_file, start_pos)
                if abs(start_pos - pages[0]) > 100:
                    pages.insert(0, start_pos)
                    toc.insert(0, "start")
                toc_len = []
                for j in range(len(toc)):
                    start_page = pages[j]
                    if j == len(toc) - 1:
                        toc_len.append(len(tmp_file) - start_page)
                    else:
                        end_page = pages[j + 1]
                        toc_len.append(end_page - start_page)

                file_toc_loc[file_id] = (pages, toc)
                file_toc_len[file_id] = (toc_len, toc)

        except Exception as e:
            traceback.print_exc()
            pass
        num_file += 1

    return file_toc_loc, file_toc_len