#!/usr/bin/env python3

__author__ = 'golim'

from flask import Flask, render_template, send_file, request, redirect, url_for, session, flash, jsonify
from waitress import serve

import urllib.parse
import subprocess
import sqlite3
import logging
import random
import os

if 'FLAG' in os.environ:
    FLAG = os.environ['FLAG']
else:
    FLAG = 'UniTN{placeholder_flag}'

app = Flask(__name__)

app.secret_key = 'youshouldnotbeabletoreadthisotherwiseitsaproblemohoh'

DATABASE = 'database.db'
CARD_TYPES = ['bastoni', 'coppe', 'denari', 'spade']

logging.basicConfig(level=logging.DEBUG)

logger = logging.getLogger('main')
logger.setLevel(logging.DEBUG)

DENYLISTED_KEYWORDS = [
    'wget',
    'curl',
    'dig',
    'bash',
    'python',
    'ping',
    'nc',
    'netcat',
    'ssh',
    'scp',
    'sftp',
    'ftp',
    'telnet',
    'rm',
    'mv',
]

FORBIDDEN_CHARACTERS = [
    '`', '$(',
]

DO_NOT_EVEN_TRY = [
    'rm', 'mv', 'database', 'data', '.db'
]

def invalid(string):
    '''
    Prevent command injection vulnerabilities by checking if the string contains any denylisted keywords.
    '''
    if any(keyword in string for keyword in DENYLISTED_KEYWORDS):
        return True, 'Dnylisted Keyword Detected'
    if any(character in string for character in FORBIDDEN_CHARACTERS):
        return True, 'Forbidden Character Detected'
    if any(keyword in string for keyword in DO_NOT_EVEN_TRY):
        return True, 'What you are trying to do is most likely against the rules, remember that we log everything.'
    return False, 'Ok'

def sanitize(filename):
    return filename.replace('../', '')

def create_database():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT,
            played_games INTEGER DEFAULT 0
        )
    ''')
    conn.commit()
    conn.close()

def populate_database():  
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    # Add the admin user if it does not exist
    cursor.execute('''
        SELECT * FROM users WHERE username = 'admin'
    ''')
    admin = cursor.fetchone()

    if not admin:
        cursor.execute('''
            INSERT INTO users (username, password, played_games) VALUES
            ('admin', 'MegaComplicatedPasswordThatWeHadToChange!', 666)
        ''')
        conn.commit()
    conn.commit()
    conn.close()

# Create the database
create_database()

# Populate the database
populate_database()

@app.route('/robots.txt')
def robots():
    return "Bisca players are not robots! :D"

@app.route('/rules')
def rules():
    if 'user_id' in session:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE id = ?', (session['user_id'],))
        user = cursor.fetchone()
        if not user:
            # User does not exist
            session.clear()
            return redirect(url_for('login'))
        conn.close()

        session['username'] = user[1]

        return render_template('rules.html', username=session['username'])
    else:
        return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = password

        # Check if the username is already taken
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        existing_user = cursor.fetchone()

        if existing_user:
            flash('Username is already taken. Please choose another.', category='error')
        else:
            # Add the new user to the database
            cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, hashed_password))
            conn.commit()
            flash('Registration successful. You can now log in.', category='success')
            conn.close()
            return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if the username exists
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        user = cursor.fetchone()

        if user and user[2] == password:
            # Login successful, set session variables
            session['user_id'] = user[0]
            session['username'] = user[1]
            conn.close()
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password. Please try again.', category='error')

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/')
def index():
    if 'user_id' in session:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE id = ?', (session['user_id'],))
        user = cursor.fetchone()
        if not user:
            # User does not exist
            session.clear()
            print('User does not exist', flush=True)
            return redirect(url_for('login'))
        conn.close()

        # If admin, redirect to the admin page
        if user[1] == 'admin':
            return redirect(url_for('admin'))

        session['username'] = user[1]

        # Select the 5 cards
        your_cards = []
        for _ in range(5):
            card_type = random.choice(CARD_TYPES)
            card_number = random.randint(1, 10)
            while f'{card_type}/{card_number}.png' in your_cards: # No duplicates
                card_type = random.choice(CARD_TYPES)
                card_number = random.randint(1, 10)
            your_cards.append(f'{card_type}/{card_number}.png')

        opponent_cards = []
        for _ in range(5):
            card_type = random.choice(CARD_TYPES)
            card_number = random.randint(1, 10)
            while f'{card_type}/{card_number}.png' in your_cards: # No cards in common
                card_type = random.choice(CARD_TYPES)
                card_number = random.randint(1, 10)
            opponent_cards.append(f'{card_type}/{card_number}.png')

        turns = []
        for i in range(5):
            your_card = your_cards[i]
            opponent_card = opponent_cards[i]

            your_card_type = your_card.split('/')[0]
            your_card_number = int(your_card.split('/')[1].split('.')[0])

            opponent_card_type = opponent_card.split('/')[0]
            opponent_card_number = int(opponent_card.split('/')[1].split('.')[0])

            if your_card_type == opponent_card_type:
                if your_card_number > opponent_card_number:
                    turns.append(0)
                else:
                    turns.append(1)
            else:
                if your_card_type == 'denari':
                    turns.append(0)
                elif opponent_card_type == 'denari':
                    turns.append(1)
                elif your_card_type == 'coppe':
                    turns.append(0)
                elif opponent_card_type == 'coppe':
                    turns.append(1)
                elif your_card_type == 'spade':
                    turns.append(0)
                elif opponent_card_type == 'spade':
                    turns.append(1)
                elif your_card_type == 'bastoni':
                    turns.append(0)
                elif opponent_card_type == 'bastoni':
                    turns.append(1)

        return render_template('index.html', username=session['username'], cards=your_cards, opponent=opponent_cards, turns=turns, played_games=user[3])
    else:
        return redirect(url_for('login'))


@app.route('/image/')
def image():
    filename = request.args.get('filename', '')

    while '%' in filename:
        filename = urllib.parse.unquote(filename)

    filename = sanitize(filename)

    filename = 'images/' + filename

    return send_file(filename, mimetype='image/png')


@app.route('/admin')
def admin():
    if 'user_id' in session:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE id = ?', (session['user_id'],))
        user = cursor.fetchone()
        if not user:
            # User does not exist
            session.clear()
            return redirect(url_for('login'))
        conn.close()

        session['username'] = user[1]

        if user[1] == 'admin':
            conn = sqlite3.connect(DATABASE)
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM users')
            users = cursor.fetchall()
            conn.close()

            usernames = [user[1] for user in users]

            return render_template('admin.html', usernames=usernames, played_games='some', username=session['username'])
        else:
            return redirect(url_for('index'))
    else:
        return redirect(url_for('login'))

@app.route('/send-mail', methods=['POST'])
def send_mail():
    if 'user_id' in session:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE id = ?', (session['user_id'],))
        user = cursor.fetchone()
        if not user:
            # User does not exist
            session.clear()
            return redirect(url_for('login'))
        conn.close()

        session['username'] = user[1]

        # Send the email
        to = request.form['to']
        subject = request.form['subject']
        message = request.form['message']

        # Check that "to" is a valid email address
        if '@' not in to:
            flash(f'{to} is not a valid email address.', category='error')
            return redirect(url_for('index'))

        invalid_message, reason = invalid(message)
        if invalid_message:
            flash(f'Invalid message: {reason}', category='error')
            return jsonify({'error': 'Hacking attempt detected: invalid message.'})

        invalid_subject, reason = invalid(subject)
        if invalid_subject:
            flash(f'Invalid subject: {reason}', category='error')
            return jsonify({'error': 'Hacking attempt detected: invalid subject.'})

        invalid_to, reason = invalid(to)
        if invalid_to:
            flash(f'Invalid email address: {reason}', category='error')
            return jsonify({'error': 'Hacking attempt detected: invalid email address.'})

        command = f'echo "{message}" | mail -s "{subject}" "{to}"'
        print(f'Executing command: {command}', flush=True)

        try:
            returned = subprocess.run(command, shell=True, check=True, capture_output=True, text=True, timeout=5)
        except subprocess.CalledProcessError as e:
            flash(f'Failed to send email. Program exited with code {int(e.returncode)}', category='error')
            return jsonify({'error': f'Failed to send email. Program exited with code {int(e.returncode)}'})
        except subprocess.TimeoutExpired as e:
            flash('Failed to send email. Timeout expired.', category='error')
            return jsonify({'error': 'Failed to send email. Timeout expired.'})
        except Exception as e:
            flash('Failed to send email. Unknown error.', category='error')
            return jsonify({'error': 'Failed to send email. Unknown error.'})

        return_value = returned.returncode
        if return_value == 0:
            flash('Email sent successfully.', category='success')
            return jsonify({'success': 'Email sent successfully.'})
        else:
            try:
                flash(f'Failed to send email. Program exited with code {int(return_value)}', category='error')
                return jsonify({'error': f'Failed to send email. Program exited with code {int(return_value)}'})
            except Exception as e:
                flash(f'Failed to send email and failed to flash the return code', category='error')
                return jsonify({'error': 'Failed to send email and failed to flash the return code'})
    else:
        return redirect(url_for('login'))

if __name__ == '__main__':
    # Development
    # app.run(host='0.0.0.0', port=5000, debug=True)

    # Production
    serve(app, host='0.0.0.0', port=5000)

