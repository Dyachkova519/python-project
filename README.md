# Определение прямой речи в художественном тексте
поиск диалогов и прямой речи в художественных текстах с использованием regexp
## Подробное описание

- Что должно получится в итоге (консольная программа, бот, что-то еще)? Итог проекта - консольная программа
- Что ваша программа принимает как входные данные? На вход программа принимает текстовые файлы
- Какие модули программа будет использовать (re, math)? Поставленная задача решается с помощью регулярных выражений, модуль re, для записи результатов в json-файл используется модуль json
- Для работы используется текст романа М. А. Булгакова "Белая гвардия".
- Реплики персонажей (прямая речь и диалоги) записываются в json-файл вместе с именем говорящего (если его возможно установить), имена говоряещих будут извлекаться из текста с помощью библиотеки natasha. (Мне кажется, можно в качестве ключей использовать ~5 имен главных героев, остальных оставить Undefined)
- Пример json-файла:
```
[
  {
    "chapter": "2",
    "speeches": 
      [
        {"author": "Николка", "speech": "Ничего не известно,", "author_text": "говорит Николка и обкусывает ломтик."}
        {"author": "Undefined", "speech": "Это я так сказал, гм... предположительно. Слухи.", "author_text": None}
        {"author": "Елена", "speech": "Нет, не слухи,  это  не  слух,  а  верно; сегодня видела Щеглову, и она сказала, что из-под  Бородянки  вернули  два немецких полка.", "author_text": упрямо отвечает Елена,"}
      ]
  }
]
```
- Основные способы оформить прямую речь по Д. Э. Розенталю:
> -- П.!?...

> -- П, -- а.

> -- П, -- а. -- П.

> -- П, -- а, -- п.

> -- П!?... -- а. -- П.

> А: "П!?...".

> "П", -- а.

> "П!?..." -- А.

## Критерий завершенного проекта

Программа может при получении файла с текстом художественного произведения диалоги и прямую речь из него записать в отдельный файл json.

## Команда проекта

- Дьячкова Мария Дмитриевна, БКЛ-204

## Таймлайн проекта

- 14.03.21: описание проекта
- 22.03.21: функция, работающая с несколькими видами прямой речи
- 31.03.21: функция, разделяющая прямую речь на слова автора и речь персонажа
- 12.04.21: функция, записывающая слова автора и персонажа в файл json по главам
- 19.04.21: расширен список регулярных выражений для более точного поиска прямой речи

## Чего вам не хватает для реализации проекта

- Что надо еще узнать? Как работает библиотека natasha
- Какие-то другие проблемы
- ...

## Распределение обязанностей в команде

По каждому человеку, кто и что будет делать
