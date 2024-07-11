# -*- coding: utf8 -*-
import configparser
from telebot import TeleBot
from telebot.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
import random
import time
from pathlib import Path
from keyboards import *
from date_validator import *
from word_validator import *
from answers import *
from adress_validator import *
from sqlite_req import main
from popularity_sights import most_popular_sights

config = configparser.ConfigParser()

config.read('config.ini')

# main("CREATE TABLE Sights (`id` INTEGER PRIMARY KEY AUTOINCREMENT, `area` TEXT, `year` INTEGER, `season` TEXT, `month` TEXT, `description` TEXT, `feedback` TEXT, `mark` INTEGER, `tags` TEXT, `date` TEXT, `userid` INTEGER, `src` TEXT);")
# main("CREATE TABLE Moders (`id` INTEGER PRIMARY KEY AUTOINCREMENT, `moder_id` INTEGER, UNIQUE(moder_id));")
# main("CREATE TABLE Reactions (`id` INTEGER PRIMARY KEY AUTOINCREMENT, `userid` INTEGER, `messageid` INTEGER, `flag` INTEGER);")
# main("DROP TABLE Reactions;")
# main("DELETE FROM Reactions;")
# main(f"INSERT INTO Moders (`moder_id`) VALUES ('')")


TOKEN_BOT = config['BOT']['TokenBot']
bot = TeleBot(TOKEN_BOT)
MODER_IDS = main(f"SELECT moder_id FROM Moders;")

def menu(message):  
    bot.send_message(message.chat.id, '⬇️<b>Выберите, что вы хотите сделать:\n</b>/new - Создать новую запись о месте\n\n/find - Подобрать подходящие вам места по фильтрам\n\n/feedback - Отзывы/предложения/Нашли баг\n\n/help - Помощь', reply_markup=ReplyKeyboardRemove(), parse_mode="html")
    bot.register_next_step_handler(message, get_menu_mess)


def get_menu_mess(message):
    if message.content_type == 'text':
        if message.text == '/start':
                start(message)

        elif message.text == '/new':
            get_area(message)
        
        elif message.text == '/find':
            get_find_criterion(message)

        elif message.text == '/feedback':
            start_support(message)

        elif message.text == '/help':
            help(message)

        elif len(set(message.text.lower().split()) & set(["как", "дела"])) == 2:
            bot.send_message(message.chat.id, f'<b>{howareyou[random.randint(0, 3)]}</b>', reply_markup=ReplyKeyboardRemove(), parse_mode="html")
            menu(message)
        elif len(set(message.text.lower().split()) & set(["что", "делаешь"])) == 2:
            bot.send_message(message.chat.id, f'<b>{whatareudo[random.randint(0, 3)]}</b>', reply_markup=ReplyKeyboardRemove(), parse_mode="html")
            menu(message)
        elif len(set(message.text.lower().split()) & set(["как", "тебя", "зовут"])) == 3:
            bot.send_message(message.chat.id, f'<b>{botname[random.randint(0, 2)]}</b>', reply_markup=ReplyKeyboardRemove(), parse_mode="html")
            menu(message)
        elif len(set(message.text.lower().split()) & set(["кто", "ты"])) == 2: 
            bot.send_message(message.chat.id, f'<b>{whoareu[random.randint(0, 1)]}</b>', reply_markup=ReplyKeyboardRemove(), parse_mode="html")
            menu(message)
        else:
            bot.send_message(message.chat.id, '🙁<b>Извините, не понимаю Вас. Попробуйте снова</b>', reply_markup=ReplyKeyboardRemove(), parse_mode="html")
            menu(message)
    else:
        bot.send_message(message.chat.id, '📄<b>Следует отправлять текст. Попробуйте снова</b>', reply_markup=ReplyKeyboardRemove(), parse_mode="html")
        menu(message)


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, '<b>Здравствуй, хочешь предложить или найти свою достопримечательность/место? Вперёд!</b>\n\nОчень актуально сейчас в связи с геополитической обстановкой в мире давать больше информации населению о привлекательности наших курортов, городов.\n\nНаша страна имеет невероятное количество возможностей для развития внутренней туристической отрасли.\n\nШирокая география, богатство культурных и природных ценностей дает нам возможность внутри страны получать новые впечатления, знания и эмоции. Множество уголков остаются неизведанными для некоторой аудитории нашей огромной Родины.\n\nЕсли непонятно, что нужно делать\n/help\n\nНаш канал с различными достопримечательностями и прочим: https://t.me/LocalSight73', reply_markup=ReplyKeyboardRemove(), parse_mode="html")
    menu(message)



@bot.message_handler(commands=['new'])
def get_area(message):
    bot.send_message(message.chat.id, '1️⃣ <b>Напишите адрес места (с указанием города) или отправьте точку на карте:</b>', reply_markup=ReplyKeyboardRemove(), parse_mode="html")
    bot.register_next_step_handler(message, get_year)


def get_year(message):
    if message.content_type == 'text':
        if check_words(message.text.lower()):
            if get_coords(message.text):
                bot.send_message(message.chat.id, '2️⃣ <b>В каком году Вы посещали достопримечательность/место?</b>', reply_markup=kb_year, parse_mode="html")
                bot.register_next_step_handler(message, get_season, get_coords(message.text))
            else:
                bot.send_message(message.chat.id, '🙁<b>Извините, мне не удалось определить координаты места. Проверьте правильность написания адреса (не забудьте указывать город) или попробуйте отправить точку на карте.</b>', reply_markup=ReplyKeyboardRemove(), parse_mode="html")
                menu(message)
        elif message.text.lower() == "🔙 назад":
            menu(message)
        else:
            bot.send_message(message.chat.id, '🙁<b>Извините, не понимаю Вас. Текст может содержать только буквы русского алфавита, цифры и базовые знаки препинания</b>', reply_markup=ReplyKeyboardRemove(), parse_mode="html")
            menu(message)
    elif message.location is not None:
        coord = str(message.location.longitude) + ',' + str(message.location.latitude) 
        if get_adress(coord):
            bot.send_message(message.chat.id, '2️⃣ <b>В каком году Вы посещали достопримечательность/место?</b>', reply_markup=kb_year, parse_mode="html")
            bot.register_next_step_handler(message, get_season, coord)
        else:
            bot.send_message(message.chat.id, '🙁<b>Извините, мне не удалось определить адрес места. Проверьте правильность написания координат ыили попробуйте отправить адрес места (не забудьте указывать город).</b>', reply_markup=kb_year, parse_mode="html")
            menu(message)
    else:
        bot.send_message(message.chat.id, '📄📍<b>Следует отправлять текст или геолокацию. Попробуйте снова</b>', reply_markup=ReplyKeyboardRemove(), parse_mode="html")
        menu(message)


def get_season(message, ms_area):
    if message.content_type == 'text':
        if message.text in ("2024","2023", "2022", "2021", "2020", "2019"):
            bot.send_message(message.chat.id, '3️⃣ <b>В каком сезоне Вы посещали её/его?</b>', reply_markup=kb_season, parse_mode="html")
            bot.register_next_step_handler(message, get_month, ms_area, message.text)
        elif message.text.lower() == "🔙 назад":
            bot.send_message(message.chat.id, '1️⃣ <b>В каком районе находится достопримечательность/место?</b>', reply_markup=kb_area, parse_mode="html")
            bot.register_next_step_handler(message, get_year)
        else:
            bot.send_message(message.chat.id, '🙁<b>Извините, не понимаю Вас. Попробуйте снова</b>', reply_markup=ReplyKeyboardRemove(), parse_mode="html")
            menu(message)
    else:
        bot.send_message(message.chat.id, '📄<b>Следует отправлять текст. Попробуйте снова</b>', reply_markup=ReplyKeyboardRemove(), parse_mode="html")
        menu(message)


def get_month(message, ms_area, ms_year):
    if message.content_type == 'text':
        if message.text.lower() in ("зима", "весна", "лето", "осень"):
            bot.send_message(message.chat.id, '4️⃣ <b>В каком месяце Вы посещали достопримечательность/место?</b>', reply_markup=set_month(message.text.lower()), parse_mode="html")
            bot.register_next_step_handler(message, get_description, ms_area, ms_year, message.text)
        elif message.text.lower() == "🔙 назад":
            bot.send_message(message.chat.id, '2️⃣ <b>В каком году Вы посещали достопримечательность/место?</b>', reply_markup=kb_year, parse_mode="html")
            bot.register_next_step_handler(message, get_season, message.text)
        else:
            bot.send_message(message.chat.id, '🙁<b>Извините, не понимаю Вас. Попробуйте снова</b>', reply_markup=ReplyKeyboardRemove(), parse_mode="html")
            menu(message)
    else:
        bot.send_message(message.chat.id, '📄<b>Следует отправлять текст. Попробуйте снова</b>', reply_markup=ReplyKeyboardRemove(), parse_mode="html")
        menu(message)


def set_month(season):
    kb_mnh = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    if season == "зима":
        for btn_winter in btns_winter:     
            kb_mnh.add(btn_winter)
    elif season == "весна":
        for btn_spring in btns_spring:     
            kb_mnh.add(btn_spring)
    elif season == "лето":
        for btn_summer in btns_summer:     
            kb_mnh.add(btn_summer)
    elif season == "осень":
        for btn_autumn in btns_autumn:     
            kb_mnh.add(btn_autumn)
    return kb_mnh
            

def get_description(message, ms_area, ms_year, ms_sesson):
    if message.content_type == 'text':
        if message.text.lower() == "🔙 назад":
            bot.send_message(message.chat.id, '3️⃣ <b>В каком сезоне Вы посещали её/его?</b>', reply_markup=kb_season, parse_mode="html")
            bot.register_next_step_handler(message, get_month, ms_area, message.text)
        elif message.text.lower() in ("декабрь", "январь", "февраль", "март", "апрель", "май", "июнь", "июль", "август", "сентябрь", "октябрь", "ноябрь"):
            bot.send_message(message.chat.id, '5️⃣ <b>Опишите данную достопримечательность/место: </b>\n<em>Не менее 100 символов</em>\n<em>Текст может содержать только буквы русского алфавита, цифры и базовые знаки препинания</em>', reply_markup=ReplyKeyboardRemove(), parse_mode="html")
            bot.register_next_step_handler(message, get_feedback, ms_area, ms_year, ms_sesson, message.text)
        else:
            bot.send_message(message.chat.id, '🙁<b>Извините, не понимаю Вас. Попробуйте снова</b>', reply_markup=ReplyKeyboardRemove(), parse_mode="html")
            menu(message)
    else:
        bot.send_message(message.chat.id, '📄<b>Следует отправлять текст. Попробуйте снова</b>', reply_markup=ReplyKeyboardRemove(), parse_mode="html")
        menu(message)


def get_feedback(message, ms_area, ms_year, ms_sesson, ms_month):
    if message.content_type == 'text':
        if 100 <= len(message.text) <= 1000:
            if check_words(message.text.lower()):
                bot.send_message(message.chat.id, '6️⃣ <b>Напишите отзыв о ней/нём: </b>\n<em>Не менее 50 символов\nТекст может содержать только буквы русского алфавита, цифры и базовые знаки препинания</em>', reply_markup=ReplyKeyboardRemove(), parse_mode="html")
                bot.register_next_step_handler(message, get_mark, ms_area, ms_year, ms_sesson, ms_month, message.text)
            elif check_words(message.text.lower()) == 'forbidden_words':
                bot.send_message(message.chat.id, '🙁<b>Текст содержит недопустимые слова. Попробуйте снова</b>', reply_markup=ReplyKeyboardRemove(), parse_mode="html")
                menu(message)
            else:
                bot.send_message(message.chat.id, '🙁<b>Текст может содержать только буквы русского алфавита, цифры и базовые знаки препинания. Попробуйте снова</b>', reply_markup=ReplyKeyboardRemove(), parse_mode="html")
                menu(message)
        else:
            bot.send_message(message.chat.id, '🙁<b>Извините, количество символов должно быть не менее 100 и не более 1000. Попробуйте снова</b>', reply_markup=ReplyKeyboardRemove(), parse_mode="html")
            menu(message)
    else:
        bot.send_message(message.chat.id, '📄<b>Следует отправлять текст. Попробуйте снова</b>', reply_markup=ReplyKeyboardRemove(), parse_mode="html")
        menu(message)


def get_mark(message, ms_area, ms_year, ms_sesson, ms_month, ms_description):
    if message.content_type == 'text':
        if message.text.lower() == "🔙 назад":
                bot.send_message(message.chat.id, '5️⃣ <b>Опишите данную достопримечательность/место: </b>\n<em>Не менее 100 символов\nТекст может содержать только буквы русского алфавита, цифры и базовые знаки препинания</em>', reply_markup=ReplyKeyboardRemove(), parse_mode="html")
                bot.register_next_step_handler(message, get_feedback, ms_area, ms_year, ms_sesson, message.text)
        elif 50 <= len(message.text) <= 1000:
            if check_words(message.text.lower()):
                bot.send_message(message.chat.id, '7️⃣ <b>Ваша субъективная оценка </b>\n<em>От 1 до 10:</em>', reply_markup=ReplyKeyboardRemove(), parse_mode="html")
                bot.register_next_step_handler(message, get_tags, ms_area, ms_year, ms_sesson, ms_month, ms_description, message.text)
            elif check_words(message.text.lower()) == 'forbidden_words':
                bot.send_message(message.chat.id, '🙁<b>Текст содержит недопустимые слова. Попробуйте снова</b>', reply_markup=ReplyKeyboardRemove(), parse_mode="html")
                menu(message) 
            else:
                bot.send_message(message.chat.id, '🙁<b>Текст может содержать только буквы русского алфавита, цифры и базовые знаки препинания. Попробуйте снова</b>', reply_markup=ReplyKeyboardRemove(), parse_mode="html")
                menu(message)
        else:
            bot.send_message(message.chat.id, '🙁<b>Извините, количество символов должно быть не менее 50 и не более 1000. Попробуйте снова</b>', reply_markup=ReplyKeyboardRemove(), parse_mode="html")
            menu(message)
    else:
        bot.send_message(message.chat.id, '📄<b>Следует отправлять текст. Попробуйте снова</b>', reply_markup=ReplyKeyboardRemove(), parse_mode="html")
        menu(message)


def get_tags(message, ms_area, ms_year, ms_sesson, ms_month, ms_description, ms_feedback):
    if message.content_type == 'text':
        if message.text in ("1", "2", "3", "4", "5", "6", "7", "8", "9", "10"):
            bot.send_message(message.chat.id, '8️⃣ <b>Напишите одну категорию, к которой относится данное место</b>', reply_markup=ReplyKeyboardRemove(), parse_mode="html")
            bot.register_next_step_handler(message, choise_photo, ms_area, ms_year, ms_sesson, ms_month, ms_description, ms_feedback, message.text)
        elif message.text.lower() == "🔙 назад":
            bot.send_message(message.chat.id, '6️⃣ <b>Напишите отзыв о ней/нём: </b>\n<em>Не менее 50 символов</em>', reply_markup=ReplyKeyboardRemove(), parse_mode="html")
            bot.register_next_step_handler(message, get_mark, ms_area, ms_year, ms_sesson, ms_month, message.text)
        else:
            bot.send_message(message.chat.id, '🙁<b>Извините, число должно быть от 1 до 10. Попробуйте снова</b>', reply_markup=ReplyKeyboardRemove(), parse_mode="html")
            menu(message)
    else:
        bot.send_message(message.chat.id, '📄<b>Следует отправлять текст. Попробуйте снова</b>', reply_markup=ReplyKeyboardRemove(), parse_mode="html")
        menu(message)


def choise_photo(message, ms_area, ms_year, ms_sesson, ms_month, ms_description, ms_feedback, ms_mark):
    if message.content_type == 'text':
        if check_words(message.text.lower()):
            bot.send_message(message.chat.id,  '9️⃣ <b>У вас есть фотография этой достопримечательности/места?</b>', reply_markup=kb_y_n, parse_mode="html")
            bot.register_next_step_handler(message, choise_moder, ms_area, ms_year, ms_sesson, ms_month, ms_description, ms_feedback, ms_mark, message.text)
        elif message.text.lower() == "🔙 назад":
            bot.send_message(message.chat.id, '7️⃣ <b>Ваша субъективная оценка </b>\n<em>От 1 до 10:</em>', reply_markup=ReplyKeyboardRemove(), parse_mode="html")
            bot.register_next_step_handler(message, get_tags, ms_area, ms_year, ms_sesson, ms_month, ms_description, message.text)
        else:
            bot.send_message(message.chat.id, '🙁<b>Следует писать единственную категорию длинною не меньше 2 знаков, используя русские символы</b>', reply_markup=ReplyKeyboardRemove(), parse_mode="html")
            menu(message)
    else:
        bot.send_message(message.chat.id, '📄<b>Следует отправлять текст. Попробуйте снова</b>', reply_markup=ReplyKeyboardRemove(), parse_mode="html")
        menu(message)


def choise_moder(message, ms_area, ms_year, ms_sesson, ms_month, ms_description, ms_feedback, ms_mark, ms_tags):
    if message.content_type == 'text':
        if message.text.lower() in ("✅да", "да"):
            bot.send_message(message.chat.id, '📸<b>Отправьте фотографию: </b>', reply_markup=ReplyKeyboardRemove(), parse_mode="html")
            bot.register_next_step_handler(message, get_photo, ms_area, ms_year, ms_sesson, ms_month, ms_description, ms_feedback, ms_mark, ms_tags)
        elif message.text.lower() in ("❌нет", "нет"):     
            bot.send_message(message.chat.id, '📥<b>Данные получены, отправить на модерацию?</b>', reply_markup=kb_y_n, parse_mode="html")
            bot.register_next_step_handler(message, insert_and_send, ms_area, ms_year, ms_sesson, ms_month, ms_description, ms_feedback, ms_mark, ms_tags)
        elif message.text.lower() == "🔙 назад":
            bot.send_message(message.chat.id, '8️⃣ <b>Напишите одну категорию, к которой относится данное место</b>', reply_markup=ReplyKeyboardRemove(), parse_mode="html")
            bot.register_next_step_handler(message, choise_photo, ms_area, ms_year, ms_sesson, ms_month, ms_description, ms_feedback, message.text)
        else:
            bot.send_message(message.chat.id, '🫢<b>Выберите одно из предложенных ответов. Попробуйте снова</b>', reply_markup=kb_y_n, parse_mode="html")
            menu(message)
    else:
        bot.send_message(message.chat.id, '📄<b>Следует отправлять текст. Попробуйте снова</b>', reply_markup=ReplyKeyboardRemove(), parse_mode="html")
        menu(message)


def get_photo(message, ms_area, ms_year, ms_sesson, ms_month, ms_description, ms_feedback, ms_mark, ms_tags):
    try:
        Path(f'files/{message.chat.id}/').mkdir(parents = True, exist_ok = True) # Создание папки

        if message.content_type == 'photo':              
            file_info = bot.get_file(message.photo[len(message.photo) - 1].file_id) 
            downloaded_file = bot.download_file(file_info.file_path)
            src = f'files/{message.chat.id}/{datetime.datetime.now().strftime("%Y%m%d_%H%M")}{file_info.file_path.replace("photos/", "")}'
            bot.send_message(message.chat.id, '📥<b>Данные получены, отправить на модерацию?</b>', reply_markup=kb_y_n, parse_mode="html")
          
            with open(src, 'wb') as new_file:   # Сохраняем файл
                new_file.write(downloaded_file)
            bot.register_next_step_handler(message, insert_and_send, ms_area, ms_year, ms_sesson, ms_month, ms_description, ms_feedback, ms_mark, ms_tags, src)
        else:
            bot.send_message(message.chat.id, '🫢<b>Нужно отправлять изображение, а не прочие типы данных. Попробуйте снова</b>', reply_markup=ReplyKeyboardRemove(), parse_mode="html")
            menu(message)

    except Exception as e:
        bot.send_message(message.chat.id, '🫢<b>Произошла ошибка при сохранении фотографии. Попробуйте снова</b>', reply_markup=ReplyKeyboardRemove(), parse_mode="html")
        menu(message)
        print(f'!!!{e}')


bot.message_handler(content_types=["text"])
def insert_and_send(message, ms_area, ms_year, ms_sesson, ms_month, ms_description, ms_feedback, ms_mark, ms_tags, src = False):
    if message.content_type == 'text':
        if message.text.lower() in ("✅да", "да"):
            bot.send_message(message.chat.id, '🆗 <b>Спасибо за то, что внесли данные. Мы уведовим вас, если данные пройдут модерацию</b>', reply_markup=ReplyKeyboardRemove(), parse_mode="html")  
            date = datatime.now().strftime("%d.%m.%Y") 
            for moder_id in MODER_IDS:
                if src:
                    main(f"INSERT INTO Sights (`area`, `year`, `season`, `month`, `description`, `feedback`, `mark`, `tags`, `date`, `userid`, `src`) VALUES ('{ms_area}', '{ms_year}', '{ms_sesson}', '{ms_month}', '{ms_description}', '{ms_feedback}', '{ms_mark}', '{ms_tags}', '{date}', '{message.from_user.id}', '{src}')")
                    dates_id = main(f"SELECT id FROM Sights WHERE area='{ms_area}' AND year='{ms_year}' AND season='{ms_sesson}' AND month='{ms_month}' AND description='{ms_description}' AND feedback='{ms_feedback}' AND mark='{ms_mark}' AND tags='{ms_tags}' AND userid='{message.from_user.id}' AND `src`='{src}';")
                    if dates_id:
                        bot.send_photo(moder_id[0], open(src,'rb'))
                        bot.send_location(moder_id[0], longitude=ms_area.split(',')[0], latitude=ms_area.split(',')[1])
                        bot.send_message(moder_id[0], f"<b>Локация:</b> {get_adress(ms_area)}\n\n<b>Год:</b> {ms_year}\n\n<b>Сезон:</b> {ms_sesson}\n\n<b>Месяц:</b> {ms_month}\n\n<b>Описание:</b> {ms_description}\n\n<b>Отзыв:</b> {ms_feedback}\n\n<b>Субъективная оценка пользователя:</b> {ms_mark}\n\n{ms_tags}", reply_markup = mod_markup(dates_id), parse_mode="html")
                    else:
                        bot.send_message(message.chat.id, '🫢<b>Произошла ошибка при сохранении фотографии. Попробуйте снова</b>', reply_markup=ReplyKeyboardRemove(), parse_mode="html")
                        menu(message)
                        print("dates_id не найдено")
                else:
                    main(f"INSERT INTO Sights (`area`, `year`, `season`, `month`, `description`, `feedback`, `mark`, `tags`, `date`, `userid`, `src`) VALUES ('{ms_area}', '{ms_year}', '{ms_sesson}', '{ms_month}', '{ms_description}', '{ms_feedback}', '{ms_mark}', '{ms_tags}', '{date}', '{message.from_user.id}', '0')")
                    dates_id = main(f"SELECT id FROM Sights WHERE area='{ms_area}' AND year='{ms_year}' AND season='{ms_sesson}' AND month='{ms_month}' AND description='{ms_description}' AND feedback='{ms_feedback}' AND mark='{ms_mark}' AND tags='{ms_tags}' AND userid='{message.from_user.id}' AND src='0';")
                    if dates_id:
                        bot.send_location(moder_id[0], longitude=ms_area.split(',')[0], latitude=ms_area.split(',')[1])
                        bot.send_message(moder_id[0], f"<b>Локация:</b> {get_adress(ms_area)}\n\n<b>Год:</b> {ms_year}\n\n<b>Сезон:</b> {ms_sesson}\n\n<b>Месяц:</b> {ms_month}\n\n<b>Описание:</b> {ms_description}\n\n<b>Отзыв:</b> {ms_feedback}\n\n<b>Субъективная оценка пользователя:</b> {ms_mark}\n\n{ms_tags}", reply_markup = mod_markup(dates_id), parse_mode="html")
                    else:
                        bot.send_message(message.chat.id, '🫢<b>Произошла ошибка при сохранении фотографии. Попробуйте снова</b>', reply_markup=ReplyKeyboardRemove(), parse_mode="html")
                        menu(message)
                        print("dates_id не найдено")

        elif message.text.lower() in ("❌нет", "нет"):
            bot.send_message(message.chat.id, '🔜<b>Будем ждать вас снова!</b>', reply_markup=ReplyKeyboardRemove(), parse_mode="html")
            start(message)

        else:
            bot.send_message(message.chat.id, '🙁<b>Извините, не понимаю Вас. Попробуйте снова</b>', reply_markup=ReplyKeyboardRemove(), parse_mode="html")
            menu(message)
    else:
        bot.send_message(message.chat.id, '📄<b>Следует отправлять текст. Попробуйте снова</b>', reply_markup=ReplyKeyboardRemove(), parse_mode="html")
        menu(message)



@bot.message_handler(commands=['feedback'])
def start_support(message):
    bot.send_message(message.chat.id , '↘️<b>Оставьте ваше сообщение:</b>\n<em>Я передам его модераторам бота</em>', parse_mode="html", reply_markup=ReplyKeyboardRemove())
    bot.register_next_step_handler(message, get_support)


def get_support(message):
    bot.send_message(message.chat.id, '😇<b>Cпасибо за обратную связь, мы ценим это!</b>', parse_mode="html")
    for moder_id in MODER_IDS:
        bot.send_message(moder_id[0], f"<b>Сообщение пользователя</b> @{message.from_user.username}", parse_mode="html", reply_markup=ReplyKeyboardRemove())
        bot.forward_message(moder_id[0], message.chat.id, message.message_id)



# Кнопки для модератора
def mod_markup(dates_id):
    markup_y_n = InlineKeyboardMarkup()
    markup_y_n.row_width = 2
    markup_y_n.add(InlineKeyboardButton("✅Запостить", callback_data=f"1 {dates_id[0][0]} Yes"), InlineKeyboardButton("❌Проигноривовать", callback_data=f"1 {dates_id[0][0]} No"))
    return markup_y_n

def reaction_markup(postid):
    likes, dislikes = get_reactions_from_bd(postid)
    markup_reaction = InlineKeyboardMarkup()
    markup_reaction.row_width = 2
    markup_reaction.add(InlineKeyboardButton(f"🔥 {likes}", callback_data=f"reaction {postid} 1"), InlineKeyboardButton(f"❄ {dislikes}", callback_data=f"reaction {postid} 0"))
    return markup_reaction

def get_reactions_from_bd(postid):
    flags = main(f'SELECT flag FROM Reactions WHERE messageid = "{postid}"') # [(1,), (1,), (1,)]
    sum_or_likes = 0
    for flag in flags:
        sum_or_likes += flag[0]
    dislike = len(flags) - sum_or_likes
    return [sum_or_likes, dislike]

# Обработчик call_back
@bot.callback_query_handler(func=lambda call: True)
def get_call(call):
    call_data = call.data.split()
    if call_data[0] == '1':
        print(call_data)
        data = main(f"SELECT * FROM Sights WHERE `id`={call_data[1]}")
        area, year, season, month, description, feedback, mark, tags, src = data[0][1], data[0][2], data[0][3], data[0][4], data[0][5], data[0][6], data[0][7], data[0][8], data[0][11]
        for moder_id in MODER_IDS:
            if call_data[2] == "Yes":
                if src != '0':
                    bot.send_photo(-1001701836271, open(src, 'rb'))
                bot.send_location(-1001701836271, longitude=area.split(',')[0], latitude=area.split(',')[1])
                bot.send_message(-1001701836271, f"<b>🏢Район: </b> {get_adress(area)}\n\n<b>⏳Год: </b> {year}\n\n<b>🏝️Сезон: </b> {season}\n\n<b>📅Месяц: </b> {month}\n\n<b>📝Описание: </b> {description}\n\n<b>📈Отзыв: </b> {feedback}\n\n<b>🌟Оценка пользователя: </b> {mark}\n\n{tags}", parse_mode="html")
                bot.send_message(moder_id[0], "✅<b>Пост опубликован</b>", reply_markup=ReplyKeyboardRemove(), parse_mode="html")
                bot.send_message(data[0][10], '✅<b>Спасибо, ваши данные успешно прошли модерацию и опубликованы на канал!</b>', reply_markup=ReplyKeyboardRemove(), parse_mode="html")
                bot.answer_callback_query(call.id, "OK, POST PUBLISHED")

            elif call_data[2] == "No":
                bot.send_message(data[0][10], '❌<b>Простите, данные не прошли модерацию. Повторите попытку</b>', parse_mode="html")
                bot.send_message(moder_id[0], "❌<b>Пост проигнорирован</b>", reply_markup=ReplyKeyboardRemove(), parse_mode="html")
                main(f"DELETE FROM Sights WHERE `id` = {call_data[1]};")
                bot.answer_callback_query(call.id, "OK, POST IGNORED")
            
    
    if call_data[0] == 'reaction':   #  ['reaction', '1', '1']     
        userid_to_check = main(f"SELECT userid, messageid, flag FROM Reactions WHERE messageid = '{call_data[1]}' AND userid = '{call.message.chat.id}'")
        if userid_to_check:
            if tuple([call.message.chat.id, int(call_data[1])]) == userid_to_check[0][:2]: # сравнивание пары userid - messageid
                bot.answer_callback_query(callback_query_id=call.id, show_alert=True, text="Вы уже поставили реакцию!")
                 
        else:
            bot.edit_message_reply_markup(chat_id = call.message.chat.id, message_id=call.message.message_id, reply_markup = recreation_markup_plus(call_data[1], call_data[2]))
            main(f"INSERT INTO Reactions (`userid`, `messageid`, `flag`) VALUES ('{call.message.chat.id}', '{call_data[1]}', '{call_data[2]}')")      
            if call_data[2] == "1":  
                bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="LIKE")
            elif call_data[2] == "0":
                bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="DISLIKE")
            else:
                bot.answer_callback_query(callback_query_id=call.id, show_alert=True, text="Произошла ошибка, попробуйте снова!")


def recreation_markup_plus(postid, flag):
    likes, dislikes = get_reactions_from_bd(postid)
    if likes >= 0 and dislikes >= 0:
        recreation_markup_reaction = InlineKeyboardMarkup()
        if flag == '1':
            recreation_markup_reaction.row(InlineKeyboardButton(f"🔥 {likes + 1}", callback_data=f"reaction {postid} 1"), InlineKeyboardButton(f"❄ {dislikes}", callback_data=f"reaction {postid} 0"))
        elif flag == '0':
            recreation_markup_reaction.row(InlineKeyboardButton(f"🔥 {likes}", callback_data=f"reaction {postid} 1"), InlineKeyboardButton(f"❄ {dislikes + 1}", callback_data=f"reaction {postid} 0"))
        else:
            print('Error recreation_markup_plus')
        return recreation_markup_reaction
    else:
        print('Кол-во лайков меньше 0')
        return recreation_markup_reaction.row(InlineKeyboardButton(f"🔥 {likes}", callback_data=f"reaction {postid} 1"), InlineKeyboardButton(f"❄ {dislikes}", callback_data=f"reaction {postid} 0"))
        


@bot.message_handler(commands=['find'])
def get_find_criterion(message): 
    bot.send_message(message.chat.id, '🔍<b>Выберите, по чему вы хотите найти место</b>', reply_markup=kb_criterion, parse_mode="html")
    bot.register_next_step_handler(message, processing_criterion)


def processing_criterion(message):
    if message.content_type == 'text':
        if message.text.lower() in ("дата добавления", "📆 дата добавления"):
            bot.send_message(message.chat.id , '📆<b>Введите дату в формате ДД.ММ.ГГГГ</b>\n<em>Или ДД.ММ.ГГГГ-ДД.ММ.ГГГГ</em>', reply_markup=ReplyKeyboardRemove(), parse_mode="html")
            bot.register_next_step_handler(message, for_date)
        elif message.text.lower() in ("оценка", "🌟 оценка"):
            bot.send_message(message.chat.id , '🌟<b>Напишите число или промежуток чисел</b>\n<em>Через "-"</em>\n<em>От 1 до 10:</em>', reply_markup=ReplyKeyboardRemove(), parse_mode="html")
            bot.register_next_step_handler(message, for_mark)
        elif message.text.lower() in ("категория", "#⃣ категория"):
            bot.send_message(message.chat.id , '#⃣<b>Напишите одну категорию\n\nНапример: Музей; Кинотеатр</b>', reply_markup=ReplyKeyboardRemove(), parse_mode="html")
            bot.register_next_step_handler(message, for_tag)
        elif message.text.lower() in ("популярное", "🔥 популярное"):
            for_popularity(message)
        elif message.text.lower() in ("случайно", "🎲 случайно"):
            for_random(message)
        elif message.text.lower() == "🔙 назад":
            menu(message)
        else:
            bot.send_message(message.chat.id , '🙁<b>Пожалуйста, выберите критерий из списка</b>', reply_markup=ReplyKeyboardRemove(), parse_mode="html")
            menu(message)
    else:
        bot.send_message(message.chat.id, '📄<b>Следует отправлять текст. Попробуйте снова</b>', reply_markup=ReplyKeyboardRemove(), parse_mode="html")
        menu(message)


def send_posts(message, posts): # Добавить 10 мест (пока что по 1)  
    if posts:
        for post in posts[:1]: # [:5]
            print("photo save path:", post[9])
            if post[9] != '0':
                bot.send_photo(message.chat.id, open(post[9], 'rb'))
            bot.send_location(message.chat.id, longitude=post[1].split(',')[0], latitude=post[1].split(',')[1])
            send_post = ''
            check_post = {
                'area': f'<b>🏢Район: </b> {get_adress(post[1])}',
                'year': f'\n\n<b>⏳Год: </b> {post[2]}',
                'season': f'\n\n<b>🏝️Сезон: </b> {post[3]}',
                'month': f'\n\n<b>📅Месяц: </b> {post[4]}',
                'description': f'\n\n<b>📝Описание: </b> {post[5]}',
                'feedback': f'\n\n<b>📈Отзыв: </b> {post[6]}',
                'mark': f'\n\n<b>🌟Оценка: </b> {post[7]}',
                'tags': f'\n\n<b>#⃣ Категория: </b> {post[7]}'
            }
            for el in check_post:
                if check_post[el].split()[-1] != 'None':
                    send_post += check_post[el]

            bot.send_message(message.chat.id, send_post, reply_markup = reaction_markup(post[0]), parse_mode="html")
            posts.remove(posts[0]) # [x:]
            bot.send_message(message.chat.id , '🔄<b>Загрузить еще?</b>', reply_markup=kb_y_n, parse_mode="html")
            bot.register_next_step_handler(message, get_answer_to_send, posts)
    else:
        bot.send_message(message.chat.id , '🔚<b>Записей по данной категории нет</b>', reply_markup=ReplyKeyboardRemove(), parse_mode="html")
        menu(message)


def get_answer_to_send(message, posts):
    if message.content_type == 'text':
        if message.text.lower() in ("✅да", "да"):
            send_posts(message, posts)
        elif message.text.lower() in ("❌нет", "нет"):
            bot.send_message(message.chat.id , '😊<b>Надеюсь, вы нашли место по душе</b>', reply_markup=ReplyKeyboardRemove(), parse_mode="html")
            menu(message)
        else: 
            bot.send_message(message.chat.id, '🙁<b>Извините, не понимаю Вас. Попробуйте снова</b>', reply_markup=ReplyKeyboardRemove(), parse_mode="html")
            menu(message)
    else:
        bot.send_message(message.chat.id, '📄<b>Следует отправлять текст. Попробуйте снова</b>', reply_markup=ReplyKeyboardRemove(), parse_mode="html")
        menu(message)


def for_popularity(message):
    if message.content_type == 'text':
        posts = most_popular_sights()
        send_posts(message, posts)
    else:
        bot.send_message(message.chat.id, '📄<b>Следует отправлять текст. Попробуйте снова</b>', reply_markup=ReplyKeyboardRemove(), parse_mode="html")
        menu(message)


def for_random(message):
    if message.content_type == 'text':
        all_sights = main(f'SELECT id, area, year, season, month, description, feedback, mark, tags, src FROM Sights')
        posts = random.sample(all_sights, len(all_sights))
        send_posts(message, posts)
    else:
        bot.send_message(message.chat.id, '📄<b>Следует отправлять текст. Попробуйте снова</b>', reply_markup=ReplyKeyboardRemove(), parse_mode="html")
        menu(message)


def for_tag(message):
    if message.content_type == 'text':
        if check_words(message.text.lower()):
            posts = main(f'SELECT id, area, year, season, month, description, feedback, mark, tags, src FROM Sights WHERE tags LIKE "%{message.text.lower()}%"')
            send_posts(message, posts)
        elif message.text.lower() == "назад":
            processing_criterion(message)
        else:
            bot.send_message(message.chat.id, '🙁<b>Следует писать единственную категорию длинною не меньше 2 знаков, используя русские символы</b>', parse_mode="html")
            menu(message)
    else:
        bot.send_message(message.chat.id, '📄<b>Следует отправлять текст. Попробуйте снова</b>', reply_markup=ReplyKeyboardRemove(), parse_mode="html")
        menu(message)


def for_mark(message):
    if message.content_type == 'text':
        if message.text.lower() == "назад":
            processing_criterion(message)
        elif "-" in message.text:
            if message.text.split('-')[0] in ("1", "2", "3", "4", "5", "6", "7", "8", "9", "10"):
                if message.text.split('-')[1] in ("1", "2", "3", "4", "5", "6", "7", "8", "9", "10"):
                    mark_first = message.text.split('-')[0]
                    mark_second = message.text.split('-')[1]
                    posts = main(f'SELECT id, area, year, season, month, description, feedback, mark, tags, src FROM Sights WHERE mark >= "{mark_first}" AND date <= "{mark_second}"')
                    send_posts(message, posts)
                else:
                    bot.send_message(message.chat.id, '🙁<b>Следует вводить число или промежуток чисел через "-". Попробуйте снова</b>', parse_mode="html")
                    menu(message)
            else:
                bot.send_message(message.chat.id, '🙁<b>Следует вводить число или промежуток чисел через "-". Попробуйте снова</b>', parse_mode="html")
                menu(message)
        elif message.text in ("1", "2", "3", "4", "5", "6", "7", "8", "9", "10"):
            posts = main(f'SELECT id, area, year, season, month, description, feedback, mark, tags, src FROM Sights WHERE mark LIKE "{message.text}"')
            send_posts(message, posts)
        else:
            bot.send_message(message.chat.id, '🙁<b>Следует вводить число или промежуток чисел через "-". Попробуйте снова</b>', parse_mode="html")
            menu(message)
    else:
        bot.send_message(message.chat.id, '📄<b>Следует отправлять текст. Попробуйте снова</b>', reply_markup=ReplyKeyboardRemove(), parse_mode="html")
        menu(message)


def for_date(message):
    if message.content_type == 'text':
        if message.text.lower() == "назад":
            processing_criterion(message)
        else:
            for i in message.text.split():
                if '.' in i:               
                    dates = i.split('-') 
                    if len(dates) == 1:
                        ms_date_part = is_date(dates[0])
                        if ms_date_part:
                            posts = main(f'SELECT id, area, year, season, month, description, feedback, mark, tags, src FROM Sights WHERE date LIKE "%{ms_date_part}%"') # [(), (), ()]
                            send_posts(message, posts)
                        else:
                            bot.send_message(message.chat.id, '🙁<b>Извините, мне не удалось найти дату/даты в сообщении. Попробуйте снова</b>', parse_mode="html")
                            menu(message)
                    elif len(dates) == 2:
                        ms_date_part1 = is_date(dates[0])
                        ms_date_part2 = is_date(dates[1])
                        if ms_date_part1 and ms_date_part2:
                            posts = main(f'SELECT id, area, year, season, month, description, feedback, mark, tags, src FROM Sights WHERE date >= "{ms_date_part1}" AND date <= "{ms_date_part2}"')
                            send_posts(message, posts)   
                        else:
                            bot.send_message(message.chat.id, '🙁<b>Извините, мне не удалось найти дату/даты в сообщении. Попробуйте снова</b>', parse_mode="html")
                            menu(message)
                else:
                    bot.send_message(message.chat.id, '🙁<b>Следует вводить дату в формате ДД.ММ.ГГГГ. Попробуйте снова</b>', parse_mode="html")
                    menu(message)
    else:
        bot.send_message(message.chat.id, '📄<b>Следует отправлять текст. Попробуйте снова</b>', reply_markup=ReplyKeyboardRemove(), parse_mode="html")
        menu(message)



@bot.message_handler(commands=['help'])
def help(message): 
    bot.send_message(message.chat.id, help_answer, parse_mode="html")
    bot.register_next_step_handler(message, get_menu_mess)


while True:
    try:
        bot.polling(none_stop=True, timeout=90)
    except Exception as e:
        print(datetime.datetime.now(), e)
        time.sleep(5)
        continue