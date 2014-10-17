import sqlite3
from flask import Flask, request, url_for, render_template, g, redirect

DATABASE = 'kekse.db'
DEBUG = True
SECRET_KEY = "12345"
USERNAME = 'admin'
PASSWORD = 'god' # "Don't forget god. System operators love to use god. It's that whole male ego thing." <-- toller Film

app = Flask(__name__)
app.config.from_object(__name__)

def connect_db():
	return sqlite3.connect(app.config['DATABASE'])


@app.before_request
def before_request():
	g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
	db = getattr(g, 'db', None)
	if db is not None:
		db.close()

@app.route('/')
def show_map():
	cur = g.db.execute('select title, creator, description, latitude, longitude from kekse order by id desc')
	entries = [dict(title=row[0], creator=row[1], description=row[2], latitude=row[3], longitude=row[4]) for row in cur.fetchall()]
	return render_template('map.html', kekse=entries)

@app.route('/add', methods=['POST'])
def add_kekse():
	if request.form['title'] and request.form['creator'] and request.form['latitude'] and request.form['longitude'] and request.form['description']:
		g.db.execute('insert into kekse (title, creator, description, latitude, longitude) values (?, ?, ?, ?, ?)', [request.form['title'], request.form['creator'], request.form['description'], request.form['latitude'], request.form['longitude']])
		g.db.commit()
	return redirect(url_for('show_map'))

@app.route('/add_keks')
def add_form():
	return render_template('add_keks.html')


if __name__ == "__main__":
	app.run()
