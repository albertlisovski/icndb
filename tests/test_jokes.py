import pytest
import subprocess
import os.path
import json
import random
from langdetect import detect

class Test_Jokes:
    
    #@pytest.mark.randomize(num=int, min_num=1, max_num=1000, ncalls=20)
    
    #Общая проверка
    def test_general(self):
        #Проверка на наличие тестируемой программы
        assert os.path.exists("./icndb.py")
        #Проверка на успешность запуска
        code = subprocess.call(["./icndb.py"])
        assert code == 0
        #Проверка на наличие выходного файла
        assert os.path.exists("./output.json")
        #Проверка на то, что выходной файл представлен в формате json
        try:
            with open("./output.json", "r") as output_file:
                data = json.load(output_file)
        except json.decoder.JSONDecodeError:
            raise AssertionError("JSONDecodeError")
        #Проверяем наличие необходимых ключей в JSON файле
        assert data["value"] != None
        #По умолчанию у нас value - это список, поэтому обрабатываем в цикле
        for joke in data["value"]:
            assert joke["joke"] != None
            assert type(joke["joke"]) == str
            assert joke["id"] != None
            assert type(joke["id"]) == int
    
    def test_id_negative1(self):
        code = subprocess.call(["./icndb.py", "--id", "-1"])
        assert code == 0
    
    def test_id_negative2(self):
        code = subprocess.call(["./icndb.py", "--id", "0"])
        assert code == 0
    
    def test_id_negative3(self):
        code = subprocess.call(["./icndb.py", "--id", "A"])
        assert code == 0
    
    @pytest.mark.skip            
    def test_id_positive(self):
        for i in range(10):                     #10 итераций
            id = random.randint(1,100)          #Рандомная шутка с номером от 1 до 100
            code = subprocess.call(["./icndb.py", "--id", str(id)])
            assert code == 0
            with open("./output.json", "r") as output_file:
                data = json.load(output_file)
            assert data["value"]["id"] == id    #Проверяем, что на выходе у нас именно те шутки, которые мы передавали в параметре
    
    def test_show_original(self):
        code = subprocess.call(["./icndb.py", "--show-original"])
        assert code == 0
        with open("./output.json", "r") as output_file:
                data = json.load(output_file)
        assert data["show_original"]    #Проверяем, что есть флаг в выходном json
        if type(data["value"]) == list:
            for joke in data["value"]:
                assert joke["joke_original"] != None        #Проверяем, что есть ключ joke_oiginal
                assert type(joke["joke_original"]) == str   #И что его тип - строка
    
    def test_jokes_count_negative1(self):
        code = subprocess.call(["./icndb.py", "--jokes-count", "-1"])
        assert code == 0
        with open("./output.json", "r") as output_file:
                data = json.load(output_file)
        assert data["value"] != []
    
    def test_jokes_count_negative2(self):
        code = subprocess.call(["./icndb.py", "--jokes-count", "0"])
        assert code == 0
        with open("./output.json", "r") as output_file:
                data = json.load(output_file)
        assert data["value"] != []
    
    @pytest.mark.skip                  
    def test_jokes_count_positive(self):
        for i in range(5):                     #5 итераций
            code = subprocess.call(["./icndb.py", "--jokes-count", str(i)])
            assert code == 0
            with open("./output.json", "r") as output_file:
                data = json.load(output_file)
            assert len(data["value"]) == i
    
    def test_set_name(self):                    #Проверка параметра --set-name
        code = subprocess.call(["./icndb.py", "--set-name", "Victor", "Tsoy", "--show-original"])   #Оставляем оригинал для проверки
        assert code == 0
        with open("./output.json", "r") as output_file:
                data = json.load(output_file)
        assert data["value"][0]["joke_original"].find("Victor") != -1                               #Ишем в json заданные имя
        assert data["value"][0]["joke_original"].find("Tsoy") != -1                                 #и фамилию
    
    
    def test_lang_detect_negative(self):
        try:
            code = subprocess.call(["./icndb.py", "--translate-to", "http"])        
            assert code == 0
        except ValueError:
            raise AssertionError("invalid destination language")
            
            
        
    def test_lang_detect_positive(self):
        lang_list = ["ru", "ar", "uk", "de", "fr", "it", "tr"]                    #И можно продолжать этот список еще очень долго
        for lang in lang_list:                                                    #Но есть проблема с похожими языками, например, тест будет падать при сравнении af и de, tr и az.
            code = subprocess.call(["./icndb.py", "--translate-to", lang])        #Потому что для функции detect эти языки очень похожи.
            assert code == 0
            with open("./output.json", "r") as output_file:
                data = json.load(output_file)
            assert detect(data["value"][0]["joke"]) == lang           #Вызов внешней функции проверки языка
    
    def test_integral(self):
        lang = "fr"
        id = 101
        cnt = 3
        code = subprocess.call(["./icndb.py", "--translate-to", lang, "--id", str(id), "--jokes-count", str(cnt), "--show-original", "--set-name", "Victor", "Tsoy", "Robertovich"])
        assert code == 0
        with open("./output.json", "r") as output_file:
                data = json.load(output_file)
        assert detect(data["value"]["joke"]) == lang
        assert data["value"]["id"] == id
        assert type(data["value"]) == dict                  #Так зашито в коде, чтобы одна и та же шутка не дублировалась! Поэтому в независимости от --jokes-count, у нас будет на
                                                            # выходе одна шутка, а значит в json запишется словарь, а не список.
        assert data["show_original"]    #Проверяем, что есть флаг в выходном json
        if type(data["value"]) == list:
            for joke in data["value"]:
                assert joke["joke_original"] != None        #Проверяем, что есть ключ joke_oiginal
                assert type(joke["joke_original"]) == str   #И что его тип - строка
        assert data["value"]["joke_original"].find("Victor") != -1                               #Ишем в json заданные имя
        assert data["value"]["joke_original"].find("Tsoy") != -1                                 # и фамилию
