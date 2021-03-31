# -*- coding: utf-8 -*-

import re

p_dialog = re.compile(r'^— .*[.!?]$')
p_speech = re.compile(r'[^.!?]*: «.*»\.')

def speech_from_text(file):
    f = open(file, 'r', encoding= 'utf-8')
    speechlist = []
    for line in f:
        resultdialog = p_dialog.findall(line)
        if len(resultdialog) != 0:
            speechlist.extend(resultdialog)
        resultspeech = p_speech.findall(line)
        if len(resultspeech) != 0:
            speechlist.extend(resultspeech)
    f.close()

    return speechlist
#for i in speech_from_text('belaya_gvardia.txt'):
  #print(i)
myli = speech_from_text('belaya_gvardia.txt')

p_author2 = re.compile(r'[,...!?] — [^—]*\. — ')
p_author3 = re.compile(r'[,...!?] — [^—]*, — ')
p_speechandauthor1 = re.compile(r'^— [^—]*[,.] — [^—]*\.$')
p_author1 = re.compile(r', — [^—]*\.')

def author_com_from_dialog(dialoglist):
  authors_comments = []
  for dialog in dialoglist:
    authorlist1 = p_speechandauthor1.findall(dialog)
    if len(authorlist1) != 0:
      for elem in authorlist1:
        result = p_author1.findall(elem)
        if len(result) != 0:
            authors_comments.extend(result)
    authorlist2 = p_author2.findall(dialog)
    if len(authorlist2) != 0:
        authors_comments.extend(authorlist2)
    authorlist3 = p_author3.findall(dialog)
    if len(authorlist3) != 0:
        authors_comments.extend(authorlist3)
      
  return authors_comments


for i in author_com_from_dialog(myli):
  print(i)
