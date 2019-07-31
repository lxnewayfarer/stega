#   Подключение необходимых библиотек 
from tkinter import *   # библиотека интерфейса
from tkinter.filedialog import *    # для окон выбора файлов
from PIL import Image # для работы с изображениями
import random   # для случайного распределения по пикселям изображения
import re # библиотека регулярных выражений чтобы спарсить файл с ключами

whatisstego = """_________________________________________________________\
    Стеганография — способ передачи или хранения информации с учётом \
сохранения в тайне самого факта такой передачи (хранения). 
    В данном программном средстве для кодирования текста в изображение \
используется замена голубого канала RGB случайных пикселей изображения. \
Случайное распределение гарантирует схожесть с простым шумом на изображении, \
а выбор голубого канала обусловлен наименьшей силой восприятия \
человеческим глазом именно оттенков синего цвета. \
Для кодирования текста \
в текст используется метод преобразования текста в двоичный код с последующей \
заменой английских букв на русские из последовательности [ayopxcAETOPHKXCBM] в тексте \
контейнере, если очередное число равно 1 и оставлением без изменений, если \
число равно 0. """

#   основная геометрия окна
root = Tk()
root.geometry("470x540")
#   прокручеваемое поле с информацией 
info = Text(root, wrap=WORD)
info.place(x = 5, y = 5, width = 460, height = 260)
info.insert(1.0, whatisstego)
scrollbar = Scrollbar(root)
scrollbar['command'] = info.yview
info['yscrollcommand'] = scrollbar.set

#   глобальные переменные
savefilesdir = ''   # директория сохранения закодированных файлов
text4encode = ''    # текст для шифрования
container = ''  # текст - контейнер
alphabeten = 'ayopxcAETOPHKXCBM'    # англ. словарь букв с идентичным написанием
alphabetru = 'ауорхсАЕТОРНКХСВМ'    # рус. словарь
containerCapacity = 0 # вместимость контейнера

#   функция выбора текста для кодирования (привязка к кнопке №1)
def chstext():
    global text4encode
    # обработка ошибки правильного открытия текстового файла
    try:
        handle = open(askopenfilename(), "r")
        text4encode = handle.read()
    except:
        info.insert(1.0, "•  Ошибка открытия текста для кодирования! Файл не соответствует расширению .txt, либо же поврежден\n\n")
    
#   функция выбора изображения для кодирования (привязка к кнопке №2)
def chsimg():
    global imgencode # глобальная переменная изображения
    # запрос на открытие изображения пользователем
    op = askopenfilename()
    # проверка на .png расширение
    if op[-3:] != 'png':
        info.insert(1.0, "•  Ошибка открытия изображения! Файл не соответствует \
        расширению .png, либо же поврежден\n\n")
    # открытие изображения
    imgencode = Image.open(op)
    
#   функция выбора текста-контейнера (привязка к кнопке №3)
def chscnt():
    global container
    global SavePrivateContainer
    global containerCapacity
    # проверка на правильность открытия файла
    try:
        handle = open(askopenfilename(), "r")
        container = handle.read()
        #   переменная, призванная сохранить контейнер
        SavePrivateContainer = container    
    except:
        info.insert(1.0, "•  Ошибка открытия текста-контейнера! Файл не соответствует \
        расширению .txt, либо же поврежден\n\n")
        return
    #   рассчет вместимости контейнера
    i = len(container) - 1
    endfoundflag = False
    while i != 0:
        if alphabeten.rfind(container[i]) != -1 and endfoundflag:
            containerCapacity += 1
        if container[i] == 'e':
            endfoundflag = True
        i -= 1
    containerCapacity = int(containerCapacity / 8)
    info.insert(1.0, "•  Открыт контейнер, вместимость контейнера равна " + str(containerCapacity) + " символов\n\n")
    
#   функция выбора пути сохранения (привязка к кнопке №4)
def chssavedir():
    global savefilesdir
    # запрос на выбор директории
    savefilesdir = askdirectory()

# функция, кодирующая в текст
def encodetext():
    global text4encode
    global container
    
    # проверка существования текста - контейнера
    if container == '':
        info.insert(1.0, "•  Вы не выбрали текст-контейнер\n\n")
        return 
    if containerCapacity < len(text4encode):
        info.insert(1.0, "•  Вместимость текста-контейнера меньше сообщения\n\n")
        return
    # решение проблемы с юникодом
    for i in range(len(text4encode)):
        if ord(text4encode[i]) > 1039:
            text4encode = text4encode[:i] + chr(ord(text4encode[i]) - 848) + text4encode[i+1:]
    # преобразование текста в двоичную строку        
    bintext = ''.join('{:08b}'.format(ord(c)) for c in text4encode)
    index = 0 # индекс текущего символа в двоичной строке
    i = 0 # бегунок по контейнеру
    # процесс шифрования - замены идентичных букв контейнере, когда "1"
    while i < len(container) and index < len(bintext):
        n = alphabeten.rfind(container[i])
        if n != -1:
            if bintext[index] == '1':
                container = container[:i] + alphabetru[n] + container[i+1:]  
            index += 1
        i += 1   
    #   замена английской буквы "е" на русскую как обозначение конца сообщения
    while i < len(container):
        if container[i] == 'e':
            container = container[:i] + 'е' + container[i+1:]
            break
        i += 1
    # сохранение файла с зашифрованным текстом
    handle = open(savefilesdir + "/encodedToText.txt", "w")
    handle.write(container)
    container = SavePrivateContainer # восстановление контейнера
    handle.close()
    info.insert(1.0, "•  Успешно выполнено кодирование в текстовый файл. Результат сохранен в " + savefilesdir + "/encodedToText.txt\n\n")

# ф-я, кодирующая в изображение
def encodeimg():
    width = imgencode.size[0]  # Определяем ширину изображения
    height = imgencode.size[1]  # Определяем высоту.
    pix = imgencode.load()  # Выгружаем значения пикселей.
    savepix = pix # сохранение пикселей
    #   проверка на вместимость изображения
    if len(text4encode) > width * height:
        info.insert(1.0, "•  Невозможно зашифровать этот текст в это изображение, так как \
        кол-во символов превышает кол-во пикселей\n\n")
        return
    #   массив ключей
    keyarray = [] #     (X0, Y0), (...), (Xi, Yi), (...), (Xn, Yn).
    #   процесс шифрования
    for i in range(len(text4encode)):
        x = random.randint(0, width-1)
        y = random.randint(0, height-1)
        while keyarray.count((x, y)):   #   проверка на уже существующее значение координат
            x = random.randint(0, width)
            y = random.randint(0, height)
        keyarray.append((x, y)) #   добавление координат к массиву
        #   шифрование в голубой канал и обход юникод проблемы
        if ord(text4encode[i]) > 1039:  
            pix[x, y] = (pix[x, y][0],
                        pix[x, y][1],
                        ord(text4encode[i]) - 848)
        else:       
            pix[x, y] = (pix[x, y][0],
                        pix[x, y][1],
                        ord(text4encode[i]))
    #   сохранение изображения и файла с ключами
    imgencode.save(savefilesdir + "/encodedimage.png", "PNG") 
    handle = open(savefilesdir + "/keys.txt", "w")
    handle.write(str(keyarray))
    handle.close()  
    pix = savepix # восстановление пикселей
    info.insert(1.0, "•  Успешно выполнено кодирование в изображение. Результат сохранен в " + savefilesdir + "/encodedimage.png,\
     а ключи сохранены в " + savefilesdir + "/keys.txt\n\n")

#   функция начала кодирования (привязка к кнопке №5)
def startencode():
    #   проверка на выбор файлов
    if text4encode == '':
        info.insert(1.0, "•  Вы не выбрали текст для кодирования\n\n")
        return
    elif savefilesdir == '':
        info.insert(1.0, "•  Вы не выбрали директорию сохранения файла\n\n")
        return
    if istotext.get():
        encodetext()
    if istoimg.get():
        encodeimg()
    if (istoimg.get() or istotext.get()) == False:
        info.insert(1.0, "•  Вы не выбрали ни одного способа кодирования\n\n")

#   интерфейс кодирования - кнопки и чекбоксы
choosetext = Button(text = "Выбрать текст для кодирования", command = chstext)
choosetext.place(x = 5, y = 270, width = 210, height = 40)

chooseimg = Button(text = "Выбрать изображение (если \nбудет кодирование в изображение)", command = chsimg)
chooseimg.place(x = 5, y = 315, width = 210, height = 40)

choosecontainer = Button(text = "Выбрать текст-контейнер", command = chscnt)
choosecontainer.place(x = 5, y = 360, width = 210, height = 40)

choosesavedir = Button(text = "Выбрать путь сохранения", command = chssavedir)
choosesavedir.place(x = 5, y = 405, width = 210, height = 40)

istotext = IntVar()
totext = Checkbutton(root, text=u'Кодировать в текст' , variable = istotext, onvalue = 1, offvalue = 0)
totext.place(x = 5, y = 445, height = 30)

istoimg = IntVar()
toimg = Checkbutton(root, text=u'Кодировать в изображение' , variable = istoimg, onvalue = 1, offvalue = 0)
toimg.place(x = 5, y = 465, height = 30)

goencode = Button(text = "Начать кодирование", command = startencode)
goencode.place(x = 5, y = 495, width = 210, height = 40)    


#   глобальные переменные для декодирования
text4decode = ''
keys = ''
savedecodeddir = ''
decodedtext = ''

#   ф-и для декодирования
#   ф-я для выбора файла с зашифрованном в нем коде
def chscodedtext():
    global text4decode
    try:
        handle = open(askopenfilename(), "r")
        text4decode = handle.read()
    except:
        info.insert(1.0, "•  Ошибка открытия текста для декодирования! Файл не соответствует расширению .txt, либо же поврежден\n\n")
    
#   функция выбора изображения для кодирования (привязка к кнопке №2)
def chscodedimg():
    global imgdecode
    op = askopenfilename()
    if op[-3:] != 'png':
        info.insert(1.0, "•  Ошибка открытия изображения! Файл не соответствует \
        расширению .png, либо же поврежден\n\n")
    imgdecode = Image.open(op)

#   функция выбора текста-контейнера (привязка к кнопке №3)
def chskeys():
    global keys
    try:
        handle = open(askopenfilename(), "r")
        keys = handle.read()
    except:
        info.insert(1.0, "•  Ошибка открытия файла с ключами! Возможно, файл не соответствует \
        расширению .txt, либо же поврежден\n\n")

#   функция выбора пути сохранения (привязка к кнопке №4)
def chsdecodedsavedir():
    global savedecodeddir
    savedecodeddir = askdirectory()

def decodetext():
    if text4decode == '':
        info.insert(1.0, "•  Вы не выбрали текст для кодирования\n\n")
        return
    global decodedtext
    decodedtext = ''
    binarytext = ''
    i = 0 # бегунок по контейнеру
    #  цикл до конца сообщения и собирание двоичной строки
    while text4decode[i] != 'е': 
        if alphabetru.rfind(text4decode[i]) != -1:  #  поиск русских символов
            binarytext = binarytext + '1'
        if alphabeten.rfind(text4decode[i]) != -1:  #  поиск англ. символов
            binarytext = binarytext + '0'
        i += 1
        if i == len(text4decode):   #  проверка на наличие конца сообщения (русской буквы "е")
            break
            info.insert(1.0, "•  Не найден конец сообщения в зашифрованном тексте\n\n")
    i = 0
    #  перевод двоичной строки в нормальную
    while i < len(binarytext):
        hub = int(binarytext[i:i+8],2)
        if hub > 191:
            decodedtext = decodedtext + chr(hub + 848)
        else:
            decodedtext = decodedtext + chr(hub)
        i += 8
    #  сохранение расшифрованного текста
    handle = open(savedecodeddir + "/decoded.txt", "w")
    handle.write(decodedtext)
    handle.close()
    info.insert(1.0, "•  Успешно выполнено декодирование из текста. Результат сохранен в " + savedecodeddir + "/decoded.txt\n\n")

#  расшифровка из изображения
def decodeimg():
    try:
        pixels = imgdecode.load()  # Выгружаем значения пикселей.
    except:
        info.insert(1.0, "•  Отсутствует изображение для декодирования\n\n")
        return
    textdecoded = ''
    if keys == '':
        info.insert(1.0, "•  Отсутствует файл с ключами\n\n")
        return
    rawkeys = re.findall(r'\d+', keys) #  поиск всех чисел в файле с ключами
    for i in range(len(rawkeys)):
        rawkeys[i] = int(rawkeys[i])    #  перевод ключей из строкового в целочисленный тип
    i = 0
    while i < len(rawkeys): #  проход по массиву с ключами
        x = rawkeys[i]
        y = rawkeys[i+1]
        #  проверка юникода
        if pixels[x, y][2] > 191:
            textdecoded += chr(pixels[x, y][2] + 848)
        else:
            textdecoded += chr(pixels[x, y][2])
        i += 2
    #  сохранение файла
    handle = open(savedecodeddir + "/decodedFromimage.txt", "w")
    handle.write(textdecoded)
    handle.close()  
    info.insert(1.0, "•  Успешно выполнено декодирование из изображения. Результат сохранен в " + savedecodeddir + "/decodedFromimage.txt\n\n")

#  ф-я запуска деодирования
def startdecode():
    if savedecodeddir == '':
        info.insert(1.0, "•  Вы не выбрали директорию сохранения расшифрованного файла\n\n")
        return
    if isfromtext.get():
        decodetext()
    if isfromimg.get():
        decodeimg()
    if (isfromimg.get() or isfromtext.get()) == False:
        info.insert(1.0, "•  Вы не выбрали ни одного способа декодирования\n\n")

#   интерфейс декодирования - кнопки и чекбоксы
choosecodetext = Button(text = "Выбрать текст для декодирования", command = chscodedtext)
choosecodetext.place(x = 255, y = 270, width = 210, height = 40)

choosecodeimg = Button(text = "Выбрать изображение с \nзашифрованным текстом", command = chscodedimg)
choosecodeimg.place(x = 255, y = 315, width = 210, height = 40)

choosefilewkeys = Button(text = "Выбрать путь файла с ключами", command = chskeys)
choosefilewkeys.place(x = 255, y = 360, width = 210, height = 40)

choosesavedecodir = Button(text = "Выбрать путь сохранения для \nдекодированного текста", command = chsdecodedsavedir)
choosesavedecodir.place(x = 255, y = 405, width = 210, height = 40)

isfromtext = IntVar()
fromtext = Checkbutton(root, text=u'Декодировать из текста' , variable = isfromtext, onvalue = 1, offvalue = 0)
fromtext.place(x = 255, y = 445, height = 30)

isfromimg = IntVar()
fromimg = Checkbutton(root, text=u'Декодировать из изображения' , variable = isfromimg, onvalue = 1, offvalue = 0)
fromimg.place(x = 255, y = 465, height = 30)

godecode = Button(text = "Начать декодирование", command = startdecode)
godecode.place(x = 255, y = 495, width = 210, height = 40)

#   запуск цикла обработки событий
root.mainloop()
