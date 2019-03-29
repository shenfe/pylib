# coding: utf8

from __future__ import print_function

import libcpp


def test():
    a = libcpp.args()
    a.input = 'i'
    a.output = 'o'
    print(a.dumpArgs())
