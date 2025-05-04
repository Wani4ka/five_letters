from words import words


def test_words_not_empty():
    """Проверка, что список слов не пустой."""
    assert len(words) > 0, "Список слов должен содержать хотя бы одно слово"


def test_words_length():
    """Проверка, что все слова состоят из 5 букв."""
    for word in words:
        assert len(word) == 5, f"Слово '{word}' должно состоять из 5 букв"


def test_words_unique():
    """Проверка, что все слова уникальны."""
    unique_words = set(words)
    assert len(words) == len(unique_words), "В списке есть повторяющиеся слова"


def test_words_cyrillic():
    """Проверка, что слова содержат только кириллические буквы."""
    cyrillic_letters = set('АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ')
    for word in words:
        for letter in word:
            assert letter in cyrillic_letters, f"Слово '{word}' содержит некириллический символ"


def test_no_empty_strings():
    """Проверка на отсутствие пустых строк в списке."""
    assert '' not in words, "Список слов содержит пустую строку"
