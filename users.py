import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DB_PATH = "sqlite:///sochi_athletes.sqlite3"
Base = declarative_base()


class User(Base):    
    __tablename__ = 'user'    
    id = sa.Column(sa.Integer, primary_key=True, autoincrement="auto")    
    first_name = sa.Column(sa.Text)    
    last_name = sa.Column(sa.Text)    
    gender = sa.Column(sa.Text) 
    email = sa.Column(sa.Text)
    birthdate = sa.Column(sa.Text)
    height = sa.Column(sa.Float)

def connect_db():       
    engine = sa.create_engine(DB_PATH)
    Base.metadata.create_all(engine)
    session = sessionmaker(engine)
    return session()


def request_data():
    print("Регистрация нового пользователя")        
    first_name = input("Имя: ")
    last_name = input("Фамилия: ")
    gender = input("Пол (Male, Female): ")
    email = input("Адрес электронной почты: ")
    birthdate = input("Дата рождения (гггг-мм-дд): ")
    height = input("Рост м. (в формате *.**): ")
        
    user = User(        
        first_name=first_name,
        last_name=last_name,
        gender=gender,
        email=email,
        birthdate=birthdate,
        height=height
    )    
    return user

def main():
    session = connect_db()    
    mode = input("Добавить нового пользователя? 1-Да, 0-Нет: ")    

    while int(mode) == 1 :
        user = request_data()
        session.add(user)
        session.commit()
        print("Спасибо, данные сохранены!")
        mode = input("Добавить нового пользователя? 1-Да, 0-Нет: ")    
    print("Выход")
    
if __name__ == "__main__":
    main()