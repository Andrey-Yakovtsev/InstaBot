import logging
import sys
from selenium import webdriver
from selenium.webdriver.remote.remote_connection import LOGGER
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from auth_data import username, password, bot_creds, tg_chat_auth
from datasets import tags
import time
import random
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
import telebot

'''Припилить бота чтобы мог запускать скрипт'''

bot = telebot.TeleBot(bot_creds)
sleep = False


class InstagramBot:
    """Instagram Bot на Python by PythonToday"""

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.options = Options()
        self.options.headless = True
        self.profile = webdriver.FirefoxProfile()
        self.profile.set_preference("general.useragent.override", "Mozilla/5.0")
        self.browser = webdriver.Firefox(self.profile, options=self.options)

    # метод для закрытия браузера
    def close_browser(self):

        self.browser.close()
        self.browser.quit()
        bot.send_message(chat_id=tg_chat_auth, text=f'Закрыл сессию...')

    # метод логина
    def login(self):

        browser = self.browser
        browser.get('https://www.instagram.com')
        time.sleep(random.randrange(5, 10))

        username_input = browser.find_element_by_name('username')
        username_input.clear()
        username_input.send_keys(username)

        time.sleep(2)

        password_input = browser.find_element_by_name('password')
        password_input.clear()
        password_input.send_keys(password)

        password_input.send_keys(Keys.ENTER)
        bot.send_message(chat_id=tg_chat_auth, text=f'Залогинился')
        time.sleep(50)

    # метод поиска значения "полайкано", чтбы не кликать повторно на лайк
    def find_already_liked_posts(self):
        requiredHtml = self.browser.page_source
        soup = BeautifulSoup(requiredHtml, 'html.parser')
        liked_post = soup.find_all('span', class_='fr66n')  # '_8-yf5 '
        for item in liked_post:
            svg = item.find('svg')  # Нашел контейнер
            lookup = str(svg).split('=')
            like = '"Не нравится" class'  # Нашел строчку, которая говорит, что уже полайкано
            if like in lookup:
                return False
            else:
                return True

    # метод ставит лайки по hashtag
    def like_photo_by_hashtag(self, hashtag):
        like_clicks = 0
        subscribe_clicks = 0
        ht_counter = 1
        browser = self.browser
        browser.get(f'https://www.instagram.com/explore/tags/{hashtag}/')
        time.sleep(5)
        bot.send_message(
            chat_id=tg_chat_auth,
            text=f'Бот {hashtag}  стартанул.'f'Tag {ht_counter}/{len(tags)}'
            )
        for i in range(1, 9):
            browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(random.randrange(15, 20))

        hrefs = browser.find_elements_by_tag_name('a')
        posts_urls = [item.get_attribute('href') for item in hrefs if "/p/" in item.get_attribute('href')]
        bot.send_message(chat_id=tg_chat_auth, text=f'Набил список длиной: {len(posts_urls)}')

        url_counter = 0
        for url in posts_urls[10:int(len(posts_urls))]: # liking for random posts under 1 hashtag starting from 10th as "newest"
            url_counter += 1
            try:
                browser.get(url)
                time.sleep(5)
                if self.find_already_liked_posts():     # Если еще не полайкали, то вперед
                    browser.find_element_by_xpath(
                        '/html/body/div[1]/section/main/div/div[1]/article/div[3]/section[1]/span[1]/button/div'
                    ).click()   #click to LIKE BUTTON
                    like_clicks +=1
                    bot.send_message(chat_id=tg_chat_auth, text=f'Новый лайк')
                    time.sleep(random.randrange(80, 100))
                    if url_counter % 10 == 0:
                        browser.find_element_by_xpath(
                            '/html/body/div[1]/section/main/div/div[1]/article/header/div[2]/div[1]/div[2]/button'
                        ).click() #CLICK SUBSCRIBE BUTTON
                        subscribe_clicks += 1
                        bot.send_message(chat_id=tg_chat_auth, text=f'ПОДПИСОЧКА')
                        time.sleep(random.randrange(80, 100))
                else:
                    bot.send_message(chat_id=tg_chat_auth, text=f'Лайк уже был')
                    time.sleep(random.randrange(10, 20))
                    continue

            except Exception as ex:
                print(ex)
                bot.send_message(chat_id=tg_chat_auth, text=f'Ошибка внутри функции {ex}')

        bot.send_message(
            chat_id=tg_chat_auth,
            text=f'Бот по тэгу {hashtag} закончил. '
            f'Likes: {like_clicks}. '
            f'Подписок {subscribe_clicks}'
        )
        ht_counter += 1


# bot.send_message(chat_id=tg_chat_auth, text=f'Бот ВООБЩЕ ВСЕ СДЕЛАЛ И ЗАКОНЧИЛ. Налупили лайков: {like_clicks}'
#                                                     f'и {subscribe_clicks} подписок')


def run_script():
    try:
        logging.basicConfig(filename="Logs/like_photo_by_hashtag.log", level=logging.INFO, filemode='w+')
        logger = logging.getLogger('Botlogging:')
        logging.info("Informational message")
        tags_enum = list(enumerate(tags))
        my_bot = InstagramBot(username, password)
        my_bot.login()
        bot.send_message(chat_id=tg_chat_auth, text=f'Залогинился на первый вход')
        for key, hashtag in tags_enum:
            if key != 0 and key % 5 == 0:
                my_bot.like_photo_by_hashtag(hashtag)
                bot.send_message(chat_id=tg_chat_auth, text=f'Прошел цикл. Отрубаемся на час.')
                my_bot.close_browser()
                time.sleep(60 * 60)
                bot.send_message(chat_id=tg_chat_auth, text=f'Прошел час. Стартуем снова.')
                my_bot = InstagramBot(username, password)
                my_bot.login()
                bot.send_message(chat_id=tg_chat_auth, text=f'Залогинился')
                my_bot.like_photo_by_hashtag(hashtag)
            else:
                my_bot.like_photo_by_hashtag(hashtag)

    except Exception as exep:
        bot.send_message(chat_id=tg_chat_auth, text=f'Ошибка внутри основного старта: {exep}')


@bot.message_handler(commands=['start'])
def start_message(message):
    print("Bot started")
    try:

        bot.send_message(message.chat.id, run_script())
    except Exception as exep:
        bot.send_message(chat_id=tg_chat_auth, text=f'Ошибка внутри хэндлера СТАРТ: {exep}')


@bot.message_handler(commands=['stop'])
def start_message(message):
    bot.send_message(chat_id=tg_chat_auth, text=f'Тормознули бота руками')
    sys.exit(0)



@bot.message_handler(commands=['sleep'])
def start_message(message):
    global sleep
    sleep = True
    print('Bot sleep for 24 h')
    bot.send_message(chat_id=tg_chat_auth, text=f'Пауза на 25 часов ')
    time.sleep(60*60*25)
    sleep = False
    bot.send_message(chat_id=tg_chat_auth, text=f'Время прошло. Sleep = False')

@bot.message_handler(commands=['run'])
def start_message(message):
    global sleep
    sleep = False
    print('Bot waked up')
    bot.send_message(chat_id=tg_chat_auth, text=f'Разбудил бота принудительно. Sleep = False')

bot.polling(none_stop=True)




