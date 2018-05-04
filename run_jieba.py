#!/usr/bin/python
# -*- coding: UTF-8 -*-
# coding=UTF-8
execfile("install_packages.py")
win_unicode_console.enable()

configParser = ConfigParser.RawConfigParser()   
configParser.read("config/config.ini")

mode = configParser.get("jieba-config", "mode")
separator = configParser.get("jieba-config", "separator")
enable_pos_tag = configParser.get("jieba-config", "enable_pos_tag")
pos_tag_separator = configParser.get("jieba-config", "pos_tag_separator")

if os.stat(configParser.get("jieba-config", "user_dict")).st_size > 0:
    jieba.set_dictionary(configParser.get("jieba-config", "user_dict"))

stopwords = []
if os.stat(configParser.get("jieba-config", "stop_words")).st_size > 0:
    jieba.analyse.set_stop_words(configParser.get("jieba-config", "stop_words"))
    with codecs.open(configParser.get("jieba-config", "stop_words"),'r',encoding='utf8') as f:
        stopwords = f.read()

all_files = filemapper.load(configParser.get("jieba-config", "input_dir"))
for f in all_files:
    if f == ".gitignore": 
        continue

    content = ""
    for i in filemapper.read(f):content = content+i
    #print(content)
    
    seg_list = []
    if mode == "exact":
        seg_list = jieba.cut(content, cut_all=False)
    elif mode == "all":
        seg_list = jieba.cut(content, cut_all=True)
    elif mode == "search":
        seg_list = jieba.cut_for_search(content)
    else:
        seg_list = jieba.cut(content, cut_all=False)

    seg_list_filtered = []
    
    for s in seg_list:
        try:
            print(stopwords.index(s))
        except ValueError:
            if enable_pos_tag == "true":
                words = pseg.cut(s)
                s = []
                for word, flag in words:
                    s.append(word + pos_tag_separator + flag)
                    #print('%s %s' % (word, flag))
                s = (separator+" ").join(s)
            seg_list_filtered.append(s)

    result = (separator+" ").join(seg_list_filtered)
    print("Result: " + result)

    
