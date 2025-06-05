import os
import re

# Dictionary chuyển số sang chữ tiếng Nga (giữ nguyên từ bài mẫu)
digit_to_word = {
    '0': 'ноль',
    '1': 'один',
    '2': 'два',
    '3': 'три',
    '4': 'четыре',
    '5': 'пять',
    '6': 'шесть',
    '7': 'семь',
    '8': 'восемь',
    '9': 'девять'
}

def number_to_words(n):
    """Chuyển số nguyên (0-999) sang chữ tiếng Nga"""
    if n < 20:
        return digit_to_word.get(str(n), '')
    
    tens = n // 10
    units = n % 10
    words = []
    
    if tens >= 2:
        words.append(digit_to_word.get(str(tens*10), ''))
    if units > 0:
        words.append(digit_to_word.get(str(units), ''))
    
    return ' '.join(words)

def process_file():
    """Xử lý file theo yêu cầu Lab 2"""
    # Sử dụng đúng tên file từ Bài 1
    filename = 'c:/Users/PC/OneDrive/Desktop/code/file code của linh.py/lab1.txt'
    
    if not os.path.exists(filename):
        print("Файл не найден")
        return

    results = []
    position = 0
    
    # Regex tìm số tự nhiên chẵn có 1-5 chữ số
    pattern = re.compile(r'\b[1-9]\d{0,4}\b')
    
    with open(filename, 'r', encoding='utf-8') as file:
        for line in file:
            numbers = pattern.findall(line)
            for num_str in numbers:
                num = int(num_str)
                if num % 2 == 0:  # Chỉ xử lý số chẵn
                    position += 1
                    if position % 2 == 1:  # Vị trí lẻ -> chữ
                        results.append(number_to_words(num))
                    else:  # Vị trí chẵn -> số
                        results.append(num_str)
    
    print(' '.join(results))

if __name__ == "__main__":
    process_file()