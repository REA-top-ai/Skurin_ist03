import database as db_mod
from sqlalchemy import text

def reset():
    db = next(db_mod.get_db())
    try:
        print("Очистка базы данных...")
        # Удаляем данные и сбрасываем счетчик ID
        db.execute(text("TRUNCATE TABLE users RESTART IDENTITY CASCADE;"))
        db.commit()
        print("Готово! Все пользователи удалены, ID сброшены к 1.")
    except Exception as e:
        print(f"Ошибка: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    reset()