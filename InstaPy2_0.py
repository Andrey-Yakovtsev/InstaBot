from instapy import InstaPy
from datasets import tags, skipped_friends, to_follow_list
from datetime import datetime
import time
import schedule
# from instapy.plugins import InstaPyTelegramBot
import logging
import telebot


bot = telebot.TeleBot('1095292391:AAHpAyz2zfnkQmHzq53rJ8ce_2BfpHa09LI')
def print_bot_start_status(text):
    bot.send_message(chat_id='212438834', text=f'Бот {text}  стартанул')

def print_bot_end_status(text):
    bot.send_message(chat_id='212438834', text=f'Бот {text} закончил')

def error_bot():
    bot.send_message(chat_id='212438834', text=f'Бот поломался')


def like_by_tags_bot():
    '''Функция нужна только для запуска планировщика'''
    logging.basicConfig(filename="Logs/like_by_tags.log", level=logging.INFO, filemode='w')
    print_bot_start_status('like_by_tags_bot')
    session = InstaPy(
        username="a_yakovtsev",
        password="Insta331133",
        # username="trisport_russia",
        # password="Pivovar3312",
        headless_browser=True,
        disable_image_load=True,
        multi_logs=True,
        show_logs=True,
        bypass_security_challenge_using='sms',

    )

    session.login()
    start = datetime.now()
    print('Время начала:', start)
    session.like_by_tags(tags, amount=1)  # 1 like на тэг на 1 друга.
    session.set_do_follow(enabled=True, percentage=15, times=1)
    # session.set_do_comment(enabled=True, percentage=10)
    # session.set_comments(['Классно!', 'Здорово!'])
    session.set_dont_include(skipped_friends)
    session.set_mandatory_language(enabled=True, character_set=['CYRILLIC'])

    session.set_action_delays(
        enabled=True,
        like=3, comment=5,
        follow=4,
        unfollow=10,
        randomize=True,
        random_range_from=70,
        random_range_to=140)

    # session.like_by_feed(amount=10, randomize=True)

    # session.set_delimit_commenting(enabled=True, max_comments=None, min_comments=1)



    session.set_relationship_bounds(enabled=True, delimit_by_numbers=True, max_followers=1020500, min_posts=3)

    session.set_skip_users(skip_private=True, skip_no_profile_pic=True,
                           skip_bio_keyword=['доставка', 'заказ', 'оплата', 'магазин'])  # skip_business=True,
    session.unfollow_users(amount=15,
                           instapy_followed_enabled=True,
                           instapy_followed_param="nonfollowers",
                           style="FIFO",
                           unfollow_after=90 * 60 * 60)

    session.set_dont_unfollow_active_users(enabled=True, posts=3)

    session.set_quota_supervisor(enabled=True, peak_comments_daily=240,
                                 peak_comments_hourly=21,
                                 peak_likes_hourly=50,
                                 peak_follows_hourly=20,
                                 sleep_after=["likes", "comments_d", "follows", "unfollows"],
                                 notify_me=True)

    # telegram.end()
    session.end()
    print_bot_end_status('like_by_tags_bot')
    end = datetime.now()
    print('Время окончания:', end)
    print('Время работы:', end-start)

def follow_user_followers_bot():
    '''Функция нужна только для запуска планировщика'''
    logging.basicConfig(filename="Logs/follow_user_followers.log", level=logging.INFO, filemode='w')
    print_bot_start_status('follow_user_followers_bot')
    session = InstaPy(
        username="a_yakovtsev",
        password="Insta331133",
        # username="trisport_russia",
        # password="Pivovar3312",
        headless_browser=False,
        disable_image_load=True,
        multi_logs=True,
        show_logs=True,
        bypass_security_challenge_using='sms')
    # telegram = InstaPyTelegramBot(token='1095292391:AAHpAyz2zfnkQmHzq53rJ8ce_2BfpHa09LI',
    #                               telegram_username='@andrey_yakovtsev',
    #                               debug=True,
    #                               instapy_session=session)
    session.login()
    start = datetime.now()
    print('Время начала:', start)
    # список аккаунтов, по подписчикам которых наддо профолловить
    session.follow_user_followers(to_follow_list, amount=5, randomize=True, sleep_delay=30)
    session.set_dont_include(skipped_friends)
    session.set_mandatory_language(enabled=True, character_set=['CYRILLIC'])
    session.set_action_delays(
        enabled=True,
        like=4, comment=5,
        follow=5,
        unfollow=7,
        randomize=True,
        random_range_from=70,
        random_range_to=140)
    # session.set_do_comment(enabled=True, percentage=10)
    # session.like_by_feed(amount=5, randomize=True)

    # session.set_delimit_commenting(enabled=True, max_comments=None, min_comments=1)

    # session.set_comments(['Классно!', 'Здорово!'])

    session.unfollow_users(amount=15,
                           instapy_followed_enabled=True,
                           instapy_followed_param="nonfollowers",
                           style="FIFO",
                           unfollow_after=90 * 60 * 60)

    session.set_dont_unfollow_active_users(enabled=True, posts=3)

    session.set_relationship_bounds(enabled=True, delimit_by_numbers=True, max_followers=1020500, min_posts=3)

    session.set_skip_users(skip_private=True, skip_no_profile_pic=True,
                           skip_bio_keyword=['доставка', 'заказ', 'оплата', 'магазин'])  # skip_business=True,

    session.set_quota_supervisor(enabled=True, peak_comments_daily=240,
                                 peak_comments_hourly=21,
                                 peak_likes_hourly=50,
                                 peak_follows_hourly=20,
                                 sleep_after=["likes", "comments_d", "follows", "unfollows"],
                                 notify_me=True)

    # telegram.end()
    session.end()
    print_bot_end_status('follow_user_followers_bot')
    end = datetime.now()
    print('Время окончания:', end)
    print('Время работы:', end-start)

def follow_photo_likers_bot():
    '''Функция нужна только для запуска планировщика'''
    logging.basicConfig(filename="Logs/follow_photo_likers.log", level=logging.INFO, filemode='w')
    print_bot_start_status('follow_photo_likers_bot')
    session = InstaPy(
        username="a_yakovtsev",
        password="Insta331133",
        # username="trisport_russia",
        # password="Pivovar3312",

        headless_browser=True,
        disable_image_load=True,
        multi_logs=True,
        show_logs=True,
        bypass_security_challenge_using='sms',
        want_check_browser=True

    )
    # telegram = InstaPyTelegramBot(token='1095292391:AAHpAyz2zfnkQmHzq53rJ8ce_2BfpHa09LI',
    #                               telegram_username='@andrey_yakovtsev',
    #                               debug=True,
    #                               instapy_session=session)
    session.login()
    start = datetime.now()
    print('Время начала:', start)
    # зафолловить лайкеров фоточек именованных аккаунтов
    session.follow_likers(to_follow_list,
                          photos_grab_amount=3,
                          follow_likers_per_photo=3,
                          randomize=True,
                          sleep_delay=5,
                          interact=True)
    session.set_dont_include(skipped_friends)
    session.set_mandatory_language(enabled=True, character_set=['CYRILLIC'])
    session.set_action_delays(
        enabled=True,
        like=4, comment=5,
        follow=5,
        unfollow=8,
        randomize=True,
        random_range_from=70,
        random_range_to=140)
    # session.set_do_comment(enabled=True, percentage=10)
    # session.set_comments(['Классно!', 'Здорово!'])

    session.set_relationship_bounds(enabled=True, delimit_by_numbers=True, max_followers=1020500, min_posts=3)

    session.set_skip_users(skip_private=True, skip_no_profile_pic=True,
                           skip_bio_keyword=['доставка', 'заказ', 'оплата', 'магазин'])  # skip_business=True,

    session.set_quota_supervisor(enabled=True, peak_comments_daily=240,
                                 peak_comments_hourly=21,
                                 peak_likes_hourly=50,
                                 peak_follows_hourly=20,
                                 sleep_after=["likes", "comments_d", "follows", "unfollows"],
                                 notify_me=True)

    # telegram.end()
    session.end()
    print_bot_start_status('follow_photo_likers_bot')
    end = datetime.now()
    print('Время окончания:', end)
    print('Время работы:', end-start)


'''Перенес отписки в стандариный функционал'''
# def my_unsubscriber_bot():
#     '''Задание для отписок'''
#     # logging.basicConfig(filename="Logs/unsubscribe.log", level=logging.INFO)
#     session = InstaPy(
#         username="trisport_russia",
#         password="Pivovar3312",
#         headless_browser=True,
#         disable_image_load=True,
#         multi_logs=True,
#         bypass_security_challenge_using='sms',
#         show_logs=True
#     )
#     telegram = InstaPyTelegramBot(token='1095292391:AAHpAyz2zfnkQmHzq53rJ8ce_2BfpHa09LI',
#                                   telegram_username='@andrey_yakovtsev',
#                                   debug=True,
#                                   instapy_session=session)
#     session.login()
#     start = datetime.now()
#     print('Время начала:', start)
#
#     session.set_action_delays(unfollow=60)
#
#     session.unfollow_users(amount=20,
#                            instapy_followed_enabled=True,
#                            instapy_followed_param="nonfollowers",
#                            style="FIFO",
#                            unfollow_after=90*60*60)
#
#     session.set_dont_unfollow_active_users(enabled=True, posts=3)
#     telegram.end()
#     session.end()
#     end = datetime.now()
#     print('Время завершения:', end)
#     print('Время работы:', end - start)

# schedule.every().monday.at("17:45").do(like_by_tags_bot)
# schedule.every().wednesday.at("17:45").do(like_by_tags_bot)
# schedule.every().friday.at("17:45").do(like_by_tags_bot)
# schedule.every().sunday.at("17:45").do(like_by_tags_bot)
#
# schedule.every().tuesday.at("17:45").do(follow_user_followers_bot)
# schedule.every().thursday.at("17:45").do(follow_user_followers_bot)
# schedule.every().saturday.at("17:45").do(follow_user_followers_bot)
#
# schedule.every().day.at("06:23").do(follow_photo_likers_bot)

try:
    # follow_user_followers_bot()
    # follow_photo_likers_bot()
    like_by_tags_bot()
except Exception as e:
    if e:
        bot.send_message(chat_id='212438834', text=f'Бот словил ошибку {e}, класса{e.__class__}')
        try:
            bot.send_message(chat_id='212438834', text=f'Стартуем снова')
            like_by_tags_bot()
        except Exception as e:
                bot.send_message(chat_id='212438834', text=f'Бот словил ошибку {e}, класса{e.__class__}')
# while True:
#     schedule.run_pending()
