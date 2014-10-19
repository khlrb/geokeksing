import os
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
	
def generate_possible_secret(g):
	res = ['dummy']
	while res:
		hash = os.urandom(4).encode('hex')
		cur = g.db.execute('select secret from kekse where secret = ?', [hash])
		res = cur.fetchall()
	return hash	


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
	cur = g.db.execute('select k.title, k.creator, k.description, k.latitude, k.longitude \
						from kekse k \
						inner join status s \
						on k.status = s.id \
						where s.title = \'aktiv\' \
						order by k.id desc')
	entries = [dict(title=row[0], creator=row[1], description=row[2], latitude=row[3], longitude=row[4]) for row in cur.fetchall()]
	return render_template('map.html', kekse=entries)

@app.route('/add', methods=['POST'])
def add_kekse():
	if request.form['title'] and request.form['creator'] \
			and request.form['latitude'] and request.form['longitude'] \
			and request.form['description']:
		hash = generate_possible_secret(g)		
		g.db.execute('insert into kekse (title, creator, description, latitude, longitude, secret, status) \
					  values (?, ?, ?, ?, ?, ?, \
					  (select id from status where title = \'aktiv\'))', \
					  [request.form['title'], request.form['creator'], request.form['description'], request.form['latitude'], \
					  request.form['longitude'], hash])
		g.db.commit()
	return redirect(url_for('show_map'))
	
@app.route('/remove', methods=['POST'])
def remove_kekse():
	if request.form['secret']:
		g.db.execute('update kekse set status = \
					  (select id from status where title = \'inaktiv\') \
					  where secret = ?', [request.form['secret']])
		g.db.commit()
	return redirect(url_for('show_map'))

@app.route('/add_keks')
def add_form():
	return render_template('add_keks.html')
	
@app.route('/remove_keks')
def remove_form():
	return render_template('remove_keks.html')


if __name__ == "__main__":
	app.run()
