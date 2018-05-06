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
save_pos_tag_field = configParser.get("pos", "save_pos_tag_field")
enable_csv_to_arff = configParser.get("arff", "enable_csv_to_arff")
export_text_feature = configParser.get("arff", "export_text_feature")


user_dict_file = configParser.get("config", "user_dict")
if os.stat(user_dict_file).st_size > 0:
    jieba.set_dictionary(user_dict_file)

stopwords = []
stopwords_file = configParser.get("config", "stop_words")
if os.stat(stopwords_file).st_size > 0:
    jieba.analyse.set_stop_words(stopwords_file)
    with codecs.open(stopwords_file,'r',encoding='utf8') as f:
        stopwords = f.read()

input_dir = configParser.get("file", "input_dir")
all_files = filemapper.load(configParser.get("file", "input_dir"))
output_dir = configParser.get("file", "output_dir")

def exec_segment(content):
    content = content.strip()
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
    pos_tag_list = []
    seg_list_filtered_count = 0
    distinct_words = {}
    
    for s in seg_list:
        try:
            stopword_index = stopwords.index(s)
        except ValueError:
            p = []
            if enable_pos_tag == "true":
                words = pseg.cut(s)
                s = []
                p = []
                for word, flag in words:
                    if flag != "eng":
                        if save_pos_tag_field == "false":
                            s.append(word + pos_tag_separator + flag)
                        else:
                            s.append(word)
                            p.append(flag)
                        seg_list_filtered_count = seg_list_filtered_count + 1
                        distinct_words = add_distinct_words(distinct_words, word)
                    else:
                        #print(word)
                        pypos_words = Lexer().lex(word)
                        pypos_tagged_words 	= POSTagger().tag(pypos_words)
                        for x in pypos_tagged_words:
                            word = x[0]
                            tag  = x[1]
                            if save_pos_tag_field == "false":
                                s.append(word + pos_tag_separator + tag)
                            else:
                                s.append(word)
                                p.append(tag)
                            seg_list_filtered_count = seg_list_filtered_count + 1
                            distinct_words = add_distinct_words(distinct_words, word)
                    #print('%s %s' % (word, flag))
                s = (separator+" ").join(s)
                p = (separator+" ").join(p)
            else:
                seg_list_filtered_count = seg_list_filtered_count + 1
                distinct_words = add_distinct_words(distinct_words, word)
            seg_list_filtered.append(s)
            pos_tag_list.append(p)
    #print(pos_tag_list)
    if save_pos_tag_field == "false" or enable_pos_tag == "false":
        result = (separator+" ").join(seg_list_filtered)
        return result
    else:
        result = []
        result.append((separator+" ").join(seg_list_filtered))
        result.append((separator+" ").join(pos_tag_list))
        if export_text_feature == "true":
            result.append(str(len(content)))
            #print(seg_list_filtered)
            #print(str(seg_list_filtered_count)) 
            result.append(str(seg_list_filtered_count))            
            result.append(str(len(distinct_words.keys())))
            entropy = 0
            for word in distinct_words:
                freq = distinct_words[word]
                prop = freq / (seg_list_filtered_count * 1.0)
                if prop > 0:
                    e = prop * log(prop)
                    entropy = entropy + e
            entropy = entropy * -1
            result.append(str(entropy))            
        return result

def add_distinct_words(distinct_words, word):
    if word in distinct_words:
        distinct_words[word] = distinct_words[word]+1
    else:
        distinct_words[word] = 1
    return distinct_words
        
def write_file(filename, content):
    #print("File: " + filename)
    #print(content)
    file = codecs.open(filename, "w", "utf-8")
    file.write(content)
    file.close()

for f in all_files:
    if f == ".gitignore": 
        continue
    elif f.endswith(".txt"):
        content = ""
        for i in filemapper.read(f):content = content+i
        #print(content)
        result = exec_segment(content)
        if isinstance(result, list):
            result = ",".join(result)
        
        write_file(output_dir + "/" + f, result)
    elif f.endswith(".csv"):
        reader = unicode_csv_reader(open(input_dir + "/" + f))
        #print(f)
        is_header = True
        lines = []
        for fields in reader:
            line = []
            for field in fields:
                
                if is_header == True:
                    result = field
                    line.append(result)
                    if save_pos_tag_field == "true"  or enable_pos_tag == "true":
                        line.append(result + "_pos")
                    if export_text_feature == "true":
                        line.append(result + "_len")
                        line.append(result + "_seg_len")
                        line.append(result + "_types_count")
                        line.append(result + "_entropy_count")
                else: 
                    result = exec_segment(field)
                    #print(result)
                    if isinstance(result, list):
                        for r in result:
                            line.append(r)
                    else:
                        line.append(result)
            #lines.append('"' + ('","').join(line) + '"')
            lines.append(line)
            
            if is_header == True:
                is_header = False

        content = ""
        if enable_csv_to_arff == "true":
            content = "@RELATION " + f + "\n\n"
            for i, line in enumerate(lines):
                if i == 0:
                    for attr in line:
                        if attr.endswith("_len") or attr.endswith("_count"):
                            content = content + "@ATTRIBUTE " + attr + " NUMERIC" + "\n"
                        else:
                            content = content + "@ATTRIBUTE " + attr + " STRING" + "\n"
                        
                    content = content + "\n@DATA"
                else:
                    content = content + '\n"' + ('","').join(line) + '"'
            f = f + ".arff"
        else:
            for i, line in enumerate(lines):
                lines[i] = '"' + ('","').join(line) + '"'
            content = ("\n").join(lines)
                
        write_file(output_dir + "/" + f, content)
            
            
        
