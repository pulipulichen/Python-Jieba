#!/usr/bin/python
# -*- coding: UTF-8 -*-
# coding=UTF-8
execfile("install_packages.py")
jieba.dt.cache_file = 'jieba.cache.new'


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
        
stop_pos_tags = []
stop_pos_tags_file = configParser.get("pos", "stop_pos_tags")
if os.stat(stop_pos_tags_file).st_size > 0:
    with codecs.open(stop_pos_tags_file,'r',encoding='utf8') as f:
        stop_pos_tags = f.read()

input_dir = configParser.get("file", "input_dir")
all_files = filemapper.load(configParser.get("file", "input_dir"))
output_dir = configParser.get("file", "output_dir")

def in_string(str1, str2):
    try:
        i = str1.index(str2)
        return True
    except ValueError:
        try:
            i = str2.index(str1)
            return True
        except ValueError:
                return False

def cut_result_to_list(result):
    output = []
    for s in result:
        output.append(s)
    return output

def exec_segment(content):
    content = content.strip()
    seg_list = []
    if mode == "exact":
        seg_list = jieba.cut(content, cut_all=False)
    elif mode == "all":
        seg_list = jieba.cut(content, cut_all=True)
    elif mode == "search":
        seg_list = jieba.cut_for_search(content)
    elif mode == "mix":
        temp_seg_list = jieba.cut_for_search(content)
        for s in temp_seg_list:
            seg_list.append(s)
        
        temp_seg_list = jieba.cut(content, cut_all=True)
        temp_seg_list = cut_result_to_list(temp_seg_list)
        for j, t in enumerate(temp_seg_list):
            t = temp_seg_list[(len(temp_seg_list) - j - 1)]
            if list_index_of(seg_list, t) == -1:
                # 如果找不到這個字...再來決定要插入在那個位置
                found = False
                for i, s in enumerate(seg_list):
                    if in_string(t, s):
                        # 位置在i
                        if len(s) > len(t):
                            i = i+1
                        seg_list.insert(i, t)
                        found = True
                        break
                if found == False:
                    seg_list.append(t)
                    
        temp_seg_list = jieba.cut(content, cut_all=False)
        temp_seg_list = cut_result_to_list(temp_seg_list)
        for j, t in enumerate(temp_seg_list):
            t = temp_seg_list[(len(temp_seg_list) - j - 1)]
            if list_index_of(seg_list, t) == -1:
                # 如果找不到這個字...再來決定要插入在那個位置
                found = False
                for i, s in enumerate(seg_list):
                    if in_string(t, s):
                        # 位置在i
                        if len(s) > len(t):
                            i = i+1
                        seg_list.insert((i+1), t)
                        found = True
                        break
                if found == False:
                    seg_list.append(t)
        
    else:
        seg_list = jieba.cut(content, cut_all=False)

    seg_list_filtered = []
    pos_tag_list = []
    seg_list_filtered_count = 0
    distinct_words = {}
    distinct_pos = {}
    
    for s in seg_list:
        if s.strip() == "":
            continue
    
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
                        if list_index_of(stop_pos_tags, flag) > -1:
                            continue
                        
                        if save_pos_tag_field == "false":
                            s.append(word + pos_tag_separator + flag)
                        else:
                            s.append(word)
                            p.append(flag)
                        seg_list_filtered_count = seg_list_filtered_count + 1
                        distinct_words = add_distinct_words(distinct_words, word)
                        distinct_pos = add_distinct_words(distinct_pos , flag)
                    else:
                        #print(word)
                        pypos_words = Lexer().lex(word)
                        pypos_tagged_words 	= POSTagger().tag(pypos_words)
                        for x in pypos_tagged_words:
                            word = x[0]
                            tag  = x[1]
                            if list_index_of(stop_pos_tags, tag) > -1:
                                continue
                            
                            if save_pos_tag_field == "false":
                                s.append(word + pos_tag_separator + tag)
                            else:
                                s.append(word)
                                p.append(tag)
                            seg_list_filtered_count = seg_list_filtered_count + 1
                            distinct_words = add_distinct_words(distinct_words, word)
                            distinct_pos = add_distinct_words(distinct_pos , tag)
                    #print('%s %s' % (word, flag))
                s = (separator+" ").join(s)
                p = (separator+" ").join(p)
            else:
                seg_list_filtered_count = seg_list_filtered_count + 1
                distinct_words = add_distinct_words(distinct_words, word)
            
            if len(s) > 0:
                seg_list_filtered.append(s)
                pos_tag_list.append(p)
    #print(pos_tag_list)
    if save_pos_tag_field == "false" or enable_pos_tag == "false":
        result = (separator+" ").join(seg_list_filtered)
        return result
    else:
        result = []
        result.append((separator+" ").join(seg_list_filtered))
        if enable_pos_tag == "true":
            result.append((separator+" ").join(pos_tag_list))
        if export_text_feature == "true":
            result.append(str(len(content)))
            #print(seg_list_filtered)
            #print(str(seg_list_filtered_count)) 

            # 斷詞後的結果
            result.append(str(seg_list_filtered_count)) 

            # 詞性的種類
            if enable_pos_tag == "true":
                result.append(str(len(distinct_pos.keys()))) 
            #result.append("2")

            # 用詞的entropy
            entropy = 0
            for word in distinct_words:
                freq = distinct_words[word]
                prop = freq / (seg_list_filtered_count * 1.0)
                if prop > 0:
                    e = prop * log(prop)
                    entropy = entropy + e
            entropy = entropy * -1
            result.append(str(entropy))

            # 詞性的entropy
            if enable_pos_tag == "true":
                entropy = 0
                for pos in distinct_pos:
                    freq = distinct_pos[pos]
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

def list_index_of(list, item):
    try:
        return list.index(item)
    except ValueError:
        return -1
    
def write_file(filename, content):
    try:
        print("File: " + filename)
    except UnicodeDecodeError:
        print("File")
    print(content)
    file = codecs.open(filename, "w", "utf-8")
    file.write(content)
    file.close()

# -----------------------

win_unicode_console.enable()
if len(sys.argv) > 1: #len小於2也就是不帶參數啦
    sys.argv = map(lambda arg: arg.decode(sys.stdout.encoding), sys.argv)
    text = " ".join(sys.argv[1:])
    #print(exec_segment(text))
    text = unicode(text, 'utf-8')
    print(text)
    sys.exit()

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
        
        write_file(output_dir + "/" + f + ".csv", result)
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
                        if (enable_pos_tag == "true"):
                            line.append(result + "_pos_count")
                        line.append(result + "_entropy_count")
                        if (enable_pos_tag == "true"):
                            line.append(result + "_pos_entropy_count")
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
            content = "@RELATION " + "csv" + "\n\n"
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
            
            
        
