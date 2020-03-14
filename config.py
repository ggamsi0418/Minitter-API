db = {
    'user': 'root',
    'password': '01032645255',
    'host': 'localhost',
    'port': 3306,
    'database': 'minitter'
}

DB_URL = f"mysql+mysqlconnector://{db['user']}:{db['password']}@{db['host']}:{db['port']}/{db['database']}?charset=utf8"
