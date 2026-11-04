#!/usr/bin/env python3
"""Єдине джерело даних SUBIT-KIRCHER v2.1: твори, події, люди, твердження, джерела.
Дані — з вторинних джерел (див. специфікацію §10); анотація κ — інтерпретація автора.
Запуск: python3 kircher_data.py  — перевіряє дані й друкує підсумки."""
import json
from collections import Counter, defaultdict

# --- коди алфавіту (SUBIT v6.13.5 §1) ---
A = ['10', '11', '01', '00']
WHO = {'ME': '10', 'WE': '11', 'YOU': '01', 'THEY': '00'}
WHERE = {'EAST': '10', 'SOUTH': '11', 'WEST': '01', 'NORTH': '00'}
WHEN = {'SPRING': '10', 'SUMMER': '11', 'AUTUMN': '01', 'WINTER': '00'}


def code6(k):
    bits = WHO[k[0]] + WHERE[k[1]] + WHEN[k[2]]
    return int(bits, 2)


FIELDS = {
    'egypt': 'Єгипет, мови, давнина',
    'china': 'Китай',
    'earth': 'Земля, магнетизм, медицина',
    'sense': 'Світло, звук, машини',
    'method': 'Універсальні методи',
    'world': 'Космос, Лацій, Біблія, музей',
}

# w: id, year, end, ynote, la, uk, field, k(who,where,when), conf(h/m/l), why, sum, claims, src
WORKS = [
 dict(id='ars_magnesia', year=1631, la='Ars Magnesia', uk='Магнетичне мистецтво', field='earth', k=('ME', 'NORTH', 'SPRING'), conf='m',
      why='перша власна праця, Вюрцбург', sum='Перша книга Кірхера, про магнетизм. Того ж року Вюрцбург захопили, і Кірхер опинився в Авіньйоні.', claims=[], src=['S3', 'S10']),
 dict(id='primitiae', year=1635, la='Primitiae gnomonicae catoptricae', uk='Початки гномоніки та катоптрики', field='sense', k=('ME', 'NORTH', 'SPRING'), conf='l',
      why='за назвою: власні розробки з сонячних годинників і дзеркал; змісту в зібраних джерелах немає', sum='У зібраних джерелах лише назва й рік (список праць у Wikipedia).', claims=[], src=['S3']),
 dict(id='prodromus', year=1636, la='Prodromus Coptus sive Aegyptiacus', uk='Коптський провісник', field='egypt', k=('THEY', 'SOUTH', 'SPRING'), conf='h',
      why='спирається на давні рукописи (Пейреск, делла Валле); Єгипет; попередник майбутнього «Едіпа»',
      sum='Перша друкована граматика коптської в Європі. Присвячена кардиналу Ф. Барберіні. Порівнює письма (грецьке, єврейське, сирійське, арабське, ефіопське, китайське).', claims=['C1', 'C3'], src=['S13', 'S14', 'S26']),
 dict(id='specula', year=1637, end=1638, ynote='1637 за Wikipedia, 1638 за Catholic Encyclopedia (Мессіна)', la='Specula Melitensis Encyclica', uk='Мальтійська спостережниця', field='earth', k=('ME', 'SOUTH', 'SUMMER'), conf='l',
      why='за назвою і місцем видання (Мессіна): власні фізико-математичні прилади, юг', sum='Нова збірка фізико-математичних приладів; видана в Мессіні. Змісту в зібраних джерелах немає.', claims=[], src=['S3', 'S36']),
 dict(id='magnes', year=1641, ynote='1640 за Catholic Encyclopedia; 3-тє, значно розширене видання 1654', la='Magnes sive de Arte Magnetica', uk='Магніт, або Магнетичне мистецтво', field='earth', k=('WE', 'NORTH', 'SUMMER'), conf='m',
      why='дані з єзуїтської мережі (Файндлен називає Magnes прикладом «єзуїтського емпіризму»)',
      sum='Від магнетизму Землі до іграшок; «притягання» взагалі, зокрема любов і тяжіння. Пояснив магнітний годинник водяною моделлю: це спростувало твердження Пейреска про магнітну силу Сонця й підтримало Коперника.', claims=['C15'], src=['S3', 'S10', 'S37']),
 dict(id='lingua', year=1643, la='Lingua Aegyptiaca Restituta', uk='Відновлена єгипетська мова', field='egypt', k=('THEY', 'SOUTH', 'SUMMER'), conf='h',
      why='збір і виправлення коптського матеріалу', sum='Про коптську; виправляє помилки «Провісника»; пов’язує давньоєгипетські, вавилонські й індійські назви зірок.', claims=['C1'], src=['S15', 'S13']),
 dict(id='lucis', year=1646, end=None, ynote='1644, 1645 або 1646 залежно від джерела; 2-ге видання 1671', la='Ars Magna Lucis et Umbrae', uk='Велике мистецтво світла й тіні', field='sense', k=('ME', 'NORTH', 'AUTUMN'), conf='m',
      why='авторський синтез оптики (світло, тіні, дзеркала, годинники)',
      sum='Перший у Європі друкований опис освітлення й проєкції зображень. Перше друковане зображення Сатурна, власні малюнки сонячних плям, складні сонячні годинники, листок із часом в усіх місіях єзуїтів. У виданні 1671 р. є опис «чарівного ліхтаря»; оптична схема в ньому має помилки.', claims=['C5', 'C6'], src=['S16', 'S28', 'S29']),
 dict(id='obeliscus', year=1650, la='Obeliscus Pamphilius', uk='Обеліск Памфілі', field='egypt', k=('YOU', 'SOUTH', 'WINTER'), conf='h',
      why='замовлення Інокентія X; публічний переклад написів', sum='Спроба прочитати ієрогліфи обеліска з Пьяцца Навона. Помилкові «переклади» вирізано на постаменті фонтана Бернінi. Цензор Ніколаус Вайзінг 1652 р. скаржився, що Кірхер не виконав вимог цензури.', claims=['C12', 'C18', 'C19'], src=['S39', 'S15']),
 dict(id='musurgia', year=1650, la='Musurgia Universalis', uk='Універсальна музургія', field='sense', k=('THEY', 'NORTH', 'SUMMER'), conf='m',
      why='компендіум історичного й сучасного знання про музику',
      sum='Два томи, 10 книг, понад 1100 сторінок. Музика як відбиток універсальних пропорцій; вчення про афекти; водяні органи, запис пташиних співів, рупор і «Arca musarithmica» для механічного складання гімнів. «Котяче фортепіано» ніколи не будували.', claims=[], src=['S17', 'S10', 'S3']),
 dict(id='oedipus', year=1652, end=1654, ynote='4 томи 1652–1655 за різними джерелами', la='Oedipus Aegyptiacus', uk='Єгипетський Едіп', field='egypt', k=('ME', 'SOUTH', 'AUTUMN'), conf='h',
      why='авторський синтез', sum='Найвідоміша праця: єгиптологія й порівняльна релігія з халдейською астрологією, кабалою, піфагорійською математикою, арабською алхімією. Цензори критикували її ще до друку. Переклади написів не збігаються з оригіналом.', claims=['C2', 'C12'], src=['S18', 'S2', 'S3', 'S15']),
 dict(id='itinerarium', year=1656, ynote='1660: друге видання «Iter Exstaticum Coeleste» (Шотт)', la='Itinerarium Exstaticum', uk='Екстатична подорож', field='world', k=('ME', 'NORTH', 'SPRING'), conf='m',
      why='уявний діалог власного задуму, без географічного джерела', sum='Теодідакт, зачарований сакральною музикою, подорожує небесами з ангелом. Цензори переглянули рукопис; погляди незвичні для єзуїта XVII ст. Одна з двох художніх праць Кірхера.', claims=[], src=['S8', 'S19']),
 dict(id='iter2', year=1657, la='Iter Exstaticum II', uk='Екстатична подорож II', field='earth', k=('ME', 'SOUTH', 'SPRING'), conf='m',
      why='провісник «Підземного світу»: подорож під землю', sum='Друга художня праця; рекламована як вступ до «Mundus Subterraneus».', claims=[], src=['S8', 'S19', 'S37']),
 dict(id='scrutinium', year=1658, la='Scrutinium Physico-Medicum Contagiosae Luis', uk='Фізико-медичне дослідження чуми', field='earth', k=('ME', 'SOUTH', 'SUMMER'), conf='h',
      why='власні мікроскопні досліди під час італійської чуми 1656 р.', sum='Кров хворих на чуму «повна червів». Висунуто контагіозну теорію, радив ізоляцію, карантин, спалювання одягу, маски. Допускав мимовільне зародження. Згадує болота Лаціуму й малярію.', claims=['C4a', 'C4b', 'C17', 'C23'], src=['S20', 'S27', 'S3', 'S38']),
 dict(id='diatribe', year=1661, la='Diatribe de prodigiosis crucibus', uk='Розвідка про дивовижні хрести', field='earth', k=('YOU', 'SOUTH', 'WINTER'), conf='h',
      why='звернена до публіки, щоб заспокоїти після виверження Везувію 1660 р.', sum='Про хрестоподібні об’єкти, що впали з неба під час виверження. Кірхер шукав пояснення, яке уникне паніки; як і інші праці, пройшла цензуру ордену.', claims=[], src=['S21']),
 dict(id='polygraphia', year=1663, la='Polygraphia Nova et Universalis', uk='Нова й універсальна поліграфія', field='method', k=('YOU', 'NORTH', 'SPRING'), conf='m',
      why='за його свідченням, створена на прохання; адресат', sum='Штучна універсальна мова: листування між людьми без спільної мови. Єдина повна праця Кірхера з криптографії.', claims=[], src=['S4', 'S3']),
 dict(id='mundus', year=1664, end=1665, ynote='гравіровані титули 1664, друкований 1665; 2-ге видання 1678', la='Mundus Subterraneus', uk='Підземний світ', field='earth', k=('WE', 'SOUTH', 'SUMMER'), conf='h',
      why='зібрані спостереження й мережа', sum='Геокосмос від вулканів до скам’янілостей. Окрема тема: припливи як рух води до підземного океану, гідрологічний цикл, плями на Сонці як вулкани, дракони. Відкидав повільну картезіанську еволюцію Землі з біблійних причин.', claims=['C9', 'C13a', 'C13b', 'C14'], src=['S22', 'S9', 'S32', 'S33']),
 dict(id='eustachio', year=1665, la='Historia Eustachio-Mariana', uk='Євстахієво-Маріанська історія', field='world', k=('ME', 'NORTH', 'WINTER'), conf='m',
      why='публічний звіт про власне знаходження святилища (Ментореллa, 1661)', sum='Розповідь про відкриття руїн церкви, що, за переказом, побудована Костянтином; пізніше святилище Ментореллa, де поховано серце Кірхера.', claims=[], src=['S3', 'S38', 'S36']),
 dict(id='arithmologia', year=1665, la='Arithmologia', uk='Арифмологія', field='method', k=('THEY', 'NORTH', 'SPRING'), conf='l',
      why='за назвою: числова символіка давніх авторитетів; змісту в джерелах немає', sum='У зібраних джерелах лише назва й рік.', claims=[], src=['S3']),
 dict(id='obelisci', year=1666, ynote='1666 за Wikipedia; 1676 за переліком у S37', la='Obelisci Aegyptiaci ... interpretatio hieroglyphica', uk='Єгипетські обеліски', field='egypt', k=('ME', 'SOUTH', 'AUTUMN'), conf='l',
      why='той самий метод, що в «Едіпі»; змісту в зібраних джерелах немає', sum='Тлумачення написів на обелісках.', claims=['C12'], src=['S3', 'S37']),
 dict(id='china', year=1667, la='China Monumentis Illustrata', uk='Китай, ілюстрований пам’ятками', field='china', k=('WE', 'EAST', 'SUMMER'), conf='h',
      why='дані місіонерів (Бойм, Мартіні, Грюбер)', sum='Енциклопедія Китаю: точна картографія поряд із драконами. Латинський переклад Сіаньської стели, шляхи до Китаю. Хами як предки китайців, Конфуцій як Гермес, китайські знаки як абстраговані ієрогліфи. Сам автор у Китаї не був і китайської не знав.', claims=['C7', 'C8', 'C10'], src=['S23', 'S24', 'S31', 'S30']),
 dict(id='magneticum', year=1667, la='Magneticum naturae regnum', uk='Магнетичне царство природи', field='earth', k=('ME', 'NORTH', 'AUTUMN'), conf='l',
      why='за назвою: розвиток теми «Магніта»; змісту в джерелах немає', sum='У зібраних джерелах лише назва й рік.', claims=[], src=['S3', 'S37']),
 dict(id='organum', year=1668, la='Organum mathematicum', uk='Математичний орган', field='sense', k=('WE', 'NORTH', 'AUTUMN'), conf='l',
      why='виданий Шоттом за винаходом Кірхера; Кірхер — співавтор', sum='За S3 Кірхер — співавтор; Monumenta Kircheri датує працю приблизно 1661 р.', claims=[], src=['S3', 'S6']),
 dict(id='principis', year=1669, la='Principis Christiani archetypon politicum', uk='Політичний прообраз християнського правителя', field='world', k=('YOU', 'NORTH', 'WINTER'), conf='l',
      why='за назвою адресована правителеві; змісту в джерелах немає', sum='У зібраних джерелах лише назва й рік.', claims=[], src=['S3']),
 dict(id='latium', year=1669, ynote='друге видання, Амстердам, 1671', la='Latium', uk='Лацій', field='world', k=('ME', 'NORTH', 'SUMMER'), conf='h',
      why='власні пішохідні обстеження околиць Рима', sum='Перша праця про топографію, археологію й історію Лаціуму; присвячена Клименту X; 5 книг, 27 гравюр. Ной заселив Лацій, Сатурн і Янус — це Ной; мозаїку з Пренесте прочитано як церемонії богині Фортуни. Фабретті знайшов багато помилок.', claims=['C20', 'C21'], src=['S38']),
 dict(id='sciendi', year=1669, la='Ars Magna Sciendi sive Combinatoria', uk='Велике мистецтво знання', field='method', k=('THEY', 'NORTH', 'AUTUMN'), conf='h',
      why='луллівська традиція; комбінаторний синтез', sum='12 книг: універсальна система знання на дев’яти божественних атрибутах, розвиток комбінаторики Рамона Луллія. Волвелі й таблиці символів. За Кнутом, можливо, перші відомі малюнки повних дводольних графів. «Arca Musarithmica» складає гімни з музичних фраз.', claims=['C11', 'C24'], src=['S25', 'S3']),
 dict(id='phonurgia', year=1673, la='Phonurgia Nova', uk='Нова фонургія', field='sense', k=('ME', 'NORTH', 'SUMMER'), conf='m',
      why='власні досліди з рупором і ехом; Кірхер заявляв про пріоритет', sum='Акустика: підсилення звуку, відлуння, музикотерапія тарантизму. «Фонургія» за визначенням автора: здатність викликати дивовижне за допомогою звуків. Він стверджував, що першим винайшов рупор («tuba»), і посилався на «Музургію».', claims=[], src=['S10', 'S17', 'S3']),
 dict(id='arca', year=1675, la='Arca Noë', uk='Ноїв ковчег', field='world', k=('THEY', 'NORTH', 'AUTUMN'), conf='m',
      why='біблійний авторитет і зоологічний синтез', sum='Розрахував, що переповнення не було б проблемою. Перетворення видів після потопу (олені стали північними оленями); броненосець — гібрид черепахи й дикобраза. Деякі історики бачать у ньому протоеволюціоніста.', claims=['C22'], src=['S3', 'S37']),
 dict(id='sphinx', year=1676, ynote='1673 за S26, 1676 за переліком у S37', la='Sphinx Mystagoga', uk='Сфінкс-містагог', field='egypt', k=('ME', 'SOUTH', 'WINTER'), conf='l',
      why='остання вилазка в єгиптологію; підсумок власної лінії', sum='Остання вилазка Кірхера в єгиптологію.', claims=[], src=['S26', 'S37']),
 dict(id='turris', year=1679, la='Turris Babel', uk='Вавилонська вежа', field='egypt', k=('THEY', 'EAST', 'AUTUMN'), conf='m',
      why='давня історія мов після потопу; синтез на авторитетах', sum='Хронологія розселення народів і поділу мов після потопу, історія мов-нащадків.', claims=[], src=['S4', 'S3']),
 dict(id='musaeum', year=1679, ynote='каталог Дж. де Сепібуса — 1678; Бонанні — 1709', la='Musaeum Collegii Romani Societatis Jesu', uk='Музей Римської колегії', field='world', k=('WE', 'NORTH', 'WINTER'), conf='m',
      why='колективний каталог музею, що його вели учні', sum='Каталог музею Колегіо Романо. Музей зберіг античність, етнографію, природознавство й наукові прилади; пізніше розійшовся по римських збірках, тож каталоги — єдиний запис вмісту.', claims=[], src=['S3', 'S10', 'S11']),
 dict(id='tariffa', year=1679, la='Tariffa Kircheriana', uk='Тариф Кірхера', field='sense', k=None, conf=None,
      why='не анотовано: у зібраних джерелах лише назва й рік', sum='У зібраних джерелах лише назва й рік.', claims=[], src=['S3']),
 dict(id='physiologia', year=1680, la='Physiologia Kircheriana Experimentalis', uk='Експериментальна фізіологія Кірхера', field='sense', k=('WE', 'NORTH', 'WINTER'), conf='m',
      why='складена учнем Й. Кестлером: колективна праця', sum='Збірка про світло й тінь, музику й акустику, алхімію, гідравліку й гіпноз тварин.', claims=[], src=['S37', 'S17']),
]

# e: id, year, end, label, place, lat, lon, kind, text, src, note
EVENTS = [
 dict(id='birth', year=1601, end=1602, label='Народження', place='Гейса', lat=50.80, lon=9.96, kind='life', text='Народився 2 травня 1601 або 1602 р. у Гейсі (Бухонія) поблизу Фульди. Сам не знав, якого року.', src=['S3', 'S5', 'S36'], note='рік: 1601 (S36, S5-варіант) чи 1602 (S3)'),
 dict(id='fulda', year=1614, end=1618, label='Школа у Фульді', place='Фульда', lat=50.55, lon=9.68, kind='life', text='Єзуїтський колегіум у Фульді.', src=['S3', 'S36']),
 dict(id='novitiate', year=1618, label='Новіціат', place='Падерборн', lat=51.72, lon=8.76, kind='life', text='Вступив до Товариства Ісуса (2 жовтня 1618 за S36); навчався філософії й теології в Падерборні.', src=['S3', 'S36']),
 dict(id='cologne', year=1622, label='Утеча до Кельна', place='Кельн', lat=50.94, lon=6.96, kind='life', text='Утік до Кельна від наступу протестантських військ (S3); S36 ставить філософські студії в Кельні «невдовзі після 1618».', src=['S3', 'S36'], note='дата: 1622 (S3) чи невдовзі по 1618 (S36)'),
 dict(id='koblenz', year=1622, end=1624, label='Регентство в Кобленці', place='Кобленц', lat=50.36, lon=7.59, kind='life', text='Викладав у Кобленці як регент.', src=['S3']),
 dict(id='heiligenstadt', year=1624, end=1628, label='Хайліґенштадт', place='Хайліґенштадт', lat=51.38, lon=10.14, kind='life', text='Викладав математику, єврейську й сирійську; створив феєрверки й рухомі декорації для курфюрста-архієпископа Майнца. Дата в S3 не вказана; рік оцінено.', src=['S3'], note='дата орієнтовна: міститься між Кобленцем і 1628'),
 dict(id='mainz', year=1625, label='Теологія в Майнці', place='Майнц', lat=50.00, lon=8.27, kind='life', text='Почав вивчати теологію в Майнці, де його помітив курфюрст.', src=['S36']),
 dict(id='ordained', year=1628, label='Висвячення', place='Шпаєр', lat=49.32, lon=8.43, kind='life', text='Висвячений на священника. Тоді ж, за S3, його інтерес до ієрогліфів пов’язаний зі збіркою в Шпаєрі.', src=['S3', 'S36']),
 dict(id='wurzburg', year=1628, end=1631, label='Професор у Вюрцбурзі', place='Вюрцбург', lat=49.79, lon=9.93, kind='life', text='Професор етики й математики; викладав єврейську й сирійську. Після захоплення міста здобув повагу за «передбачення» нещастя астрологією, хоч приватно це заперечував.', src=['S3', 'S36']),
 dict(id='china_wish', year=1629, label='Бажання їхати до Китаю', place='Вюрцбург', lat=49.79, lon=9.93, kind='life', text='Повідомив начальство, що хоче стати місіонером у Китаї. Бажання не здійснилось.', src=['S3', 'S36']),
 dict(id='avignon', year=1631, label='Втеча в Авіньйон', place='Авіньйон', lat=43.95, lon=4.81, kind='life', text='Через війну залишив Вюрцбург; спершу Ліон, потім папський університет в Авіньйоні. Того ж року вийшла «Ars Magnesia».', src=['S3', 'S36']),
 dict(id='rome', year=1633, label='Прибуття до Рима', place='Рим', lat=41.90, lon=12.50, kind='life', text='Вивчив коптську. Його покликали до Відня на місце Кеплера, але призначення скасували після втручання Пейреска. Корабель знесло, і він прибув до Рима.', src=['S3', 'S36'], note='Catholic Encyclopedia: аварія біля Чивітавекк’ї'),
 dict(id='collegio', year=1634, label='Колегіо Романо', place='Рим', lat=41.90, lon=12.50, kind='life', text='Почав викладати математику, фізику й східні мови в Колегіо Романо (нині Папський Григоріанський університет); з часом звільнений для досліджень.', src=['S3', 'S36']),
 dict(id='sicily', year=1637, end=1638, label='Мальта, Сицилія, Мессінська протока', place='Мессіна', lat=38.19, lon=15.55, kind='life', text='Вивчав Мессінську протоку, Етну й Стромболі; їздив на Мальту; скам’янілі рештки слонів у Трапані й Палермо.', src=['S3', 'S36', 'S9']),
 dict(id='malta', year=1637, end=1638, label='Мальта', place='Мальта', lat=35.90, lon=14.51, kind='life', text='Поїздка на Мальту й вивчення вулканів між Неаполем і Мальтою.', src=['S36']),
 dict(id='vesuvius', year=1638, label='Калабрійський землетрус і Везувій', place='Везувій', lat=40.82, lon=14.43, kind='life', text='Коли Кірхер залишив Мессіну, землетрус зруйнував місто Евфемію. У Неаполі піднявся на Везувій і, за його розповіддю, його спустили в кратер.', src=['S3', 'S36', 'S9']),
 dict(id='descartes', year=1643, label='Декарт про Кірхера', place='', lat=None, lon=None, kind='reception', text='Декарт у листі назвав Кірхера «більше шарлатаном, ніж ученим» і відмовлявся читати його книги.', src=['S28', 'S34']),
 dict(id='pamphilj', year=1650, label='Обеліск на Пьяцца Навона', place='Рим', lat=41.90, lon=12.47, kind='life', text='Папа Інокентій X доручив Кірхеру очолити перенесення й тлумачення обеліска; Бернінi збудував над ним фонтан Чотирьох річок. Фінансували книгу папа, імператор і Фердінандо II Медичі.', src=['S39']),
 dict(id='museum', year=1651, label='Музей у Колегіо Романо', place='Рим', lat=41.90, lon=12.48, kind='life', text='Заснований музей: з приватної збірки, переведеної в галерею Колегіо Романо. Античність, етнографія, природознавство, прилади.', src=['S10', 'S3']),
 dict(id='censor', year=1652, label='Цензор Вайзінг', place='Рим', lat=None, lon=None, kind='reception', text='Єзуїтський цензор Ніколаус Вайзінг поскаржився, що Кірхер не виконав вимог цензури щодо «Obeliscus Pamphilius».', src=['S39']),
 dict(id='plague', year=1656, label='Чума в Італії', place='Рим', lat=41.90, lon=12.50, kind='life', text='Чума прийшла до Неаполя навесні 1656 р., у Римі померло близько 15 000 осіб. Кірхер вивчає кров під мікроскопом. За S3 перші мікроскопні дослідження датуються 1646 р.', src=['S20', 'S3', 'S27'], note='мікроскоп: 1646 (S3) чи 1656 (Public Domain Review)'),
 dict(id='mentorella', year=1661, label='Руїни Ментореллі', place='Ментореллa', lat=41.92, lon=12.98, kind='life', text='Відкрив руїни церкви, що, за переказом, збудував Костянтин; згодом святилище Ментореллa. Того ж року Ян Янссон отримав виняткове право друкувати Кірхера.', src=['S3', 'S9', 'S38']),
 dict(id='voynich', year=1665, label='Рукопис Войнича', place='Прага', lat=50.08, lon=14.43, kind='network', text='Отримав від Йоганнеса Марка Марці рукопис Войнича (за S3). Приклад мережі з Богемії.', src=['S3', 'S12']),
 dict(id='death', year=1680, label='Смерть', place='Рим', lat=41.90, lon=12.50, kind='life', text='Помер у Римі 27 листопада 1680 р. (S3; S36 дає 28 листопада). Серце поховане в Ментореллі.', src=['S3', 'S36']),
 dict(id='bonanni', year=1709, label='Каталог Бонанні', place='Рим', lat=None, lon=None, kind='reception', text='Учень і наступник Філіппо Бонанні видав майже 800-сторінковий каталог музею.', src=['S11']),
 dict(id='champollion', year=1822, label='Шампольйон', place='', lat=None, lon=None, kind='reception', text='Шампольйон оприлюднив розшифрування ієрогліфів, спираючись на коптську, яку вивчав, наслідуючи Кірхера. 1827 р. переклав і напис Памфілійського обеліска.', src=['S26', 'S39']),
 dict(id='yersinia', year=1894, label='Бацила чуми', place='', lat=None, lon=None, kind='reception', text='Відкрито Yersinia pestis. Кірхер у XVII ст. не міг її бачити.', src=['S20']),
]

# p: id, name, role, text, works, src
PEOPLE = [
 dict(id='peiresc', name='Ніколя-Клод Фабрі де Пейреск', role='patron', text='Друг і патрон. Передав коптські рукописи; 1633 р. втрутився й скасував віденське призначення Кірхера.', works=['prodromus', 'magnes'], src=['S3', 'S13']),
 dict(id='barberini', name='Кардинал Франческо Барберіні', role='patron', text='Спонсор і адресат «Prodromus Coptus». Після обрання Інокентія X втік у вигнання.', works=['prodromus'], src=['S15', 'S39']),
 dict(id='innocent', name='Папа Інокентій X', role='patron', text='Доручив Кірхеру тлумачення обеліска на Пьяцца Навона.', works=['obeliscus'], src=['S39']),
 dict(id='alexander', name='Папа Олександр VII', role='patron', text='Адресат «Mundus Subterraneus».', works=['mundus'], src=['S9']),
 dict(id='clement', name='Папа Климент X', role='patron', text='Адресат «Latium».', works=['latium'], src=['S38']),
 dict(id='habsburg', name='Габсбурзький двір', role='patron', text='Двоє імператорів у списку кореспондентів; двір фінансував і обговорював праці. Згодом Кірхер втратив прихильність двору.', works=['obeliscus', 'sciendi'], src=['S6', 'S12', 'S25', 'S39']),
 dict(id='medici', name='Фердінандо II Медичі', role='patron', text='Фінансував книгу про обеліск.', works=['obeliscus'], src=['S39']),
 dict(id='dellavalle', name='П’єтро делла Валле', role='network', text='Привіз з Єгипту арабсько-коптський словник.', works=['prodromus'], src=['S13']),
 dict(id='boym', name='Міхал Бойм', role='network', text='Єзуїт-місіонер; джерело «China Illustrata»; з китайським співавтором дав переклад Сіаньської стели.', works=['china'], src=['S23']),
 dict(id='martini', name='Мартіно Мартіні', role='network', text='Єзуїт-місіонер; джерело «China Illustrata».', works=['china'], src=['S23']),
 dict(id='grueber', name='Йоганн Грюбер', role='network', text='Єзуїт; сухопутні шляхи до Китаю в «China Illustrata».', works=['china'], src=['S23']),
 dict(id='dorville', name='Альберт д’Орвіль', role='network', text='Єзуїт; сухопутні шляхи до Китаю.', works=['china'], src=['S23']),
 dict(id='marci', name='Йоганнес Марк Марці', role='network', text='З Богемії; передав рукопис Войнича.', works=[], src=['S3', 'S12']),
 dict(id='leibniz', name='Ґотфрід Лейбніц', role='network', text='Кореспондент; «Scrutinium» вплинув на його думки про контагіозність; власна «Ars combinatoria» вийшла 1666.', works=['scrutinium', 'sciendi'], src=['S6', 'S20', 'S25']),
 dict(id='torricelli', name='Еванджеліста Торрічеллі', role='network', text='Серед відомих кореспондентів.', works=[], src=['S6']),
 dict(id='gassendi', name='П’єр Гассенді', role='network', text='Серед відомих кореспондентів.', works=[], src=['S6']),
 dict(id='lastanosa', name='Вінсенсіо Хуан де Ластаноса й Дієго Вінсенсіо Відання', role='network', text='Іспанські кореспонденти; листи 1656–1672 рр.', works=[], src=['S6']),
 dict(id='schott', name='Ґаспар Шотт', role='collaborator', text='Видав «Iter Exstaticum Coeleste» (1660) і захищав Кірхера від цензорів; видав «Organum mathematicum».', works=['itinerarium', 'organum'], src=['S19', 'S6']),
 dict(id='kestler', name='Йоганн Кестлер', role='collaborator', text='Учень, що склав «Physiologia Kircheriana».', works=['physiologia'], src=['S37']),
 dict(id='bonanni_p', name='Філіппо Бонанні', role='collaborator', text='Учень і наступник як професор і хранитель музею; каталог 1709.', works=['musaeum'], src=['S11']),
 dict(id='sepibus', name='Джорджо де Сепібус', role='collaborator', text='Склав каталог музею 1678 р.', works=['musaeum'], src=['S17']),
 dict(id='jansson', name='Ян Янссон ван Васберґе', role='publisher', text='Амстердамський видавець; з 1661 р. має виняткове право друкувати Кірхера.', works=['mundus', 'china', 'sciendi', 'latium', 'arca', 'turris'], src=['S9', 'S25']),
 dict(id='grignani', name='Лудовіко Гріньяні', role='publisher', text='Римський друкар «Magnes» і «Obeliscus Pamphilius».', works=['magnes', 'obeliscus'], src=['S37', 'S39']),
 dict(id='descartes_p', name='Рене Декарт', role='critic', text='1643 р. назвав Кірхера шарлатаном і не читав його книг.', works=[], src=['S28', 'S34']),
 dict(id='redi', name='Франческо Реді', role='critic', text='Намагався відтворити досліди «Scrutinium» і не зміг; поставив під сумнів, що Кірхер їх проводив.', works=['scrutinium'], src=['S20']),
 dict(id='fabretti', name='Раффаелло Фабретті', role='critic', text='Знайшов у «Latium» багато помилок, зокрема в акведуках.', works=['latium'], src=['S38']),
 dict(id='wysing', name='Ніколаус Вайзінг', role='censor', text='Єзуїтський цензор; 1652 р. скаржився на невиконання вимог.', works=['obeliscus'], src=['S39']),
 dict(id='champollion_p', name='Жан-Франсуа Шампольйон', role='successor', text='Вивчав коптську, наслідуючи Кірхера; розшифрував ієрогліфи (1822).', works=['prodromus', 'oedipus'], src=['S26']),
 dict(id='bernini', name='Джан Лоренцо Бернінi', role='successor', text='Збудував фонтан Чотирьох річок над обеліском, що його тлумачив Кірхер.', works=['obeliscus'], src=['S39']),
 dict(id='findlen', name='Пола Файндлен', role='scholar', text='Автор формули «останній, хто знав усе» й праці про музей Кірхера.', works=[], src=['S1', 'S9']),
 dict(id='stolzenberg', name='Даніель Стольценберг', role='scholar', text='Автор «Egyptian Oedipus» (2013): заперечує образ «ексцентричного анахроніста».', works=['oedipus'], src=['S18', 'S35']),
 dict(id='eco', name='Умберто Еко', role='scholar', text='«Найсучасніший з-поміж наших предків і найзастарілиший з-поміж наших сучасників».', works=[], src=['S6']),
]
ROLES = {
    'patron': 'Патрони', 'network': 'Мережа й кореспонденти', 'collaborator': 'Учні й співавтори', 'publisher': 'Видавці',
    'critic': 'Критики', 'censor': 'Цензура', 'successor': 'Наступники', 'scholar': 'Дослідники',
}

# c: id, text, t, f, pro, con, src
CLAIMS = [
 dict(id='C1', text='Коптська мова походить від давньоєгипетської і є ключем до ієрогліфів', t=1, f=0, pro='Перший висунув гіпотезу прямого зв’язку; вона підтвердилась. Шампольйон вивчав коптську, наслідуючи його.', con='', src=['S13', 'S14', 'S15', 'S26']),
 dict(id='C2', text='Ієрогліфи — суто символічне, нефонетичне письмо', t=0, f=1, pro='', con='Кірхер відкидав фонетичність як пізню; розшифрування Шампольйона показало фонетичну природу.', src=['S26', 'S15']),
 dict(id='C3', text='Одну ієрогліфічну групу (mu, «вода») прочитано правильно', t=1, f=0, pro='Правильно названо групу mu («вода»), джерело літери M.', con='', src=['S26']),
 dict(id='C4a', text='Чуму переносять живі мікроскопічні агенти', t=1, f=0, pro='Першим явно сформулював теорію контагіозності через «animalcula»; вплив на Лейбніца.', con='', src=['S20', 'S27']),
 dict(id='C4b', text='У крові хворих під мікроскопом було видно збудників чуми', t=0, f=1, pro='', con='Yersinia pestis відкрито 1894 р.; він бачив, ймовірно, клітини крові. Реді не відтворив низку дослідів.', src=['S20', 'S27']),
 dict(id='C5', text='Кірхер винайшов «чарівний ліхтар»', t=0, f=1, pro='', con='Перші друковані зображення лише 1671 р.; оптична схема помилкова; він удосконалив пристрій, але не винайшов.', src=['S16', 'S28', 'S29']),
 dict(id='C6', text='«Ars Magna Lucis et Umbrae» — найраніший опублікований у Європі опис освітлення й проєкції зображень', t=1, f=0, pro='Так стверджують огляди видання.', con='', src=['S16']),
 dict(id='C7', text='Сіаньська стела автентична, і Кірхер опублікував її текст', t=1, f=0, pro='Стела 781 р., знайдена 1625 р.; «China Illustrata» містить репродукцію й переклади Бойма.', con='', src=['S23', 'S24', 'S30']),
 dict(id='C8', text='«China Illustrata» загалом достовірно описує Китай', t=1, f=1, pro='Точна картографія, шляхи, стела.', con='Дракони; Конфуцій = Гермес; китайські знаки як ієрогліфи. Автор не був у Китаї й не знав мови.', src=['S23', 'S24', 'S31']),
 dict(id='C9', text='«Mundus Subterraneus» загалом достовірно описує будову Землі', t=1, f=1, pro='Спостереження вулканів; гідрологічний цикл.', con='Плями на Сонці як вулкани; дракони; велетні.', src=['S22', 'S32', 'S33']),
 dict(id='C10', text='Китайські знаки — абстраговані єгипетські ієрогліфи', t=0, f=0, pro='', con='У корпусі є лише формулювання самого Кірхера; оцінки немає.', src=['S23', 'S3']),
 dict(id='C11', text='«Ars Magna Sciendi» дає універсальний метод для будь-якого предмета', t=0, f=0, pro='', con='У корпусі є лише задум; перевірки немає.', src=['S25']),
 dict(id='C12', text='Кірхерові переклади конкретних ієрогліфічних написів правильні', t=0, f=1, pro='', con='«Жоден не наближається до оригіналу» (Фріммер); «повна нісенітниця» (Бадж).', src=['S18', 'S34', 'S15', 'S3']),
 dict(id='C13a', text='Скам’янілості — рештки тварин', t=1, f=0, pro='Усвідомлював, що це залишки тварин.', con='', src=['S3']),
 dict(id='C13b', text='Великі кістки належали велетенським людським расам', t=0, f=1, pro='', con='Деякі його «скам’янілості» не були такими; велетні — хибне пояснення.', src=['S3']),
 dict(id='C14', text='Припливи спричиняє рух води до підземного океану й від нього', t=0, f=0, pro='', con='Подано без оцінки в зібраних джерелах.', src=['S22', 'S3']),
 dict(id='C15', text='Магнітний годинник працює на водяному механізмі, а не на магнетизмі Сонця', t=1, f=0, pro='Модель Кірхера спростувала твердження Пейреска; підтримка Коперника (за S3).', con='', src=['S3']),
 dict(id='C17', text='Живі істоти виникають мимовільно в гниючій матерії', t=0, f=1, pro='', con='Прихильник мимовільного зародження; це хибна гіпотеза.', src=['S3', 'S20']),
 dict(id='C18', text='Південну грань Памфілійського обеліска «прочитано» як текст про триєдине божество «Хемпта»', t=0, f=1, pro='', con='Справжній напис: «Гор, сильний бик, коханий Маат».', src=['S39']),
 dict(id='C19', text='Обеліск замовив фараон Сотіс близько 1336 р. до н. е., привіз Каракалла', t=0, f=1, pro='', con='За S39 ця історія не має зв’язку з реальністю; насправді його замовив Доміціан.', src=['S39']),
 dict(id='C20', text='Лацій заселив Ной, а Сатурн і Янус — це Ной', t=0, f=1, pro='', con='Спекулятивна теорія; Фабретті знайшов у праці багато помилок. Оцінка слабка.', src=['S38']),
 dict(id='C21', text='«Latium» — перша праця про топографію, археологію й історію Лаціуму', t=1, f=0, pro='Перша спроба повної хронологічної реконструкції регіону (хоч неточна).', con='', src=['S38']),
 dict(id='C22', text='Види змінюються після потопу (олені стали північними оленями)', t=1, f=1, pro='Деякі історики називають його протоеволюціоністом.', con='Броненосець як гібрид черепахи й дикобраза.', src=['S3']),
 dict(id='C23', text='Хінін проти малярії рекомендовано в Римі ще за Кірхера', t=1, f=0, pro='Імовірно, серед перших у Римі (слово «probably» у джерелі).', con='', src=['S38']),
 dict(id='C24', text='«Ars Magna Sciendi» містить перші відомі малюнки повних дводольних графів', t=1, f=0, pro='За Кнутом, можливо.', con='', src=['S3']),
]
BEL = {(1, 0): 'T', (0, 1): 'F', (1, 1): 'B', (0, 0): 'N'}

# джерела
SOURCES = {
 'S1': ('Kircher, Athanasius (Springer)', 'https://link.springer.com/rwe/10.1007/978-3-319-14169-5_561'),
 'S2': ('Kircher, Athanasius (Encyclopedia.com)', 'https://www.encyclopedia.com/people/science-and-technology/mathematics-biographies/athanasius-kircher'),
 'S3': ('Athanasius Kircher (Wikipedia)', 'https://en.wikipedia.org/wiki/Athanasius_Kircher'),
 'S4': ('Polygraphia Nova (Wikipedia)', 'https://en.wikipedia.org/wiki/Polygraphia_Nova'),
 'S5': ('Athanasius Kircher (HandWiki)', 'https://handwiki.org/wiki/Biography:Athanasius_Kircher'),
 'S6': ('Кореспонденція Кірхера (Stanford, Флоренція)', 'https://web.stanford.edu/group/kircher/cgi-bin/site/?page_id=7'),
 'S7': ('Mapping the Republic of Letters', 'https://brewminate.com/?p=161820'),
 'S8': ('Itinerarium exstaticum (Wikipedia)', 'https://en.wikipedia.org/wiki/Itinerarium_exstaticum'),
 'S9': ('Mundus subterraneus, перше видання (Christie’s)', 'https://onlineonly.christies.com.cn/s/fine-printed-books-manuscripts-including-americana/mundus-subterraneus-70/195398'),
 'S10': ('Phonurgia nova (Unibo); Arca musarithmica (Digicult)', 'https://digicult.it/digimag/issue-055/athanasius-kircher-arca-musarithmica-and-many-sound-devices/'),
 'S11': ('Harmonic Cabinet / Бонанні', 'https://roughlydaily.com/tag/harmonic-cabinet/'),
 'S12': ('Lelková, Findlen, Sutherland, Kircher’s Bohemia', 'https://asep.lib.cas.cz/arl-cav/cs/detail-cav_un_epca-0524780-Kirchers-Bohemia-Jesuit-Networks-and-Habsburg-Patronage-in-the-Seventeenth-Century/'),
 'S13': ('Prodromus Coptus (Sokol Books)', 'https://sokol.co.uk/?p=9913793'),
 'S14': ('Prodromus Coptus (Christie’s)', 'https://onlineonly.christies.com.cn/s/fine-printed-books-manuscripts-including-americana/prodromus-coptus-sive-aegyptiacus-27/208815'),
 'S15': ('Egyptian Society of South Africa', 'https://www.egyptiansociety.co.za/?p=2118'),
 'S16': ('Ars Magna Lucis et Umbrae (Wikipedia)', 'https://en.wikipedia.org/wiki/Ars_Magna_Lucis_et_Umbrae'),
 'S17': ('Musurgia universalis (Melbourne); Stanford, ілюстрації', 'https://library.unimelb.edu.au/asc/teaching-and-learning/objects/musurgia-universalis'),
 'S18': ('Stolzenberg, Public Domain Review', 'https://publicdomainreview.org/essay/athanasius-kircher-and-the-hieroglyphic-sphinx'),
 'S19': ('The Kircher Circle (Wichita State)', 'https://wichita.edu/academics/fairmount_las/geology/wparcell/Kircher/Intro.php'),
 'S20': ('Scrutinium Physico-Medicum (Wikipedia)', 'https://en.wikipedia.org/wiki/Scrutinium_Physico-Medicum'),
 'S21': ('Diatribe de prodigiosis crucibus (Wikipedia)', 'https://en.wikipedia.org/wiki/Diatribe_de_Progidiosis_Crucibus'),
 'S22': ('NASA Earth Observatory: Happy birthday, Kircher', 'https://science.nasa.gov/blogs/earth-matters/2012/04/30/happy-birthday-athanasius-kircher/'),
 'S23': ('China Illustrata (Beijing Center)', 'https://thebeijingcenter.org/cultural-dialogues/library-tour-a-look-inside-kirchers-china-illustrata/'),
 'S24': ('Xi’an Stele (Wikipedia)', 'https://en.wikipedia.org/wiki/Xi%27an_Stele'),
 'S25': ('Ars Magna Sciendi (Scranton)', 'https://sites.scranton.edu/library/2017/02/24/athanasius-kirchers-ars-magna-sciendi-sive-combinatoria-1669'),
 'S26': ('Yale Peabody, Echoes of Egypt', 'https://echoesofegypt.peabody.yale.edu/egyptosophy/sphinx-mystagogaturris-babel'),
 'S27': ('Історія медицини: Scrutinium', 'https://historyofmedicine.com/id/3487'),
 'S28': ('Univ. of Oregon, Special Collections', 'https://blogs.uoregon.edu/scua/?p=9922'),
 'S29': ('Gruber: Ars magna lucis et umbrae', 'https://www.antiquariat-gruber.de/buch/105663-01'),
 'S30': ('Marx J.: Сіаньська стела', 'https://ulb.academia.edu/MARXJacques'),
 'S31': ('Keevak, The Story of a Stele (рецензія)', 'https://www.cuhk.edu.hk/ics/journal/articles/v49p465.pdf'),
 'S32': ('Mundus Subterraneus (Crouch Rare Books)', 'https://crouchrarebooks.com/browse/horrid-phantasms-and-apparitions-of-devils/?print=pdf'),
 'S33': ('G. Glazer Gallery', 'https://www.georgeglazer.com/archives/maps/archive-celestial/kirchertrio.html'),
 'S34': ('Grafton, He had fun (LRB)', 'https://www.lrb.co.uk/v35/n21/anthony-grafton/he-had-fun'),
 'S35': ('Stolzenberg, огляд (Bookshare)', 'https://www.bookshare.org/browse/book/1130542'),
 'S36': ('Catholic Encyclopedia: Athanasius Kircher', 'https://www.newadvent.org/cathen/08661a.htm'),
 'S37': ('Перелік праць (fulltable.com)', 'https://fulltable.com/ak/LAK01.html'),
 'S38': ('Latium (1669) (Wikipedia)', 'https://en.wikipedia.org/wiki/Latium_(1669)'),
 'S39': ('Obeliscus Pamphilius (Wikipedia)', 'https://en.wikipedia.org/wiki/Obeliscus_Pamphilius'),
}


# ===== v2.2: доповнення (S40–S47) =====
SOURCES.update({
 'S40': ('Kircherian Museum (Wikipedia)', 'https://en.wikipedia.org/wiki/Kircherian_Museum'),
 'S41': ('Polygraphia Nova (Wikipedia)', 'https://en.wikipedia.org/wiki/Polygraphia_Nova'),
 'S42': ('Athanasius Kircher and the Egyptian Oedipus (Univ. of Chicago, Fathom)', 'https://fathom.lib.uchicago.edu/1/777777122590/'),
 'S43': ('Opere di Kircher (BEWEB, Chiesa Cattolica Italiana)', 'https://www.beweb.chiesacattolica.it/UI/attachments/Opere di Kircher.pdf'),
 'S44': ('China Illustrata (Wikipedia)', 'https://en.wikipedia.org/wiki/China_Illustrata'),
 'S45': ('Musurgia Universalis (Wikipedia)', 'https://en.wikipedia.org/wiki/Musurgia_Universalis'),
 'S46': ('Ars Magna Lucis et Umbrae (Wikipedia)', 'https://en.wikipedia.org/wiki/Ars_Magna_Lucis_et_Umbrae'),
 'S47': ('Mundus Subterraneus (Wikipedia)', 'https://en.wikipedia.org/wiki/Mundus_Subterraneus'),
})

def _w(i): return next(w for w in WORKS if w['id'] == i)
def _more(i, text, src, claims=()):
    w = _w(i); w['sum'] = w['sum'].rstrip() + ' ' + text
    w['src'] = list(w['src']) + [s for s in src if s not in w['src']]
    w['claims'] = list(w['claims']) + [c for c in claims if c not in w['claims']]

_more('musurgia', 'Рим, друкар Гріньяні; присвячена ерцгерцогу Леопольду Вільгельму; два томи, 1112 с., десять книг (від фізіології слуху й звуків тварин — до «мусаритмічного» методу складання музики з лічильною машиною, дії консонансу й дисонансу та гармонії сфер). Давній опис вчення про афекти. Наклад близько 1500 прим.; 1656 р. два десятки примірників вивезено до Китаю; друге видання — Амстердам, 1662.', ['S45'])
_more('lucis', 'Рим, Гріньяні; присвячена Фердинанду IV, королю римлян; десять розділів (за десятьма струнами псалмового інструмента й сефірот), 34 гравюри, фронтиспис П’єра Міотта; великий сонячний годинник у формі оливи, тіні шпильок якого складають «IHS». Друге видання — Амстердам, Янссон, 1671, з описом «чарівного ліхтаря»; зображення Сатурна з двома супутниками не виправлено. Вважати Кірхера винахідником ліхтаря хибно: на його малюнку дзеркало зміщене, а слайд стоїть перед тубусом лінзи.', ['S46'])
_more('polygraphia', 'За словами Кірхера, імператор Фердинанд III замовив універсальну мову письма; девіз «Omnia in uno sunt». Три частини: зведення мов до однієї (римські цифри — значення, арабські — граматична функція), перетворення літер у латинські слова (за Тритеміусом) і «arca steganographica» — скриня зі 144 пласкими стрижнями, що працюють як логарифмічні лінійки. Книгу дарували обраним правителям; жодного відомого застосування, крім листа Карамуеля, серпень 1663.', ['S41'])
_more('china', 'Амстердам, 1667: два майже тотожні видання (під маркою Якоба ван Мурса та від звичного видавця Кірхера). Перша частина тлумачить Сіаньську стелу VIII ст.; письмо Кірхер виводив із єгипетських ієрогліфів; джерела — Річчі, Мартіні, Шалль, Грюбер, Рот; рослини й тварини — за «Flora Sinensis» Бойма. Деякі зображення вигадані («Гора Дракона й Тигра»). Лейбніц вважав книгу розвагою, а не ґрунтовною наукою. Переклади: нідерландський 1668, англійський Огілбі 1669 і 1673, французький 1670.', ['S44'])
_more('mundus', 'За S47: посібник із географії Землі з розкішними ілюстраціями; Кірхер ним розвиває раціоналістичну лінію — природні закони замість чудес (пов’язано з «Diatribe de prodigiosis crucibus»).', ['S47'])
_more('lingua', 'Повний коптсько-арабський переклад і виправлена коптська граматика.', ['S42'])
_more('prodromus', 'Вступ до коптської; теза: копт — нащадок давньоєгипетської, а отже ключ до ієрогліфів. Мельхіор Інхофер спершу назвав її «гідним початком».', ['S42'])
_more('magnes', 'Спирається на досліди в Колегіо Романо.', ['S42'])

WORKS += [
 dict(id='pantometrum', year=1660, end=None, ynote='', la='Pantometrum Kircherianum', uk='Пантометр Кірхера', field='method', k=None, conf='l',
      why='у зібраних джерелах лише назва й рік', sum='Лише назва й рік (S43); зміст у джерелах не описано.', claims=[], src=['S43']),
 dict(id='chine', year=1670, end=None, ynote='переклад чужою рукою', la='La Chine illustrée', uk='Китай, ілюстрований (французьке видання)', field='china', k=('YOU', 'EAST', 'WINTER'), conf='m',
      why='переклад для французького читача; публікація', sum='Переклад «China Illustrata» Франсуа Савіньєна д’Алькіє (Амстердам): додано розмову Фердінандо II Медичі з Грюбером і китайсько-французький словник.', claims=[], src=['S44']),
]

EVENTS += [
 dict(id='ferdinand3', year=1640, label='Інтерес Фердинанда III', place='Відень', lat=48.21, lon=16.37, kind='life', text='Імператор Фердинанд III починає серйозно цікавитись розвідками Кірхера (за S42); пізніше він замовляє універсальну мову, що стане «Polygraphia Nova».', src=['S42', 'S41']),
 dict(id='urban', year=1644, label='Смерть Урбана VIII', place='Рим', lat=41.90, lon=12.45, kind='life', text='Помирає Урбан VIII, родина Барберіні йде у вигнання; Кірхер заздалегідь забезпечив союз із новим папою Інокентієм X (S42).', src=['S42']),
 dict(id='inchofer', year=1645, label='Сатира Інхофера', place='', lat=None, lon=None, kind='reception', text='Мельхіор Інхофер, який раніше хвалив «Prodromus Coptus» як «гідний початок», друкує сатиру «Monarchia Solipsorum» на Кірхера (S42; рік подано за цим джерелом).', src=['S42']),
 dict(id='arca1659', year=1659, label='Перша «arca» Медічі', place='Флоренція', lat=43.77, lon=11.26, kind='network', text='Першу «arca steganographica» отримує Фердінандо II Медічі; 1661 р. скриня для ерцгерцога Карла Йосифа містить помилки, що, ймовірно, спонукали до друкованого видання (S41).', src=['S41']),
 dict(id='musurgia_china', year=1656, label='Музургія їде до Китаю', place='', lat=None, lon=None, kind='network', text='Близько двох десятків примірників «Musurgia Universalis» вивезено до Китаю з єзуїтами (S45).', src=['S45']),
 dict(id='caramuel', year=1663, label='Лист Карамуеля', place='', lat=None, lon=None, kind='reception', text='Єдине відоме застосування «Polygraphia Nova» — лист Хуана Карамуеля-і-Лобковіца, серпень 1663 (S41); використання для запропонованих Кірхером перекладів невідоме.', src=['S41']),
 dict(id='china_tr', year=1668, end=1673, label='Переклади «China Illustrata»', place='Амстердам; Лондон', lat=52.37, lon=4.90, kind='reception', text='Нідерландський 1668, англійські 1669 і 1673 (Огілбі, скорочені), французький 1670; книга сформувала західне уявлення про Китай на два століття (S44).', src=['S44']),
 dict(id='sepibus78', year=1678, label='Каталог де Сепібуса', place='Рим', lat=41.90, lon=12.48, kind='reception', text='Джорджо де Сепібус видає перший каталог музею; його таблиці — єдине свідчення розташування збірки (S40).', src=['S40']),
 dict(id='pio', year=1773, label='Ліквідація єзуїтів', place='Рим', lat=41.90, lon=12.45, kind='reception', text='Після розпуску ордену частину знахідок передано музею Піо-Клементіно у Ватикані (S40).', src=['S40']),
 dict(id='pigorini', year=1881, end=1913, label='Державний музей Пігоріні', place='Рим', lat=41.90, lon=12.48, kind='reception', text='Колегіо Романо повертається єзуїтам 1824 р.; 1881 р. під керівництвом Луїджі Пігоріні музей стає державним (S40).', src=['S40']),
 dict(id='dissolution', year=1916, label='Розпорошення збірки', place='Рим', lat=None, lon=None, kind='reception', text='Музей розформовано: етруські старожитності — Національний етруський музей, римські — Національний римський, середньовічні — Кастель Сант-Анджело; частина, зокрема дерев’яні моделі обелісків, лишилась у коледжі. 2001 р. — виставка в Палаццо Венеція (S40).', src=['S40']),
]

# уточнення дат: S42 називає 1635 р. прибуттям до Рима
for _e in EVENTS:
    if _e['id'] == 'collegio':
        _e['note'] = (_e.get('note') + '; ' if _e.get('note') else '') + 'S42: 1635'

CLAIMS += [
 dict(id='C25', text='Кірхер винайшов еолову арфу', t=0, f=0, pro='', con='Сам заявляв про винахід у кн. 10 «Musurgia» (S45); незалежна перевірка не зібрана.', src=['S45']),
 dict(id='C26', text='«Polygraphia Nova» застосовували для запропонованих Кірхером перекладів', t=0, f=1, pro='', con='Відомий єдиний слід використання — лист Карамуеля 1663 р.; перекладів ніхто не робив (S41).', src=['S41']),
 dict(id='C27', text='«Mensa Isiaca» (Ісіда-таблиця) — давньоєгипетська пам’ятка, на якій можна читати ієрогліфи', t=0, f=1, pro='', con='Пізніше показано, що це римська декоративна робота з вигаданими ієрогліфами (S42).', src=['S42']),
 dict(id='C28', text='Критики XVII ст. сприймали Кірхера лише з глузуванням', t=1, f=1, pro='Декарт і Інхофер насміхалися (S34, S42).', con='Інхофер спершу хвалив «Prodromus»; Стольценберг: критики поділяли з ним передумови (S35).', src=['S34', 'S42', 'S35']),
 dict(id='C29', text='Збірка музею Кірхера збереглася у первісному вигляді', t=0, f=1, pro='', con='Каталог 1709 р. показав, що багато об’єктів уже зникло; 1916 р. збірку розформовано (S40).', src=['S40']),
 dict(id='C30', text='«Musurgia Universalis» — перша музична енциклопедія', t=1, f=0, pro='Таку характеристику подає S45.', con='', src=['S45']),
]

for _i, _c in [('musurgia', ['C25', 'C30']), ('polygraphia', ['C26']), ('oedipus', ['C27']), ('musaeum', ['C29'])]:
    _w(_i)['claims'] = list(_w(_i)['claims']) + _c
PEOPLE += [
 dict(id='inchofer', name='Мельхіор Інхофер', role='critic', text='Єзуїт-цензор; спершу похвалив «Prodromus Coptus», 1645 р. видав сатиру «Monarchia Solipsorum» (S42).', works=['prodromus', 'lucis'], src=['S42']),
 dict(id='caramuel', name='Хуан Карамуель-і-Лобковіц', role='network', text='Автор єдиного відомого листа, написаного за допомогою «Polygraphia Nova» (серпень 1663).', works=['polygraphia'], src=['S41']),
 dict(id='leopold', name='Ерцгерцог Леопольд Вільгельм', role='patron', text='Адресат присвяти «Musurgia Universalis».', works=['musurgia'], src=['S45']),
 dict(id='ogilby', name='Джон Огілбі', role='publisher', text='Англійські переклади «China Illustrata» 1669 і 1673 (скорочені).', works=['china'], src=['S44']),
 dict(id='pigorini', name='Луїджі Пігоріні', role='successor', text='Директор, за якого 1881 р. музей Кірхера став державним.', works=['musaeum'], src=['S40']),
]

# Лексикон: терміни й поняття (лише те, що є в зібраних джерелах)
TERMS = [
 dict(id='omnia', term='Omnia in uno sunt', la='Omnia in uno sunt', text='«Усе єдине» — девіз «Polygraphia Nova»; відображає переконання Кірхера в основній єдності всього сущого.', works=['polygraphia'], src=['S41']),
 dict(id='arca', term='Arca steganographica', la='Arca steganographica', text='Скриня зі 144 пласких стрижнів, що правили за логарифмічні лінійки для шифрування й розшифрування. Першу отримав Фердінандо II Медічі 1659 р.', works=['polygraphia'], src=['S41']),
 dict(id='musarithmica', term='Мусаритмічний метод', la='Musarithmica', text='Метод складання музики за таблицями, описаний у книзі 8 «Musurgia», разом із лічильною машиною для його застосування.', works=['musurgia'], src=['S45']),
 dict(id='affekt', term='Вчення про афекти', la='Affektenlehre', text='Вплив музики на душу й тіло: за S45, «Musurgia» подає найдавніший виклад цього вчення; книга 9 розглядає дію консонансу й дисонансу, включно з тарантизмом.', works=['musurgia'], src=['S45']),
 dict(id='harp', term='Еолова арфа', la='Harpa Aeolia', text='Кірхер заявляв, що сам її винайшов (книга 10 «Musurgia»).', works=['musurgia'], src=['S45']),
 dict(id='hydro', term='Гідрофілакії', la='Hydrophylacia', text='Підземні водойми, що, за Кірхером, живлять ріки світу; одна з опорних ідей його геокосмосу.', works=['mundus'], src=['S42', 'S47']),
 dict(id='mensa', term='Ісіда-таблиця', la='Mensa Isiaca', text='Бронзова таблиця, яку Кірхер вивчав як єгипетську. Пізніше доведено: римська декоративна робота з вигаданими ієрогліфами.', works=['oedipus'], src=['S42']),
 dict(id='coptic', term='Коптська мова', la='Lingua Coptica', text='За Кірхером, нащадок давньоєгипетської, а отже ключ до ієрогліфів; цю тезу він виклав у «Prodromus Coptus» (1636) і розвинув у «Lingua Aegyptiaca restituta» (1643).', works=['prodromus', 'lingua'], src=['S42']),
 dict(id='lantern', term='Чарівний ліхтар', la='Laterna magica', text='Опис проєкції зображень є в «Ars Magna Lucis et Umbrae» (друге видання 1671 р.). Приписувати Кірхеру винахід хибно: ілюстрація має помилки, ймовірно, він не бачив пристрою в дії.', works=['lucis'], src=['S46']),
 dict(id='gnomon', term='Гномонічна космометрія', la='Cosmometria gnomonica', text='Вимірювання всесвіту світлом і тінню: тема «Ars Magna Lucis et Umbrae» і її попередниці «Primitiae gnomonicae catoptricae».', works=['lucis', 'primitiae'], src=['S46']),
 dict(id='stele', term='Сіаньська стела', la='Stela Sinica', text='Сино-сирійський пам’ятник VIII ст. у Сіані; Кірхер прочитав його як свідчення про ранню проповідь Євангелія в Китаї. Перша частина «China Illustrata».', works=['china'], src=['S44']),
 dict(id='museum_t', term='Музей Кірхера', la='Musaeum Kircherianum', text='Колекція в Колегіо Романо, що виросла з кабінету Альфонсо Доннини (1651); Кірхер додав природничі об’єкти, музичні інструменти, власні машини й етнографію з місій. Каталоги: де Сепібус 1678, Бонанні 1709.', works=['musaeum'], src=['S40']),
 dict(id='collegio_t', term='Колегіо Романо', la='Collegium Romanum', text='Єзуїтський коледж у Римі; за S42 збудований на руїнах храму Ісіди. Місце кафедри математики Кірхера й його музею.', works=[], src=['S42', 'S40']),
 dict(id='kabbala', term='Десять струн і сефірот', la='Decachordon', text='«Ars Magna Lucis et Umbrae» поділена на десять частин за десятьма струнами псалмового інструмента, пов’язаними з сефірот.', works=['lucis'], src=['S46']),
 dict(id='combin', term='Ars combinatoria', la='Ars magna sciendi', text='Універсальний метод пізнання, що розвиває Луллієву комбінаторику; 12 книг на дев’яти божественних атрибутах.', works=['sciendi'], src=['S3', 'S1']),
]

# ===== v2.3: повне покриття сітки (S48–S50) =====
SOURCES.update({
 'S48': ('Searching for Athanasius Kircher’s Brazilian collection (Roma Tre)', 'https://www.uniroma3.it/articoli/searching-for-athanasius-kirchers-brazilian-collection-159927/'),
 'S49': ('Arca Noë (Wikipedia)', 'https://en.wikipedia.org/wiki/Arca_No%C3%AB'),
 'S50': ('Kircher: Ocean Currents, Chilean Volcanos and the Subterranean Headwaters of the Amazon River (Raremaps)', 'https://raremaps.com/gallery/detail/99934'),
})
EVENTS.append(dict(id='brazil', year=1678, end=None, label='Бразильські предмети в музеї', place='Баїя', lat=-12.97, lon=-38.5, kind='network',
  text='Кірхер листувався з Валентином Станселем з єзуїтського коледжу в Баїї, який міг надсилати дарунки з Бразилії (за S48 — припущення, не підтверджена передача). Каталог 1678 р. згадує кілька предметів корінних бразильців; у музеї Пігоріні нині є невелика кількість артефактів можливого кірхерівського походження.', src=['S48', 'S40'],
  note='дату 1678 подано лише за каталогом; час надходження невідомий'))

# вторинні анотації праць: окремі компоненти змісту, що лежать в іншій клітині
K2 = {
 'mundus': [dict(k=('WE', 'WEST', 'AUTUMN'), why='карта Америки: течії, чилійські вулкани, «підземні» витоки Амазонки; джерела карти джерело не називає (S50)', src=['S50'], conf='l')],
 'arca':   [dict(k=('THEY', 'WEST', 'AUTUMN'), why='проблема тварин Нового Світу: походять від створінь Едему й пристосувались до клімату (S49); класифікація здебільшого за видами Старого світу', src=['S49'], conf='l')],
 'musaeum': [dict(k=('WE', 'WEST', 'SUMMER'), why='предмети з Бразилії в каталозі 1678 р.; листування зі Станселем (S48)', src=['S48'], conf='l')],
}
for _w_ in WORKS:
    _w_['k2'] = K2.get(_w_['id'], [])

# анотація подій: механічна, за місцем, видом дії й стадією (див. §3.3 специфікації); впевненість для всіх — низька
EVENT_K = {
 'birth': ('THEY', 'NORTH', 'SPRING'), 'fulda': ('THEY', 'NORTH', 'SPRING'), 'novitiate': ('WE', 'NORTH', 'SPRING'), 'cologne': ('ME', 'NORTH', 'SPRING'),
 'koblenz': ('YOU', 'NORTH', 'SPRING'), 'heiligenstadt': ('YOU', 'NORTH', 'SUMMER'), 'mainz': ('THEY', 'NORTH', 'SUMMER'), 'ordained': ('THEY', 'NORTH', 'AUTUMN'),
 'wurzburg': ('ME', 'NORTH', 'SUMMER'), 'china_wish': ('ME', 'EAST', 'SPRING'), 'avignon': ('WE', 'NORTH', 'SUMMER'), 'rome': ('YOU', 'NORTH', 'SUMMER'),
 'collegio': ('WE', 'NORTH', 'AUTUMN'), 'sicily': ('ME', 'SOUTH', 'SPRING'), 'malta': ('YOU', 'SOUTH', 'SUMMER'), 'vesuvius': ('ME', 'SOUTH', 'SUMMER'),
 'descartes': ('THEY', 'NORTH', 'WINTER'), 'pamphilj': ('YOU', 'SOUTH', 'WINTER'), 'museum': ('WE', 'NORTH', 'WINTER'), 'censor': ('THEY', 'NORTH', 'WINTER'),
 'plague': ('ME', 'SOUTH', 'AUTUMN'), 'mentorella': ('ME', 'NORTH', 'AUTUMN'), 'voynich': ('WE', 'NORTH', 'SUMMER'), 'death': ('THEY', 'NORTH', 'WINTER'),
 'bonanni': ('WE', 'NORTH', 'WINTER'), 'champollion': ('THEY', 'SOUTH', 'WINTER'), 'yersinia': ('YOU', 'SOUTH', 'AUTUMN'), 'ferdinand3': ('YOU', 'NORTH', 'SUMMER'),
 'urban': ('THEY', 'NORTH', 'AUTUMN'), 'inchofer': ('THEY', 'NORTH', 'AUTUMN'), 'arca1659': ('YOU', 'NORTH', 'AUTUMN'), 'musurgia_china': ('WE', 'EAST', 'WINTER'),
 'caramuel': ('YOU', 'NORTH', 'SPRING'), 'china_tr': ('YOU', 'EAST', 'WINTER'), 'sepibus78': ('WE', 'NORTH', 'AUTUMN'), 'pio': ('THEY', 'NORTH', 'AUTUMN'),
 'pigorini': ('YOU', 'NORTH', 'AUTUMN'), 'dissolution': ('THEY', 'NORTH', 'SPRING'), 'brazil': ('WE', 'WEST', 'SUMMER'),
}
for _e_ in EVENTS:
    _e_['k'] = EVENT_K.get(_e_['id'])
    _e_['code'] = code6(_e_['k']) if _e_['k'] else None

# ===== v2.4: розширення енциклопедії (S51–S57), модель джерел і перевірки =====
SOURCES.update({
 'S51': ('Phonurgia Nova (Wikipedia)', 'https://en.wikipedia.org/wiki/Phonurgia_Nova'),
 'S52': ('Turris Babel (Wikipedia)', 'https://en.wikipedia.org/wiki/Turris_Babel'),
 'S53': ('Voynich manuscript (Wikipedia)', 'https://en.wikipedia.org/wiki/Voynich_manuscript'),
 'S54': ('Athanasius Kircher’s Musical Ark (JSTOR Daily)', 'https://daily.jstor.org/athanasius-kirchers-musical-ark'),
 'S55': ('The first printed map of Atlantis (Crouch Rare Books)', 'https://crouchrarebooks.com/?p=99293'),
 'S56': ('Kircher Project: gallery contents (Stanford)', 'https://web.stanford.edu/group/kircher/gallery/contents.html'),
 'S57': ('Athanasius Kircher’s Ars Magna Sciendi Sive Combinatoria (1669) (Scranton)', 'https://sites.scranton.edu/library/?p=9955'),
})
ROLES['predecessor'] = 'Попередники й авторитети'

# Модель джерел: type (вид), tier (1 первинне, 2 академічне, 3 установа або довідник, 4 допоміжне), access (як прочитано)
STYPE = {'wiki': 'Вікіпедія', 'encyclopedia': 'енциклопедія', 'academic': 'академічне', 'institutional': 'бібліотека, музей, університет', 'essay': 'есей, огляд', 'dealer': 'торговельний листинг', 'popular': 'популярне', 'blog': 'блог'}
TIER = {1: 'первинне', 2: 'академічне', 3: 'установа або довідник', 4: 'допоміжне'}
_SM = {
 'S1': ('encyclopedia', 2), 'S2': ('encyclopedia', 3), 'S3': ('wiki', 4), 'S4': ('wiki', 4), 'S5': ('wiki', 4), 'S6': ('institutional', 3), 'S7': ('popular', 4),
 'S8': ('wiki', 4), 'S9': ('dealer', 4), 'S10': ('popular', 4), 'S11': ('blog', 4), 'S12': ('academic', 2), 'S13': ('dealer', 4), 'S14': ('dealer', 4),
 'S15': ('popular', 4), 'S16': ('wiki', 4), 'S17': ('institutional', 3), 'S18': ('essay', 3), 'S19': ('institutional', 3), 'S20': ('wiki', 4), 'S21': ('wiki', 4),
 'S22': ('institutional', 3), 'S23': ('institutional', 3), 'S24': ('wiki', 4), 'S25': ('institutional', 3), 'S26': ('institutional', 3), 'S27': ('dealer', 4),
 'S28': ('institutional', 3), 'S29': ('dealer', 4), 'S30': ('academic', 2), 'S31': ('academic', 2), 'S32': ('dealer', 4), 'S33': ('dealer', 4), 'S34': ('essay', 2),
 'S35': ('popular', 4), 'S36': ('encyclopedia', 3), 'S37': ('popular', 4), 'S38': ('wiki', 4), 'S39': ('wiki', 4), 'S40': ('wiki', 4), 'S41': ('wiki', 4),
 'S42': ('institutional', 3), 'S43': ('institutional', 3), 'S44': ('wiki', 4), 'S45': ('wiki', 4), 'S46': ('wiki', 4), 'S47': ('wiki', 4), 'S48': ('institutional', 3),
 'S49': ('wiki', 4), 'S50': ('dealer', 4), 'S51': ('wiki', 4), 'S52': ('wiki', 4), 'S53': ('wiki', 4), 'S54': ('popular', 3), 'S55': ('dealer', 4),
 'S56': ('institutional', 3), 'S57': ('institutional', 3),
}
_DUP = {'S41': 'S4', 'S46': 'S16', 'S57': 'S25'}
SMETA = {}
for _k in SOURCES:
    _ty, _ti = _SM[_k]
    SMETA[_k] = dict(type=_ty, tier=_ti, access=('summary' if int(_k[1:]) >= 36 else 'unspecified'), dup_of=_DUP.get(_k))

def _more2(i, text, src, claims=()):
    _more(i, text, src, claims)

_more('phonurgia', 'Кемптен, Рудольф Дрехер, 1673; присвячена Леопольду I. Книга 1 «Phonosophia anacamptica» — відлуння («sonus lucis simia est», звук подібний до світла) і труби для збирання й посилення звуку; книга 2 «Phonosophia nova» — вплив музики на розум, терапія, тарантизм. Перша книга, цілком присвячена акустиці; найдавніший опис еолової арфи; написана й для захисту пріоритету щодо мовної труби.', ['S51'], ['C32', 'C33'])
_more('turris', 'Амстердам, Ваесберге, 1679; присвячена Леопольду I; остання праця, видана за життя Кірхера, парна до «Arca Noë». Він доводив, що вежа Німрода не могла сягнути неба: Місяць лежить близько в 25 діаметрах Землі, а матеріалу не вистачило б. Мова Едему — «Lingua Humana», рання форма івриту. Ілюстрації Коненрата Декера за малюнком Лівена Крюйля; фронтиспіс Жерара де Ляресса.', ['S52'])
_more('arca', 'Три томи: події до потопу, потоп (з алегорією ковчега як людської душі), життя Ноя й розселення. Звірів Кірхер класифікував за розміром, гібридів (як-от жирафа) виключав. Понад сто гравюр; присвячена дванадцятирічному Карлові II Іспанському.', ['S49'])
_more('itinerarium', 'Діалог: ангел Космієл веде Теодидакта планетами. Єдина праця Кірхера цілком про астрономію; тихонівська система; цензори, дехто з яких вважав погляди «небезпечними для віри»; присвячена королеві Христині.', ['S8'])
_w('iter2')['ynote'] = ((_w('iter2').get('ynote') or '') + ('; ' if _w('iter2').get('ynote') else '') + '1657 (S43) чи 1660 (S8: німецьке видання Каспара Шотта)')
_more('sciendi', 'Амстердам, Янссон ван Ваесберге й вдова Елізея Ейєрстрата. Дванадцять книг; усе знання зведено до дев’яти атрибутів Бога; у виданні є волвела.', ['S57'])
_more('china', 'Галерея Stanford зараховує до цього розділу також ацтекський міф про заснування Мехіко й мексиканський храм (S56).', ['S56'])
_more('mundus', 'За S55: мапа Атлантиди; рішення нанести її Кірхер ухвалив 1664 р.', ['S55'], ['C34'])
_more('musurgia', 'Прилад «Arca musarithmica» — шафка з дощечками для складання чотириголосної церковної музики аматорами; один примірник належав Піпсу, інший — Фердинанду III (S54).', ['S54'])

for _c_ in CLAIMS:
    if _c_['id'] == 'C25':
        _c_['pro'] = 'Найдавніший відомий опис еолової арфи — у «Phonurgia nova» (S51).'; _c_['con'] = 'Винахідництво — його власна заява (S45); незалежного підтвердження не зібрано.'; _c_['src'] = list(_c_['src']) + ['S51']

CLAIMS += [
 dict(id='C31', text='Кірхер прочитав або прокоментував рукопис Войнича', t=0, f=0, pro='', con='Марці надіслав рукопис Кірхеру (1665/66); Кірхер, схоже, хотів його здобути, але його відповіді чи коментаря не зафіксовано (S53).', src=['S53']),
 dict(id='C32', text='«Phonurgia nova» — перша книга, цілком присвячена акустиці', t=1, f=0, pro='Так подає S51.', con='', src=['S51']),
 dict(id='C33', text='Кірхер першим винайшов мовну трубу (рупор)', t=1, f=1, pro='Кірхер стверджував, що багато років користувався «tuba stentorophonica» у Ментореллі (S51).', con='Семюел Морленд заявляв про той самий винахід; джерело спору не вирішує (S51).', src=['S51']),
 dict(id='C34', text='Мапа Атлантиди в «Mundus Subterraneus» — перша друкована мапа Атлантиди', t=1, f=0, pro='Так подає торговий листинг (S55); академічного підтвердження не зібрано.', con='', src=['S55']),
]

PEOPLE += [
 dict(id='morland', name='Семюел Морленд', role='critic', text='Англійський винахідник; заявив про винахід мовної труби, що спонукало Кірхера захищати пріоритет у «Phonurgia nova».', works=['phonurgia'], src=['S51']),
 dict(id='stansel', name='Валентин Станзель', role='network', text='Єзуїт у колегії в Баїї (Бразилія); листувався з Кірхером і міг надсилати дарунки з Бразилії (припущення, не підтверджена передача).', works=['musaeum'], src=['S48']),
 dict(id='christina', name='Королева Христина Шведська', role='patron', text='Адресатка присвяти «Itinerarium exstaticum».', works=['itinerarium'], src=['S8']),
 dict(id='leopold1', name='Імператор Леопольд I', role='patron', text='Адресат присвят «Phonurgia nova» і «Turris Babel».', works=['phonurgia', 'turris'], src=['S51', 'S52']),
 dict(id='charles2', name='Карл II Іспанський', role='patron', text='Дванадцятирічний адресат присвяти «Arca Noë»; присвята порівнює ковчег із його імперією.', works=['arca'], src=['S49']),
 dict(id='baresch', name='Георг Бареш', role='network', text='Празький алхімік, перший підтверджений власник рукопису Войнича; просив поради Кірхера, але відмовився віддати книгу.', works=[], src=['S53']),
 dict(id='pepys', name='Семюел Піпс', role='network', text='Власник одного з небагатьох збережених примірників «Arca musarithmica».', works=['musurgia'], src=['S54']),
 dict(id='decker', name='Коненрат Декер', role='collaborator', text='Гравер; ілюстрації «Arca Noë» (три найвідоміші) і «Turris Babel».', works=['arca', 'turris'], src=['S49', 'S52']),
 dict(id='lairesse', name='Жерар де Ляресс', role='collaborator', text='Автор фронтиспіса «Turris Babel».', works=['turris'], src=['S52']),
 dict(id='miotte', name='П’єр Міотт', role='collaborator', text='Автор фронтиспіса «Ars Magna Lucis et Umbrae».', works=['lucis'], src=['S46']),
 dict(id='lull', name='Раймон Луллій', role='predecessor', text='Тринадцятиторічний… [див. нижче]', works=['sciendi', 'musurgia'], src=['S57', 'S54']),
 dict(id='trithemius', name='Йоганн Тритеміус', role='predecessor', text='Його «Polygraphia» (1518) була відправною точкою Кірхерової «Polygraphia Nova».', works=['polygraphia'], src=['S41']),
 dict(id='mersenne', name='Марен Мерсенн', role='predecessor', text='Джерело органології «Musurgia»; пропонував перебирати всі перестановки «Ut–Re–Mi–Fa–Sol–La».', works=['musurgia'], src=['S45', 'S54']),
 dict(id='kepler', name='Йоганн Кеплер', role='predecessor', text='Кірхер виступав проти нього у «Magnes» (1641).', works=['magnes'], src=['S8']),
 dict(id='horapollo', name='Горапполон і Плутарх', role='predecessor', text='Джерела тлумачень ієрогліфів: пізня грецька праця й автор, що не знав єгипетської.', works=['oedipus'], src=['S42']),
 dict(id='tycho', name='Тіхо Браге', role='predecessor', text='Його геліо-геоцентрична система — космологія «Itinerarium exstaticum».', works=['itinerarium'], src=['S8']),
]
for _p in PEOPLE:
    if _p['id'] == 'lull':
        _p['text'] = 'Мальоркський філософ XIII ст.; Кірхерова «Ars Magna Sciendi» розширює його «комбінаторне мистецтво», а «Arca musarithmica» вдалась до луллівської ідеї.'

EVENTS += [
 dict(id='itin_ded', year=1656, end=None, label='Присвята Христині', place='', lat=None, lon=None, kind='life', text='«Itinerarium exstaticum» присвячено королеві Швеції Христині, яка невдовзі після виходу книги відвідала Ватикан (S8).', src=['S8']),
 dict(id='itin_cens', year=1656, end=None, label='Цензори про «Itinerarium»', place='', lat=None, lon=None, kind='reception', text='Рукопис розглядали цензори, Генерал дозволив друк; дехто вважав погляди «небезпечними для віри». Критика за відхід від арістотелівської космології; відповідь — видання 1660 р. зі Шоттом (S8).', src=['S8']),
 dict(id='atlantis1664', year=1664, end=None, label='Задум мапи Атлантиди', place='', lat=None, lon=None, kind='life', text='Кірхер вирішує нанести Атлантиду на мапу; мапа вийде в «Mundus Subterraneus» (Амстердам, 1665). За торговим листингом S55.', src=['S55']),
 dict(id='morland1673', year=1673, end=None, label='Спір про мовну трубу', place='', lat=None, lon=None, kind='life', text='Морленд заявив про винахід мовної труби; «Phonurgia nova» написана, зокрема, щоб захистити пріоритет Кірхера: він посилався на «tuba stentorophonica» з Ментореллі й на «Musurgia» (S51).', src=['S51']),
]
for _e in EVENTS:
    if _e['id'] == 'voynich':
        _e['text'] = _e['text'].rstrip('.') + '. За S53: Ян Марек Марці надіслав рукопис Кірхеру, вважаючи, що лише той зможе його прочитати; відповіді Кірхера не зафіксовано; з його збірки рукопис, імовірно, потрапив до бібліотеки Колегіо Романо; 1912 р. його придбав Вілфрід Войнич.'
        _e['src'] = list(_e['src']) + ['S53']
EVENT_K.update({'itin_ded': ('YOU', 'NORTH', 'WINTER'), 'itin_cens': ('THEY', 'NORTH', 'AUTUMN'), 'atlantis1664': ('ME', 'WEST', 'SPRING'), 'morland1673': ('ME', 'NORTH', 'WINTER')})
for _e in EVENTS:
    _e['k'] = EVENT_K.get(_e['id'])
    _e['code'] = code6(_e['k']) if _e['k'] else None
for _w_ in WORKS:
    if _w_['id'] == 'china':
        _w_['k2'] = [dict(k=('THEY', 'WEST', 'SUMMER'), why='ацтекський міф про заснування Мехіко й мексиканський храм серед ілюстрацій (S56); чужі повідомлення', src=['S56'], conf='l')]

TERMS += [
 dict(id='tuba', term='Мовна труба', la='Tuba stentorophonica', text='Рупор, яким, за Кірхером, він багато років скликав вірних на месу в святині св. Євстахія в Ментореллі; на нього він посилався, відстоюючи пріоритет проти Семюела Морленда.', works=['phonurgia'], src=['S51']),
 dict(id='echo', term='Фоносфія анакамптика', la='Phonosophia anacamptica', text='Перша книга «Phonurgia nova»: звук — хвилі, що відбиваються, як світло від дзеркала («sonus lucis simia est»: звук — наслідувач світла, буквально «мавпа»); опис труб для збирання й посилення звуку.', works=['phonurgia'], src=['S51']),
 dict(id='lingua_humana', term='Lingua Humana', la='Lingua Humana', text='Мова Едему, за Кірхером, — рання форма івриту, де слова відповідали речам. Після змішання мов нащадки Сима зберегли іврит, потомки його братів узяли грецьку, латину, тевтонську й слов’янську; ці п’ять розгалузились на сімдесят дві материнські мови.', works=['turris'], src=['S52']),
 dict(id='babel_t', term='Вавилонська вежа', la='Turris Babel', text='Кірхер доводив, що вежа Німрода не могла бути збудована: Місяць, найнижча сфера, лежить близько в 25 діаметрах Землі, а матеріалу не вистачило б; до того ж така вежа вивела б Землю з рівноваги.', works=['turris'], src=['S52']),
 dict(id='atlantis_t', term='Мапа Атлантиди', la='Atlantis in Mundus Subterraneus', text='Рішення нанести Атлантиду на мапу ухвалено 1664 р.; мапа в «Mundus Subterraneus» (1665). Земля — живе тіло, крізь яке тече вода, як крізь зябра риби; їй потрібен «скелет» — гірські пасма, зокрема підводні; Атлантида править за доказ. Джерело — торговий листинг.', works=['mundus'], src=['S55']),
 dict(id='ecstatic', term='Екстатична подорож', la='Itinerarium exstaticum', text='Уявна розмова: ангел Космієл веде Теодидакта («навченого Богом») планетами, коли той забувається під час священного концерту в єзуїтському коледжі. Єдина праця Кірхера цілком про астрономію. 1660 р. — перероблене німецьке видання «Iter Exstaticum» Каспара Шотта.', works=['itinerarium', 'iter2'], src=['S8']),
 dict(id='tycho_t', term='Система Тихо Браге', la='Systema Tychonicum', text='Земля в центрі, Сонце обертається навколо неї, інші планети — навколо Сонця. Кірхер вважав планети виконаними з тієї ж матерії, що Земля, і визнавав плями на Сонці; у «Magnes» (1641) виступив проти Кеплера.', works=['itinerarium', 'magnes'], src=['S8']),
 dict(id='voynich_t', term='Рукопис Войнича', la='Codex Voynich', text='Ян Марек Марці надіслав рукопис Кірхеру (лист 1665/66 р.); відповіді Кірхера не зафіксовано. З його збірки рукопис, імовірно, потрапив до бібліотеки Колегіо Романо; 1912 р. його придбав Вілфрід Войнич.', works=[], src=['S53']),
 dict(id='arca_mus', term='Arca musarithmica', la='Arca musarithmica', text='Прилад для алгоритмічного складання музики, схожий на мініатюрну комодну шафку: користувач обирав вірш і стиль, а з дерев’яних дощечок збиралась чотириголосна церковна музика. Збереглось кілька примірників, один належав Піпсу, інший Фердинанду III. Музику оцінюють як «безбарвну».', works=['musurgia'], src=['S54']),
 dict(id='volvelle', term='Волвела', la='Volvella', text='Обертове паперове коло з покажчиком; у «Ars Magna Sciendi» таке коло ілюструє Луллеву комбінаторику (S57 називає його раннім паперовим аналоговим комп’ютером). Rota combinatoria в атласі влаштована за тим самим принципом.', works=['sciendi'], src=['S57']),
 dict(id='nine', term='Дев’ять атрибутів Бога', la='Novem attributa', text='У «Ars Magna Sciendi» Кірхер логікою зводить усе знання до дев’яти атрибутів Бога, вважаючи їх взірцем усього створеного; метод подано як науковий шлях до істини для богослов’я, медицини, логіки.', works=['sciendi'], src=['S57']),
 dict(id='tarantella', term='Тарантизм і музичний антидот', la='Tarantismus', text='«Musurgia» (кн. 9) розглядає дію музики на душу й тіло, зокрема тарантизм; галерея Stanford має тарантелу з танцюючими тарантулами й музичний антидот до отрути.', works=['musurgia', 'phonurgia'], src=['S45', 'S56']),
 dict(id='cosmic_organ', term='Космічний орган', la='Organum cosmicum', text='Ілюстрація «Musurgia»: творіння — орган із шістьма регістрами, кожен відповідає одному дню творіння.', works=['musurgia'], src=['S45']),
 dict(id='sunflower', term='Соняшниковий годинник', la='Horologium helianthium', text='Магнітний пристрій з «Magnes» (1641). Поряд у галереї Stanford: прилад для вимірювання магнітного нахилу, магнітний анемоскоп з Мальти, «магнітний оракул», магнітна криптологічна машина. Устрій приладів джерело не описує.', works=['magnes'], src=['S56']),
 dict(id='dragon', term='Летючий дракон', la='Draco volans', text='Зображення літаючого дракона в «Physiologia Kircheriana Experimentalis» (Кестлер), с. 247.', works=['physiologia'], src=['S56']),
 dict(id='minerva', term='Обеліск Мінерви', la='Obeliscus Minervae', text='Проєкт Берніні для обеліска Мінерви й Кірхерів переклад його написів; також переміщення Ватиканського обеліска (за галереєю Stanford).', works=['obelisci'], src=['S56']),
 dict(id='aztec', term='Ацтекський міф у «China Illustrata»', la='Mexicanum', text='Галерея Stanford зараховує до розділу «Китай, Азія й Америка» ацтекський міф про заснування Мехіко й мексиканський храм; свідчення про «захід» у корпусі.', works=['china'], src=['S56']),
 dict(id='priority', term='Спір про пріоритет мовної труби', la='Tuba stentorophonica', text='Семюел Морленд заявив про винахід мовної труби; «Phonurgia nova» (1673) написана, зокрема, щоб захистити пріоритет Кірхера; він посилався на власну «tuba stentorophonica» й на «Musurgia».', works=['phonurgia'], src=['S51']),
]

def check():
    ids = [w['id'] for w in WORKS]
    assert len(ids) == len(set(ids))
    all_src = set(SOURCES)
    for w in WORKS:
        assert set(w['src']) <= all_src, w['id']
        for c in w['claims']:
            assert c in {x['id'] for x in CLAIMS}, (w['id'], c)
    for e in EVENTS:
        assert set(e['src']) <= all_src, e['id']
    for p in PEOPLE:
        assert set(p['src']) <= all_src, p['id']
        assert set(p['works']) <= set(ids), p['id']
        assert p['role'] in ROLES
    for c in CLAIMS:
        assert set(c['src']) <= all_src, c['id']
    for w in WORKS:
        assert w['field'] in FIELDS
        if w['k']:
            assert w['k'][0] in WHO and w['k'][1] in WHERE and w['k'][2] in WHEN
    # claim -> work back-references are present in the work records
    used = {c for w in WORKS for c in w['claims']}
    unused = {c['id'] for c in CLAIMS} - used
    return unused


def summary():
    unused = check()
    ann = [w for w in WORKS if w['k']]
    by_code = defaultdict(list)
    for w in ann:
        by_code[code6(w['k'])].append(w['id'])
    print('творів:', len(WORKS), '; анотовано:', len(ann), '; без анотації:', [w['id'] for w in WORKS if not w['k']])
    print('різних кодів:', len(by_code), '; колізій (код з >1 твору):', {c: v for c, v in sorted(by_code.items()) if len(v) > 1})
    print('WHERE:', dict(Counter(w['k'][1] for w in ann)))
    print('WHO:', dict(Counter(w['k'][0] for w in ann)))
    print('WHEN:', dict(Counter(w['k'][2] for w in ann)))
    print('conf:', dict(Counter(w['conf'] for w in ann)))
    print('події:', len(EVENTS), dict(Counter(e['kind'] for e in EVENTS)), '; з координатами:', sum(1 for e in EVENTS if e['lat'] is not None))
    print('люди:', len(PEOPLE), dict(Counter(p['role'] for p in PEOPLE)))
    cnt = Counter(BEL[(c['t'], c['f'])] for c in CLAIMS)
    print('твердження:', len(CLAIMS), dict(cnt))
    print('твердження без посилань з творів:', sorted(unused))
    print('джерел:', len(SOURCES))
    return by_code


def _cmeta(c):
    tiers = [SMETA[s]['tier'] for s in c['src']]
    types = sorted({SMETA[s]['type'] for s in c['src']})
    uniq = {SMETA[s].get('dup_of') or s for s in c['src']}
    return dict(n_src=len(uniq), best_tier=min(tiers), weak=all(x == 4 for x in tiers), only_dealer=all(SMETA[s]['type'] == 'dealer' for s in c['src']),
                src_types=types, ver='не звірено з першоджерелом', loc=c.get('loc') or {})


def export(path):
    out = dict(
        fields=FIELDS, roles=ROLES, stype=STYPE, tier=TIER, sources={k: dict(t=v[0], u=v[1], **SMETA[k]) for k, v in SOURCES.items()},
        works=[dict(w, code=(code6(w['k']) if w['k'] else None), k2=[dict(x, code=code6(x['k'])) for x in w['k2']]) for w in WORKS],
        events=EVENTS, people=PEOPLE, terms=TERMS,
        claims=[dict(c, b=BEL[(c['t'], c['f'])], **_cmeta(c)) for c in CLAIMS],
    )
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, separators=(',', ':'))
    return out


if __name__ == '__main__':
    summary()
    export('/home/claude/kircher/atlas_data.json')
