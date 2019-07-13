import getpass
import os
import random
import sys
import time

from tqdm import tqdm

sys.path.append(os.path.join(sys.path[0], '../'))
from instabot import Bot

def initial_checker():
    files = [hashtag_file, users_file, whitelist, blacklist, setting]
    try:
        for f in files:
            with open(f, 'r') as f:
                pass
    except BaseException:
        for f in files:
            with open(f, 'w') as f:
                pass
        print("""
        selamat datang""")
        setting_input()
        print("""
        anda bisa menambahkan hashtag database, competitor database,
        whitelists, blacklists dan juga bisa menambahkan user pengguna di menu setting.
        Have fun with the bot!
        """)
        time.sleep(5)
        os.system('cls')


def read_input(f, msg, n=None):
    if n is not None:
        msg += " (enter to use default number: {})".format(n)
    print(msg)
    entered = sys.stdin.readline().strip() or str(n)
    if isinstance(n, int):
        entered = int(entered)
    f.write(str(entered) + "\n")


def setting_input():
    inputs = [("berapa banyak like yang kamu butuhkan?", 1000),
              ("bagaimana kalau unlike? ", 1000),
              ("berapa banyak komentar yang anda inginkan per hari? ", 100),
              (("Maximal likes in media you will like?\n"
                "kita akan skip jika jumlah like lebih besar dari inlai "), 100),
              ("kasih delay/detik per satu like agar tidak di curigai ", 10),
              ("kasih delay/detik per unlike agar tidak di curigai ", 10),
              ("mau pakai proxy? masukan proxy mu atau kosongkan saja. (tekan enter saja", 'None')]
    
    with open(setting, "w") as f:
        while True:
            for msg, n in inputs:
                read_input(f, msg, n)
            break
        print("Done with all settings!")

def parameter_setting():
    settings = ["Max likes per day: ",
                "Max unlikes per day: ",
                "Max likes to like: ",
                "Like delay: ",
                "Unlike delay: ",
                "Proxy: "]

    with open(setting) as f:
        data = f.readlines()

    print("Current parameters\n")
    for s, d in zip(settings, data):
        print(s + d)

def username_adder():
    with open(SECRET_FILE, "a") as f:
        print("kami butuh akun ig kalian.")
        print("jangan kawatir penyimpanan lokal di perangkat anda saja.")
        while True:
            print("Enter your username: ")
            f.write(str(sys.stdin.readline().strip()) + ":")
            print("Enter your password: (it will not be shown due to security reasons - just start typing and press Enter)")
            f.write(getpass.getpass() + "\n")
            print("mau masukan akun lagi? (y/n)")
            if "y" not in sys.stdin.readline():
                break

def get_adder(name, fname):
    def _adder():
        print("Database yang sudah di buat:")
        print(bot.read_list_from_file(fname))
        with open(fname, "a") as f:
            print('Add {} to database'.format(name))
            while True:
                print("Enter {}: ".format(name))
                f.write(str(sys.stdin.readline().strip()) + "\n")
                print("Do you want to add another {}? (y/n)\n".format(name))
                if "y" not in sys.stdin.readline():
                    print('Done adding {}s to database'.format(name))
                    break
    return _adder()


def hashtag_adder():
    return get_adder('hashtag', fname=hashtag_file)


def competitor_adder():
    return get_adder('username', fname=users_file)


def blacklist_adder():
    return get_adder('username', fname=blacklist)


def whitelist_adder():
    return get_adder('username', fname=whitelist)


def comment_adder():
    return get_adder('comment', fname=comment)


def userlist_maker():
    return get_adder('username', userlist)

def menu():
    ans = True
    while ans:
        print("===============================================")
        print("""[1].Like""")
        print("""[2].setting""")
        print("===============================================")
        ans = input("masukan angka yang anda inginkan\n").strip()
        if ans == "1":
            menu_like()
        elif ans == "2":
            menu_setting()
        else:
            print("\n masukan anda salah")

def menu_like():
    ans = True
    while ans:
        print("===================================================")
        print("""
        1. Like dari masukan hastag
        2. Like postingan pengikut dari si pengikut
        3. Like postingan yg di ikuti
        4. Like dari media sebelumnya
        5. Like dengan gariswaktu anda
        6. Main menu
        """)
        print("===================================================")
        ans = input("bagaimana cara Like yang ingin anda lakukan?\n").strip()

        if ans == "1":
            print("""
            1.Insert hashtag
            2.gunakan hashtag database
            """)
            hashtags = []
            if "1" in sys.stdin.readline():
                print("==========================================================================================")
                hashtags = input("masukan hastag yang di inginkan\ncontoh: kucing indonesia\nmasukan hastag?\n").strip().split(' ')
                print("==========================================================================================")
            else:
                hashtags.append(random.choice(bot.read_list_from_file(hashtag_file)))
            for hashtag in hashtags:
                bot.like_hashtag(hashtag)

        elif ans == "2":
            print("""
            1.Insert username
            2.gunakan username database
            """)
            if "1" in sys.stdin.readline():
                user_id = input("siapa username nya?\n").strip()
            else:
                user_id = random.choice(bot.read_list_from_file(users_file))
            bot.like_followers(user_id)

        elif ans == "3":
            print("""
            1.Insert username
            2.gunakan username database
            """)
            if "1" in sys.stdin.readline():
                user_id = input("siapa username nya?\n").strip()
            else:
                user_id = random.choice(bot.read_list_from_file(users_file))
            bot.like_following(user_id)

        elif ans == "4":
            print("""
            1.Insert username
            2.gunakan username database
            """)
            if "1" in sys.stdin.readline():
                user_id = input("siapa username nya?\n").strip()
            else:
                user_id = random.choice(bot.read_list_from_file(users_file))
            medias = bot.get_user_medias(user_id, filtration=False)
            if len(medias):
                likers = bot.get_media_likers(medias[0])
                for liker in tqdm(likers):
                    bot.like_user(liker, amount=2, filtration=False)

        elif ans == "5":
            bot.like_timeline()

        elif ans == "6":
            menu()

        else:
            print("nomor yang anda masukan salah")
            menu_like()

def menu_setting():
    ans = True
    while ans:
        print("""
        1. Setting bot parameter
        2. Add user accounts
        3. Add competitor database
        4. Add hashtag database
        5. Add blacklist
        6. Add whitelist
        7. Clear all database
        8. Main menu
        """)
        ans = input("settingan apakah yang ingin anda rubah?\n").strip()

        if ans == "1":
            parameter_setting()
            change = input("beneran mau di ganti? y/n\n").strip()
            if change == 'y' or change == 'Y':
                setting_input()
            else:
                menu_setting()
        elif ans == "2":
            username_adder()
        elif ans == "3":
            competitor_adder()
        elif ans == "4":
            hashtag_adder()
        elif ans == "5":
            blacklist_adder()
        elif ans == "6":
            whitelist_adder()
        elif ans == "7":
            print(
                "semua setingan sudah di bersihkan/di reset ulang")
            time.sleep(5)
            open(hashtag_file, 'w')
            open(users_file, 'w')
            open(whitelist, 'w')
            open(blacklist, 'w')
            print("selesai, anda bisa memasukan nya lagi!")
        elif ans == "8":
            menu()
        else:
            print("nomor tidak ada di list?")
            menu_setting()

# untuk mencocokan input
try:
    input = raw_input
except NameError:
    pass

#lokasi file
hashtag_file = "hashtagsdb.txt"
users_file = "usersdb.txt"
whitelist = "whitelist.txt"
blacklist = "blacklist.txt"
userlist = "userlist.txt"
setting = "setting.txt"
SECRET_FILE = "secret.txt"

#cek setting
initial_checker()

if os.stat(setting).st_size == 0:
    print("terlihat like rusak")
    print("yuk bikin baru")
    setting_input()
f = open(setting)
lines = f.readlines()
setting_0 = int(lines[0].strip())
setting_1 = int(lines[1].strip())
setting_2 = int(lines[2].strip())
setting_3 = int(lines[3].strip())
setting_4 = int(lines[4].strip())
setting_5 = int(lines[5].strip())
setting_6 = int(lines[6].strip())
setting_7 = int(lines[7].strip())
setting_8 = int(lines[8].strip())
setting_9 = int(lines[9].strip())
setting_10 = int(lines[10].strip())
setting_11 = int(lines[11].strip())
setting_12 = int(lines[12].strip())
setting_13 = int(lines[13].strip())
setting_14 = int(lines[14].strip())
setting_15 = int(lines[15].strip())
setting_16 = int(lines[16].strip())
setting_17 = int(lines[17].strip())
setting_18 = lines[18].strip()

bot = Bot(
    max_likes_per_day=setting_0,
    max_unlikes_per_day=setting_1,
    max_likes_to_like=setting_5,
    like_delay=setting_13,
    whitelist_file=whitelist,
    blacklist_file=blacklist,
    stop_words=[
        'order',
        'shop',
        'store',
        'free',
        'doodleartindonesia',
        'doodle art indonesia',
        'fullofdoodleart',
        'commission',
        'vector',
        'karikatur',
        'jasa',
        'open'])

bot.login()

while True:
    try:
        menu()
    except Exception as e:
        bot.logger.info("error, read exception bellow")
        bot.logger.info(str(e))
    time.sleep(1)
