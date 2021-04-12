# -*- coding: utf-8 -*-

import re
import json

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

p_author2 = re.compile(r'^(— .+[,.!?]+) — ([^—]+\.) — (.+)$')
p_author3 = re.compile(r'^(— .+[,.!?]+) — ([^—]+,) — (.+)$')
p_speechandauthor1 = re.compile(r'^— ([^—]+[,.]) — ([^—]+\.)$')
p_author4 = re.compile(r'^(— [^—]+[.!?]+)$')

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


delimited_speech = author_com_from_dialog(myli)

def write_to_json(speech_and_comments):
  with open('results.json', 'w', encoding='utf-8') as f:
      jsonspeeches = {'chapter': 'all'}
      speechesdilist = []
      for elem in speech_and_comments:
        newdi = {}
        if type(elem) != tuple:
          newdi['author'] = 'undefined'
          newdi['speech'] = elem
          newdi['author_text'] = None
        elif type(elem) == tuple and len(elem) == 2:
          newdi['author'] = 'undefined'
          newdi['speech'] = elem[0]
          newdi['author_text'] = elem[-1]
        elif type(elem) == tuple and len(elem) == 3:
          newdi['author'] = 'undefined'
          newdi['speech'] = elem[0] + ' ' + elem[-1]
          newdi['author_text'] = elem[1]
        speechesdilist.append(newdi)
      jsonspeeches['speeches'] = speechesdilist
      listforjson = [jsonspeeches]
      
      f.write(json.dumps(listforjson, ensure_ascii = False))

write_to_json(delimited_speech)
