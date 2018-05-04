#!/usr/bin/python
# -*- coding: UTF-8 -*-
execfile("install_packages.py")
win_unicode_console.enable()

configParser = ConfigParser.RawConfigParser()   
configParser.read("config/config.ini")

mode = configParser.get("jieba-config", "mode")
separator = configParser.get("jieba-config", "separator")
jieba.set_dictionary(configParser.get("jieba-config", "user_dict"))
jieba.analyse.set_stop_words(configParser.get("jieba-config", "stop_words"))
with open(configParser.get("jieba-config", "stop_words")) as f:
    stopwords = f.readlines()

all_files = filemapper.load(configParser.get("jieba-config", "input_dir"))
for f in all_files:
    if f == ".gitignore": 
        continue

    content = ""
    for i in filemapper.read(f):content = content+i
    #print(content)
    
    if mode == "exact":
        seg_list = jieba.cut(content, cut_all=False)
    elif mode == "all":
        seg_list = jieba.cut(content, cut_all=True)
    elif mode == "search":
        seg_list = jieba.cut_for_search(content)
    else:
        seg_list = jieba.cut(content, cut_all=False)

    result = (separator+" ").join(seg_list)
    print("Result: " + result)

    
