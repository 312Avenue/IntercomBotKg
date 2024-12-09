from aiogram.types import (
    InlineKeyboardMarkup, InlineKeyboardButton,
    ReplyKeyboardMarkup, KeyboardButton
)

helper = ReplyKeyboardMarkup(
    resize_keyboard=True, 
    input_field_placeholder="Кандай жардам бере алам?",
    keyboard=[
        [KeyboardButton(text="Балансты текшерүү")],
        [KeyboardButton(text="Домофонду кантип туташтырса болот?")],
        [KeyboardButton(text="Системаны нөлдөн баштап кантип колдонуу керек")],
        [KeyboardButton(text="Пикир/даттануу калтыргым келет")],
        [KeyboardButton(text="Жаңы ачкычты кайдан сатып алсам болом?")],
        [KeyboardButton(text="Кто такая Сию?"), KeyboardButton(text="О компании")],
    ]
)

cancel = ReplyKeyboardMarkup(
    resize_keyboard=True, 
    keyboard=[
        [KeyboardButton(text="Жокко чыгаруу")],
    ]
)


### Как подключить домофон
inl_connection = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Даяр!", callback_data="report")]
    ]
)

inl_inter = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Көп кабаттуу үй", callback_data="apparts")],
        [InlineKeyboardButton(text="Жер үй", callback_data="house")],
    ]
)

inl_connection_type = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Мага Whatsapp'ка жазыңыз", callback_data="whats")],
        [InlineKeyboardButton(text="Мага чалыңыз", callback_data="mobile")],
    ]
)


### Расскажи, что умеет умный домофон
inl_about = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Ооба, бар", callback_data="ihave")]
    ]
)

inl_letsgo = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Сонун! Кандай ыңгайлуу, улантыңыз", callback_data="gonext")]
    ]
)

inl_without = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="ЭШИКТИ АЧКЫЧСЫЗ АЧА АЛАМЫН!", callback_data="without_key")]
    ]
)

### Развлетвление по ключам
inl_keys =  InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Онлайн ачкыч деген эмне?", callback_data="online_key")],
        [InlineKeyboardButton(text="Убактылуу кирүү деген эмне?", callback_data="time_key")]
    ]
)

### First choose
inl_keys_ex = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Ачкыч барбы?", callback_data="keys_ex")]
    ]
)

inl_how_work = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Ал эми домофон кантип иштейт", callback_data="how_work")]
    ]
)

inl_what_if = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Ыңгайлуу!", callback_data="good")],
        [InlineKeyboardButton(text="Бузулуп калса кандай болот?", callback_data="good")],
    ]
)

inl_how_much = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Сколько стоит домофон?", callback_data="how_much")]
    ]
)

inl_find_money = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Бааларын билүү", url="https://inter.kg/")]
    ]
)

### Где можно купить новый ключ?
inl_where_ibuy = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Биз", url="https://inter.kg/navigation")]
    ]
)

### О компании
inl_about_us = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Биздин сайтыбызга Өтүңүз", url="https://inter.kg/navigation")],
        [InlineKeyboardButton(text="Биздин - Instagram", url="https://www.instagram.com/intercom.kg/")],
        [InlineKeyboardButton(text="Жаңылыктар Телеграм канал", url="https://t.me/intercomkg")]
    ]
)

### У меня не работает...
not_work = ReplyKeyboardMarkup(
    resize_keyboard=True, 
    input_field_placeholder="Тилекке каршы(",
    keyboard=[
        [KeyboardButton(text="Face ID иштебей жатат")],
        [KeyboardButton(text="Тиркемеге кирбей жатат")],
        [KeyboardButton(text="Камералар иштебей жатат")],
        [KeyboardButton(text="Телефонго чалуулар түшкөн жок")],
        [KeyboardButton(text="Башка")], 
        [KeyboardButton(text="Артка")],
    ]
)

inl_im_read = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Я ознакомился(-ась)", callback_data="im_read")]
    ]
)

inl_im_understood = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Понял(-а), хорошо", callback_data="report_w")]
    ]
)

inl_dnot_work = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Я ознакомился(-ась)", callback_data="im_read_app")]
    ]
)

inl_app_dnot = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Я ознакомился(-ась)", callback_data="im_app_dnot")]
    ]
)

inl_start = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Начнем!", callback_data="report_w")]
    ]
)

contacts = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Instagram", callback_data="instagram")],
        [InlineKeyboardButton(text="Telegram", callback_data="telegram")]
    ]
)