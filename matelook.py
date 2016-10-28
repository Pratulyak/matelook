from random import randint

from flask import Flask, render_template, request, session , g
import sqlite3
import re
import os
app = Flask(__name__)
app.secret_key = os.urandom(24)

conn = sqlite3.connect('matelook.db')
curs = conn.cursor()

@app.route('/', methods=['GET'])
def homepage():
        # This is how you should distinguish between loading a page and submitting data
    return render_template("login.html")
@app.route('/profile',methods=['POST','GET'])
def login():
	zid = "guest";
	if request.method == 'POST':
		zid = request.form['zid']
		passw = request.form['password']
		#print zid
		temp = ""
		error = "Login Failed! Credential error"
		curs.execute("select * from User where zid = (?)",(zid,))
		for temp in curs.fetchall():
			#temp = curs.fetchall()
			#temp =temp.split(",")
			zid = temp[0]
			fullname = temp[1]
			email = temp[2]
			program = temp[4]
			homesuburb= temp[6]
			longitude = temp[9]
			latitude = temp[10]
			birthday = temp[11]
			image =  "dataset/" + zid + "/profile.jpg"#temp[12]
			password=temp[3]
		curs.execute("select zidB,profile from mates where zidA = (?)",(zid,))
		mates = []
		mateImages= []
		for row in curs.fetchall():
			mates.append(row[0])
			mateImages.append(row[1])

	if password == passw:
		session['user'] = zid
		g.user = session['user']
		return render_template("profile.html", zid=zid, image=image,name=fullname,email=email,program=program,suburb=homesuburb
		,longitude=longitude,latitude=latitude,birthday=birthday,mates=mates,mateImages=mateImages)
	else:
		return render_template("login.html",error=error)


@app.route('/viewProfile',methods=['POST','GET'])
def viewProfile():

	temp = request.form['profileID']
	root = request.form['rootID']
	submit = request.form['profileID']
	if temp == root:
		submit = request.form['rootID']

	return render_template("guess.html",submit=submit,rootid=root)
"""	if request.form['submit'] == "My Profile":
		curs.execute("select * from User where zid = (?)",(root,))
	elif request.form['submit'] == "View Profile":
		curs.execute("select * from User where zid = (?)",(temp,))
	for temp in curs.fetchall():
			#temp = curs.fetchall()
			#temp =temp.split(",")
		zid = temp[0]
		fullname = temp[1]
		email = temp[2]
		program = temp[4]
		homesuburb= temp[6]
		longitude = temp[9]
		latitude = temp[10]
		birthday = temp[11]
		image =  "dataset/" + zid + "/profile.jpg"#temp[12]
		password=temp[3]
	curs.execute("select zidB,profile from mates where zidA = (?)",(zid,))
	mates = []
	mateImages= []
	for row in curs.fetchall():
		mates.append(row[0])
		mateImages.append(row[1])

	
	session['user'] = zid
	g.user = session['user']
	return render_template("profile.html",rootid=root, zid=zid, image=image,name=fullname,email=email,program=program,suburb=homesuburb
		,longitude=longitude,latitude=latitude,birthday=birthday,mates=mates,mateImages=mateImages)
	"""
	

@app.route('/logout',methods=['POST','GET'])
def logout():
	#zid = session['user']
	session.pop('user', None)
	return render_template("login.html")

@app.route('/search',methods=['POST','GET'])
def search():
	searchString = request.form['matesearch']
	searchString += '%'
	root = request.form['profileID']
	curs.execute("select * from User where full_name LIKE (?)",(searchString,))
	searchList = curs.fetchall()
	return render_template('searchResults.html',results=searchList,zid=root)
# your css, js, images, and anything that you wouldn't want CGI to execute, but the user should see go in the "static" directory during testing
# During production, it's advisable to set this up to be served by apache instead
@app.route('/static/<path:path>')
def send_static_file(path):
    return send_from_directory('static', path)

if __name__ == '__main__':
    # you should be using this to debug. This allows you to attach an actual debugger to your script,
    # and you can see any errors that occurred in the command line. No pesky log files like cgi does
    # Also note that since use_reloader is on, you shouldn't make changes to the code while the app is paused in a debugger,
    # because it will reload as soon as you hit play again
    app.run(debug=True, use_reloader=True)