import time
import datetime

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

class Athelete(Base):    
    __tablename__ = 'athelete'    
    id = sa.Column(sa.Integer, primary_key=True, autoincrement="auto")    
    age = sa.Column(sa.Integer)
    birthdate = sa.Column(sa.Text)
    gender = sa.Column(sa.Text) 
    height = sa.Column(sa.Float)
    name = sa.Column(sa.Text)    
    weight = sa.Column(sa.Integer)
    gold_medals = sa.Column(sa.Integer)
    silver_medals = sa.Column(sa.Integer)
    bronze_medals = sa.Column(sa.Integer)
    total_medals = sa.Column(sa.Integer)
    sport = sa.Column(sa.Text)    
    country = sa.Column(sa.Text)        
    
def connect_db():
    engine = sa.create_engine(DB_PATH)
    Base.metadata.create_all(engine)
    session = sessionmaker(engine)
    return session()

def find_id(id, session):
    query = session.query(User).filter(User.id == id)    
    if query.count() > 0 : return True
    else : return False 

def find_ath_height(query_athlete, min_diff_height, user_height):
    for athlete in query_athlete:
        try: 
            if abs(user_height - athlete.height) < min_diff_height :
                min_diff_height = abs(user_height - athlete.height)
                ath = athlete                
        except: pass
    return ath

def find_ath_birth(query_athlete, min_diff_birthdate, user_timestamp):
    for athlete in query_athlete:
        try:
            athlete_birthdate = athlete.birthdate
            athlete_date_time = datetime.datetime.fromisoformat(athlete_birthdate)
            athlete_timestamp = athlete_date_time.timestamp()
            if abs(user_timestamp - athlete_timestamp) < min_diff_birthdate :
                min_diff_birthdate = abs(user_timestamp - athlete_timestamp)
                ath = athlete                
        except: pass   
    return ath

def main():
    
    session = connect_db()
    
    user_id = input("Введите id пользователя: ")
    if not find_id(user_id, session) :        
        print("Нет такого пользователя!")
    else :
        query_user = session.query(User).filter(User.id == user_id)        
        for user in query_user:
            user_birthdate = user.birthdate
            user_height =  user.height
        print("Дата рождения пользователя: ", user_birthdate)
        print("Рост пользователя: ", user_height)
        
        user_date_time = datetime.datetime.fromisoformat(user_birthdate)
        user_timestamp = user_date_time.timestamp()        
                    
        query_athlete = session.query(Athelete).all()        
        print("Всего атлетов: ",len(query_athlete))

        min_diff_height = 1000
        min_diff_birthdate = 1000000000

        athlete_height = find_ath_height(query_athlete, min_diff_height, user_height)        
        athlete_birthdate = find_ath_birth(query_athlete, min_diff_birthdate, user_timestamp)
        
        print("Ближайший атлет по дате рождения: id - {}, Имя - {}, д.р. - {} ".format(athlete_birthdate.id, athlete_birthdate.name, athlete_birthdate.birthdate))
        print("Ближайший атлет по росту: id - {}, Имя - {}, рост - {} ".format(athlete_height.id, athlete_height.name, athlete_height.height))
        
if __name__ == "__main__":
    main()