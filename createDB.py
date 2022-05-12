# SQLite 모듈을 사용하기 위한 선언
import sqlite3

# 'database.db' 데이터베이스에 SQLite DB 연결
conn = sqlite3.connect('database.db')
print('create & connect database')

conn.execute(
    '''
    create table users (email text, name text)
    ''')
print('create table')

conn.close()