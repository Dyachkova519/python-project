import re
def speech_from_text(file):
    f = open(file, 'r', encoding= 'utf-8')
    speechlist = []
    for line in f:
        resultdialog = re.findall(r'^— [^—]*[.!?]$', line)#вытаскивает реплики, которые оканчиваются точкой без авторских комментариев. но сюда не попадают реплики, врутри которых есть тире :(
  #можно поменять регулярку на '^— .*[.!?]$', тогда ей вытаскиваются все (кажется) виды диалогов, в том числе с авторскими комментариями внутри. может, так даже лучше, но не очень понятно, как отделять зёрна от плевел
        if len(resultdialog) != 0:
            speechlist.extend(resultdialog)
        resultspeech = re.findall(r'[^.!?]*: ".*"\.', line)
        if len(resultspeech) != 0:
            speechlist.extend(resultspeech)
    f.close()

    return speechlist

print(speech_from_text('belaya_gvardia.txt'))