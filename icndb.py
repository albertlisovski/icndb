#!.env/bin/python3

import sys
import argparse
import requests
import json
from py_translator import Translator

# обработка аргументов командной строки

#Описание класса Parser - наследника ArgumentParser
class Parser(argparse.ArgumentParser):
    
    def __init__(self):
        super().__init__()  #Инициализация родителя класса
        self.add_argument ('--translate-to', default="ru")
        self.add_argument ('--jokes-count', default=1, type=int)
        self.add_argument ('--show-original', action='store_const', const=True)
        self.add_argument ('--set-name', nargs="+", default=["Chuck", "Norris"])
        self.add_argument ('--id', default="random")
 
#Создаем парсер 
parser = Parser()
#Читаем аргументы
namespace = parser.parse_args()

#Описание класса Joke
class Joke(object):
    
    def __init__(self, destLang, jokesCount, firstName, lastName, id, show_original):   #конструктор класса
        self.destLang = destLang
        self.jokesCount = jokesCount
        self.firstName = firstName
        self.lastName = lastName
        self.id = id
        self.show_original = show_original
    
    def read(self):
        #Подготовка подстроки в зависимости от набора аргументов
        if self.id != "random":                  
            substr = self.id
        else:
            substr = self.id + "/" + str(self.jokesCount)

        #Обращение к API, отправка GET-запроса
        url =" http://api.icndb.com/jokes/" + substr + "?escape=javascript" + "&firstName=" + self.firstName + "&lastName=" + self.lastName
        response = requests.get(url)
        #Преобразование ответа сервера в JSON
        return json.loads(response.text)
                
        
    def translate(self, jokes):     #Перевод
                            
        translator = Translator()   #Создание объекта класса Translator
        
        if self.show_original:
            jokes["show_original"] = True
            
        i = 0                       #Счетчик цикла
        while i < self.jokesCount:
            if self.id == "random":     #Если мы запросили случайную шутку, то обрабатываем ее как список
                if self.show_original:  #Сохраняем оригинал шутки
                    jokes["value"][i]["joke_original"] = jokes["value"][i]["joke"]
                    print("Original: " + jokes["value"][i]["joke"]) #Выводим оригинал шутки
                jokes["value"][i]["joke"] = translator.translate(jokes["value"][i]["joke"], src='en', dest=self.destLang).text  #вызываем переводчик                  
                print("Translated: Шутка №" + str(jokes["value"][i]["id"]) + ": " + jokes["value"][i]["joke"])
            else:                       #Если мы запрашивали шутку по ID, то обрабатываем ее как словарь
                if self.show_original:  #Сохраняем оригинал шутки
                    jokes["value"]["joke_original"] = jokes["value"]["joke"]
                    print("Original: " + jokes["value"]["joke"])    #Выводим оригинал шутки
                jokes["value"]["joke"] = translator.translate(jokes["value"]["joke"], src='en', dest=self.destLang).text        #вызываем переводчик
                print("Translated: Шутка №" + str(jokes["value"]["id"]) + ": " + jokes["value"]["joke"])
                self.jokesCount = 1      #На тот случай, если укажут одновременно номер шутки и количество шуток более 1, мы прекращаем цикл на первой итерации
            i += 1
          
        return jokes

if __name__ == "__main__":
    #Создаем объект класса Joke
    joke = Joke(namespace.translate_to, namespace.jokes_count, namespace.set_name[0], namespace.set_name[1], namespace.id, namespace.show_original)    

    #Вызываем метод Прочитать
    jokeJSON = joke.read()

    #Вызываем метод Перевести

    jokeJSON = joke.translate(jokeJSON)

    #Сохранение файла    
    with open("output.json", "w") as outfile:
        json.dump(jokeJSON, outfile, ensure_ascii=False)
