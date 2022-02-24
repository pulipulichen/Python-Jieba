# Python-Jieba
A jieba application for desktop user

# Installation

1. Install git: https://github.com/git-guides/install-git .
2. Clone this project into your computer by `git clone https://github.com/pulipulichen/Python-Jieba.git` .
3. Install docker-compose: https://docs.docker.com/compose/install/ .
4. Run `docker-compose build` .

# Usage

1. Put file into the input directory.
2. Run `docker-compose up` .
3. Get the result in the output directory.

----

# Txt格式輸出

各欄位說明：
1. 所有斷詞結果
2. 所有斷詞結果對應的詞性
3. 原本字數
4. 斷詞數量
5. 詞性類型的數量
6. 用詞的entropy：數字越大，表示使用字詞越多元
7. 詞性的entropy：數字越大，表示使用詞性越多元

# Reference
- Jeiba (Python): https://github.com/fxsjy/jieba#%E4%B8%BB%E8%A6%81%E5%8A%9F%E8%83%BD
- jieba-zh_TW: https://github.com/ldkrsi/jieba-zh_TW
- pypos : for English POS tags https://github.com/th0ma5w/pyPartOfSpeech
- POS tags help: http://blog.pulipuli.info/2017/11/fasttag-identify-part-of-speech-in.html
- 停用詞表：
  - 停用詞.txt https://github.com/tomlinNTUB/Machine-Learning/blob/master/data/%E5%81%9C%E7%94%A8%E8%A9%9E.txt
  - 停用詞-繁體中文.txt https://github.com/tomlinNTUB/Machine-Learning/blob/master/data/%E5%81%9C%E7%94%A8%E8%A9%9E-%E7%B9%81%E9%AB%94%E4%B8%AD%E6%96%87.txt
- 107年國慶大會總統致詞 https://www.president.gov.tw/News/23769