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
		messageType = "post"
		curs.execute("select * from messages where from_user=(?) and type =(?)",(zid,str(messageType)))
		postRS = curs.fetchall()
		commentRS = []
		#replyRS 
		for t in postRS:
			messageType = "comment"
			index_path = t[12]
			index_path += "%"
			curs.execute("select * from messages where index_path like (?) and type=(?) order by rowid",(index_path,str(messageType)))
			commentRS.append(curs.fetchone())

			#for k in commentRS:
			#	messageType = "reply"
			#	curs.execute("select * from messages where parent_msg_dir=(?) and type=(?)",(k[9],str(messageType)))
			#	replyRS.append(curs.fetchall())


	if password == passw:
		session['user'] = zid
		g.user = session['user']
		return render_template("profile.html", zid=zid, image=image,name=fullname,email=email,program=program,suburb=homesuburb
		,longitude=longitude,latitude=latitude,birthday=birthday,mates=mates,mateImages=mateImages, postRS=postRS,commentRS=commentRS)
	else:
		return render_template("login.html",error=error)


@app.route('/viewProfile',methods=['POST','GET'])
def viewProfile():
	profileID = request.form['profileID']
	root = request.form['rootID']
	if profileID == root:
		curs.execute("select * from User where zid = (?)",(profileID,))
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
			password=temp[3]
			image =  "dataset/" + root + "/profile.jpg"#temp[12]
		curs.execute("select zidB,profile from mates where zidA = (?)",(root,))
		mates = []
		mateImages= []
		messageType = "post"
		curs.execute("select * from messages where from_user=(?) and type =(?)",(profileID,str(messageType)))
		postRS = curs.fetchall()

		for row in curs.fetchall():
			mates.append(row[0])
			mateImages.append(row[1])
		return render_template("profile.html", zid=root, image=image,name=fullname,email=email,program=program,suburb=homesuburb,longitude=longitude,latitude=latitude,birthday=birthday,mates=mates,mateImages=mateImages,postRS=postRS)
	else:
		curs.execute("select * from User where zid = (?)",(profileID,))
		for temp in curs.fetchall():
			#temp = curs.fetchall()
			#temp =temp.split(",")
			zidB = temp[0]
			fullname = temp[1]
			email = temp[2]
			program = temp[4]
			homesuburb= temp[6]
			longitude = temp[9]
			latitude = temp[10]
			birthday = temp[11]
			image =  "dataset/" + zidB + "/profile.jpg"#temp[12]
			password=temp[3]
		
		curs.execute("select zidB,profile from mates where zidA = (?)",(profileID,))
		mates = []
		mateImages= []
		for row in curs.fetchall():
			mates.append(row[0])
			mateImages.append(row[1])
		messageType = "post"
		curs.execute("select * from messages where from_user=(?) and type =(?)",(zidB,str(messageType)))
		postRS1 = curs.fetchall()

		return render_template("viewProfile.html", zid=zidB, image=image,name=fullname,email=email,program=program,suburb=homesuburb
		,longitude=longitude,latitude=latitude,birthday=birthday,mates=mates,mateImages=mateImages,root=root,postRS=postRS1)
		"""
		return render_template("guess.html",submit=temp)
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

@app.route('/searchPost',methods=['POST','GET'])
def searchPost():
	searchString = request.form['postsearch']
	searchString += '%'
	root = request.form['profileID']
	curs.execute("select * from messages where message LIKE (?) and type = 'post'",(searchString,))
	searchList = curs.fetchall()
	return render_template('postSearch.html',results=searchList,zid=root)
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