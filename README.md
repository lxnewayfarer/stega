# Стеганография / Steganography
    steganography, python, tkinter, images
Стеганография — способ передачи или хранения информации с учётом сохранения в тайне самого факта такой передачи (хранения).
 
В данном программном средстве для кодирования текста в изображение используется замена голубого канала RGB случайных пикселей изображения на определенные значения.
Случайное распределение гарантирует схожесть с простым шумом на изображении, а выбор голубого канала обусловлен наименьшей силой восприятия человеческим глазом именно оттенков синего цвета. 
Для кодирования текста в текст используется метод преобразования текста в двоичный код с последующей заменой английских букв на русские из последовательности [ayopxcAETOPHKXCBM] в тексте контейнере, если   очередное число равно 1 и оставлением без изменений, если число равно 0.

Steganpgraphy - is the way of transfer or storage information hiding this fact of transfer (or storage).

For encoding text to image this program using replacement vaandom lue of blue RGB channel of random pixels from original to certain value.

Random allocation guarantees that replaced pixels will be look like a basic noise on the image, and choice of blue channel determined by worst perception of blue color by human eye.

Text encodes to the container text by the way of transfer text to the binary code and then replacement similar letters of Russian alphabet to the English (ayopxcAETOPHKXCBM) when it is "1" and not replacement when it is "0".
