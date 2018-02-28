#!/usr/bin/env python3.4
import os,sys
import time, datetime
import cgi, cgitb #для обмена с браузером
cgitb.enable()    #для отладки
sys.stderr  =  sys.stdout

import pymysql #для обмена с базой данных
#import py_form_processing #для обработки строки запроса
#import py_matplot #столбиковые и точечные диаграммы
#import py_sql_test_cgi #для тестирования CGI
#import py_pavl_02 #вариант лабораторной работы
#import py_sql_visits #записываем посещаемость в базу, считываем обработанные данные из базы и записываем в файл 
#import py_sql_shop #магазина
#после подключения модулей не забыть вызвать (раскомментировать) вызовы соответствующих функций в файлах



#лучше поместить здесь для тестирования отладки с использованием браузера 
print('''\
Content-type:text/html\r\n
''', end = '')

domen = "g04u58.nn2000.info" #указать свой домен
words = ('http://',domen, '/cgi-bin/py_sql_pages.py')
href_py_file = "".join(words) # абсолютный адрес движка сайта
#print(href_py_file)

#разбираем строку запроста 
qr_string  =  cgi.FieldStorage() 
'''
print (type(qr_string))
print (qr_string)
print ("qr_string.keys:",qr_string.keys())
for key in qr_string.keys():
    print (str(key),"=",qr_string.getvalue(key))
'''

function = qr_string.getvalue("function") #получаем значения переменных, укащзанных в строке запроса
page_id = qr_string.getvalue("page_id")

if "function" not in qr_string: #если строки запроса нет -  присваиваем для исключения ошибок 
    function = "page"
    page_id = 1

#соединяемся с базой данных
db  =  pymysql.connect(host = "127.0.0.1", user = "g04u58", passwd = "mysql16", db = "g04u58", charset = "utf8",use_unicode = True) # Open database connection
cur  =  db.cursor() # prepare a cur object using cursor() method
cur.execute('SET NAMES utf8') # execute SQL query using execute() method
#отладочное считывание содержимого базы данных
'''
cur.execute("""SELECT * FROM `sql_pages`""") 
db_all  =  cur.fetchall()
print("db_all:",type(db_all),db_all,sep="\n\n", end="\n\n\n")
'''

#   готовим данные для заголовка страницы
#   `page_id` -значение записи в поле базы данных  ; (page_id)  - значение переменной в строе запроса   
#    сравнением получаем нужную запись в получаем соответствующие значения для заголовка страницы 
cur.execute("""SELECT `page_title`, `page_keywords` FROM `sql_pages` WHERE `page_id`  =  %s""",(page_id))
db_one  =  cur.fetchone()
#print("\nto head: \ntype(db_one),db_one\n",type(db_one),db_one, sep=" ", end="\n\n")
page_title = str(db_one[0])
page_keywords = str(db_one[1])

#   начинаем форомировать страницу
print('''\
<!DOCTYPE html>
<html>
<head>
<meta http-equiv = "Content-Type" CONTENT = "text/html; charset = utf-8">
''', end = '')
print('<title>', page_title,'</title>', sep = '', end = '')
print('\n<link rel = "stylesheet" href = "../css/engine.css">', sep = '', end = '')
print('\n<meta name = "keywords"" content = "', page_keywords,'">', sep = '', end = '')
print('''\
\n</head>

\n\n<body>
''', end = '')

#регистрация посещаемости (файл.функция(объекты и пременныые)) 
#py_sql_visits.py_sql_visits(db,cur,page_id, page_title, page_keywords)


print('''
\n<div>
''')

print('''
\n<div  class = "hellobox">
''', end = '')        
with open('../public_html/hello/info.htm', mode = 'r', encoding = "utf-8", errors = None) as hello_info_stream:
    print (hello_info_stream.read(), end="")
print ('''
</div>
''')

print("<nav>\n<ul>", end = '')
#    готовим данные навигационного  фрагмента страницы
#   `page_id` -значение записи в поле базы данных  ; (page_id)  - значение переменной в строе запроса   
#    сравнением получаем нужную запись в получаем соответствующие значения для заголовка страницы 
cur.execute("""SELECT `page_id`,`page_prior_navig`,`page_title`, `page_keywords`, `page_content` FROM `sql_pages` ORDER BY `sql_pages`.`page_prior_navig` DESC """)
db_all  =  cur.fetchall()
#print("\n\n\ndb_all:",type(db_all),db_all,sep="\n\n", end="\n\n\n")
for result in db_all:
    #print ("\n", type(page_id), page_id, type(result[0]),result[0], type(result[2]),result[2], end = '')
    if (int(result[1])!= 0): #если 0 - убираем ссылку из навигации
        if (int(result[0]) == int(page_id)): 
            print ('\n<li><a href = "%s'%href_py_file,
                '?function=page&page_id=%s"' % result[0],
                ' class = "active">', sep = '', end = '')
        else:
            print ('\n<li><a href = "%s'%href_py_file,
                '?function=page&page_id=%s"' % result[0],
                '>', sep = '', end = '') 
        print("%s" % result[2], "</a>", end = '')
print("\n</ul>\n</nav>\n")

        
print ('\n<main>')
if (function == "page"): # отрицанием резервируем ветвление для будущих особенных страниц с уникальным содержанием
    # создаем записи в базе данных, но информационное поле 'page_content' оставляем пустым
    if (int(page_id) == 2):
        py_form_processing.py_form_processing()  #обработчик строки запроса
    if (int(page_id) == 3):
        py_pavl_02.py_pavl_02(qr_string) #для задачи или лабораторной работающей в цикле
    if (int(page_id) == 4):
        py_sql_test_cgi.py_sql_test_cgi() #изучаем CGI
    if (int(page_id) == 5):
        py_matplot.py_matplot() #создаем графики
    if (int(page_id) == 6):
        py_sql_shop.py_sql_shop(cur, qr_string) #интерфейс для магазина
    else:
        #    готовим данные главного  фрагмента страницы
        #   `page_id` -значение записи в поле базы данных  ; (page_id)  - значение переменной в строе запроса   
        #    сравнением получаем нужную запись в получаем соответствующие значения для заголовка страницы 
        cur.execute("""SELECT `page_id`,`page_prior_navig`,`page_title`, `page_keywords`, `page_content` FROM `sql_pages`  WHERE `page_id`  =  %s""",(page_id))
        db_one  =  cur.fetchone()
        #print("\nСписок из базы для основного блока - db_one:\n",db_one, "\n")
        page_content = db_one[4]
        print(page_content, end = '')
print ('\n</main>', end = '\n')


print ('\n<footer>') 
with open('../public_html/footer/info.htm', mode = 'r', encoding = "utf-8", errors = None) as footer_info_stream:
    print (footer_info_stream.read(), end="")
print ('</footer>')
print ('\n</div>\n\n</body>\n</html>')
db.close()

