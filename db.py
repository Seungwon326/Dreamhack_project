import sqlite3

def init_db():
    conn = sqlite3.connect('webserver.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS accounts (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            username    TEXT UNIQUE NOT NULL,
            password    TEXT NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS posts (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            title       TEXT NOT NULL,
            content     TEXT NOT NULL,
            author      INTEGER NOT NULL,
            FOREIGN KEY (author) REFERENCES accounts(id)
        )
    ''')
    conn.commit()
    conn.close()


def add_account(username, password):
    conn = sqlite3.connect('webserver.db')
    cursor = conn.cursor()
    try:
        cursor.execute('INSERT INTO accounts (username, password) VALUES (?, ?)',
                       (username, password))
        conn.commit()
        conn.close()
        return True # success
    except sqlite3.IntegrityError:
        conn.close()
        return False # failure


def check_account(username, password):
    conn = sqlite3.connect('webserver.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM accounts WHERE username = ? AND password = ?',
                   (username, password))
    user = cursor.fetchone()
    conn.close()
    return user


def get_all_posts():
    conn = sqlite3.connect('webserver.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT posts.id, posts.title, accounts.username
        FROM posts JOIN accounts
        ON posts.author = accounts.id
    ''')
    posts = cursor.fetchall()
    conn.close()
    return posts


def create_post(title, content, author_id):
    conn = sqlite3.connect('webserver.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO posts (title, content, author) VALUES (?, ?, ?)',
                   (title, content, author_id))
    conn.commit()
    conn.close()


def get_post_by_post_id(post_id):
    conn = sqlite3.connect('webserver.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT posts.id, posts.title, posts.content, accounts.username
        FROM posts JOIN accounts
        ON posts.author = accounts.id
        WHERE posts.id = ?
    ''', (post_id))
    post = cursor.fetchone()
    conn.close()
    return post


def update_post(post_id, new_title, new_content):
    conn = sqlite3.connect('webserver.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE posts SET title = ?, content = ? WHERE id = ?',
        (new_title, new_content, post_id))
    conn.commit()
    conn.close()


def delete_post(post_id):
    conn = sqlite3.connect('webserver.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM posts WHERE id = ?', (post_id))
    conn.commit()
    conn.close()
