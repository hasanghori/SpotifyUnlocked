from spotipy import Spotify
from pprint import pprint
from sklearn.cluster import KMeans
import pandas as pd
from scipy.spatial.distance import cdist
from statistics import mean
from statistics import stdev
import requests
import time
import random
from genres import genreDictionary

class PlaylistCreation:
    def createObjectsList(self, songIDList, spotifyObject):
        songObjectsList = []
        for i in range(0, len(songIDList)):
            songFeatures = spotifyObject.audio_features(songIDList[i])
            songObj = songObject(songIDList[i], acousticness=songFeatures[0]['acousticness'],
                                 danceability=songFeatures[0]['danceability'], energy=songFeatures[0]['energy'],
                                 tempo=songFeatures[0]['tempo'], valence=songFeatures[0]['valence'])
            songObjectsList.append(songObj)
        return songObjectsList

    def genreDictionary(self, subGenre):
        genreDict = genreDictionary

        if subGenre not in genreDict.keys():
            genreDict[subGenre] = "N/A"

        return genreDict[subGenre]

    def loadPlaylists(self, token):
        #Authenticate with Spotify
        spotifyObject = Spotify(auth=token)
        spotifyUser = spotifyObject.current_user()
        username = spotifyUser['id']
        count = int(0)
        playlistDict = {}
        response = spotifyObject.user_playlists(user=username, offset=count)

        #Stores all playlists into a Dictionary
        while count < response["total"]:
            response = spotifyObject.user_playlists(user=username, offset=count)
            count = count + 50
            for x in range(0, len(response['items'])):
                playlistDict[response['items'][x]['name']] = response['items'][x]['id']

        return playlistDict


    def averageError(self, data):
        dataset = []
        for d in data:
            dataset.append(min(d))
        error = mean(dataset)
        return error

    #Creates clusters graphically using song elements to define a Vibe
    def KMeansVibe(self, data):
        k_rng = range(1, int(len(data) / 3))
        df = pd.DataFrame(data=data)
        sse = []
        centroidsAndError = []
        centroids = []
        numClusterFound = False
        for k in k_rng:
            km = KMeans(n_clusters=k)
            km.fit_predict(df)
            sse.append(km.inertia_)
            centroids.append(km.cluster_centers_)
            if k > 1:
                if (sse[k - 2] - sse[k - 1] < 0.7):
                    centroidsAndError.append(centroids[k - 2])
                    avgError = self.averageError(data=cdist(data, centroidsAndError[0], 'euclidean'))
                    centroidsAndError.append(round(avgError, 4))
                    numClusterFound = True
                    break

        if (numClusterFound == False):
            centroidsAndError.append(centroids[int(len(data) / 3) - 2])
            avgError = self.averageError(data=cdist(data, centroidsAndError[0], 'euclidean'))
            centroidsAndError.append(avgError)

        return centroidsAndError

    #Converts a Cluster into a string that can be easily stored in the database
    def finalListToStringEncoder(self, list):
        string = ""
        string = string + "|"
        for val in range(0, 7):
            string = string + str(round(list[val], 4)) + ", "
        string = string + str(round(list[val + 1], 4)) + "|"

        return string

    #Decodes the Cluster String into floats so they can be used in the program
    def finalListDecoder(self, string):
        array = string.split("|")
        strings = array[1].split(", ")
        for val in range(0, len(strings)):
            strings[val] = float(strings[val])
        return strings


    def likedSongsCreateVibe(self, token):
        # Authenticate
        spotifyObject = Spotify(auth=token)
        spotifyUser = spotifyObject.current_user()
        username = spotifyUser['id']

        # create genre dictionary
        genreDict = {}

        # get songs from LikedSongs
        playlistSongs = spotifyObject.current_user_saved_tracks(limit=50)
        pprint(playlistSongs)
        numberOfSongs = int(playlistSongs['total'])
        totalAdded = int(0)
        songObjectsList = []
        songID_List = []
        while (numberOfSongs > totalAdded):
            playlistSongs = spotifyObject.current_user_saved_tracks(limit=50, offset=totalAdded)
            for i in range(0, len(playlistSongs['items'])):
                try:
                    songURI = playlistSongs['items'][i]['track']['uri']
                    songID = playlistSongs['items'][i]['track']['id']
                    songID_List.append(songID)
                    songFeatures = spotifyObject.audio_features(songURI)

                    genreDict = self.genreVibe(spotifyObject=spotifyObject, songId=songID,
                                               genreDict=genreDict)

                    songObj = [songFeatures[0]['acousticness'],
                               songFeatures[0]['danceability'], songFeatures[0]['energy'],
                               songFeatures[0]['instrumentalness'], songFeatures[0]['liveness'],
                               songFeatures[0]['speechiness'],
                               round(songFeatures[0]['tempo'] / 180, 6), songFeatures[0]['valence']]
                    songObjectsList.append(songObj)
                except:
                    print("song was removed from spotify sorry")
            totalAdded = totalAdded + 50

        #Create Clusters and Return Answer
        centroidsAndError = self.KMeansVibe(data=songObjectsList)
        centroidsAndError_GenreDict = [centroidsAndError, genreDict, songID_List]
        return centroidsAndError_GenreDict

    def newCreateVibe(self, playlistName, token):
        # find playlist
        spotifyObject = Spotify(auth=token)
        spotifyUser = spotifyObject.current_user()
        username = spotifyUser['id']

        # find playlist
        playlistID = playlistName

        #create genre dictionary
        genreDict = {}

        # get songs from playlist
        playlistSongs = spotifyObject.user_playlist_tracks(user=username, playlist_id=playlistID)
        numberOfSongs = int(playlistSongs['total'])
        totalAdded = int(0)
        songObjectsList = []
        songID_List = []
        while (numberOfSongs > totalAdded):
            playlistSongs = spotifyObject.user_playlist_tracks(user=username, playlist_id=playlistID, offset=totalAdded)
            for i in range(0, len(playlistSongs['items'])):
                try:
                    songURI = playlistSongs['items'][i]['track']['uri']
                    songID = playlistSongs['items'][i]['track']['id']
                    songID_List.append(songID)
                    songFeatures = spotifyObject.audio_features(songURI)

                    genreDict = self.genreVibe(spotifyObject=spotifyObject, songId=songID,
                                               genreDict=genreDict)

                    songObj = [songFeatures[0]['acousticness'],
                               songFeatures[0]['danceability'], songFeatures[0]['energy'],
                               songFeatures[0]['instrumentalness'], songFeatures[0]['liveness'], songFeatures[0]['speechiness'],
                               round(songFeatures[0]['tempo'] / 180, 6), songFeatures[0]['valence']]
                    songObjectsList.append(songObj)
                except:
                    print("song was removed from spotify sorry")
            totalAdded = totalAdded + 100

        

        centroidsAndError = self.KMeansVibe(data=songObjectsList)
        centroidsAndError_GenreDict = [centroidsAndError, genreDict, songID_List]
        return centroidsAndError_GenreDict
    
    #Method Takes a song and finds all the genre classifications and adds them to the GenreDict
    def genreVibe(self, spotifyObject, songId, genreDict):
        #get song
        song = spotifyObject.track(songId)

        #get genres and add them
        for artist in song['artists']:
            artistInfo = spotifyObject.artist(artist_id=artist['id'])
            genres = artistInfo['genres']
            for genre in genres:
                if genre not in genreDict.keys():
                    genreDict[genre] = 1
                else:
                    genreDict[genre] = genreDict[genre] + 1

        return genreDict

    #Checks if a song contains one of the genres that defines a specific Vibe
    def songGenreInVibe (self, spotifyObject, songId, songGenreDict, vibeGenreDict):
        songGenreDict = {}
        songGenreDict = self.genreVibe(spotifyObject=spotifyObject, songId=songId, genreDict=songGenreDict)
        
        genre_exists_in_vibe = False

        for key in songGenreDict:
            if key in vibeGenreDict:
                genre_exists_in_vibe = True
                break

        #print(genre_exists_in_vibe)
        return genre_exists_in_vibe

   
    #Returns a list of recomendations to be shown on a users homepage
    def homepageRecs(self, token, songList):
        spotifyObject = Spotify(auth=token)
        songWorks = False

        recs = spotifyObject.recommendations(seed_tracks=songList)

        track = random.choice(recs['tracks'])

        return track['id']
    
    def newBuildPlaylist (self, playlistName, clustersAndError, token, newPlaylist, genreDict):
        # get user
        spotifyObject = Spotify(auth=token)
        spotifyUser = spotifyObject.current_user()
        username = spotifyUser['id']

        # find playlist
        playlistID = playlistName

        # find playlist where we will add songs
        playlist_to_add_to = newPlaylist

        #vibe Genres
        vibeGenresTest = genreDict
        vibeGenres = []
        for vibe in vibeGenresTest:
            vibeGenres.append(str(vibe))


        songGenreDict = {}

        # get songs
        playlist = spotifyObject.user_playlist_tracks(user=username, playlist_id=playlistID)
        numberOfSongs = int(playlist['total'])
        totalAdded = int(0)
        songsToAdd = []
        listOfAllSongsToAdd = []
        while (numberOfSongs > totalAdded):
            playlist = spotifyObject.user_playlist_tracks(user=username, playlist_id=playlistID, offset=totalAdded)
            for i in range(0, len(playlist['items'])):
                try:
                    songURI = playlist['items'][i]['track']['uri']
                    songId = playlist['items'][i]['track']['id']
                    songFeatures = spotifyObject.audio_features(songURI)


                    #if song contains a genre that matches the inputted vibe
                    if (self.songGenreInVibe(spotifyObject=spotifyObject, songId=songId, songGenreDict=songGenreDict,
                                             vibeGenreDict=vibeGenres) == True):
                        song = [[songFeatures[0]['acousticness'],
                                   songFeatures[0]['danceability'], songFeatures[0]['energy'],
                                   songFeatures[0]['instrumentalness'], songFeatures[0]['liveness'],
                                songFeatures[0]['speechiness'], round(songFeatures[0]['tempo'] / 180, 6),
                                songFeatures[0]['valence']]]
                        distArray = cdist(song, clustersAndError[0], 'euclidean')
                        dist = min(distArray[0])
                        
                        #is the min distance between song and cluster within average min distance
                        if float(dist) < float(clustersAndError[1]):
                            songsToAdd.append(songURI)

                        if len(songsToAdd) == 100 or i == len(playlist['items']) - 1:
                            listOfAllSongsToAdd.append(songsToAdd)
                            songsToAdd = []
                except:
                    print("spotify does not have this song anymore. Sorry")
            totalAdded = totalAdded + 100

        if (len(listOfAllSongsToAdd) < 1):
            #if there is less than 100 songs to add
            spotifyObject.user_playlist_add_tracks(user=username, playlist_id=playlist_to_add_to, tracks=songsToAdd)
        else:
            for songs in listOfAllSongsToAdd:
                spotifyObject.user_playlist_add_tracks(user=username, playlist_id=playlist_to_add_to, tracks=songs)
                time.sleep(5)

    def shuffle(self, playlistName, clustersAndError, token, shuffleTime, genreDict):
        # get user
        spotifyObject = Spotify(auth=token)
        spotifyUser = spotifyObject.current_user()
        username = spotifyUser['id']

        # find playlist
        playlistID = playlistName

        #vibe Genres
        vibeGenresTest = genreDict
        vibeGenres = []
        for vibe in vibeGenresTest:
            vibeGenres.append(str(vibe))

        songGenreDict = {}

        # get songs
        playlist = spotifyObject.user_playlist_tracks(user=username, playlist_id=playlistID)
        numberOfSongs = int(playlist['total'])
        totalAdded = int(0)
        songsToAdd = []
        while (numberOfSongs > totalAdded):
            playlist = spotifyObject.user_playlist_tracks(user=username, playlist_id=playlistID, offset=totalAdded)
            for i in range(0, len(playlist['items'])):
                try:
                    songURI = playlist['items'][i]['track']['uri']
                    songId = playlist['items'][i]['track']['id']
                    songFeatures = spotifyObject.audio_features(songURI)

                    if (self.songGenreInVibe(spotifyObject=spotifyObject, songId=songId, songGenreDict=songGenreDict,
                                             vibeGenreDict=vibeGenres) == True):

                        song = [[songFeatures[0]['acousticness'],
                                   songFeatures[0]['danceability'], songFeatures[0]['energy'],
                                   songFeatures[0]['instrumentalness'], songFeatures[0]['liveness'],
                                songFeatures[0]['speechiness'], round(songFeatures[0]['tempo'] / 180, 6),
                                songFeatures[0]['valence']]]
                        distArray = cdist(song, clustersAndError[0], 'euclidean')
                        dist = min(distArray[0])
                        if float(dist) < float(clustersAndError[1]):
                            if len(songsToAdd) < 2:
                                songsToAdd.append(songURI)
                                spotifyObject.add_to_queue(songURI)

                            else:
                                songsToAdd.append(songURI)

                except:
                    print("spotify does not have this song anymore. Sorry")
            totalAdded = totalAdded + 100

        numSongsToAdd = int(int(shuffleTime) / 2)
        songsAdded = 0
        while songsAdded < numSongsToAdd or len(songsToAdd) == 0:
            try:
                addSong = random.choice(songsToAdd)
                spotifyObject.add_to_queue(addSong)
                songsToAdd.remove(addSong)
                songsAdded = songsAdded + 1
                time.sleep(int(5))
            except:
                print("song not added")

    def randomShuffle(self, token, playlistId, shuffleTime):
        # get user
        spotifyObject = Spotify(auth=token)
        spotifyUser = spotifyObject.current_user()
        username = spotifyUser['id']

        tracks = []

        songsAdded = 0
        numSongsToAdd = int(int(shuffleTime) / 2)
        playlist = spotifyObject.user_playlist_tracks(user=username, playlist_id=playlistId)
        numberOfSongs = int(playlist['total'])

        if numberOfSongs < numSongsToAdd:
            numSongsToAdd = numberOfSongs
        while songsAdded < numSongsToAdd:
            for i in range (0, 5):
                offsetNum = random.randint(0, numberOfSongs-1)
                playlist = spotifyObject.user_playlist_tracks(user=username, playlist_id=playlistId, offset=offsetNum)
                song = random.choice(playlist['items'])
                if song['track']['id'] not in tracks:
                    spotifyObject.add_to_queue(song['track']['id'])
                    tracks.append(song['track']['id'])
                    songsAdded = songsAdded + 1



    def recomendations(self, token, tracksFullList, shuffleTime):
        # get user
        spotifyObject = Spotify(auth=token)
        spotifyUser = spotifyObject.current_user()
        username = spotifyUser['id']

        tracks = []

        tracksDict = {}


        songsAdded = 0
        numSongsToAdd = int(int(shuffleTime) / 2)

        while songsAdded < numSongsToAdd:
            for i in range(0, 4):
                tracks.append(random.choice(tracksFullList))

            recs = spotifyObject.recommendations(seed_tracks=tracks)

            tracks = []

            for i in range (0, 4):
                track = random.choice(recs['tracks'])
                if track['id'] not in tracksDict.keys():
                    spotifyObject.add_to_queue(track['id'])
                    tracksDict[track['id']] = "added"
                    songsAdded = songsAdded + 1

