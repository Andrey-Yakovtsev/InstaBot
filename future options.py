'''ищет кнопку "Подписаться". Пока решил ее не запускать.
Потом можно в цикла по хэштегам поставить слайс на каждый 5й, например...'''

'''

def xpath_exists(self):
    url = '/html/body/div[1]/section/main/div/div[1]/article/header/div[2]/div[1]/div[2]/button'

    try:
        self.browser.find_element_by_xpath(url).click()  # click to SUBSCRIBE BUTTON
        bot.send_message(chat_id=tg_chat_auth, text=f'Подписался')
        time.sleep(random.randrange(10, 15))
    except NoSuchElementException:
        pass





def skip_if_already_subscribed(self):
    """Если подписаны уже, то скипаем пост
    (но Юзер-то м.б. не подписан на нас!!!!)"""

    requiredHtml = self.browser.page_source
    soup = BeautifulSoup(requiredHtml, 'html.parser')
    subscribed_user = soup.find_all('div', class_='bY2yH')  # Нашел контейнер
    sub_confirmed = str(subscribed_user).split(' ')
    nonconfirmed = 'type="button">Подписаться</button></div>]'  # Нашел строчку, которая говорит, что уже подписан
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
    # не до конца нормально работает


def like_3_thread_posts(self):
    hrefs = self.browser.find_elements_by_tag_name('a')
    extra_urls = [item.get_attribute('href') for item in hrefs if "/p/" in item.get_attribute('href')]
    for url in extra_urls[:3]:
        pass
    # выкатить в лайкинг в отдельную фенкцию...
'''