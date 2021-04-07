from flask import Flask, redirect, url_for, render_template, request, session
from spotifyWebBackend import PlaylistCreation
from datetime import timedelta
import spotipy
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from SpotifySecret import client_id, client_secret, redirect_uri
from flask_sqlalchemy import SQLAlchemy
from flask_caching import Cache
import json
import random
from pprint import pprint

app = Flask(__name__)
cache = Cache()
app.config['CACHE_TYPE'] = 'simple'
app.secret_key = "PLZWORK"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.permanent_session_lifetime = timedelta(minutes=30)
cache.init_app(app)

db = SQLAlchemy(app)

class users(db.Model):
    id = db.Column("id", db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    mood = db.relationship('Mood', backref='author', lazy=True)


    def __repr__(self):
        return f"users('{self.username}')"

class Mood(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    vibeName = db.Column(db.String(20))
    clusters = db.relationship('Clusters', backref='author', lazy=True)
    error = db.Column(db.String(6))
    adds = db.Column(db.Integer)
    public = db.Column(db.Boolean)
    genreRepresentation = db.relationship('Genres', backref='author', lazy=True)
    songs = db.relationship('Songs', backref='author', lazy=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __init__(self, vibeName, error, adds, public, user_id):
        self.vibeName = vibeName
        self.error = error
        self.adds = adds
        self.public = public
        self.user_id = user_id


    def __repr__(self):
        return f"Vibe('{self.vibeName}','{self.clusters}', Privacy '{self.public}', Adds '{self.adds})"

class Clusters(db.Model):
    id = db.Column("id", db.Integer, primary_key=True)
    cluster = db.Column(db.String(75))
    moodId = db.Column(db.Integer, db.ForeignKey('mood.id'), nullable=False)

    def __init__(self, cluster, moodId):
        self.cluster = cluster
        self.moodId = moodId

    def __repr__(self):
        return self.cluster

class Genres(db.Model):
    id = db.Column("id", db.Integer, primary_key=True)
    genre = db.Column(db.String(30))
    moodId = db.Column(db.Integer, db.ForeignKey('mood.id'), nullable=False)

    def __init__(self, genre, moodId):
        self.genre = genre
        self.moodId = moodId

    def __repr__(self):
        return self.genre


class Songs(db.Model):
    id = db.Column("id", db.Integer, primary_key=True)
    song = db.Column(db.String(25))
    moodId = db.Column(db.Integer, db.ForeignKey('mood.id'), nullable=False)

    def __init__(self, song, moodId):
        self.song = song
        self.moodId = moodId

    def __repr__(self):
        return self.song


@app.route("/login", methods=["POST", "GET"])
def create():
        # lookup code query parameter from request
    scope = ' '.join([
        'user-read-email',
        'playlist-read-private',
        'playlist-modify-private',
        'playlist-modify-public',
        'user-modify-playback-state',
        'user-library-read'
    ])
    code = request.args.get('code')

    auth = SpotifyOAuth(client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri, scope=scope)
    token = auth.get_access_token(code)['access_token']
    session["token"] = token

    webBackend = PlaylistCreation()


    spotifyObject = Spotify(auth=session["token"])
    spotifyUser = spotifyObject.current_user()
    spotifyID = spotifyUser['id']
    found_user = users.query.filter_by(username=spotifyID).first()
    if not found_user:
        newUser = users(username=spotifyID)
        db.session.add(newUser)
        db.session.commit()
        found_user = users.query.filter_by(username=spotifyID).first()

    loadPlaylists(spotifyID)
    recommendations = [["70TM2AQY0TiC539o01iFJQ" ,"Create a Vibe Now to get Song Recomendations"]]

    if len(found_user.mood) > 0:
        print("here")
        recommendations = []
        for x in range(0, 4):
            vibe = random.choice(found_user.mood)
            songsList = []
            for y in range(0, 4):
                songsList.append(str(random.choice(vibe.songs)))
            print(songsList)
            recommendations.append([webBackend.homepageRecs(session["token"], songsList), vibe.vibeName])

    return render_template("homepage.html", songs=recommendations)

@app.route("/home", methods=["POST", "GET"])
def home():

    webBackend = PlaylistCreation()


    spotifyObject = Spotify(auth=session["token"])
    spotifyUser = spotifyObject.current_user()
    spotifyID = spotifyUser['id']
    found_user = users.query.filter_by(username=spotifyID).first()
    if not found_user:
        newUser = users(username=spotifyID)
        db.session.add(newUser)
        db.session.commit()
        found_user = users.query.filter_by(username=spotifyID).first()

    loadPlaylists(spotifyID)
    recommendations = [["Create a Vibe Now to get Song Recomendations"]]
    if len(found_user.mood) > 0:
        print("here")
        recommendations = []
        for x in range (0, 4):
            vibe = random.choice(found_user.mood)
            songsList = []
            for y in range (0, 4):
                songsList.append(str(random.choice(vibe.songs)))
            print(songsList)
            recommendations.append([webBackend.homepageRecs(session["token"], songsList), vibe.vibeName])

    return render_template("homepage.html", songs=recommendations)

@cache.memoize(timeout=300)
def loadPlaylists(userID):
    playlistLoad = PlaylistCreation()
    playlists = playlistLoad.loadPlaylists(token=session["token"])
    return playlists

@app.route("/<usr>")
def user(usr):
    return render_template("displayMessage.html", usr=usr)

@app.route("/createPage")
def createPage():
    return render_template("createPage.html")

@app.route("/shuffle", methods=["POST", "GET"])
def shuffle():
    if request.method == "POST":
        playlistCreation = PlaylistCreation()

        vibe = request.form["VibeName"]
        if vibe != "RAND0M$HUFFL3":
            moodFound = Mood.query.filter_by(id=vibe).first()
            clusters = moodFound.clusters
            clustersAsList = []
            clustersAndError = []
            for cluster in clusters:
                cluster = str(cluster)
                clusterList = playlistCreation.finalListDecoder(cluster)
                clustersAsList.append(clusterList)
            clustersAndError.append(clustersAsList)
            clustersAndError.append(float(moodFound.error))

            spotifyObject = Spotify(auth=session["token"])
            spotifyUser = spotifyObject.current_user()
            spotifyID = spotifyUser['id']

            genreDictLoaded = moodFound.genreRepresentation

            songsListLoaded = []
            for song in moodFound.songs:
                songsListLoaded.append(str(song))


            if request.form["Playlist"] == "NOPLAYLIST":
                playlistCreation.recomendations(token=session["token"], tracksFullList=songsListLoaded,
                                            shuffleTime=request.form["time"])
            else:
                playlistCreation.shuffle(playlistName=request.form["Playlist"], clustersAndError= clustersAndError,
                                       token=session["token"], shuffleTime=request.form["time"],
                                          genreDict=genreDictLoaded)
        else:
            playlistId = request.form["Playlist"]
            if playlistId == "NOPLAYLIST":
                spotifyObject = Spotify(auth=session["token"])
                spotifyUser = spotifyObject.current_user()
                spotifyID = spotifyUser['id']
                playlists = loadPlaylists(spotifyID)
                playlistId = random.choice(playlists)
            playlistCreation.randomShuffle(token=session["token"], playlistId=playlistId,
                                           shuffleTime=request.form["time"])

        return redirect(url_for("user", usr="Shuffled"))

    else:
        spotifyObject = Spotify(auth=session["token"])
        spotifyUser = spotifyObject.current_user()
        spotifyID = spotifyUser['id']
        playlists = loadPlaylists(spotifyID)
        found_user = users.query.filter_by(username=spotifyID).first()
        times = [15, 20, 25, 30 , 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100,
                 120, 140, 160, 180, 200, 220, 240, 260, 280, 300, 320, 340, 360, 380, 400]
        return render_template("shuffle.html", playlists=playlists, vibes=found_user.mood, times=times)

@app.route("/vibe", methods=["POST", "GET"])
def vibe():
    if request.method == "POST":
        #request.form["VibeName"]
        playlistCreation = PlaylistCreation()

        if request.form["playlistName"] == '$L1k3dS0nGz$':
            clustersAndError_GenreDict = playlistCreation.likedSongsCreateVibe(token=session["token"])
        else:
            clustersAndError_GenreDict = playlistCreation.newCreateVibe(playlistName=request.form["playlistName"],
                                                       token=session["token"])
        #serialized = clustersAndError_GenreDict[0]
        genreDict = clustersAndError_GenreDict[1]
        songIDList = clustersAndError_GenreDict[2]
        error = clustersAndError_GenreDict[0][1]
        #json_songIDList = json.dumps(songIDList)
        genresTest = playlistCreation.testGenres(genreDict)
        #genreDict = json.dumps(genreDict)
        songsDict = playlistCreation.findSongsToTest(genresTest, session["token"])

        #new stuff
        spotifyObject = Spotify(auth=session["token"])
        spotifyUser = spotifyObject.current_user()
        spotifyID = spotifyUser['id']
        found_user = users.query.filter_by(username=spotifyID).first()  # how to make a new user!!!?
        returnState = ""
        if found_user:
            if len(found_user.mood) > 0:
                for mood in found_user.mood:
                    if mood.vibeName == request.form["VibeName"]:
                        returnState = "can't return since you have a vibe of this name already"
                if returnState == "":
                    mood1 = Mood(request.form["VibeName"], adds=int(0), error=error,  public=("public" == request.form["privacy"]),
                                  user_id=found_user.id)
                    db.session.add(mood1)
                    db.session.commit()
                    for cluster in clustersAndError_GenreDict[0][0]:
                        clusterList = list(cluster)
                        clusterString = playlistCreation.finalListToStringEncoder(clusterList)
                        #clusterString = json.dumps(clusterstr)
                        addCluster = Clusters(cluster=clusterString, moodId=mood1.id)
                        db.session.add(addCluster)
                        db.session.commit()
                    for song in songIDList:
                        addSong = Songs(song=song, moodId=mood1.id)
                        db.session.add(addSong)
                    db.session.commit()
                    for genre in genreDict.keys():
                        addGenre = Genres(genre=genre, moodId=mood1.id)
                        db.session.add(addGenre)
                    db.session.commit()
                    moodID = mood1.id

                    #songsDict = playlistCreation.findSongsToTest(genresTest, session["token"])
            else:
                mood1 = Mood(request.form["VibeName"], adds=int(0), error=error,
                             public=("public" == request.form["privacy"]),
                             user_id=found_user.id)
                db.session.add(mood1)
                db.session.commit()
                for cluster in clustersAndError_GenreDict[0][0]:
                    clusterList = list(cluster)
                    clusterString = playlistCreation.finalListToStringEncoder(clusterList)
                    # clusterString = json.dumps(clusterstr)
                    addCluster = Clusters(cluster=clusterString, moodId=mood1.id)
                    db.session.add(addCluster)
                    db.session.commit()
                for song in songIDList:
                    addSong = Songs(song=song, moodId=mood1.id)
                    db.session.add(addSong)
                db.session.commit()
                for genre in genreDict.keys():
                    addGenre = Genres(genre=genre, moodId=mood1.id)
                    db.session.add(addGenre)
                db.session.commit()
                moodID = mood1.id

        else:
            mood1 = Mood(request.form["VibeName"], adds=int(0), error=error,
                         public=("public" == request.form["privacy"]),
                         user_id=found_user.id)
            db.session.add(mood1)
            db.session.commit()
            for cluster in clustersAndError_GenreDict[0][0]:
                clusterList = list(cluster)
                clusterString = playlistCreation.finalListToStringEncoder(clusterList)
                # clusterString = json.dumps(clusterstr)
                addCluster = Clusters(cluster=clusterString, moodId=mood1.id)
                db.session.add(addCluster)
                db.session.commit()
            for song in songIDList:
                addSong = Songs(song=song, moodId=mood1.id)
                db.session.add(addSong)
            db.session.commit()
            for genre in genreDict.keys():
                addGenre = Genres(genre=genre, moodId=mood1.id)
                db.session.add(addGenre)
            db.session.commit()
            moodID = mood1.id
        session['songsDict'] = songsDict
        session['moodID'] = moodID
        return redirect(url_for("user", usr="Songs have been Added"))

    else:
        spotifyObject = Spotify(auth=session["token"])
        spotifyUser = spotifyObject.current_user()
        spotifyID = spotifyUser['id']
        playlists = loadPlaylists(spotifyID)
        return render_template("spotifyVibeMaker.html", playlists=playlists) #create vibe page


@app.route("/songTest", methods=["POST", "GET"])
def songTest():
    if request.method == "POST":
        songsDict = session['songsDict']
        moodID = session['moodID']

        spotifyObject = Spotify(auth=session["token"])
        spotifyUser = spotifyObject.current_user()
        spotifyID = spotifyUser['id']
        found_user = users.query.filter_by(username=spotifyID).first()
        playlistCreation = PlaylistCreation()


        for mood in found_user.mood:
            if moodID == mood.id:
                genres = mood.genreRepresentation
                genresDict = json.loads(genres)
                for song in songsDict:
                    if request.form[song] != "FALSE":
                        genresDict = playlistCreation.refineGenreVibe(genresDict, request.form[song])
                mood.genreRepresentation = json.dumps(genresDict)
                break

        return redirect(url_for("user", usr="Songs have been Added"))

    else:
        songsDict = session['songsDict']
        return render_template("songTest.html", songsDict=songsDict)



@app.route("/playlistCreation", methods=["POST", "GET"])
def playlistCreation():
    if request.method == "POST":
        playlistCreation = PlaylistCreation()

        vibe = request.form["VibeName"]
        moodFound = Mood.query.filter_by(id=vibe).first()
        clusters = moodFound.clusters
        clustersAsList = []
        clustersAndError = []
        for cluster in clusters:
            cluster = str(cluster)
            clusterList = playlistCreation.finalListDecoder(cluster)
            clustersAsList.append(clusterList)
        clustersAndError.append(clustersAsList)
        clustersAndError.append(float(moodFound.error))

        spotifyObject = Spotify(auth=session["token"])
        spotifyUser = spotifyObject.current_user()
        spotifyID = spotifyUser['id']

        genreDictLoaded = moodFound.genreRepresentation

        playlistCreation.newBuildPlaylist(playlistName=request.form["oldPlaylist"], clustersAndError= clustersAndError,
                                       token= session["token"], newPlaylist=request.form["newPlaylist"],
                                          genreDict=genreDictLoaded)

        return redirect(url_for("user", usr="Songs have been Added"))

    else:
        spotifyObject = Spotify(auth=session["token"])
        spotifyUser = spotifyObject.current_user()
        spotifyID = spotifyUser['id']
        playlists = loadPlaylists(spotifyID)
        found_user = users.query.filter_by(username=spotifyID).first()
        return render_template("playlistCreation.html", playlists=playlists, vibes=found_user.mood) #playlistCreation html page

@app.route("/", methods=["POST", "GET"])
def login():
    return render_template("login.html") # redirects you through to the name function
#https://accounts.spotify.com/authorize?client_id=0564e53d485643aaa292796e7d73cc43&response_type=code&redirect_uri=http%3A%2F%2Fspotifypro.pythonanywhere.com&scope=user-read-email%20playlist-read-private%20playlist-modify-private%20playlist-modify-public

@app.route("/VibeViewer", methods=["POST", "GET"])
def vibeviewer():
    if request.method == "POST":

        spotifyObject = Spotify(auth=session["token"])
        spotifyUser = spotifyObject.current_user()
        spotifyID = spotifyUser['id']
        found_user = users.query.filter_by(username=spotifyID).first()
        if found_user:
            for mood in found_user.mood:
                if request.form["VibeName"] == mood.vibeName:

                    for cluster in mood.clusters:
                        db.session.delete(cluster)
                    db.session.commit()
                    for song in mood.songs:
                        db.session.delete(song)
                    db.session.commit()
                    for genre in mood.genreRepresentation:
                        db.session.delete(genre)
                    db.session.commit()

                    db.session.delete(mood)
                    db.session.commit()
                    break

        return redirect(url_for("user", usr="deleted"))
    else:
        spotifyObject = Spotify(auth=session["token"])
        spotifyUser = spotifyObject.current_user()
        spotifyID = spotifyUser['id']
        found_user = users.query.filter_by(username=spotifyID).first()
        return render_template("VibeViewer.html", values=found_user.mood)

@app.route("/publicVibes", methods=["POST", "GET"])
def publicVibeViewer():
    if request.method == "POST":
        spotifyObject = Spotify(auth=session["token"])
        spotifyUser = spotifyObject.current_user()
        spotifyID = spotifyUser['id']
        found_user = users.query.filter_by(username=spotifyID).first()
        if found_user:
            for mood in Mood.query.filter_by(public=True).all():
                if request.form["VibeName"] == mood.vibeName:
                    author = users.query.filter_by(id=mood.user_id).first()
                    name = mood.vibeName + " by: " + str(author.username)
                    mood.adds = mood.adds + 1


                    mood1 = Mood(name, adds=int(0), error=mood.error,
                                 public=False,
                                 user_id=found_user.id)
                    db.session.add(mood1)
                    db.session.commit()
                    for cluster in mood.clusters:
                        clusterString = str(cluster)
                        addCluster = Clusters(cluster=clusterString, moodId=mood1.id)
                        db.session.add(addCluster)
                    db.session.commit()
                    for song in mood.songs:
                        songAdd = str(song)
                        addSong = Songs(song=songAdd, moodId=mood1.id)
                        db.session.add(addSong)
                    db.session.commit()
                    for genre in mood.genreRepresentation:
                        genreAdd = str(genre)
                        addGenre = Genres(genre=genreAdd, moodId=mood1.id)
                        db.session.add(addGenre)
                    db.session.commit()


                    break

        return redirect(url_for("user", usr="deleted"))
    else:
        spotifyObject = Spotify(auth=session["token"])
        spotifyUser = spotifyObject.current_user()
        spotifyID = spotifyUser['id']
        #found_user = users.query.filter_by(username=spotifyID).first()
        return render_template("publicVibes.html", values=Mood.query.filter_by(public=True).all())



db.create_all()

if __name__ == '__main__':
    app.run()

