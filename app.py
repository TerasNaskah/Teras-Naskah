
from flask import Flask, render_template, request, redirect, session, url_for
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# Initialize database
conn = sqlite3.connect('naskah.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS naskah (id INTEGER PRIMARY KEY AUTOINCREMENT, judul TEXT, isi TEXT)''')
conn.commit()
conn.close()

@app.route('/')
def index():
    conn = sqlite3.connect('naskah.db')
    c = conn.cursor()
    c.execute('SELECT * FROM naskah')
    naskah_list = c.fetchall()
    conn.close()
    return render_template('index.html', naskah_list=naskah_list)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'Agung181' and password == 'Agung01082001':
            session['username'] = username
            return redirect(url_for('admin'))
        else:
            return render_template('login.html', error='Username atau Password salah')
    return render_template('login.html')

@app.route('/admin')
def admin():
    if 'username' not in session:
        return redirect(url_for('login'))
    conn = sqlite3.connect('naskah.db')
    c = conn.cursor()
    c.execute('SELECT * FROM naskah')
    naskah_list = c.fetchall()
    conn.close()
    return render_template('admin.html', naskah_list=naskah_list)

@app.route('/upload', methods=['POST'])
def upload():
    if 'username' not in session:
        return redirect(url_for('login'))
    judul = request.form['judul']
    isi = request.form['isi']
    conn = sqlite3.connect('naskah.db')
    c = conn.cursor()
    c.execute('INSERT INTO naskah (judul, isi) VALUES (?, ?)', (judul, isi))
    conn.commit()
    conn.close()
    return redirect(url_for('admin'))

@app.route('/delete/<int:id>')
def delete(id):
    if 'username' not in session:
        return redirect(url_for('login'))
    conn = sqlite3.connect('naskah.db')
    c = conn.cursor()
    c.execute('DELETE FROM naskah WHERE id=?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('admin'))

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    if 'username' not in session:
        return redirect(url_for('login'))
    conn = sqlite3.connect('naskah.db')
    c = conn.cursor()
    if request.method == 'POST':
        judul = request.form['judul']
        isi = request.form['isi']
        c.execute('UPDATE naskah SET judul=?, isi=? WHERE id=?', (judul, isi, id))
        conn.commit()
        conn.close()
        return redirect(url_for('admin'))
    else:
        c.execute('SELECT * FROM naskah WHERE id=?', (id,))
        naskah = c.fetchone()
        conn.close()
        return render_template('edit.html', naskah=naskah)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
