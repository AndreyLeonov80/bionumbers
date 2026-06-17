class BioNum:
    LETTER_MAP = {
        1: ['и', 'с', 'э'],
        2: ['а', 'й', 'т', 'п'],
        3: ['б', 'з', 'м', 'ю'],
        4: ['в', 'к', 'ф', 'я'],
        5: ['д', 'л', 'х', 'ы'],
        6: ['е', 'о', 'ц', 'ь'],
        7: ['ё', 'н', 'ъ'],
        8: ['г', 'у', 'ч', 'щ'],
        9: ['ж', 'р', 'ш']
    }

    def __init__(self):
        self.char_to_number = {}
        for number, letters in self.LETTER_MAP.items():
            for letter in letters:
                self.char_to_number[letter] = number

    def _reduce(self, value: int) -> int:
        while value > 9:
            value = sum(int(digit) for digit in str(value))
        return value

    def calculate(self, text: str) -> int:
        total = 0

        for char in text.lower():
            if char in self.char_to_number:
                total += self.char_to_number[char]

        return self._reduce(total)


# проверка
calc = BioNum()

#tests = [
#    "один",
#    "два",
#    "три",
#    "четыре",
#    "пять",
#    "шесть",
#    "семь",
#    "восемь",
#    "девять"
#]

#for word in tests:
#    print(word, "=", calc.calculate(word))
