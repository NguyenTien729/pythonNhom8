import mysql.connector
from datetime import datetime

class Database:
    def __init__(self):
        self.conn = mysql.connector.connect(  #thay đổi thành sql của bản thân
            host="localhost",      
            user="root",           
            password="max1236987",
            database="pythondb"    
        )
        self.cursor = self.conn.cursor()

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(255) UNIQUE,
                password VARCHAR(255),
                player_name VARCHAR(255)
            )
        """)

 
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS scores (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT,
                score INT,
                date_time DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        """)
        self.conn.commit()


    def login(self, username, password):
        self.cursor.execute(
            "SELECT id FROM users WHERE username=%s AND password=%s",
            (username, password)
        )
        result = self.cursor.fetchone()
        return result[0] if result else None


    def register_user(self, username, password):
        try:
            self.cursor.execute(
                "INSERT INTO users (username, password, player_name) VALUES (%s, %s, %s)",
                (username, password, "")
            )
            self.conn.commit()
            return True
        except mysql.connector.IntegrityError:
            return False

    def update_player_name(self, user_id, player_name):
        self.cursor.execute(
            "UPDATE users SET player_name=%s WHERE id=%s",
            (player_name, user_id)
        )
        self.conn.commit()

    def get_player_name(self, user_id):
        self.cursor.execute("SELECT player_name FROM users WHERE id=%s", (user_id,))
        result = self.cursor.fetchone()
        return result[0] if result else None

    def save_score(self, user_id, score):
        self.cursor.execute(
            "INSERT INTO scores (user_id, score, date_time) VALUES (%s, %s, %s)",
            (user_id, score, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        )
        self.conn.commit()

    def get_top_scores(self, limit=10):
        self.cursor.execute("""
            SELECT u.player_name, s.score, s.date_time
            FROM scores s
            JOIN users u ON s.user_id = u.id
            ORDER BY s.score DESC, s.date_time ASC
            LIMIT %s
        """, (limit,))
        return self.cursor.fetchall()

    def get_latest_score(self, user_id):
        self.cursor.execute("""
            SELECT u.player_name, s.score
            FROM scores s
            JOIN users u ON s.user_id = u.id
            WHERE s.user_id = %s
            ORDER BY s.date_time DESC
            LIMIT 1
        """, (user_id,))
        result = self.cursor.fetchone()  
        player_name, score = result
        if player_name is None:
            player_name = "Unknown"
        if score is None:
            score = 0

        return (str(player_name), int(score))