# -*- coding: utf-8 -*-

import re
import json

p_dialog = re.compile(r'^— .+[.!?]$')
p_dialog_with_comm = re.compile(r'[.!?]*[^.!?]+:$\n^— .+[.!?]$', flags=re.MULTILINE)
p_speech = re.compile(r'[^.!?]*: «[^»]*»')


# -*- coding: utf-8 -*-

def speech_from_text(file):
    f = open(file, 'r', encoding= 'utf-8')
    allspeecheslist = []
    speechlist = []
    previous_line = ''
    for line in f:
        if len(line) > 1:
          two_lines = previous_line + line
          sample = line.strip()
          flag = False
          for elem in sample:
            if elem in '1234567890':
              flag = True
            else:
              flag = False
              break
          if flag == True:
            allspeecheslist.append(speechlist)
            speechlist = []
          resultdialog_with_comm = p_dialog_with_comm.findall(two_lines)
          if len(resultdialog_with_comm) != 0:
              speechlist.extend(resultdialog_with_comm)
          resultdialog = p_dialog.findall(line)
          if len(resultdialog) != 0:
            flag = True
            if len(resultdialog_with_comm) != 0:
              for elem in resultdialog_with_comm:
                if resultdialog[0] in elem:
                  flag = False
            if flag == True:
              speechlist.extend(resultdialog)
          resultspeech = p_speech.findall(line)
          if len(resultspeech) != 0:
              speechlist.extend(resultspeech)
          previous_line = line
    allspeecheslist.append(speechlist)
    f.close()
    
    return allspeecheslist
myli = speech_from_text('belaya_gvardia.txt')

p_author2 = re.compile(r'^(— .+[,.!?]+) — ([^—]+\.) — (.+)$')
p_author3 = re.compile(r'^(— .+[,.!?]+) — ([^—]+,) — (.+)$')
p_speechandauthor1 = re.compile(r'^— ([^—]+[,.?!]) — ([^—]+\.)$')
p_author4 = re.compile(r'^(— [^—]+[.!?]+)$')
p_multilineauthor = re.compile(r'[.!?]*([^.!?]+:)\n(— .+[.!?])$')
p_speech_quotmarks = re.compile(r'([^.!?]*:) («[^»]*»)')



def author_com_from_dialog(dialoglist):
  all_author_comments = []
  authors_comments = []
  for chapter in dialoglist:
    for dialog in chapter:
      authorlist_multiline = p_multilineauthor.findall(dialog)
      if len(authorlist_multiline) != 0:
          authors_comments.extend(authorlist_multiline)
      authorlist1 = p_speechandauthor1.findall(dialog)
      if len(authorlist1) != 0:
          authors_comments.extend(authorlist1)
      authorlist2 = p_author2.findall(dialog)
      if len(authorlist2) != 0:
          authors_comments.extend(authorlist2)
      authorlist3 = p_author3.findall(dialog)
      if len(authorlist3) != 0:
          authors_comments.extend(authorlist3)
      authorlist4 = p_author4.findall(dialog)
      if len(authorlist4) != 0:
          authors_comments.extend(authorlist4)
      quotspeechlist = p_speech_quotmarks.findall(dialog)
      if len(quotspeechlist) != 0:
          authors_comments.extend(quotspeechlist)
    all_author_comments.append(authors_comments)
    authors_comments = []
      
  return all_author_comments

delimited_speech = author_com_from_dialog(myli)


def write_to_json(speech_and_comments):
  with open('results.json', 'w', encoding='utf-8') as f:
      jsonspeeches = {'chapter': 'all'}
      listforjson = []
      speechesdilist = []
      counter = 0
      for chapter in speech_and_comments:
        jsonspeeches = {'chaper': counter}
        for elem in chapter:
          newdi = {}
          if type(elem) != tuple:
            newdi['author'] = 'undefined'
            newdi['speech'] = elem
            newdi['author_text'] = None
          elif type(elem) == tuple and len(elem) == 2:
            if elem[0][-1] == ':':
              newdi['author'] = 'undefined'
              newdi['speech'] = elem[-1]
              newdi['author_text'] = elem[0]
            else:
              newdi['author'] = 'undefined'
              newdi['speech'] = elem[0]
              newdi['author_text'] = elem[-1]
          elif type(elem) == tuple and len(elem) == 3:
            newdi['author'] = 'undefined'
            newdi['speech'] = elem[0] + ' ' + elem[-1]
            newdi['author_text'] = elem[1]
          if newdi not in speechesdilist:
            speechesdilist.append(newdi)
        
        jsonspeeches['speeches'] = speechesdilist
        listforjson.append(jsonspeeches)
        counter += 1
        speechesdilist = []
      
      f.write(json.dumps(listforjson, ensure_ascii = False))

write_to_json(delimited_speech)
