# stega
Steganography, python, tkinter, images

    Стеганография — способ передачи или хранения информации с учётом 
сохранения в тайне самого факта такой передачи (хранения). 
    В данном программном средстве для кодирования текста в изображение 
используется замена голубого канала RGB случайных пикселей изображения. 
Случайное распределение гарантирует схожесть с простым шумом на изображении, 
а выбор голубого канала обусловлен наименьшей силой восприятия 
человеческим глазом именно оттенков синего цвета. 
Для кодирования текста 
в текст используется метод преобразования текста в двоичный код с последующей 
заменой английских букв на русские из последовательности [ayopxcAETOPHKXCBM] в тексте 
контейнере, если очередное число равно 1 и оставлением без изменений, если 
число равно 0.
