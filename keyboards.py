from telebot.types import Message, ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


# btns = [[KeyboardButton("Засвияжский"), KeyboardButton("Заволжский"), KeyboardButton("Железнодорожный"), KeyboardButton("Ленинский")], [KeyboardButton("2022"), KeyboardButton("2021"), KeyboardButton("2020"), KeyboardButton("2019"), KeyboardButton("2018")], [KeyboardButton("Зима"), KeyboardButton("Весна"), KeyboardButton("Лето"), KeyboardButton("Осень")]]

# for kb in (kb_area, kb_year, kb_sesson):
#     kb = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
#     for btn in btns:
#         kb.add(btn)         # Оптимизация клавиатур

kb_y_n = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
btns = [KeyboardButton("✅Да"), KeyboardButton("❌Нет")]
for btn in btns:     
    kb_y_n.add(btn) 

kb_area = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
btns_area = [KeyboardButton("Засвияжский"), KeyboardButton("Заволжский"), KeyboardButton("Железнодорожный"), KeyboardButton("Ленинский"), KeyboardButton("🔙 Назад")]
for btn in btns_area:     
    kb_area.add(btn)

kb_year = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
btns_year = [KeyboardButton("2024"), KeyboardButton("2023"), KeyboardButton("2022"), KeyboardButton("2021"), KeyboardButton("2020"), KeyboardButton("2019"), KeyboardButton("🔙 Назад")]
for btn in btns_year:     
    kb_year.add(btn)

kb_season = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
btns_season = [KeyboardButton("Зима"), KeyboardButton("Весна"), KeyboardButton("Лето"), KeyboardButton("Осень"), KeyboardButton("🔙 Назад")]
for btn in btns_season:     
    kb_season.add(btn)

kb_mnh = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
btns_winter = [KeyboardButton("Декабрь"), KeyboardButton("Январь"), KeyboardButton("Февраль"), KeyboardButton("🔙 Назад")]
btns_spring = [KeyboardButton("Март"), KeyboardButton("Апрель"), KeyboardButton("Май"), KeyboardButton("🔙 Назад")]
btns_summer = [KeyboardButton("Июнь"), KeyboardButton("Июль"), KeyboardButton("Август"), KeyboardButton("🔙 Назад")]
btns_autumn = [KeyboardButton("Сентябрь"), KeyboardButton("Октябрь"), KeyboardButton("Ноябрь"), KeyboardButton("🔙 Назад")]

kb_criterion = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
btns_criterion = [KeyboardButton("🔥 Популярное"), KeyboardButton("🌟 Оценка"), KeyboardButton("📆 Дата добавления"), KeyboardButton("#⃣ Категория"), KeyboardButton("🎲 Случайно"), KeyboardButton("🔙 Назад")]
for btn in btns_criterion:     
    kb_criterion.add(btn)