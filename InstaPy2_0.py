from instapy import InstaPy
from datasets import tags, skipped_friends, to_follow_list
from logger_decor import logger
from datetime import datetime
import time
import schedule
from instapy.plugins import InstaPyTelegramBot
import logging

@logger
def my_liker_subscriber_bot():
    '''Функция нужна только для запуска планировщика'''
    logging.basicConfig(filename="logs/like_subscribe.log", level=logging.INFO)

    session = InstaPy(
        # username="a_yakovtsev",
        # password="Insta331133",
        username="trisport_russia",
        password="Pivovar3312",
        headless_browser=True,
        disable_image_load=True,
        multi_logs=True,
        bypass_security_challenge_using='sms'
    )
    telegram = InstaPyTelegramBot(token='1095292391:AAHpAyz2zfnkQmHzq53rJ8ce_2BfpHa09LI',
                                  telegram_username='@andrey_yakovtsev',
                                  instapy_session=session)
    session.login()
    start = datetime.now()
    session.set_do_follow(enabled=True, percentage=15, times=1)
    # session.like_by_tags(tags, amount=1)  # 1 like на тэг на 1 друга. Отменил пока. Оставим только лайкателей друзей
    session.set_dont_include(skipped_friends)
    session.set_mandatory_language(enabled=True, character_set=['CYRILLIC'])
    session.set_action_delays(
        enabled=True,
        like=3, comment=5,
        follow=4,
        unfollow=3,
        randomize=True,
        random_range_from=70,
        random_range_to=140)
    session.set_do_comment(enabled=True, percentage=10)
    session.like_by_feed(amount=10, randomize=True, unfollow=True)
    # Follow the followers of each given user
    # users = session.target_list("C:\\Users\\......\\users.txt")
    session.follow_user_followers(to_follow_list, amount=10, randomize=False)
    # session.set_delimit_commenting(enabled=True, max_comments=None, min_comments=1)

    session.set_comments(['Классно!', 'Здорово!'])

    session.set_relationship_bounds(enabled=True, max_followers=1020500, min_posts=3)

    session.set_skip_users(skip_private=True, skip_no_profile_pic=True,
                           skip_bio_keyword=['доставка', 'заказ', 'оплата', 'магазин'])  # skip_business=True,

    session.set_quota_supervisor(enabled=True, peak_comments_daily=240,
                                 peak_comments_hourly=21,
                                 peak_likes_hourly=100,
                                 peak_follows_hourly=20,
                                 sleep_after=["likes", "comments_d", "follows", "unfollows"],
                                 notify_me=True)

    # список аккаунтов, по подписчикам которых наддо профолловить
    # session.follow_user_followers(to_follow_list, amount=5, randomize=False, sleep_delay=300)

    # зафолловить лайкеров фоточек именованных аккаунтов
    session.follow_likers(to_follow_list,
                          photos_grab_amount=3,
                          follow_likers_per_photo=3,
                          randomize=True,
                          sleep_delay=600,
                          interact=False)

    telegram.end()
    session.end()
    end = datetime.now()
    print('Время работы:', end-start)

@logger
def my_unsubscriber_bot():
    '''Задание для отписок'''
    logging.basicConfig(filename="logs/unsubscribe.log", level=logging.INFO)
    session = InstaPy(
        username="trisport_russia",
        password="Pivovar3312",
        headless_browser=True,
        disable_image_load=True,
        multi_logs=True,
        bypass_security_challenge_using='sms'
    )
    telegram = InstaPyTelegramBot(token='1095292391:AAHpAyz2zfnkQmHzq53rJ8ce_2BfpHa09LI',
                                  telegram_username='@andrey_yakovtsev',
                                  instapy_session=session)
    session.login()
    start = datetime.now()
    print('Время начала:', start)

    session.set_action_delays(unfollow=3)

    session.unfollow_users(amount=30,
                           instapy_followed_enabled=True,
                           instapy_followed_param="nonfollowers",
                           style="FIFO",
                           unfollow_after=90*60*60)

    session.set_dont_unfollow_active_users(enabled=True, posts=3)
    telegram.end()
    session.end()
    end = datetime.now()
    print('Время завершения:', end)
    print('Время работы:', end - start)

schedule.every().day.at("18:22").do(my_liker_subscriber_bot)
schedule.every().day.at("08:30").do(my_liker_subscriber_bot)
schedule.every().day.at("14:31").do(my_unsubscriber_bot) #подправить время поотм на 14.30
schedule.every().day.at("02:30").do(my_unsubscriber_bot)

"""На основании времени по серверу в Огайо -7 часов"""
# schedule.every().day.at("11:22").do(my_liker_subscriber_bot)
# schedule.every().day.at("01:30").do(my_liker_subscriber_bot)
# schedule.every().day.at("07:30").do(my_unsubscriber_bot)
# schedule.every().day.at("19:30").do(my_unsubscriber_bot)

while True:
    schedule.run_pending()
