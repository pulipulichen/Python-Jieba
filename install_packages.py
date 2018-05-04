#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os
import pip

def install(package):
    pip.main(['install', package])

try:
    import jieba
    import jieba.analyse
except ImportError, e:
    install("jieba")
    import jieba
    import jieba.analyse

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
