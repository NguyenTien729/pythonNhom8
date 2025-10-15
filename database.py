import sqlite3
from datetime import datetime

class Database:
    def __init__(self):
        # Kết nối SQLite
        self.conn = sqlite3.connect("pythondb.db")
        self.cursor = self.conn.cursor()

        # --- Tạo bảng users ---
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE,
                password TEXT,
                player_name TEXT
            )
        """)

        # --- Tạo bảng scores ---
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS scores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                score INTEGER,
                date_time DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        """)

        self.conn.commit()

    # --- Đăng nhập ---
    def login(self, username, password):
        self.cursor.execute(
            "SELECT id FROM users WHERE username=? AND password=?",
            (username, password)
        )
        result = self.cursor.fetchone()
        return result[0] if result else None

    # --- Đăng ký ---
    def register_user(self, username, password):
        try:
            self.cursor.execute(
                "INSERT INTO users (username, password) VALUES (?, ?)",
                (username, password)
            )
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    # --- Cập nhật tên hiển thị ---
    def update_player_name(self, user_id, player_name):
        self.cursor.execute(
            "UPDATE users SET player_name=? WHERE id=?",
            (player_name, user_id)
        )
        self.conn.commit()

    # --- Lấy tên người chơi ---
    def get_player_name(self, user_id):
        self.cursor.execute("SELECT player_name FROM users WHERE id=?", (user_id,))
        result = self.cursor.fetchone()
        return result[0] if result else None

    # --- Lưu điểm ---
    def save_score(self, user_id, score):
        self.cursor.execute(
            "INSERT INTO scores (user_id, score, date_time) VALUES (?, ?, ?)",
            (user_id, score, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        )
        self.conn.commit()

    # --- Lấy top điểm cao ---
    def get_top_scores(self, limit=10):
        self.cursor.execute("""
            SELECT u.player_name, s.score, s.date_time
            FROM scores s
            JOIN users u ON s.user_id = u.id
            ORDER BY s.score DESC, s.date_time ASC
            LIMIT ?
        """, (limit,))
        return self.cursor.fetchall()
