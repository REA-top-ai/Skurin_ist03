from database import SessionLocal, engine, Base
from models import Author, Post, Comment
from crud import *
from datetime import datetime


def main():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    session = SessionLocal()

    try:
        print("Начинаем тестирование...\n")

        print("Создаём авторов...")
        author1 = create_author(session, "Анна Петрова", "anna@example.com")
        author2 = create_author(session, "Иван Сидоров", "ivan@example.com")
        print(f"{author1.name} (id={author1.id})\n")
        print(f"{author2.name} (id={author2.id})\n")

        # 2. Создаём посты для Анны
        print("Создаём посты...")
        post1 = create_post(session, "Первый пост", "Это содержание первого поста. Оно достаточно длинное.", author1.id,published=True)
        post2 = create_post(session, "Черновик", "Этот пост пока не опубликован.", author1.id, published=False)
        post3 = create_post(session, "Пост Ивана", "Текст от Ивана.", author2.id, published=True)
        print(f"'{post1.title}' (опубликован)")
        print(f"'{post2.title}' (черновик)")
        print(f"'{post3.title}' (опубликован)\n")

        print("Добавляем комментарии...")
        add_comment(session, post1.id, "Читатель1", "Отличная статья, очень полезно!")
        add_comment(session, post1.id, "Читатель2", "Спасибо за материал, жду продолжения.")
        add_comment(session, post1.id, "Аноним", "Коротко.")  # Этот комментарий тоже учтётся
        print("3 комментария добавлены к первому посту\n")

        print("Публикуем черновик...")
        success = update_post_status(session, post2.id, published=True)
        if success:
            print(f"'{post2.title}' теперь опубликован\n")

        print("Все опубликованные посты:")
        published = get_published_posts(session)
        for post in published:
            print(f"'{post.title}' — автор: {post.author.name}")
        print()

        print("Топ авторов по количеству постов:")
        top_authors = get_top_authors_by_posts(session, limit=3)
        for rank, (name, count) in enumerate(top_authors, 1):
            print(f"{rank}. {name}: {count} пост(ов)")
        print()

        print("Поиск автора по email...")
        found = get_author_by_email(session, "anna@example.com")
        if found:
            print(f"Найдено: {found.name}")
        else:
            print("Автор не найден")


#САМОСТОЯТЕЛЬНАЯ РАБОТА


        by_name = get_author_by_name(session, "Иван Сидоров")
        if by_name:
            print(f"{by_name.name} ({by_name.email})\n")

        #Выводит все посты за сегодняшнюю дату
        today_posts = get_published_posts_by_date(session, datetime.utcnow().date())
        for post in today_posts:
            print(f"'Посты за сегодня: {post.title}' - автор: {post.author.name}")

        #Сразу несколько авторов
        new_authors = create_authors(session, [
            ("Захар Большаков", "zakharpidor@example.com"),
            ("Федор Даняев", "fedor2010@example.com")])
        for a in new_authors:
            print(f"{a.name} (id={a.id})")

        #Пост с комментариями
        post_full = get_post_with_comments(session, post1.id)
        if post_full:
            print(f"'{post_full.title}' - комментариев: {len(post_full.comments)}")
            for c in post_full.comments:
                print(f"  - {c.author_name}: {c.text}")
        print()

    except Exception as e:
        print(f"Ошибка: {e}")
        session.rollback()

if __name__ == "__main__":
    main()