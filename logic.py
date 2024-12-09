from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.types.input_file import FSInputFile
from aiogram.filters import CommandStart, Command

import keyboards as kb
import commands as cm
import mysql.connector


router = Router()


@router.message(CommandStart())
async def start(message: Message):
    cm.upsert_report('start')
    
    await message.answer('Соонун! Төмөндө мазмуну бар — теманы тандаңыз жана баштайлы⬇️', reply_markup=kb.helper)
    

@router.message(F.text == 'Жокко чыгаруу')
async def cancel_action(message: Message):
    user = message.from_user.id
    cm.reset_state(user)
    await message.answer('Аракет жокко чыгарылды', reply_markup=kb.helper)


@router.message(Command('help'))
async def reply_help(message: Message):
    await message.answer('Сиз иш-аракеттердин бирин тандай аласыз', reply_markup=kb.helper)


@router.message(F.photo)
async def handle_photo(message: Message):
    await message.answer('Мен сүрөттөрдү көрө албайм...\nАракеттердин бирин тандаңыз жакшы болот', reply_markup=kb.helper)


### Домофонду кантип туташтырса болот?
@router.message(F.text == 'Домофонду кантип туташтырса болот?')
async def connect_intercom(message: Message):
    cm.upsert_report('how_connect')
    
    await message.answer('Домофонду туташтыруу үчүн билдирме толтуруу керек. Бул үчүн бир нече суроолорго жооп берүү талап кылынат.  Даярсызбы? ', reply_markup=kb.inl_connection)


### О компании
@router.message(F.text == 'Компания жөнүндө')
async def connect_intercom(message: Message):
    cm.upsert_report('about_us')
    
    path_to_image = 'photo/about_us.jpg'
    photo = FSInputFile(path_to_image)
    
    text = 'Интерком - это отечественная компания, которая предоставляет услуги Умной домофонии с 2023 года. ✨\n\nМы стремимся предоставить больше комфорта и безопасности жителям многоэтажных домов, устанавливая современные системы домофонов с видеонаблюдением и приложением. Таким образом мы делаем безопасными не только дома, но и город в целом. На данный момент наша база подключенных абонентов составляет более 20000 человек.\n\n🕒 Рабочий график офиса:\nПн-Пт: с 9:00 до 18:00\nСб, Вс - выходные\n\nСлужба поддержки через Whatsapp\nПн-Вс с 9:00 до 20:00\n\n📞 Колл-центр:\n0707888822\n0997888822\n\n📍 Адрес:\nул. Фрунзе, 533А (Бишкек)'
    await message.answer_photo(caption=text, reply_markup=kb.inl_about_us, photo=photo)
    

### Кто такая Сию?
@router.message(F.text == 'Сию деген ким?')
async def who_im(message: Message):
    cm.upsert_report('who_im')
    
    path_to_image = 'photo/seeu.jpg'
    photo = FSInputFile(path_to_image)
    
    text = 'Сию - маскот компаниясы "Интерком". Бул домофон камерасынын көзүн билдирген каарман. "Сию" аты англис тилиндеги "See You" деген сөздөн келип чыккан, "Мен сени көрүп жатам"дегенди билдирет. Каарман үйдүн жашоочуларын чоочун адамдардан коргойт, тартипти сактайт жана тутумга кам көрөт.'
    await message.answer_photo(photo, text)


### Жаңы ачкычты кайдан сатып алсам болом?
@router.message(F.text == 'Жаңы ачкычты кайдан сатып алсам болом?')
async def where_ibuy(message: Message):
    cm.upsert_report('where_buy')
    
    text = 'Ачкычты домкомдон же кеңсебизден тапса болот.\n\n Маалымат үчүн телефондор:\n0707888822\n0997888822\n\Иштөө графиги:\n9:00 - 18:00 менен Дш - Жм т\n\п Дареги: Молдокулова көч., 10/а3(Бишкек)'
    await message.answer(text, reply_markup=kb.inl_where_ibuy)


@router.callback_query(F.data == 'report')
async def handle_report(callback: CallbackQuery):    
    user = callback.from_user.id
    
    cm.reset_state(user)
    cm.upsert_user_state(user, 1)

    await callback.answer('Кызыгууңуз үчүн рахмат')

    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.bot.send_message(user, 'Атыңыз ким? (ФИО)', reply_markup=kb.cancel)


@router.message(lambda message: cm.get_user_state(message.from_user.id) is not None and cm.get_user_state(message.from_user.id)[0] == 1)
async def handle_name(message: Message):
    user = message.from_user.id
    text = message.text

    cm.upsert_ticket(user, 'name', text)
    cm.upsert_user_state(user, 2)

    await message.answer('Домофонду кайсы дарекке орноткуңуз келет?', reply_markup=kb.cancel)


@router.message(lambda message: cm.get_user_state(message.from_user.id) is not None and cm.get_user_state(message.from_user.id)[0] == 2)
async def handle_address(message: Message):
    user = message.from_user.id
    text = message.text
    cm.upsert_ticket(user, 'address', text)
    cm.upsert_user_state(user, 3)

    await message.answer('Үйдүн түрү?', reply_markup=kb.inl_inter)


### Have u intercom
@router.callback_query(F.data == 'apparts')
async def yes_we_have(callback: CallbackQuery):
    user = callback.from_user.id
    
    cm.upsert_ticket(user, 'inter_type', 'Көп кабаттуу үй')
    cm.upsert_user_state(user, 4)

    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.bot.send_message(user, 'Сиз менен кантип байланышса болот?', reply_markup=kb.inl_connection_type)
        

@router.callback_query(F.data == 'house')
async def house(callback: CallbackQuery):
    user = callback.from_user.id
    
    cm.upsert_ticket(user, 'inter_type', 'Жер үй')
    cm.upsert_user_state(user, 4)

    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.bot.send_message(user, 'Сиз менен кантип байланышса болот?', reply_markup=kb.inl_connection_type)


### Contact type
@router.callback_query(F.data == 'whats')
async def whats(callback: CallbackQuery):
    user = callback.from_user.id
    
    cm.upsert_ticket(user, 'callback_type', 'Мага Whatsapp\'ка жазыңыз')
    cm.upsert_user_state(user, 5)

    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.bot.send_message(user, 'Телефон номериңизди жазыңыз.', reply_markup=kb.cancel)


@router.callback_query(F.data == 'mobile')
async def whats(callback: CallbackQuery):
    user = callback.from_user.id
    
    cm.upsert_ticket(user, 'callback_type', 'Мага чалыңыз')
    cm.upsert_user_state(user, 5)

    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.bot.send_message(user, 'Телефон номериңизди жазыңыз.', reply_markup=kb.cancel)


@router.message(lambda message: cm.get_user_state(message.from_user.id) is not None and cm.get_user_state(message.from_user.id)[0] == 5)
async def handle_phone(message: Message):
    user = message.from_user.id
    text = message.text
    cm.upsert_ticket(user, 'num', text)
    cm.upsert_user_state(user, 6)

    await message.answer('Эскертүүлөрдү же комментарийлерди жазыңыз, эгер комментарий жок болсо, "жок" деп жөнөтүңүз.', reply_markup=kb.cancel)


@router.message(lambda message: cm.get_user_state(message.from_user.id) is not None and cm.get_user_state(message.from_user.id)[0] == 6)
async def handle_description(message: Message):
    user = message.from_user.id
    text = message.text
    cm.upsert_ticket(user, 'description', text)
    cm.reset_state(user)

    get_data = cm.get_ticket(user)
    date = message.date.today().strftime("%Y-%m-%d %H:%M")

    await message.bot.send_message(
        -1002009533675,
        f'Ответ пользователя @{message.from_user.username}. \nВремя: {date}\
        \n\nВопрос: Атыңыз ким? (ФИО)\nОтвет: {get_data[1]}\
        \n\nВопрос: Домофонду кайсы дарекке орноткуңуз келет?\nОтвет: {get_data[2]}\
        \n\nВопрос: Үйдүн түрү?\nОтвет: {get_data[6]}\
        \n\nВопрос: Сиз менен кантип байланышса болот?\nОтвет: {get_data[3]}\
        \n\nВопрос: Телефон номериңизди жазыңыз\nОтвет: {get_data[5]}\
        \n\nВопрос: Эскертүүлөрдү же комментарийлерди жазыңыз, эгер комментарий жок болсо, "жок" деп жөнөтүңүз.\nОтвет: {get_data[4]}'
    )

    await message.answer('Сиздин байланышыңыз ийгиликтүү жөнөтүлдү! Билдирмени кароо мөөнөтү-1-2 иш күн.\n\nБаса, бизде жаңылыктар Telegram-канал жана Instagram бар, анда биз эң акыркы жаңылыктарды жарыялайбыз. Жазылыңыз - биз менен кызыктуу! 🩵', reply_markup=kb.contacts)


### Акылдуу домофон эмне кыла алат экенин айт
@router.message(F.text == 'Акылдуу домофон эмне кыла алат экенин айт')
async def about_intercom(message: Message):
    cm.upsert_report('tell_about')
    
    path_to_image = 'photo/1.jpg'
    photo = FSInputFile(path_to_image)
    
    text = "Биздин домофон системасы видеобайкоо жана тиркеме менен бирге иштейт. Камералар короого, кире беришке, унаа токтотуучу жайга, балдар аянтчасына жана жашоочулардын талабы боюнча каалаган жерге орнотулат. 😉\n\nҮйдө жеке транспортуңуз, балдарыңыз, улгайган үй-бүлө мүчөлөрүңүз же баалуу буюмдарыңыз барбы?"

    await message.answer_photo(photo, text, reply_markup=kb.inl_about)


@router.callback_query(F.data == 'ihave')    
async def ihave(callback: CallbackQuery):
    user = callback.from_user.id
    path_to_image = 'photo/2.jpg'
    photo = FSInputFile(path_to_image)
    
    text = "Бардык камералардан түз берүү биздин колдонмо аркылуу жеткиликтүү. Сиз каалаган убакта транспортуңуздун коопсуздугун камсыздай аласыз, балаңыз ким менен ойноп жатканын көрө аласыз жана жагымсыз жагдай болгон учурда камералардан жаздыра аласыз. 👍\n\n‼️ И баса, жазуулар булут архивинде 5 күн сакталат, андан кийин жок кылынат. Бирок сиз жазууларды сактап калгыңыз келсе, аларды телефонуңузга оңой жүктөп алсаңыз болот. 💫"    

    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.bot.send_photo(user, caption=text, reply_markup=kb.inl_letsgo, photo=photo)
    

@router.callback_query(F.data == 'gonext')
async def gonext(callback: CallbackQuery):
    user = callback.from_user.id
    
    text = "Домофон камерасы датчиктер менен жабдылган, анын аркасында ал жүздөрдү таанып, тирүү адамдарды сүрөттөрдөн айырмалай алат. 😮\n\nКамера ошондой эле ультра жарык сезгич матрицага ээ, бул түстүү сүрөттү түнкүсүн да агылтууга мүмкүндүк берет. 😀👍\n\nБиз азыр акчаны унутуп калсак, которуулар төлөп койууга, же ачкычты унутсак, эшикти Face ID менен кирүүгө мүмкүнчүлүгүбүз бар убакытта жашайбыз.Өтүңүз"
    
    await callback.message.edit_reply_markup(None)
    await callback.bot.send_message(user, text=text, reply_markup=kb.inl_without)
    

@router.callback_query(F.data == 'without_key')
async def whats_this(callback: CallbackQuery):
    user = callback.from_user.id
    path_to_image = 'photo/3.jpg'
    photo = FSInputFile(path_to_image)
    
    text = "✅ Ачкычсыз эшикти ачуунун 3 жолу:\n\n\n\n1. Бетти таануу функциясы боюнча;\n2. Колдонмодогу онлайн ачкыч аркылуу;\n3. Шилтеме аркылуу убактылуу мүмкүнчүлүк бериңиз.\n\n\nжана биздин абоненттердин жашыруун лайфхак:\n\n\nдомофондон өзүңүзгө чалып, телефон аркылуу эшикти ачыңыз."
    
    await callback.message.edit_reply_markup(None)
    await callback.bot.send_photo(user, caption=text, reply_markup=kb.inl_keys, photo=photo)
    

@router.callback_query(F.data == 'online_key')
async def whats_this(callback: CallbackQuery):
    user = callback.from_user.id
    path_to_image = 'photo/4.jpg'
    photo = FSInputFile(path_to_image)
    
    text = '🔑 Онлайн ачкыч-бул колдонмодогу баскыч менен эшикти ачуу мүмкүнчүлүгү.'
    
    await callback.message.edit_reply_markup(None)
    await callback.bot.send_photo(user, caption=text, reply_markup=kb.inl_keys_ex, photo=photo)


@router.callback_query(F.data == 'time_key')
async def time_key(callback: CallbackQuery):
    user = callback.from_user.id
    path_to_image = 'photo/4.jpg'
    photo = FSInputFile(path_to_image)
    
    text = '🕐 Убактылуу кирүү мүмкүнчүлүгү — бул досторуңузга жана жакындарыңызга кирүүгө мүмкүнчүлү жөнөтүү. Шилтемени каалаган социалдык тармакта шилтемелер менен  бөлүшсөңүз болот (WhatsApp, Instagram, Telegram ж.б.). Сиздин конокторуңуз шилтемени басып, эшикти ачышы керек. Конокторду күткөндө жана эшикке алаксыгыңыз келгенде ыңгайлуу.\n\n Убактылуу кирүүнү 2, 4, 8, 12 же 24 саатка коюуга болот.'
    
    await callback.message.edit_reply_markup(None)
    await callback.bot.send_photo(user, caption=text, reply_markup=kb.inl_keys_ex, photo=photo)


@router.callback_query(F.data == 'keys_ex')
async def keys_ex(callback: CallbackQuery):
    user = callback.from_user.id
    path_to_image = 'photo/5.jpg'
    photo = FSInputFile(path_to_image)
    
    text = 'Албетте! Салттуу домофон сүйүүчүлөрү жана материалисттер үчүн бизде көчүрүлгүз ачкычтар бар. Ачкычтардын жеке идентификациялык номери бар жана шифрлөө тутуму менен корголгон. Аларды подземкада көчүрүү оңой эмес, бул сырттан келгендердин кире беришине тоскоолдук жаратат. 😌'
    
    await callback.message.edit_reply_markup(None)
    await callback.bot.send_photo(user, caption=text, reply_markup=kb.inl_how_work, photo=photo)
    

@router.callback_query(F.data == 'how_work')
async def how_work(callback: CallbackQuery):
    user = callback.from_user.id
    
    text = 'Мыкты суроо! Келгиле, сиз системага туташкансыз жана конок келди деп элестетип көрөлү. Ал сиздин домофонуңуздагы батирдин номерин терип, жооп күтөт. Чалуу телефонуңузга видео чалуу түрүндө келет. Бул учурда сиз кичинекей баланы багып жатасыз же кечки тамакты даярдап жатасыз (же экөө тең чогуу). Сиз кыла турган нерсе-бул чакырыкты кабыл алуу. Андан кийин, сиз көрүп, сүйлөшүп, андан кийин конокту киргизесизби же жокпу, чече аласыз. 🤗👍\n\nАндан тышкары, сиз үйдө жок болсоңуз дагы, башка мамлекетте болсоңуз дагы, чалууларды кабыл алууга болот. Ыңгайлуу экенби?😏'
    
    await callback.message.edit_reply_markup(None)
    await callback.bot.send_message(user, text=text, reply_markup=kb.inl_what_if)
    
    
@router.callback_query(F.data == 'good')
async def good(callback: CallbackQuery):
    user = callback.from_user.id
    
    text = 'Домофон иштебей калган учурда, тынчсыздануунун кажети жок жана аны оңдой турган техникти издөөнүн кажети жок. Бизге көйгөй жөнүндө айтып коюу жетиштүү, биз диагностика жүргүзүп, домофонду туура абалга келтиребиз😉. Табигый себептерден улам бузулуп калса, аны бекер алмаштырабыз.'
    
    await callback.message.edit_reply_markup(None)
    await callback.bot.send_message(user, text=text, reply_markup=kb.inl_how_much)
    

@router.callback_query(F.data == 'how_much')
async def how_much(callback: CallbackQuery):
    user = callback.from_user.id
    
    text = 'Эми мен сиздерди биздин сайтка кирип, биздин компаниянын тарифтери менен таанышууңуздарды сунуштайм. Маалымат пайдалуу болду деп ишенем! 🥰🤗⬇️'
    
    await callback.message.edit_reply_markup(None)
    await callback.bot.send_message(user, text, reply_markup=kb.inl_find_money)
    

### Пикир/даттануу калтыргым келет
@router.message(F.text == 'Пикир/даттануу калтыргым келет')
async def not_work(message: Message):
    text = '"Кыйынчылыктарга туш болгонуң абдан өкүнүчтүү. Мен сизге жардам бере алам деп ишенем! 🥺🤗🩵\n\nКелгиле, түшүнөлү! Төмөндөгү менюдан ылайыктуу бөлүмдү тандаңыз. ⬇️"'
    await message.answer(text, reply_markup=kb.not_work)


@router.message(F.text == 'Назад')
async def back(message: Message):
    text = 'Главное меню'
    await message.answer(text, reply_markup=kb.helper)


### Face ID иштебей жатат
@router.message(F.text == 'Face ID иштебей жатат')
async def not_work(message: Message):
    cm.upsert_report('dwork_face')
    
    text = 'Улантуудан мурун, мүмкүн болгон себептерди жана биздин кеңеш эскертүүбүздү карап чыгыңыз. 🤗⬇️\n\nТуруксуз же алсыз интернет домофондун иштешине таасирин тийгизиши мүмкүн, анткени ал тармак аркылуу иштейт.\n\nБетти таануу жакшыраак иштеши үчүн, колдонмого экиден ашык сүрөт жүктөөнү сунуштайбыз. Сүрөттөр жакшы жарыкта, тоскоолдуксуз жана аксессуарларсыз тартылганын текшериңиз.'
    await message.answer(text, reply_markup=kb.inl_im_read)
    

@router.callback_query(F.data == 'im_read')
async def im_read(callback: CallbackQuery):
    user = callback.from_user.id
    
    text = 'Эгер бул эскертме сиз үчүн иштебесе, анда адистер сиздин өтүнүчүңүздү тезирээк иштеп чыгып, көйгөйдү чечиши үчүн, билдирме толтуралы. 🤗\n\nБул көп убакытты талап кылбайт-Сиз бир нече суроолорго жооп беришиңиз керек...\n\nАр бир суроого бир билдирүү менен жооп жөнөтүңүз. Сиздин жоопторуңузду мен билдирмеге киргизем. 🤗'
    
    await callback.message.edit_reply_markup(None)
    await callback.bot.send_message(user, text, reply_markup=kb.inl_im_understood)


### Тиркемеге кирбей жатат
@router.message(F.text == 'Тиркемеге кирбей жатат')
async def dnot_cannot_enter(message: Message):
    cm.upsert_report('cannot_ent')
    
    text = '"Улантуудан мурун, мүмкүн болгон себептерди жана биздин кеңеш эскертүүбүздү карап чыгыңыз. 🤗⬇️\n\nЭгер айдын башталышы болсо, баланста жетиштүү каражат бар экендигин текшериңиз. 1 тыйын жетишсиз болсо дагы, система домофон үчүн төлөмдү түшүрбөйт. Система автоматташтырылган.\n\nОшондой эле, пароль менен логиндин туура киргизилгендигин текшериңиз."'
    await message.answer(text, reply_markup=kb.inl_im_read)
    

@router.callback_query(F.data == 'im_read_app')
async def im_read_app(callback: CallbackQuery):
    user = callback.from_user.id
    
    text = 'Эгер бул эскертме сиз үчүн иштебесе, анда адистер сиздин өтүнүчүңүздү тезирээк иштеп чыгып, көйгөйдү чечиши үчүн, билдирме толтуралы. 🤗\n\nБул көп убакытты талап кылбайт-Сиз бир нече суроолорго жооп беришиңиз керек...\n\nАр бир суроого бир билдирүү менен жооп жөнөтүңүз. Сиздин жоопторуңузду мен билдирмеге киргизем. 🤗'
    
    await callback.message.edit_reply_markup(None)
    await callback.bot.send_message(user, text, reply_markup=kb.inl_im_understood)


### Камералар иштебей жатат
@router.message(F.text == 'Камералар иштебей жатат')
async def dnot_work_cameras(message: Message):
    cm.upsert_report('dwork_camera')
    
    text = '‼️ Видеобайкоонун камералары ""Домофон 200 ""тарифи боюнча гана жеткиликтүү. Эгер сизде ушундай план болсо, бирок камералар колдонмодо көрсөтүлбөсө же иштебей жатса, анда мүмкүн болгон себептерди карап көрөлү.\n\nБул үчүн биз билдирме толтурушубуз керек. Бул көп убакытты талап кылбайт- сиз бир нече суроолорго жооп беришиңиз керек. Сураныч, ар бир суроого бир билдирүү менен жооп жөнөтүңүз. Сиздин жоопторуңузду мен билдирмеге киргизем. 🤗'
    await message.answer(text, reply_markup=kb.inl_im_understood)
    
    
### Телефонго чалуулар түшкөн жок
@router.message(F.text == 'Телефонго чалуулар түшкөн жок')
async def dnot_work_app(message: Message):
    cm.upsert_report('dwork_app')
    
    text = '"Улантуудан мурун, мүмкүн болгон себептерди жана биздин кеңеш эскертүүбүздү карап чыгыңыз. 🤗⬇️ \n\nБиздин тиркеме үчүн мобилдик түзмөктүн уруксаттарын текшериңиз. Бул үчүн, тиркемени ачкандан кийин төмөнкү менюдан "профилди" таап, андан кийин "уруксаттарды орнотууну" тандаңыз жана бардык керектүү уруксаттарды иштетиңиз. \n\nОшондой эле, VPN иштетилгенде тиркеме иштебей калышы мүмкүн. Ал өчүк экенин текшериңиз."'
    await message.answer(text, reply_markup=kb.inl_app_dnot)
    

@router.callback_query(F.data == 'im_app_dnot')
async def im_app_dnot(callback: CallbackQuery):
    user = callback.from_user.id
    
    text = 'Эгер бул эскертме сиз үчүн иштебесе, анда адистер сиздин өтүнүчүңүздү тезирээк иштеп чыгып, көйгөйдү чечиши үчүн, билдирме толтуралы. 🤗\n\nБул көп убакытты талап кылбайт-Сиз бир нече суроолорго жооп беришиңиз керек...\n\nАр бир суроого бир билдирүү менен жооп жөнөтүңүз. Сиздин жоопторуңузду мен билдирмеге киргизем. 🤗'
    
    await callback.message.edit_reply_markup(None)
    await callback.bot.send_message(user, text, reply_markup=kb.inl_im_understood)
    

### Башка
@router.message(F.text == 'Башка')
async def another(message: Message):
    cm.upsert_report('another')
    
    text = ' Эгер сунушталган бөлүмдөрдүн бири да сизге туура келбесе, сизге адис гана жардам берет. Сурамыңыз тезирээк иштетилиши үчүн, билдирмени толтуралы.\n\nМен бир нече суроолорду берем, ар бир суроого бир билдирүү менен жооп бериш керек. Бардык маалыматтарды мен билдирмеге киргизем. 🤗\n\nБаштайлыбы?'
    await message.answer(text, reply_markup=kb.inl_start)
    
    
@router.callback_query(F.data == 'report_w')
async def handle_report(callback: CallbackQuery):
    user = callback.from_user.id
    cm.reset_state(user)
    cm.upsert_user_state(user, 10)

    await callback.answer('Спасибо за ваш интерес.')

    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.bot.send_message(user, 'Как Вас зовут?', reply_markup=kb.cancel)


@router.message(lambda message: cm.get_user_state(message.from_user.id) is not None and cm.get_user_state(message.from_user.id)[0] == 10)
async def handle_name(message: Message):
    user = message.from_user.id
    text = message.text

    cm.upsert_ticket(user, 'name', text)
    cm.upsert_user_state(user, 20)

    await message.answer('Напишите ваш адрес', reply_markup=kb.cancel)


@router.message(lambda message: cm.get_user_state(message.from_user.id) is not None and cm.get_user_state(message.from_user.id)[0] == 20)
async def handle_address(message: Message):
    user = message.from_user.id
    text = message.text
    cm.upsert_ticket(user, 'address', text)
    cm.upsert_user_state(user, 3)

    await message.answer('Как с вами связаться?', reply_markup=kb.inl_connection_type)


### Contact type
@router.callback_query(F.data == 'whats')
async def whats(callback: CallbackQuery):
    user = callback.from_user.id
    
    cm.upsert_ticket(user, 'callback_type', 'Написать в What\'s App')
    cm.upsert_user_state(user, 50)

    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.bot.send_message(user, 'Напишите номер телефона.', reply_markup=kb.cancel)


@router.callback_query(F.data == 'mobile')
async def whats(callback: CallbackQuery):
    user = callback.from_user.id
    
    cm.upsert_ticket(user, 'callback_type', 'Позвонить')
    cm.upsert_user_state(user, 50)

    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.bot.send_message(user, 'Напишите номер телефона.', reply_markup=kb.cancel)


@router.message(lambda message: cm.get_user_state(message.from_user.id) is not None and cm.get_user_state(message.from_user.id)[0] == 50)
async def handle_phone(message: Message):
    user = message.from_user.id
    text = message.text
    cm.upsert_ticket(user, 'num', text)
    cm.upsert_user_state(user, 60)

    await message.answer('Пожалуйста, оставьте комментарий, чтобы мы могли лучше понять вашу ситуацию.', reply_markup=kb.cancel)


@router.message(lambda message: cm.get_user_state(message.from_user.id) is not None and cm.get_user_state(message.from_user.id)[0] == 60)
async def handle_description(message: Message):
    user = message.from_user.id
    text = message.text
    cm.upsert_ticket(user, 'description', text)
    cm.reset_state(user)

    get_data = cm.get_ticket(user)
    date = message.date.today().strftime("%Y-%m-%d %H:%M")

    await message.bot.send_message(
        -1002009533675,
        f'Ответ пользователя @{message.from_user.username}. \nВремя: {date}\
        \n\nВопрос: Как Вас зовут?\nОтвет: {get_data[1]}\
        \n\nВопрос: Напишите ваш адрес\nОтвет: {get_data[2]}\
        \n\nВопрос: Выберите способ связи\nОтвет: {get_data[3]}\
        \n\nВопрос: Отправьте номер для связи\nОтвет: {get_data[5]}\
        \n\nВопрос: Пожалуйста, оставьте комментарий, чтобы мы могли лучше понять вашу ситуацию.\nОтвет: {get_data[4]}'
    )

    await message.answer('Ваше обращение успешно отправлено! Срок обработки заявки — 1–2 рабочих дня.\n\nКстати, у нас есть новостной Telegram-канал и Instagram, где мы публикуем самые свежие новости. Подписывайтесь — с нами интересно! 🩵', reply_markup=kb.contacts)
    

@router.message(Command('report_about'))
async def report_about(message: Message):
    rep = cm.report_about_report()
    text = f'Start: {rep[0][0]}\nКак подключить умный домофон?: {rep[0][1]}\nРасскажи, что умеет умный домофон: {rep[0][2]}\
             \nГде можно купить новый ключ?: {rep[0][3]}\nКто такая Сию?: {rep[0][4]}\nО компании: {rep[0][5]}\
             \nУ меня не работает распознавание: {rep[0][6]}\nНе получается войти в приложение: {rep[0][7]}\
             \nНе работают камеры: {rep[0][8]}\nПриложение не работает: {rep[0][9]}\nДругое: {rep[0][10]}'
    
    await message.answer(text, reply_markup=kb.helper)


@router.message(F.text == 'Балансты текшерүү')
async def check_balance(message: Message):
    user = message.from_user.id
    text = 'Балансты текшерүү үчүн өздүк эсебиңиздин номерин киргизиңиз.\n\nӨздүк эсеп келишимде жазылат.\n*Көңүл буруңуз!* Сандарды гана киргизиңиз, мисалы: 05592'
    
    cm.reset_state(user)
    cm.upsert_user_state(user, 100)
        
    await message.answer(text, reply_markup=kb.cancel, parse_mode='Markdown')
    

@router.message(lambda message: cm.get_user_state(message.from_user.id) is not None and cm.get_user_state(message.from_user.id)[0] == 100)
async def check_balance_2(message: Message):
    user = message.from_user.id
    get_text = message.text.lower()
    
    cm.upsert_user_state(user, 200)
    
    mydb = mysql.connector.connect(
        host='185.39.79.69',
        user='domofon',
        password='mys897877b7',
        database='stg'
    )

    cur = mydb.cursor()
    
    TP = {
            'Domofon': 200,
            'Domofon_day': 200,
            'Domofon_100': 100,
            'Domofon_day_4': 100,
            'Domofon_60': 60,
            'Domofon_day_2': 60,
            'Domofon_300': 300,
            'Domofon_day_10': 300,
        }
    
    try:
        cur.execute(f'SELECT u.cash, u.tariff, rn.realname, ph.phone, ph.mobile, pay.summ, pay.date FROM users u LEFT JOIN realname rn ON u.login = rn.login LEFT JOIN phones ph ON ph.login = u.login LEFT JOIN payments pay ON pay.login = u.login WHERE u.login = {get_text} AND pay.admin = "openpayz"')
        
        data = cur.fetchall()[-1]
        
        cm.reset_state(user)
        
        await message.answer(f'Учурдагы тарифтик планыңыз: айына {TP.get(data[1], data[1])} сом\nУчурдагы балансыңыз: {data[0]} сом\nАкыркы толуктоо: {data[5]} сом суммасында болду\nАкыркы толуктоо: {data[-1]}', reply_markup=kb.helper)
    except IndexError:
        
        await message.answer(f'Мен сиздин эсебиңизди таба алган жокмун. Көбүрөөк маалымат алуу үчүн, кардарларды колдоо бөлүмүнө кайрылыңыз.\n\nБилдирмени азыр толтурабызбы?', reply_markup=kb.inl_im_understood)


@router.callback_query(F.data == 'instagram')
async def insta(callback: CallbackQuery):
    user = callback.from_user.id
        
    await callback.bot.send_message(user, 'Бул жерде биздин жаңылыктар баракчасына шилтеме.\nhttps://www.instagram.com/intercom.kg/', reply_markup=kb.helper)


@router.callback_query(F.data == 'telegram')
async def telegram(callback: CallbackQuery):
    user = callback.from_user.id
        
    await callback.bot.send_message(user, 'Бул жерде биздин жаңылыктар баракчасына шилтеме.\nhttps://t.me/intercomkg', reply_markup=kb.helper)