from src.Osintgram import Osintgram
import argparse
from src import printcolors as pc
from src import artwork
import sys
import signal

is_windows = False

try:
    import gnureadline  
except: 
    is_windows = True
    import pyreadline


def printlogo():
    pc.printout(artwork.ascii_art, pc.YELLOW)
    pc.printout("\nВерсия 3.0 - by KaliSecurityMax\n\n", pc.YELLOW)
    pc.printout("Введите help для просмотра команд\n")
    pc.printout("Ведите 'FILE=y' чтобы сохранить результаты в '<target username>_<command>.txt (по умолчанию отключено)'\n")
    pc.printout("Ведите 'FILE=n' чтобы отключить сохранение в .txt'\n")
    pc.printout("Ведите 'JSON=y' чтобы сохранить результат в JSON '<target username>_<command>.json (по умолчанию "
                "отключено)'\n")
    pc.printout("Ведите 'JSON=n' чтобы отключить сохранение в .JSON'\n")


def cmdlist():
    pc.printout("FILE=y/n\t")
    print("Включение/выключение вывода в '<target username>_<command>.txt' файл'")
    pc.printout("JSON=y/n\t")
    print("Включение/выключение вывода в '<target username>_<command>.json' файл'")
    pc.printout("addrs\t\t")
    print("Получить все зарегистрированные адреса по целевым фотографиям")
    pc.printout("cache\t\t")
    print("Очистить кэш")
    pc.printout("captions\t")
    print("Получить подписи к фотографиям цели")
    pc.printout("commentdata\t")
    print("Получить список всех комментариев к сообщениям цели")
    pc.printout("comments\t")
    print("Получить список всех комментариев к сообщениям цели")
    pc.printout("followers\t")
    print("Получить список подписчиков")
    pc.printout("followings\t")
    print("Получить пользователей на которых подписан человек")
    pc.printout("fwersemail\t")
    print("Получить электронную почту подписчиков")
    pc.printout("fwingsemail\t")
    print("Получить электронную почту пользователей, на которых подписана цель")
    pc.printout("fwersnumber\t")
    print("Получить номер телефона подписчиков")
    pc.printout("fwingsnumber\t")
    print("Получить номер телефона пользователей, на которых подписана цель")    
    pc.printout("hashtags\t")
    print("Получить хэштеги, используемые целью")
    pc.printout("info\t\t")
    print("Получить информацию о целе")
    pc.printout("likes\t\t")
    print("Получить общее кол-во лайков на посты цели")
    pc.printout("mediatype\t")
    print("Получите тип сообщений цели (фото или видео)")
    pc.printout("photodes\t")
    print("Получить описание фотографий цели")
    pc.printout("photos\t\t")
    print("Скачать фотографии цели")
    pc.printout("propic\t\t")
    print("Скачать фотографию профиля цели")
    pc.printout("stories\t\t")
    print("Скачать истории цели")
    pc.printout("tagged\t\t")
    print("Получить список пользователей, отмеченных по цели")
    pc.printout("target\t\t")
    print("Установить новую цель")
    pc.printout("wcommented\t")
    print("Получить список пользователей, которые прокомментировали фотографии цели")
    pc.printout("wtagged\t\t")
    print("Получить список пользователей, которые отметили цель")


def signal_handler(sig, frame):
    pc.printout("\Завершение работы!\n", pc.RED)
    sys.exit(0)


def completer(text, state):
    options = [i for i in commands if i.startswith(text)]
    if state < len(options):
        return options[state]
    else:
        return None

def _quit():
    pc.printout("Завершение работы!\n", pc.RED)
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)
if is_windows:
    pyreadline.Readline().parse_and_bind("tab: complete")
    pyreadline.Readline().set_completer(completer)
else:
    gnureadline.parse_and_bind("tab: complete")
    gnureadline.set_completer(completer)

parser = argparse.ArgumentParser(description='Данная программа -это инструмент OSINT в Instagram.'
                                             ' Разработана для проведения анализа аккаунта Instagram любого пользователя по его нику')
parser.add_argument('id', type=str,  # var = id
                    help='username')
parser.add_argument('-C','--cookies', help='очистка cookies файлов', action="store_true")
parser.add_argument('-j', '--json', help='сохранить вывод команд в виде файла JSON', action='store_true')
parser.add_argument('-f', '--file', help='сохранить вывод в файле', action='store_true')
parser.add_argument('-c', '--command', help='запуск в режиме одной команды и выполнение предоставленной команды', action='store')
parser.add_argument('-o', '--output', help='где хранить фотографии', action='store')

args = parser.parse_args()


api = Osintgram(args.id, args.file, args.json, args.command, args.output, args.cookies)



commands = {
    'list':             cmdlist,
    'help':             cmdlist,
    'quit':             _quit,
    'exit':             _quit,
    'addrs':            api.get_addrs,
    'cache':            api.clear_cache,
    'captions':         api.get_captions,
    "commentdata":      api.get_comment_data,
    'comments':         api.get_total_comments,
    'followers':        api.get_followers,
    'followings':       api.get_followings,
    'fwersemail':       api.get_fwersemail,
    'fwingsemail':      api.get_fwingsemail,
    'fwersnumber':      api.get_fwersnumber,
    'fwingsnumber':     api.get_fwingsnumber,
    'hashtags':         api.get_hashtags,
    'info':             api.get_user_info,
    'likes':            api.get_total_likes,
    'mediatype':        api.get_media_type,
    'photodes':         api.get_photo_description,
    'photos':           api.get_user_photo,
    'propic':           api.get_user_propic,
    'stories':          api.get_user_stories,
    'tagged':           api.get_people_tagged_by_user,
    'target':           api.change_target,
    'wcommented':       api.get_people_who_commented,
    'wtagged':          api.get_people_who_tagged
}


signal.signal(signal.SIGINT, signal_handler)
if is_windows:
    pyreadline.Readline().parse_and_bind("tab: complete")
    pyreadline.Readline().set_completer(completer)
else:
    gnureadline.parse_and_bind("tab: complete")
    gnureadline.set_completer(completer)

if not args.command:
    printlogo()


while True:
    if args.command:
        cmd = args.command
        _cmd = commands.get(args.command)
    else:
        signal.signal(signal.SIGINT, signal_handler)
        if is_windows:
            pyreadline.Readline().parse_and_bind("tab: complete")
            pyreadline.Readline().set_completer(completer)
        else:
            gnureadline.parse_and_bind("tab: complete")
            gnureadline.set_completer(completer)
        pc.printout("Выполнить команду: ", pc.YELLOW)
        cmd = input()

        _cmd = commands.get(cmd)

    if _cmd:
        _cmd()
    elif cmd == "FILE=y":
        api.set_write_file(True)
    elif cmd == "FILE=n":
        api.set_write_file(False)
    elif cmd == "JSON=y":
        api.set_json_dump(True)
    elif cmd == "JSON=n":
        api.set_json_dump(False)
    elif cmd == "":
        print("")
    else:
        pc.printout("Неизвестная команда. Весь список команд - help\n", pc.RED)

    if args.command:
        break
