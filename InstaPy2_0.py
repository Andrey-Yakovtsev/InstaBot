from instapy import InstaPy
from datasets import tags, skipped_friends, to_follow_list


session = InstaPy(
    username="a_yakovtsev",
    password="Insta331133",
    headless_browser=True,
    disable_image_load=True,
    multi_logs=True,
    bypass_security_challenge_using='sms'
    )
session.login()
session.set_do_follow(enabled=True, percentage=10,times=1)
session.like_by_tags(tags, amount=3)
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
session.like_by_feed(amount=100, randomize=True) # unfollow=True, interact=True) - Лайкает посты в ленте
# Follow the followers of each given user
# users = session.target_list("C:\\Users\\......\\users.txt")
# session.follow_user_followers(users, amount=10, randomize=False)
session.set_delimit_commenting(enabled=True, max_comments=None, min_comments=1)

session.set_comments([u':thumbsup:'])

session.set_relationship_bounds(enabled=True, max_followers=1020500, min_posts=5)

session.set_skip_users(skip_private=True, skip_no_profile_pic=True, skip_business=True,
                       skip_bio_keyword=['доставка', 'заказ', 'оплата'])

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

session.unfollow_users(amount=3,
                       nonFollowers=True,
                       style="RANDOM",
                       unfollow_after=42*60*60,
                       sleep_delay=655)

session.set_dont_unfollow_active_users(enabled=True, posts=5)
session.end()
