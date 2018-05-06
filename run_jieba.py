#!/usr/bin/python
# -*- coding: UTF-8 -*-
# coding=UTF-8
execfile("install_packages.py")
jieba.dt.cache_file = 'jieba.cache.new'
win_unicode_console.enable()

configParser = ConfigParser.RawConfigParser()   
configParser.read("config/config.ini")

mode = configParser.get("config", "mode")
separator = configParser.get("config", "separator")
enable_pos_tag = configParser.get("pos", "enable_pos_tag")
pos_tag_separator = configParser.get("pos", "pos_tag_separator")

user_dict_file = configParser.get("config", "user_dict")
if os.stat(user_dict_file).st_size > 0:
    jieba.set_dictionary(user_dict_file)

stopwords = []
stopwords_file = configParser.get("config", "stop_words")
if os.stat(stopwords_file).st_size > 0:
    jieba.analyse.set_stop_words(stopwords_file)
    with codecs.open(stopwords_file,'r',encoding='utf8') as f:
        stopwords = f.read()

all_files = filemapper.load(configParser.get("file", "input_dir"))
output_dir = configParser.get("file", "output_dir")
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
            stopword_index = stopwords.index(s)
        except ValueError:
            if enable_pos_tag == "true":
                words = pseg.cut(s)
                s = []
                for word, flag in words:
                    if flag != "eng":
                        s.append(word + pos_tag_separator + flag)
                    else:
                        pypos_words = Lexer().lex(word)
                        pypos_tagged_words 	= POSTagger().tag(pypos_words)
                        for x in pypos_tagged_words:
                            word = x[0]
                            tag  = x[1]
                            s.append(word + pos_tag_separator + tag)
                    #print('%s %s' % (word, flag))
                s = (separator+" ").join(s)
            seg_list_filtered.append(s)

    result = (separator+" ").join(seg_list_filtered)
    print("Result: " + result)
    file = codecs.open(output_dir + "/" + f, "w", "utf-8")
    file.write(result)
    file.close()

    
