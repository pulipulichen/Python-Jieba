#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os
import pip
import io

def install(package):
    pip.main(['install', package])

try:
    import jieba
    import jieba.analyse
    import jieba.posseg as pseg
except ImportError, e:
    install("jieba")
    import jieba
    import jieba.analyse
    import jieba.posseg as pseg

try:
    import win_unicode_console
except ImportError, e:
    install("win_unicode_console")
    import win_unicode_console

try:
    import ConfigParser
except ImportError, e:
    install("ConfigParser")
    import ConfigParser

try:
    import filemapper
except ImportError, e:
    install("filemapper")
    import filemapper

try:
    import codecs
except ImportError, e:
    install("codecs")
    import codecs
    
from Lexer import Lexer
from POSTagger import POSTagger