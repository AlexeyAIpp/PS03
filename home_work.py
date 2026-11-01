import asyncio
import requests
from bs4 import BeautifulSoup
from googletrans import Translator

# Создаём функцию, которая будет получать информацию
async def get_english_words(translator):
    url = "https://randomword.com/"

    try:
        response = requests.get(url, timeout=(15))
        response.raise_for_status()

        # Создаём объект Soup
        soup = BeautifulSoup(response.content, "html.parser")
        # Получаем слово и удаляем пробелы по краям
        english_words = soup.find("div", id="random_word").text.strip()
        # Получаем описание слова
        word_definition = soup.find("div", id="random_word_definition" ).text.strip()

        # Переводим слово на русский
        result = await translator.translate(english_words, src="en", dest="ru" )
        english_words = result.text

        # Переводим определение на русский
        result = await translator.translate( word_definition, src="en", dest="ru")
        word_definition = result.text

        # Возвращаем словарь
        return {"english_words": english_words, "word_definition": word_definition }

    except Exception as error:
        print(f"Произошла ошибка: {error}")
        return None


# Создаём функцию, которая будет делать саму игру
async def word_game():
    print("Добро пожаловать в игру")

    async with Translator() as translator:
        while True:
            # Получаем словарь со словом и определением
            word_dict = await get_english_words(translator)

            # Проверяем результат перед обращением к словарю
            if word_dict is None:
                print("Не удалось получить данные. Игра завершена.")
                break

            word = word_dict.get("english_words")
            word_definition = word_dict.get("word_definition")

            # Начинаем игру
            print(f"Значение слова - {word_definition}")
            user = input("Что это за слово? ")

            if user.strip().lower() == word.strip().lower():
                print("Все верно!")
            else:
                print(f"Ответ неверный, было загадано это слово - {word}")

            # Создаём возможность закончить игру
            play_again = input("Хотите сыграть еще раз? y/n: ")

            if play_again.strip().lower() != "y":
                print("Спасибо за игру!")
                break


asyncio.run(word_game())
