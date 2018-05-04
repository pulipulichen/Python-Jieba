#!/usr/bin/python
# -*- coding: UTF-8 -*-
import pip

def install(package):
    pip.main(['install', package])

try:
    import jieba
except ImportError, e:
    install("jieba")
    import jieba
