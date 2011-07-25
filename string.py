#!/usr/bin/env python
# -*- coding: utf-8 -*-

s = u'Hallo Welt!'
print ' '.join(s.split()[::-1]) # Welt! Hallo
#s = 112
#print len(s)
s = s[::-1]
print s # !tleW ollaH
print ''.join([char for char in reversed(s)]) # Hallo Welt!
s = s[::-1]
print ''.join([s[len(s) -1 -i] for i in range(len(s))]) # !tleW ollaH
s = s[::-1]
print ''.join([s[i] for i in range(len(s) -1, -1, -1)]) # Hallo Welt!
