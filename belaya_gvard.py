#pip install pymorphy2

#pip install natasha

# -*- coding: utf-8 -*-
import re
import json
import pymorphy2
from string import punctuation
from natasha import (Segmenter, MorphVocab, NewsEmbedding, 
NewsMorphTagger, NewsSyntaxParser, NewsNERTagger, PER, NamesExtractor, Doc)
morph = pymorphy2.MorphAnalyzer()

p_dialog = re.compile(r'^— .+[.!?]$')
p_dialog_with_comm = re.compile(r'[.!?]*[^.!?]+:$\n^— .+[.!?]$', flags=re.MULTILINE)
p_speech = re.compile(r'[^.!?]*: «[^»]*»')



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


p_author2 = re.compile(r'^— ([^—]+[,.!?]+) — ([^—]+\.) — ([^—]+)$')
p_author3 = re.compile(r'^— ([^—]+[,.!?]+) — ([^—]+,) — ([^—]+)$')
p_speechandauthor1 = re.compile(r'^— ([^—]+[,.?!]) — ([^.—]+\.)$')
p_author4 = re.compile(r'^— ([^—]+[.!?]+)$')
p_multilineauthor = re.compile(r'[.!?]*([^.!?]+:)\n— ([^—]+[.!?])$')
p_multilineauthor2 = re.compile(r'[.!?]*([^.!?]+:)\n— ([^—]+[.,!?]) — ([^—]+\.)$')
p_speech_quotmarks = re.compile(r'([^.!?]+:) («[^»]+»)')


def author_com_from_dialog(dialoglist):
  all_author_comments = []
  authors_comments = []
  for chapter in dialoglist:
    for dialog in chapter:
      authorlist_multiline = p_multilineauthor.findall(dialog)
      if len(authorlist_multiline) != 0:
          authors_comments.extend(authorlist_multiline)
      authorlist_multiline2 = p_multilineauthor2.findall(dialog)
      if len(authorlist_multiline2) != 0:
          authors_comments.extend(authorlist_multiline2)
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


def create_big_dictionary(speech_and_comments):
    jsonspeeches = {'chapter': 'all'}
    listforjson = []
    speechesdilist = []
    counter = 0
    for chapter in speech_and_comments:
      jsonspeeches = {'chapter': counter}
      for elem in chapter:
        newdi = {}
        if type(elem) != tuple:
          newdi['author_in_text'] = 'undefined'
          newdi['authors_name'] = 'undefined'
          newdi['speech'] = elem
          newdi['author_text'] = None
        elif type(elem) == tuple and len(elem) == 2:
          if elem[0][-1] == ':':
            newdi['author_in_text'] = 'undefined'
            newdi['authors_name'] = 'undefined'
            newdi['speech'] = elem[-1]
            newdi['author_text'] = elem[0]
          else:
            newdi['author_in_text'] = 'undefined'
            newdi['authors_name'] = 'undefined'
            newdi['speech'] = elem[0]
            newdi['author_text'] = elem[-1]
        elif type(elem) == tuple and len(elem) == 3:
          if elem[0][-1] == ':':
            newdi['author_in_text'] = 'undefined'
            newdi['authors_name'] = 'undefined'
            newdi['speech'] = elem[1]
            newdi['author_text'] = elem[0] + ' ' + elem[-1]
          elif elem[0][-1] != ':':
            newdi['author_in_text'] = 'undefined'
            newdi['authors_name'] = 'undefined'
            newdi['speech'] = elem[0] + ' ' + elem[-1]
            newdi['author_text'] = elem[1]
        if newdi not in speechesdilist:
          speechesdilist.append(newdi)
        
      jsonspeeches['speeches'] = speechesdilist
      listforjson.append(jsonspeeches)
      counter += 1
      speechesdilist = []
      
      
    return listforjson
      
create_big_dictionary(delimited_speech)
outerlist = create_big_dictionary(delimited_speech)


segmenter = Segmenter()
morph_vocab = MorphVocab()
emb = NewsEmbedding()
morph_tagger = NewsMorphTagger(emb)
syntax_parser = NewsSyntaxParser(emb)
ner_tagger = NewsNERTagger(emb)
names_extractor = NamesExtractor(morph_vocab)

characters = ["Алексей Турбин", "Турбин", "Алексей", "Елена", "Николка", "Мышлаевский", "Шервинский", "Карась",  "Тальберг", "Щеткин", "Василиса", "Лариосик", "Най-Турс", "Най", "старший"]
charactdict = {"Алексей Турбин": ["Алексей Турбин", "Турбин", "Алексей", "старший"], "Най-Турс": ["Най-Турс", "Най"]}

def define_speechs_author(bigoutputdict, charlist, chardi):
  for chap in bigoutputdict:
    speeches = chap['speeches']
    for onespeech in speeches:
      if onespeech['author_text'] != None:
        texttosearch = onespeech['author_text']
       
        for i in texttosearch.split():
          word = i.strip(punctuation).strip()
          if len(word) != 1:
            for i in morph.parse(word):
              if (("NOUN" in i.tag) and ("anim" in i.tag) and ('nomn' in i.tag) and ('plur' not in i.tag)) or word == "Николка" or word == "старший" or word == "Най":
                  #print(word)
                  if word in charlist:
                    onespeech['author_in_text'] = word
                    for key in chardi:
                      if word in chardi[key]:
                        onespeech['authors_name'] = key
                    if onespeech['authors_name'] == 'undefined':
                      onespeech['authors_name'] = word
                
        texttosearch = onespeech['author_text']
        natashatext = Doc(texttosearch)
        natashatext.segment(segmenter)
        natashatext.tag_morph(morph_tagger)
        textnames = ''
        for token in natashatext.tokens:
          if ((token.pos == "NOUN"  and 'Animacy' in token.feats and token.feats['Animacy'] == 'Anim') or (token.pos == "PROPN")) and 'Case' in token.feats and (token.feats['Case'] == 'Nom'):
            textnames += str(token.text) + ' '
        namestoanalize = Doc(textnames)
        namestoanalize.segment(segmenter)
        namestoanalize.tag_ner(ner_tagger)
        if len(namestoanalize.spans) != 0:
          for span in namestoanalize.spans:
            if onespeech['author_in_text'] in str(span.text) and onespeech['author_in_text'] != str(span.text) and str(span.text) in charlist:
              onespeech['author_in_text'] = str(span.text)

  with open('resultswithauth.json', 'w', encoding='utf-8') as f:
    f.write(json.dumps(bigoutputdict, ensure_ascii = False))
define_speechs_author(outerlist, characters, charactdict)
