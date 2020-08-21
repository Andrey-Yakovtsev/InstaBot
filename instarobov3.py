import logging
from selenium import webdriver
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
        time.sleep(5)

    '''ищет кнопку "Подписаться". Пока решил ее не запускать.
    Потом можно в цикла по хэштегам поставить слайс на каждый 5й, например...'''
    def xpath_exists(self):
        url = '/html/body/div[1]/section/main/div/div[1]/article/header/div[2]/div[1]/div[2]/button'

        try:
            self.browser.find_element_by_xpath(url).click()  # click to SUBSCRIBE BUTTON
            bot.send_message(chat_id=tg_chat_auth, text=f'Подписался')
            time.sleep(random.randrange(10, 15))
        except NoSuchElementException:
            pass

    def find_already_liked_posts(self):
        requiredHtml = self.browser.page_source
        soup = BeautifulSoup(requiredHtml, 'html.parser')
        liked_post = soup.find_all('span', class_='fr66n')  # '_8-yf5 '
        for item in liked_post:
            svg = item.find('svg')  #Нашел контейнер
            lookup = str(svg).split('=')
            like = '"Не нравится" class'  #Нашел строчку, которая говорит, что уже полайкано
            if like in lookup:
                return False
            else:
                return True


    def skip_if_already_subscribed(self):
        """Если подписаны уже, то скипаем пост
        (но Юзер-то м.б. не подписан на нас!!!!)"""

        requiredHtml = self.browser.page_source
        soup = BeautifulSoup(requiredHtml, 'html.parser')
        subscribed_user = soup.find_all('div', class_='bY2yH') # Нашел контейнер
        sub_confirmed = str(subscribed_user).split(' ')
        nonconfirmed = 'type="button">Подписаться</button></div>]' # Нашел строчку, которая говорит, что уже подписан
        if nonconfirmed in sub_confirmed:
            print('Можно подписаться')
            return True
        else:
            print('Уже подписаны на юзера')
            return False

    def get_list_of_post_likers(self):
        """
        собираем список эккаунтов тех, кто лайкнул пост по хаштегу
        :return: список урлов-аккаунтов лайкеров
        """
        # self.browser.find_element_by_xpath(
        # '/html/body/div[1]/section/main/div/div[1]/article/div[3]/section[2]/div/div[2]/button'
        # ).click()
        # for i in range(1, 6):
        #     self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        #     time.sleep(random.randrange(3, 5))
        # hrefs = self.browser.find_elements_by_tag_name('a')
        # profile_urls = [item.get_attribute('href') for item in hrefs if "/p/" in item.get_attribute('href')]
        # print(profile_urls)
        pass
        '''не до конца нормально работает'''

    def like_3_thread_posts(self):
        hrefs = self.browser.find_elements_by_tag_name('a')
        extra_urls = [item.get_attribute('href') for item in hrefs if "/p/" in item.get_attribute('href')]
        for url in extra_urls[:3]:
            pass
        '''выкатить в лайкинг в отдельную фенкцию...'''


    # метод ставит лайки по hashtag
    def like_photo_by_hashtag(self):
        like_clicks = 0
        subscribe_clicks = 0
        ht_counter = 1
        browser = self.browser
        for hashtag in tags:
            browser.get(f'https://www.instagram.com/explore/tags/{hashtag}/')
            time.sleep(5)
            bot.send_message(chat_id=tg_chat_auth, text=f'Бот {hashtag}  стартанул.'
                                                        f'Tag {ht_counter}/{len(tags)}')

            for i in range(1, 5):
                browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(random.randrange(15, 20))

            hrefs = browser.find_elements_by_tag_name('a')
            posts_urls = [item.get_attribute('href') for item in hrefs if "/p/" in item.get_attribute('href')]
            url_counter = 0
            for url in posts_urls[10:random.randrange(30, 51)]: # liking for random posts under 1 hashtag starting from 10th as "newest"
                url_counter += 1
                try:
                    browser.get(url)
                    time.sleep(5)
                    self.get_list_of_post_likers()
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
            bot.send_message(chat_id=tg_chat_auth, text=f'Бот по тэгу {hashtag} закончил. Likes: {like_clicks}. '
                                                        f'Подписок {subscribe_clicks}')
            time.sleep(random.randrange(80, 100))
            ht_counter += 1

        bot.send_message(chat_id=tg_chat_auth, text=f'Бот ВООБЩЕ ВСЕ СДЕЛАЛ И ЗАКОНЧИЛ. Налупили лайков: {like_clicks}'
                                                    f'и {subscribe_clicks} подписок')


# def run_script():
#     my_bot = InstagramBot(username, password)
#     bot.send_message(chat_id=tg_chat_auth, text=f'Он сказал: "ПОЕХАЛИ!"')
#     my_bot.login()
#     bot.send_message(chat_id=tg_chat_auth, text=f'Залогинился')
#     my_bot.like_photo_by_hashtag()
#
#
# @bot.message_handler(commands=['start'])
# def start_message(message):
#     print("Bot started")
#     try:
#         bot.send_message(message.chat.id, run_script())
#     except Exception as exep:
#         bot.send_message(chat_id=tg_chat_auth, text=f'Ошибка внутри блока трай: {exep}')
#
#
# @bot.message_handler(commands=['stop'])
# def start_message(message):
#     my_bot = InstagramBot(username, password)
#     bot.send_message(message.chat.id, my_bot.close_browser())
#     print('Bot stopped')
#     bot.send_message(chat_id=tg_chat_auth, text=f'Тормознули бота руками')
#
#
# bot.polling(none_stop=True)


try:
    logging.basicConfig(filename="Logs/like_photo_by_hashtag.log", level=logging.DEBUG, filemode='w')
    my_bot = InstagramBot(username, password)
    bot.send_message(chat_id=tg_chat_auth, text=f'Он сказал: "ПОЕХАЛИ!"')
    my_bot.login()
    bot.send_message(chat_id=tg_chat_auth, text=f'Залогинился')
    my_bot.like_photo_by_hashtag()
    my_bot.close_browser()
except Exception as exep:
    bot.send_message(chat_id=tg_chat_auth, text=f'Ошибка внутри основного старта: {exep}')
