import os  # Импортируем стандартный модуль для работы с операционной системой (чтение ключей из .env)
import urllib.parse  # Импортируем утилиту для кодирования строк, чтобы безопасно передавать параметры в URL-адресах
import requests  # Импортируем библиотеку для отправки HTTP-запросов к внешним API (Steam, CheapShark)
import time  # Импортируем модуль для работы со временем (нужен для создания пауз между запросами)
from fastapi import FastAPI, Depends, HTTPException, Request  # Импортируем компоненты ядра веб-фреймворка FastAPI
from fastapi.responses import HTMLResponse, RedirectResponse  # Импортируем классы ответов сервера: HTML и перенаправление
from fastapi.templating import Jinja2Templates  # Импортируем движок Jinja2 для рендеринга и связывания HTML-страниц
from sqlalchemy.orm import Session  # Импортируем класс Session для работы с контекстом сессии базы данных SQLAlchemy
from sentence_transformers import SentenceTransformer, util  # Импортируем нейросеть и математические утилиты векторного анализа
from dotenv import load_dotenv  # Импортируем функцию для считывания переменных из конфигурационного файла .env
from passlib.context import CryptContext  # Импортируем инструмент для безопасного шифрования и проверки паролей
import database as db_mod  # Импортируем наш собственный файл базы данных database.py под псевдонимом db_mod

load_dotenv()  # Инициализируем загрузку всех переменных окружения из скрытого конфигурационного файла .env в систему
db_mod.init_db()  # Вызываем функцию создания таблиц (users) в PostgreSQL, если их еще нет в базе

app = FastAPI()  # Создаем главный экземпляр веб-приложения FastAPI, который будет обрабатывать все запросы
templates = Jinja2Templates(directory="templates")  # Указываем шаблонизатору, что все файлы веб-интерфейса лежат в папке templates
model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')  # Загружаем в ОЗУ мультиязычную нейросеть для поиска
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")  # Настраиваем контекст шифрования на надежный алгоритм PBKDF2

DOMAIN = "127.0.0.1:8000"  # Задаем глобальную константу с адресом и портом нашего сервера для локальной работы


def fix_layout(text: str):  # Объявляем функцию исправления раскладки клавиатуры, принимающую строку text
    en_chars = "qwertyuiop[]asdfghjkl;'zxcvbnm,./QWERTYUIOP{}ASDFGHJKL:\"ZXCVBNM<>?"  # Строка-карта английских символов
    ru_chars = "йцукенгшщзхъфывапролджэячсмитьбю.ЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮ,"  # Строка-карта русских символов (соответствие клавиш)
    trans_table = str.maketrans(en_chars, ru_chars)  # Создаем внутреннюю таблицу сопоставления (словарь замен букв)
    if not any('а' <= char <= 'я' for char in text.lower()):  # Проверяем, если в нижнем регистре строки нет ни одной русской буквы
        return text.translate(trans_table)  # Тогда конвертируем английские символы в аналогичные по клавишам русские
    return text  # Если в тексте изначально были русские буквы, возвращаем строку без изменений


class SteamService:  # Объявляем сервисный класс, группирующий статические методы работы со внешними игровыми API
    @staticmethod  # Декларируем, что метод является статическим (не требует создания экземпляра класса)
    def get_real_sales(page=0):  # Объявляем метод запроса распродаж с внешнего API CheapShark, принимающий номер страницы
        url = f"https://www.cheapshark.com/api/1.0/deals?storeID=1&pageSize=30&pageNumber={page}"  # Формируем ссылку запроса к CheapShark
        try:  # Открываем блок try для безопасной обработки сетевых исключений
            r = requests.get(url, timeout=5)  # Делаем синхронный GET-запрос со строгим лимитом ожидания ответа в 5 секунд
            return r.json() if r.status_code == 200 else []  # Если статус ответа 200 (ОК), возвращаем JSON-массив, иначе пустой список
        except:  # Перехватываем абсолютно любые ошибки (таймаут, падение сети, битый ответ)
            return []  # Возвращаем пустой список, чтобы сервер не падал из-за проблем на стороне CheapShark

    @staticmethod  # Декларируем статический метод
    def get_steam_price(appid: int, cc: str = "ru"):  # Метод получения официальной цены игры по её AppID и коду региона cc
        url = f"https://store.steampowered.com/api/appdetails?appids={appid}&cc={cc}&filters=price_overview"  # Формируем URL к магазину Steam
        try:  # Открываем блок перехвата ошибок для безопасного парсинга стороннего API
            r = requests.get(url, timeout=3)  # Делаем быстрый запрос к серверам Steam (таймаут ожидания — 3 секунды)
            data = r.json()  # Конвертируем полученный текстовый ответ в Python-словарь
            if data and str(appid) in data and data[str(appid)]['success']:  # Проверяем, успешен ли статус ответа Steam для этого AppID
                price_data = data[str(appid)]['data'].get('price_overview')  # Достаем блок данных с ценами и валютой
                return price_data.get('final_formatted') if price_data else None  # Если блок цен существует, берем форматированную строку цены
        except:  # Перехватываем любые сбои парсинга или сети
            pass  # Игнорируем ошибку, переходя к завершению функции
        return None  # Если данные не нашлись или произошел сбой, возвращаем значение "ничего" (None)

    @staticmethod  # Декларируем статический метод
    def get_library(steam_id: str):  # Метод получения списка AppID игр, которыми уже владеет конкретный пользователь Steam
        key = os.getenv("STEAM_API_KEY")  # Считываем из переменных системы секретный токен разработчика Steam API Key
        url = "http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/"  # Ссылка на официальный метод API IPlayerService
        params = {'key': key, 'steamid': steam_id, 'format': 'json'}  # Формируем словарь GET-параметров для запроса библиотеки
        try:  # Открываем блок try для обработки потенциальных ошибок сети
            r = requests.get(url, params=params, timeout=5)  # Отправляем запрос к Steam API с заготовленными параметрами на 5 секунд
            games = r.json().get('response', {}).get('games', [])  # Извлекаем вложенный список игр из JSON-структуры ответа
            return [g['appid'] for g in games]  # С помощью генератора списка вытаскиваем только чистые цифровые AppID игр
        except:  # Ловим любой сетевой сбой во время запроса
            return []  # Возвращаем пустой список, считая, что библиотека пуста или скрыта настройками приватности

    @staticmethod  # Декларируем статический метод
    def get_all_steam_games():  # Метод получения актуального среза популярных за 2 недели игр из API SteamSpy
        url = "https://steamspy.com/api.php?request=top100in2weeks"  # Ссылка на метод запроса топ-100 трендов в SteamSpy
        try:  # Защищаем код от падения в случае недоступности серверов SteamSpy
            r = requests.get(url, timeout=10)  # Запрашиваем данные популярных трендов, таймаут 10 секунд
            data = r.json()  # Превращаем сырой текстовый ответ в словарь объектов игр
            return [{"appid": v['appid'], "name": v['name']} for k, v in list(data.items())[:100]]  # Берем строго первые 40 записей
        except:  # Перехватываем ошибки таймаута или парсинга
            return []  # Возвращаем пустой список кандидатов в случае форс-мажора

    @staticmethod  # Декларируем статический метод
    def get_game_details(appid: int):  # Метод скачивания текстовых метаданных (жанры, описание) со страницы игры в Steam
        url = f"https://store.steampowered.com/api/appdetails?appids={appid}&l=russian"  # Ссылка на appdetails с явным русским языком (&l=russian)
        try:  # Защищаем цикл обхода игр от падения из-за некорректных AppID
            r = requests.get(url, timeout=5)  # Скачиваем данные конкретной игры из магазина, лимит 5 секунд
            data = r.json()  # Парсим полученный контент в словарь
            if data and str(appid) in data and data[str(appid)]['success']:  # Проверяем флаг успешности ответа от Steam Store
                info = data[str(appid)]['data']  # Переходим к внутреннему словарю с описанием полей игры
                genres = ", ".join([g['description'] for g in info.get('genres', [])])  # Собираем жанры игры в одну текстовую строку
                return f"Жанры: {genres}. Описание: {info.get('short_description', '')}"  # Формируем итоговую текстовую карточку игры
        except:  # Если произошла ошибка при чтении полей или запросе
            pass  # Пропускаем её, выполняя дефолтный возврат ниже
        return "Игра в Steam"  # Возвращаем базовую заглушку, если не удалось загрузить реальные жанры и описание


# --- Страницы (Рендеринг интерфейса сайта) ---
@app.get("/", response_class=HTMLResponse)  # Привязываем GET-запрос к корню сайта и указываем, что ответом будет чистый HTML
async def login_page(request: Request):  # Асинхронная функция для отображения стартового экрана авторизации
    return templates.TemplateResponse("index.html", {"request": request})  # Рендерим и отдаем клиенту страницу index.html


@app.get("/dashboard", response_class=HTMLResponse)  # Привязываем GET-запрос к роуту /dashboard (главное окно личного кабинета)
async def dashboard_page(request: Request):  # Асинхронная функция страницы личного кабинета
    return templates.TemplateResponse("dashboard.html", {"request": request})  # Рендерим и отдаем файл dashboard.html


@app.get("/search", response_class=HTMLResponse)  # Назначаем роут для страницы умного ИИ-поиска /search
async def search_page(request: Request):  # Асинхронная функция для инициализации интерфейса ИИ-поиска
    return templates.TemplateResponse("search.html", {"request": request})  # Рендерим и отдаем файл search.html


@app.get("/profile", response_class=HTMLResponse)  # Привязываем роут для страницы настроек и профиля пользователя /profile
async def profile_page(request: Request):  # Асинхронная функция отображения профиля
    return templates.TemplateResponse("profile.html", {"request": request})  # Рендерим и отдаем файл profile.html


# --- API Авторизации (Работа со встроенными аккаунтами) ---
@app.post("/api/register")  # Назначаем обработку POST-запросов отправки форм на адрес /api/register
async def register(username: str, password: str, db: Session = Depends(db_mod.get_db)):  # Функция регистрации с инъекцией сессии БД через Depends
    if db.query(db_mod.User).filter(db_mod.User.username == username).first():  # Ищем в базе пользователя с точно таким же именем (логином)
        raise HTTPException(status_code=400, detail="Имя уже занято.")  # Если совпадение найдено, прерываем запрос ошибкой 400 (Bad Request)
    new_user = db_mod.User(username=username, hashed_password=pwd_context.hash(password))  # Создаем объект модели User, шифруя пароль хэшем
    db.add(new_user)  # Добавляем созданный объект нового пользователя в черновик транзакции текущей сессии БД
    db.commit()  # Жестко фиксируем транзакцию, отправляя данные на постоянное хранение в PostgreSQL
    return {"status": "success"}  # Возвращаем JSON-статус успешного прохождения регистрации нового аккаунта


@app.post("/api/login")  # Назначаем обработку POST-запросов авторизации на адрес /api/login
async def login(username: str, password: str, db: Session = Depends(db_mod.get_db)):  # Функция входа, принимающая параметры формы и сессию БД
    user = db.query(db_mod.User).filter(db_mod.User.username == username).first()  # Ищем запись пользователя по введённому логину в базе данных
    if not user or not pwd_context.verify(password, user.hashed_password):  # Если юзер не найден или хэш введённого пароля не совпал с базой
        raise HTTPException(status_code=401, detail="Ошибка входа.")  # Выкидываем ошибку авторизации 401 (Unauthorized)
    res = RedirectResponse(url="/dashboard", status_code=303)  # Создаем объект перенаправления пользователя на дашборд (код 303 See Other)
    res.set_cookie("steam_user", user.username)  # Устанавливаем в браузер куку "steam_user" с именем вошедшего пользователя
    if user.steam_id: res.set_cookie("steam_id", user.steam_id)  # Если у профиля уже привязан Steam, сохраняем его ID в отдельную куку браузера
    return res  # Возвращаем ответ с редиректом и сохранёнными в браузере куками сессии


# --- Авторизация Steam (Механизм интеграции OpenID 2.0) ---
@app.get("/login-steam")  # Назначаем GET-роут для отправки пользователя на шлюз аутентификации Valve
async def login_steam():  # Функция генерации безопасной OpenID ссылки
    steam_openid_url = "https://steamcommunity.com/openid/login"  # Базовый адрес точки входа OpenID аутентификации сообщества Steam
    params = {  # Формируем словарь обязательных параметров по спецификации OpenID 2.0
        "openid.ns": "http://specs.openid.net/auth/2.0",  # Указываем пространство имен используемой версии протокола OpenID
        "openid.identity": "http://specs.openid.net/auth/2.0/identifier_select",  # Просим Steam автоматически выдать идентификатор сущности
        "openid.claimed_id": "http://specs.openid.net/auth/2.0/identifier_select",  # Указываем тип заявляемого идентификатора пользователя
        "openid.mode": "checkid_setup",  # Задаем режим идентификации с промежуточным экраном подтверждения на сайте Steam
        "openid.return_to": f"http://{DOMAIN}/auth/callback",  # Указываем точный обратный адрес на нашем сервере для возврата данных
        "openid.realm": f"http://{DOMAIN}"  # Задаем сферу доверия (корневой домен нашего сайта), чтобы Steam понимал, кто запрашивает вход
    }  # Завершаем сборку параметров для адресной строки
    return RedirectResponse(f"{steam_openid_url}?{urllib.parse.urlencode(params)}")  # Склеиваем URL, безопасно кодируем параметры и делаем редирект


@app.get("/auth/callback")  # Назначаем GET-роут обратного вызова /auth/callback, куда Steam возвращает пользователя с его ID
async def auth_callback(request: Request, db: Session = Depends(db_mod.get_db)):  # Функция обработки ответа Steam с сессией базы данных
    params = dict(request.query_params)  # Переводим параметры пришедшего от Steam GET-запроса в стандартный словарь Python
    claimed_id = params.get("openid.claimed_id", "")  # Вытаскиваем из параметров уникальную OpenID ссылку авторизовавшегося юзера
    steam_id = claimed_id.split("/")[-1]  # Распиливаем полученную ссылку по слэшам и забираем её финал — уникальный цифровой SteamID

    if not steam_id or not steam_id.isdigit():  # Если цифровой ID отсутствует или содержит невалидные символы (не число)
        return RedirectResponse(url="/")  # Сбрасываем операцию и экстренно перенаправляем пользователя на главную страницу входа

    current_username = request.cookies.get("steam_user")  # Проверяем, залогинен ли уже кто-то локально (имя из кук браузера)

    if current_username:  # Сценарий №1: Пользователь уже вошел под своим логином и просто привязывает Steam из профиля
        user = db.query(db_mod.User).filter(db_mod.User.username == current_username).first()  # Находим этого локального юзера в базе
        if user:  # Если запись пользователя успешно найдена в PostgreSQL
            user.steam_id = steam_id  # Записываем пришедший цифровой SteamID в поле этой учетной записи
            db.commit()  # Сохраняем внесенные изменения в базу данных насовсем
    else:  # Сценарий №2: Пользователь зашел на сайт «вслепую» и нажал сразу кнопку «Войти через Steam»
        user = db.query(db_mod.User).filter(db_mod.User.steam_id == steam_id).first()  # Проверяем, есть ли уже этот Steam ID у нас в базе
        if not user:  # Если пользователя с таким привязанным Steam ID у нас еще никогда не было (первый вход)
            user = db_mod.User(username=f"User_{steam_id[-5:]}", steam_id=steam_id)  # Создаем новый профиль с логином из последних 5 цифр ID
            db.add(user)  # Добавляем новую запись учетной записи в черновик сессии базы данных
            db.commit()  # Сохраняем транзакцию создания аккаунта в PostgreSQL
            db.refresh(user)  # Обновляем объект, чтобы синхронизировать его с автоматически созданным базой данных id

    response = RedirectResponse(url="/dashboard")  # Создаем объект финального редиректа авторизованного пользователя в личный кабинет
    response.set_cookie(key="steam_user", value=user.username)  # Обновляем или выставляем куку с логином вошедшего пользователя
    response.set_cookie(key="steam_id", value=user.steam_id)  # Обновляем или выставляем куку с привязанным верифицированным Steam ID
    return response  # Отправляем готовый ответ с редиректом и куками браузеру


@app.get("/logout")  # Назначаем GET-роут для выхода пользователя из системы по адресу /logout
async def logout():  # Функция очистки текущей пользовательской сессии в браузере
    res = RedirectResponse(url="/")  # Создаем объект перенаправления пользователя на главную страницу входа
    res.delete_cookie("steam_user")  # Стираем из браузера куку локального имени пользователя
    res.delete_cookie("steam_id")  # Стираем из браузера куку привязанного цифрового Steam ID
    return res  # Возвращаем ответ браузеру, который очистит сессию и перекинет на авторизацию


# --- API Данных (Логика рекомендаций и цен) ---
@app.get("/api/recommend")  # Назначаем GET-роут получения умных персональных рекомендаций со скидками /api/recommend
async def get_recommendations(request: Request, page: int = 0):  # Функция подбора игр, принимающая номер страницы пагинации распродаж
    steam_id = request.cookies.get("steam_id")  # Извлекаем цифровой Steam ID пользователя напрямую из кук его браузера
    if not steam_id:  # Если кука Steam ID пустая (пользователь локальный и не привязывал свой Steam аккаунт)
        return {"status": "locked", "message": "Подключите Steam."}  # Возвращаем заблокированный статус (фича недоступна)

    all_sales = SteamService.get_real_sales(page)  # Запрашиваем актуальный список 30 скидок с текущей страницы CheapShark API
    owned_set = set(SteamService.get_library(steam_id))  # Скачиваем библиотеку игр юзера из Steam API и переводим в быстрый поиск-множество (set)

    suggestions = []  # Инициализируем пустой список для накопления отфильтрованных персональных рекомендаций игр
    for s in all_sales[:12]:  # Запускаем цикл обхода первых 12 скидок, пришедших с зарубежной распродажи CheapShark
        appid = int(s.get('steamAppID', 0))  # Вытаскиваем AppID текущей игры из распродажи и принудительно приводим к числу
        if appid not in owned_set:  # УМНЫЙ ФИЛЬТР: Проверяем, если у пользователя в Steam еще нет этой игры в библиотеке
            s['real_rub_price'] = SteamService.get_steam_price(appid, "ru")  # Делаем точечный запрос к магазину за живой ценой в рублях (cc=ru)
            suggestions.append(s)  # Добавляем модифицированный объект скидки с рублевой ценой в итоговый массив рекомендаций

    return {"status": "success", "recommended": suggestions}  # Возвращаем JSON-ответ со списком подобранных и проверенных скидок


@app.get("/api/rates")  # Назначаем GET-роут /api/rates для получения актуальных валютных курсов валют
async def get_rates():  # Функция мониторинга и расчета конвертации валют проекта
    try:  # Открываем блок перехвата сетевых ошибок при работе со сторонним банковским API курсов
        r = requests.get("https://open.er-api.com/v6/latest/USD")  # Запрашиваем актуальную мировую сетку курсов относительно доллара (USD)
        return {"RUB": r.json()["rates"].get("RUB", 92.0), "KZT": r.json()["rates"].get("KZT", 445.0), "USD": 1.0}  # Отдаем курсы из JSON ответа
    except:  # Если банковский API лежит, упал таймаут или нет интернета
        return {"RUB": 92.0, "KZT": 445.0, "USD": 1.0}  # Возвращаем стабильные хардкод-значения курсов по умолчанию, чтобы интерфейс не ломался


# --- ЖИВОЙ ПОИСК ИИ (Семантический анализ промптов нейросетью) ---
@app.post("/ai-prompt-search")  # Назначаем обработку POST-запросов отправки поисковых промптов на адрес /ai-prompt-search
async def ai_search(prompt: str):  # Главная функция ИИ-поиска по естественному описанию, принимающая строку prompt
    fixed_prompt = fix_layout(prompt)  # Пропускаем входящий запрос через функцию автоматической корректировки раскладки
    print(f"\n[AI] Начинаем живой поиск: '{fixed_prompt}'")  # Выводим технический лог старта операции в терминал веб-сервера

    raw_games = SteamService.get_all_steam_games()  # Скачиваем "на лету" актуальный топ-40 популярных игр прямо из SteamSpy API

    if not raw_games:  # Проверка: если SteamSpy вернул пустоту (например, лег сервер или кончились лимиты запросов)
        print("[AI] Ошибка: Не удалось получить список игр.")  # Выводим лог ошибки в терминал бэкенда
        return {"results": []}  # Возвращаем безопасный пустой ответ на фронтенд, предотвращая зависание страницы сайта

    descriptions = []  # Инициализируем пустой список для текстов описаний, которые будет читать и анализировать нейросеть
    metadata = []  # Инициализируем пустой список для метаданных игр (оригинальные имена и их AppID), идущих строго параллельно описаниям

    print(f"[AI] Скачиваем описания для {len(raw_games)} игр...")  # Логируем в консоль этап обогащения данных из официального Steam Store
    for g in raw_games:  # Запускаем цикл обхода по каждой из 40 популярных игр, полученных ранее от SteamSpy
        time.sleep(0.1)  # МИКРО-ПАУЗА (100 мс) — критически важна, чтобы Steam Store API не забанил наш IP-адрес ошибкой 429 (Too Many Requests)
        details = SteamService.get_game_details(g['appid'])  # Скачиваем жанры и русское текстовое описание игры со страницы магазина Steam
        descriptions.append(f"Игра: {g['name']}. {details}")  # Склеиваем имя и детальное описание в один массив для анализа нейросетью
        metadata.append(g)  # Сохраняем исходный объект игры в массив метаданных под тем же порядковым индексом

    print("[AI] Запускаем нейросеть...")  # Логируем переход к этапу математического расчета семантического сходства
    try:  # Открываем блок try-except для перехвата исключений работы с тензорами нейросети SentenceTransformer
        prompt_emb = model.encode(fixed_prompt, convert_to_tensor=True)  # Переводим исправленный промпт пользователя в вектор-эмбеддинг (тензор PyTorch)
        desc_embs = model.encode(descriptions, convert_to_tensor=True)  # Переводим все 40 подготовленных описаний игр в матрицу векторов-эмбеддингов
        scores = util.cos_sim(prompt_emb, desc_embs)[0]  # Рассчитываем косинусное сходство (косинус угла в многомерном пространстве) между промптом и играми

        results = []  # Инициализируем пустой список для накопления финальных результатов, прошедших порог релевантности
        for i in range(len(metadata)):  # Запускаем цикл прохода по индексам всех обработанных игр
            score = scores[i].item()  # Извлекаем чистое дробное число (Float) коэффициента сходства из тензора PyTorch
            if score > 0.2:  # ПОРОГ ЧУВСТВИТЕЛЬНОСТИ ИИ: Оставляем игру, только если совпадение по смыслу с промптом выше 20%
                game = metadata[i]  # Достаем исходные метаданные игры (AppID и имя) по текущему индексу из массива
                results.append({  # Формируем итоговую карточку совпадения для фронтенда
                    "title": game['name'],  # Записываем оригинальное название игры
                    "steamAppID": game['appid'],  # Записываем цифровой AppID для генерации ссылок и картинок в HTML
                    "ai_score": round(score, 4)  # Округляем балл совпадения ИИ до 4 знаков после запятой для красоты
                })  # Завершаем добавление объекта совпадения в массив результатов

        print(f"[AI] Поиск завершен. Найдено совпадений: {len(results)}\n")  # Выводим лог итогов работы нейросети в терминал
        return {"results": sorted(results, key=lambda x: x['ai_score'], reverse=True)[:8]}  # Сортируем игры от максимального совпадения к меньшему и отдаем ТОП-8

    except Exception as e:  # Перехватываем любые аппаратные или программные ошибки расчетов нейросети (например, нехватка ОЗУ на Mac M2)
        print(f"[AI] ERROR: {e}")  # Выводим полный текст технической ошибки в терминал для отладки
        return {"results": []}  # Возвращаем пустой список результатов, гарантируя стабильность интерфейса пользователя