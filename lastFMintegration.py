#import spotipy
from spotipy import Spotify
#from spotipy.oauth2 import SpotifyOAuth
#from refreshToken import Refresh
#from SpotifySecret import client_id, client_secret, redirect_uri
from pprint import pprint
#import requests
#import json
from sklearn.cluster import KMeans
#import numpy as np
import pandas as pd
#import math
from scipy.spatial.distance import cdist
from statistics import mean
from statistics import stdev
#from sklearn.preprocessing import MinMaxScaler
#from matplotlib import pyplot as plt
import requests
import time


class songObject:
    def __init__(self, uri, acousticness, danceability, energy, tempo,
                 valence):
        self.uri = uri
        self.acousticness = acousticness
        self.danceability = danceability
        self.energy = energy
        self.tempo = tempo
        self.valence = valence

    def __repr__(self):
        return f"Song('{self.uri}','{self.acousticness}', '{self.danceability}', '{self.energy}', '{self.tempo}', '{self.valence}')"

class newTest:
    def genreDictionary(self, subGenre):
        genreDict = {
            "POP": "POP", "ARAB POP": "POP", "ART POP": "POP", "C - POP": "POP", "CLASSIFY": "POP", "DANCE POP": "POP",
        "ESCAPE ROOM": "POP", "EUROPOP": "POP", "HIP POP": "POP", "HYPERPOP": "POP", "INDIE CAFE POP": "POP",
        "INDIE POP": "POP", "INDIE POPTIMISM": "POP", "J - POP": "POP", "K - POP": "POP", "LEVENSLIED": "POP",
        "METROPOPOLIS": "POP", "NEO MELLOW": "POP", "NEW WAVE POP": "POP", "POP ROCK": "POP%ROCK", "POST-TEEN POP": "POP",
        "SOCIAL MEDIA POP": "POP", "SOPHISTI-POP": "POP", "TALENT SHOW": "POP", "TEEN POP": "POP", "TURKISH POP": "POP",
        "VIRAL POP": "POP", "VISPOP": "POP", "MODERN INDIE POP": "POP", "BEDROOM POP": "POP", "DESI POP": "POP",
        "ACOUSTIC POP": "POP%FOLK",
        "ELECTROPOP": "POP%DANCE/EDM", "INDIE ELECTROPOP": "POP%DANCE/EDM", "POP DANCE": "POP%DANCE/EDM", "POP EDM": "POP%DANCE/EDM",
        "VAPOR SOUL": "POP%DANCE/EDM",
        "MEXICAN POP": "POP%LATIN",
        "OAKLAND INDIE": "POP%ROCK",
        "NEW ROMANTIC": "POP%ROCK",
        "SOFT ROCK": "POP%ROCK",
        "POP R&B": "POP%R&B",
        "POP RAP": "POP%HIP HOP/RAP",

        "EDM": "DANCE/EDM", "BASS HOUSE": "DANCE/EDM", "BASS TRAP": "DANCE/EDM", "BIG ROOM": "DANCE/EDM",
        "BREAKBEAT": "DANCE/EDM", "BREAKCORE": "DANCE/EDM", "BROSTEP": "DANCE/EDM", "CHILLSTEP": "DANCE/EDM",
        "COMPLEXTRO": "DANCE/EDM", "DEEP BIG ROOM": "DANCE/EDM", "DEEP GROOVE HOUSE": "DANCE/EDM", "DEEP HOUSE": "DANCE/EDM",
        "DEEP TROPICAL HOUSE": "DANCE/EDM", "DISCO HOUSE": "DANCE/EDM", "DUBSTEP": "DANCE/EDM", "ELECTRO HOUSE": "DANCE/EDM",
        "ELECTRONIC TRAP": "DANCE/EDM", "ELECTRO SWING": "DANCE/EDM", "FILTHSTEP": "DANCE/EDM", "FUTURE BASS": "DANCE/EDM",
        "FUTURE GARAGE": "DANCE/EDM", "FUTURE HOUSE": "DANCE/EDM", "GAMING DUBSTEP": "DANCE/EDM", "GAMING EDM": "DANCE/EDM",
        "GLITCH HOP": "DANCE/EDM", "HOUSE": "DANCE/EDM", "MELODIC DUBSTEP": "DANCE/EDM", "PROGRESSIVE ELECTRO HOUSE": "DANCE/EDM",
        "PROGRESSIVE HOUSE": "DANCE/EDM", "PROGRESSIVE TRANCE": "DANCE/EDM", "SKY ROOM": "DANCE/EDM", "TECH HOUSE": "DANCE/EDM",
        "TRANCE": "DANCE/EDM", "TROPICAL HOUSE": "DANCE/EDM", "UPLIFTING TRANCE": "DANCE/EDM", "VAPOR TWITCH": "DANCE/EDM",
        "VOCAL HOUSE": "DANCE/EDM", "CANADIAN ELECTRONIC": "DANCE/EDM",

        "HIP HOP": "HIP HOP/RAP", "RAP": "HIP HOP/RAP", "ALTERNATIVE HIP HOP": "HIP HOP /RAP", "ATL HIP HOP": "HIP HOP /RAP",
        "ATL TRAP": "HIP HOP /RAP", "BOUNCE": "HIP HOP/RAP", "CHICAGO RAP": "HIP HOP/RAP", "CHRISTIAN HIP HOP": "HIP HOP/RAP",
        "CONSCIOUS HIP HOP": "HIP HOP/RAP", "CRUNK": "HIP HOP/RAP", "DIRTY SOUTH RAP": "HIP HOP/RAP",
        "EAST COAST HIP HOP": "HIP HOP/RAP", "ELECTRO": "HIP HOP/RAP", "GANGSTER RAP": "HIP HOP/RAP", "G FUNK": "HIP HOP/RAP",
        "HARDCORE HIP HOP": "HIP HOP/RAP", "HYPHY": "HIP HOP/RAP", "INDUSTRIAL HIP HOP": "HIP HOP/RAP", "JAZZ RAP": "HIP HOP/RAP",
        "MELODIC RAP": "HIP HOP/RAP", "NERDCORE": "HIP HOP/RAP", "OLD SCHOOL HIP HOP": "HIP HOP/RAP", "QUEENS HIP HOP": "HIP HOP/RAP",
        "SOUTHERN HIP HOP": "HIP HOP/RAP", "TRAP": "HIP HOP/RAP", "UNDERGROUND HIP HOP": "HIP HOP/RAP", "VAPOR TRAP": "HIP HOP/RAP",
        "WEST COAST RAP": "HIP HOP/RAP", "INDIE HIP HOP": "HIP HOP/RAP",
        "COUNTRY RAP": "HIP HOP/RAP%COUNTRY",
        "R&B": "R&B", "ALTERNATIVE R&B": "R&B", "DISCO": "R&B", "FUNK": "R&B", "GOSPEL R&B": "R&B", "INDIE R&B": "R&B",
        "INDIE SOUL": "R&B", "MOTOWN": "R&B", "NEO R&B": "R&B", "NEO SOUL": "R&B", "NEW JACK SWING": "R&B", "POP SOUL": "R & B",
        "QUIET STORM": "R&B", "SOUL": "R&B", "TRAP SOUL": "R&B", "URBAN CONTEMPORARY": "R&B",
        "CHILL R&B": "R&B",
        "BOSSA NOVA": "LATIN%JAZZ",

        "LATIN JAZZ": "LATIN%JAZZ",
        "LATIN POP": "LATIN%POP",
        "LATIN": "LATIN", "BACHATA": "LATIN", "BACHATA DOMINICANA": "LATIN", "BOLERO": "LATIN", "CHICHA": "LATIN",
        "COLOMBIAN POP": "LATIN", "CUMBIA": "LATIN", "DOMINICAN POP": "LATIN", "FLAMENCO": "LATIN", "HUAYNO": "LATIN",
        "LATIN ALTERNATIVE": "LATIN", "LATIN ARENA POP": "LATIN", "LATIN HIP HOP": "LATIN", "LATIN ROCK": "LATIN",
        "MARIACHI": "LATIN", "MERENGUE": "LATIN", "NEOTANGO": "LATIN", "NUEVO FLAMENCO": "LATIN", "PERREO": "LATIN",
        "POP REGGAETON": "LATIN", "PUERTO RICAN POP": "LATIN", "RANCHERA": "LATIN", "REGGAETON": "LATIN", "REGGAETON COLOMBIANO": "LATIN",
        "REGGAETON FLOW": "LATIN", "ROCK EN ESPANOL": "LATIN", "SALSA": "LATIN", "SPANISH POP": "LATIN", "SPANISH POP ROCK": "LATIN",
        "TANGO": "LATIN", "TEJANO": "LATIN", "TIMBA": "LATIN", "TRAP LATINO": "LATIN", "TROPICAL": "LATIN", "TWOUBADOU": "LATIN",
        "ZOUK": "LATIN",

        "MELLOW GOLD": "ROCK%FOLK",

        "ROCK": "ROCK", "ACID ROCK": "ROCK", "ALBUM ROCK": "ROCK", "ALTERNATIVE ROCK": "ROCK", "ART ROCK": "ROCK",
        "BRITISH INVASION": "ROCK", "BRITPOP": "ROCK", "CLASSIC ROCK": "ROCK", "DANCE - PUNK": "ROCK", "DANCE ROCK": "ROCK",
        "GARAGE ROCK": "ROCK", "GLAM ROCK": "ROCK", "GRUNGE": "ROCK", "HEARTLAND ROCK": "ROCK", "INDIE ROCK": "ROCK",
        "MATH ROCK": "ROCK", "MODERN ALTERNATIVE ROCK": "ROCK", "MODERN BLUES ROCK": "ROCK", "MODERN ROCK": "ROCK",
        "NEW WAVE": "ROCK", "NOISE ROCK": "ROCK", "PERMANENT WAVE": "ROCK", "POST-GRUNGE": "ROCK", "PSYCHEDELIC ROCK": "ROCK",
        "ROCK-AND-ROLL": "ROCK", "ROCKABILLY": "ROCK", "SOUTHERN ROCK": "ROCK", "SYMPHONIC ROCK": "ROCK",

        "ROOTS ROCK": "ROCK%FOLK",

        "METAL": "METAL", "ALTERNATIVE METAL": "METAL", "BLACK METAL": "METAL", "BRUTAL DEATH METAL": "METAL",
        "CROSSOVER THRASH": "METAL", "DARK BLACK METAL": "METAL", "DEATH METAL": "METAL", "DOOM METAL": "METAL",
        "FOLK METAL": "METAL", "GERMAN METAL": "METAL", "GERMAN POWER METAL": "METAL", "GLAM METAL": "METAL", "GOTHIC METAL": "METAL",
        "GROOVE METAL": "METAL", "HARD ROCK": "METAL", "MELODIC DEATH METAL": "METAL", "MELODIC METAL": "METAL",
        "NEO-TRAD METAL": "METAL", "NEO CLASSICAL METAL": "METAL", "NU METAL": "METAL", "NWOTHM": "METAL",
        "OLD SCHOOL THRASH": "METAL", "POWER METAL": "METAL", "PROGRESSIVE METAL": "METAL", "SPEED METAL": "METAL",
        "SWEDISH METAL": "METAL", "SYMPHONIC BLACK METAL": "METAL", "SYMPHONIC METAL": "METAL", "TECHNICAL DEATH METAL": "METAL",
        "THRASH METAL": "METAL", "US POWER METAL": "METAL",

        "COUNTRY": "COUNTRY", "ALBERTA COUNTRY": "COUNTRY", "ALTERNATIVE COUNTRY": "COUNTRY", "AUSTRALIAN COUNTRY": "COUNTRY",
        "BAKERSFIELD SOUND": "COUNTRY", "BLUEGRASS": "COUNTRY", "BLUEGRASS GOSPEL": "COUNTRY", "CAJUN": "COUNTRY",
        "CLASSIC COUNTRY POP": "COUNTRY", "CONTEMPORARY COUNTRY": "COUNTRY", "COUNTRY DAWN": "COUNTRY", "COUNTRY GOSPEL": "COUNTRY",
        "COUNTRY POP": "COUNTRY", "COUNTRY ROAD": "COUNTRY", "COUNTRY ROCK": "COUNTRY", "COWBOY WESTERN": "COUNTRY",
        "COWPUNK": "COUNTRY", "DANSBAND": "COUNTRY", "HONKY TONK": "COUNTRY", "KENTUCKY ROOTS": "COUNTRY",
        "MODERN COUNTRY ROCK": "COUNTRY", "NASHVILLE SOUND": "COUNTRY", "NEO-TRADITIONAL BLUEGRASS": "COUNTRY",
        "NEO - TRADITIONAL COUNTRY": "COUNTRY", "OKLAHOMA COUNTRY": "COUNTRY", "OUTLAW COUNTRY": "COUNTRY",
        "PROGRESSIVE BLUEGRASS": "COUNTRY", "QUEER COUNTRY": "COUNTRY", "RED DIRT": "COUNTRY", "SERTANEJO": "COUNTRY",
        "TEXAS COUNTRY": "COUNTRY", "TRADITIONAL BLUEGRASS": "COUNTRY", "TRADITIONAL COUNTRY": "COUNTRY",
        "TRUCK-DRIVING COUNTRY": "COUNTRY", "WESTERN SWING": "COUNTRY", "WYOMING ROOTS": "COUNTRY",

        "NEW AMERICANA": "COUNTRY%FOLK",

        "FOLK": "FOLK", "AMERICAN FOLK REVIVAL": "FOLK", "ANTI-FOLK": "FOLK", "APPALACHIAN FOLK": "FOLK",
        "CONTEMPORARY FOLK": "FOLK", "ECTOFOLK": "FOLK", "FOLK ROCK": "FOLK", "FREAK FOLK": "FOLK", "INDIE FOLK": "FOLK",
        "LILITH": "FOLK", "MEDIEVAL FOLK": "FOLK", "MELANCHOLIA": "FOLK", "MODERN FOLK ROCK": "FOLK", "PSYCHEDELIC FOLK": "FOLK",
        "SINGER-SONGWRITER": "FOLK", "STOMP AND HOLLER": "FOLK", "TRADITIONAL FOLK": "FOLK",

        "CLASSICAL": "CLASSICAL", "AVANT-GARDE": "CLASSICAL", "BAROQUE": "CLASSICAL", "CHAMBER ENSEMBLE": "CLASSICAL",
        "CHAMBER ORCHESTRA": "CLASSICAL", "CHORAL": "CLASSICAL", "CLASSICAL CELLO": "CLASSICAL", "CLASSICAL ERA": "CLASSICAL",
        "CLASSICAL GUITAR": "CLASSICAL", "CLASSICAL PIANO": "CLASSICAL", "CLASSICAL SOPRANO": "CLASSICAL",
        "COMPOSITIONAL AMBIENT": "CLASSICAL", "CONTEMPORARY CLASSICAL": "CLASSICAL", "EARLY MODERN CLASSICAL": "CLASSICAL",
        "EARLY MUSIC": "CLASSICAL", "EARLY MUSIC CHOIR": "CLASSICAL", "EARLY MUSIC ENSEMBLE": "CLASSICAL",
        "EARLY ROMANTIC ERA": "CLASSICAL", "HISTORICALLY INFORMED PERFORMANCE": "CLASSICAL", "IMPRESSIONISM": "CLASSICAL",
        "ITALIAN BAROQUE": "CLASSICAL", "LATE ROMANTIC ERA": "CLASSICAL", "MEDIEVAL": "CLASSICAL", "MINIMALISM": "CLASSICAL",
        "NEOCLASSICISM": "CLASSICAL", "OPERA": "CLASSICAL", "ORCHESTRA": "CLASSICAL", "POLYPHONY": "CLASSICAL",
        "POST-ROMANTIC ERA": "CLASSICAL", "RENAISSANCE": "CLASSICAL", "SERIALISM": "CLASSICAL", "STRING QUARTET": "CLASSICAL",
        "VIOLIN": "CLASSICAL",

        "JAZZ": "JAZZ", "ACID JAZZ": "JAZZ", "AVANT-GARDE JAZZ": "JAZZ", "BEBOP": "JAZZ", "CLASSICAL JAZZ FUSION": "JAZZ",
        "CONTEMPORARY JAZZ": "JAZZ", "CONTEMPORARY POST-BOP": "JAZZ", "COOL JAZZ": "JAZZ", "DIXIELAND": "JAZZ",
        "ECM-STYLE JAZZ": "JAZZ", "ETHIO-JAZZ": "JAZZ", "FREE IMPROVISATION": "JAZZ", "FREE JAZZ": "JAZZ", "GYPSY JAZZ": "JAZZ",
        "HARD BOP": "JAZZ", "HARLEM RENAISSANCE": "JAZZ", "INDIE JAZZ": "JAZZ", "JAZZ CLARINET": "JAZZ", "JAZZ DOUBLE BASS": "JAZZ",
        "JAZZ DRUMS": "JAZZ", "JAZZ FUNK": "JAZZ", "JAZZ FUSION": "JAZZ", "JAZZ GUITAR": "JAZZ", "JAZZ PIANO": "JAZZ",
        "JAZZ QUARTET": "JAZZ", "JAZZ SAXOPHONE": "JAZZ", "JAZZ TRIO": "JAZZ", "JAZZ TRUMPET": "JAZZ", "JAZZ VIBRAPHONE": "JAZZ",
        "MODERN JAZZ PIANO": "JAZZ", "RAGTIME": "JAZZ", "SAMBA - JAZZ": "JAZZ", "SMOOTH JAZZ": "JAZZ", "SOUL JAZZ": "JAZZ",
        "SPIRITUAL JAZZ": "JAZZ", "STRAIGHT-AHEAD JAZZ": "JAZZ", "STRIDE": "JAZZ", "VINTAGE JAZZ": "JAZZ",

        "BLUES ROCK": "BLUES%ROCK",
        "BLUES": "BLUES", "ACOUSTIC BLUES": "BLUES", "BRITISH BLUES": "BLUES", "CANADIAN BLUES": "BLUES", "CHICAGO BLUES": "BLUES",
        "COUNTRY BLUES": "BLUES", "DELTA BLUES": "BLUES", "ELECTRIC BLUES": "BLUES", "GOSPEL BLUES": "BLUES", "HARMONICA BLUES": "BLUES",
        "JAZZ BLUES": "BLUES", "JUMP BLUES": "BLUES", "LOUISIANA BLUES": "BLUES", "MEMPHIS BLUES": "BLUES", "MODERN BLUES": "BLUES",
        "NEW ORLEANS BLUES": "BLUES", "PIANO BLUES": "BLUES", "PIEDMONT BLUES": "BLUES", "POWER BLUES-ROCK": "BLUES",
        "PRE-WAR BLUES": "BLUES", "PUNK BLUES": "BLUES", "RHYTHM AND BLUES": "BLUES", "SOUL BLUES": "BLUES", "SWAMP BLUES": "BLUES",
        "TEXAS BLUES": "BLUES", "TRADITIONAL BLUES": "BLUES",

        "VOCAL JAZZ": "EASY LISTENING%JAZZ",

        "EASY LISTENING": "EASY LISTENING", "ADULT STANDARDS": "EASY LISTENING", "BALLROOM": "EASY LISTENING",
        "BIG BAND": "EASY LISTENING", "BRILL BUILDING POP": "EASY LISTENING", "CLASSIC SOUNDTRACK": "EASY LISTENING",
        "SOUNDTRACK": "EASY LISTENING", "DEEP ADULT STANDARDS": "EASY LISTENING", "EXOTICA": "EASY LISTENING",
        "HOLLYWOOD": "EASY LISTENING", "LIGHT MUSIC": "EASY LISTENING", "LOUNGE": "EASY LISTENING", "MOVIE TUNES": "EASY LISTENING",
        "ROMANTICO": "EASY LISTENING", "SPACE AGE POP": "EASY LISTENING", "SWING": "EASY LISTENING", "TORCH SONG": "EASY LISTENING",

        "SOUNDTRACK": "SOUNDTRACK%EASY LISTENING",

        "NEW AGE": "NEW AGE", "AMBIENT": "NEW AGE", "BACKGROUND MUSIC": "NEW AGE", "BACKGROUND PIANO": "NEW AGE",
        "BOW POP": "NEW AGE", "CALMING INSTRUMENTAL": "NEW AGE", "FOURTH WORLD": "NEW AGE", "HEALING": "NEW AGE", "MEDITATION": "NEW AGE",
        "NEO-CLASSICAL": "NEW AGE", "NEOCLASSICAL DARKWAVE": "NEW AGE", "NEW AGE PIANO": "NEW AGE", "OPERATIC POP": "NEW AGE",
        "RELAXATIVE": "NEW AGE", "SLEEP": "NEW AGE", "WORLD MEDITATION": "NEW AGE",

        "FOLKMUSIK": "WORLD / TRADITIONAL FOLK", "WORLD": "WORLD / TRADITIONAL FOLK", "AFROPOP": "WORLD / TRADITIONAL FOLK",
        "ARAB FOLK": "WORLD / TRADITIONAL FOLK", "CANZONE GENOVESE": "WORLD / TRADITIONAL FOLK", "CELTIC": "WORLD / TRADITIONAL FOLK",
        "CELTIC HARP": "WORLD / TRADITIONAL FOLK", "CORSICAN FOLK": "WORLD / TRADITIONAL FOLK", "DESERT BLUES": "WORLD / TRADITIONAL FOLK",
        "FINNISH FOLK": "WORLD / TRADITIONAL FOLK", "GREEK FOLK": "WORLD / TRADITIONAL FOLK", "GREEK GUITAR": "WORLD / TRADITIONAL FOLK",
        "GRIOT": "WORLD / TRADITIONAL FOLK", "IRISH FOLK": "WORLD / TRADITIONAL FOLK", "KUNDIMAN": "WORLD / TRADITIONAL FOLK",
        "MALIAN BLUES": "WORLD / TRADITIONAL FOLK", "MANDE POP": "WORLD / TRADITIONAL FOLK", "MIN 'YO": "WORLD/TRADITIONAL FOLK",
        "NATIVE AMERICAN": "WORLD / TRADITIONAL FOLK",
        "NEO KYMA": "WORLD / TRADITIONAL FOLK", "NORDIC FOLK": "WORLD / TRADITIONAL FOLK", "NORWEGIAN FOLK": "WORLD / TRADITIONAL FOLK",
        "RABINDRA SANGEET": "WORLD / TRADITIONAL FOLK",
        "RUSSIAN FOLK": "WORLD / TRADITIONAL FOLK", "SCOTTISH FOLK": "WORLD / TRADITIONAL FOLK", "SHAMANIC": "WORLD / TRADITIONAL FOLK",
        "SUFI CHANT": "WORLD / TRADITIONAL FOLK", "SWEDISH FIDDLE": "WORLD / TRADITIONAL FOLK", "TATAR FOLK": "WORLD / TRADITIONAL FOLK",
        "YOIK": "WORLD / TRADITIONAL FOLK"
        }

        if subGenre not in genreDict.keys():
            print(subGenre)
            genreGrouping = input("what genre should this be placed in ")
            genreDict[subGenre] = genreGrouping

        return genreDict[subGenre]


    def getPlaylistImage(self, token):
        spotifyObject = Spotify(auth=token)
        spotifyUser = spotifyObject.current_user()
        username = spotifyUser['id']
        playlistDetails = [[0 for playlists in range(3)] for items in range(3)]
        for count in range(0, 3):
            try:
                response = spotifyObject.user_playlists(user=username, limit=1, offset=count)

                playlistID = response['items'][0]['id']
                playlistDetails[count][0] = spotifyObject.playlist_cover_image(playlist_id=playlistID) #img
                playlistDetails[count][1] = response['items'][0]['name'] #name
                playlist = spotifyObject.user_playlist_tracks(user=username, playlist_id=playlistID)
                playlistDetails[count][2] = playlist['total'] #numSongs
            except:
                if count == 0:
                    playlistID = '37i9dQZF1DWX1UA045EoPG'
                    playlistDetails[count][0] = spotifyObject.playlist_cover_image(playlist_id=playlistID)  #img
                    playlistDetails[count][1] = 'Summer Heat' #name
                    playlistDetails[count][2] = int(50)  #numSongs
                if count == 1:
                    playlistID = '7wAMnjdymZlCELAaCaoLys'
                    playlistDetails[count][0] = spotifyObject.playlist_cover_image(playlist_id=playlistID)  # img
                    playlistDetails[count][1] = 'Unlocked - Denzel Curry'  # name
                    playlistDetails[count][2] = int(8)  # numSongs
                if count == 2:
                    playlistID = '6BZoqSiFq6x1m7ceWQjCFP'
                    playlistDetails[count][0] = spotifyObject.playlist_cover_image(playlist_id=playlistID)  # img
                    playlistDetails[count][1] = 'For The Throne'  # name
                    playlistDetails[count][2] = int(14)  # numSongs
                #break


        return playlistDetails

    def loadPlaylists(self, token):
        spotifyObject = Spotify(auth=token)
        spotifyUser = spotifyObject.current_user()
        username = spotifyUser['id']
        count = int(0)
        playlistDict = {}
        response = spotifyObject.user_playlists(user=username, offset=count)

        while count < response["total"]:
            response = spotifyObject.user_playlists(user=username, offset=count)
            count = count + 50
            for x in range(0, len(response['items'])):
                playlistDict[response['items'][x]['name']] = response['items'][x]['id']

        return playlistDict

    def listToStringEncoder(self, list):
        string = ""
        count = 1
        for element in list[0]:
            string = string + "|"
            for val in range(0, 4):
                #string = string + str(element[val]) + ", "
                string = string + str(round(element[val], 4)) + ", "
            #string = string + str(element[val + 1]) + "|"
            string = string + str(round(element[val + 1], 4)) + "|"
            count = count + 1
        string = string + "|" + str(list[1])

        self.listToStringDecoder(string)
        return string

    def listToStringDecoder(self, string):
        clusters = []
        clustersAndError = []
        array = string.split("|")
        i = 1
        while i < len(array) - 2:
            strings = array[i].split(", ")
            for j in range(0, len(strings)):
                strings[j] = float(strings[j])
            clusters.append(strings)
            i = i + 2
        clustersAndError.append(clusters)
        clustersAndError.append(float(array[len(array) - 1]))
        return clustersAndError


    def averageError(self, data):
        dataset = []
        for d in data:
            dataset.append(min(d))

        #error = stdev(dataset) + mean(dataset)
        #testing accuracy
        #error = mean(dataset)
        error = mean(dataset) #+ stdev(dataset)
        return error

    def newKMeansVibe(self, data):
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
                if (sse[k - 2] - sse[k - 1] < 1):
                    centroidsAndError.append(centroids[k - 2])
                    avgError = self.averageError(data=cdist(data, centroidsAndError[0], 'euclidean'))
                    #avgError =  math.sqrt(sse[k-2] / len(data))
                    centroidsAndError.append(round(avgError, 4))
                    numClusterFound = True
                    break

        if (numClusterFound == False):
            centroidsAndError.append(centroids[int(len(data) / 3) - 2])
            avgError = self.averageError(data=cdist(data, centroidsAndError[0], 'euclidean'))
            centroidsAndError.append(avgError)

        #return self.listToStringEncoder(centroidsAndError)
        return self.newListToStringEncoder(centroidsAndError)

    def newListToStringEncoder(self, list):
        string = ""
        count = 1
        for element in list[0]:
            string = string + "|"
            for val in range(0, 7):
                #string = string + str(element[val]) + ", "
                string = string + str(round(element[val], 4)) + ", "
            #string = string + str(element[val + 1]) + "|"
            string = string + str(round(element[val + 1], 4)) + "|"
            count = count + 1
        string = string + "|" + str(list[1])

        self.listToStringDecoder(string)
        return string

    def newListToStringDecoder(self, string):
        clusters = []
        clustersAndError = []
        array = string.split("|")
        i = 1
        while i < len(array) - 2:
            strings = array[i].split(", ")
            for j in range(0, len(strings)):
                strings[j] = float(strings[j])
            clusters.append(strings)
            i = i + 2
        clustersAndError.append(clusters)
        clustersAndError.append(float(array[len(array) - 1]))
        return clustersAndError

    def newCreateVibe(self, playlistName, token):
        # find playlist
        spotifyObject = Spotify(auth=token)
        spotifyUser = spotifyObject.current_user()
        username = spotifyUser['id']
        # more efficient by storing the spotifyObject as a static instance variable and use that in the code?

        # find playlist
        playlistID = playlistName

        #create genre dictionary
        genreDict = {}

        # get songs from playlist
        playlistSongs = spotifyObject.user_playlist_tracks(user=username, playlist_id=playlistID)
        numberOfSongs = int(playlistSongs['total'])
        totalAdded = int(0)
        songObjectsList = []
        while (numberOfSongs > totalAdded):
            playlistSongs = spotifyObject.user_playlist_tracks(user=username, playlist_id=playlistID, offset=totalAdded)
            for i in range(0, len(playlistSongs['items'])):
                try:
                    songURI = playlistSongs['items'][i]['track']['uri']
                    songID = playlistSongs['items'][i]['track']['id']
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

        # send it to kmeans and get centroidsAndError
        #print(genreDict)

        self.refineGenreVibe(genreDict=genreDict)
        centroidsAndError = self.newKMeansVibe(data=songObjectsList)
        centroidsAndError_GenreDict = [centroidsAndError, genreDict]
        return centroidsAndError_GenreDict

    def refineGenreVibe(self, genreDict):
        #calls genre dict and figures out the greater genres involved
        #once it figures that out it will ask the user if they want to include certain sub genres
        #using info it will refine and return a new trimmed genre dict
        superGenreDict = {}
        genreGrouping = {}
        numGenres = int(0)
        for key in genreDict:
            superGenre = self.genreDictionary(key.upper())
            genreGrouping[key] = superGenre
            numGenres = numGenres + genreDict[key]
            if superGenre in superGenreDict.keys():
                superGenreDict[superGenre] = superGenreDict[superGenre] + genreDict[key]
            else:
                superGenreDict[superGenre] = genreDict[key]

        print(genreGrouping)

        for key in superGenreDict:
            if superGenreDict[key] / numGenres < 0.2:
                response = input("do you want " + key + " in the vibe?")
                if response == 'n':
                    for key2 in genreGrouping:
                        if genreGrouping[key2] == key:
                            del genreDict[key2]
        print(superGenreDict)
        print(genreDict)

    def genreVibe(self, spotifyObject, songId, genreDict):
        #print("in genre Vibe")
        #get song
        song = spotifyObject.track(songId)
        #print("got past track part")

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

    def songGenreInVibe (self, spotifyObject, songId, songGenreDict, vibeGenreDict):
        #print("in the genreVibe ting")
        songGenreDict = {}
        songGenreDict = self.genreVibe(spotifyObject=spotifyObject, songId=songId, genreDict=songGenreDict)
        #print("got through genreVibe")

        #print(songGenreDict)

        #print(vibeGenreDict)

        genre_exists_in_vibe = False

        for key in songGenreDict:
            #print("inside key songData")
            #print(key)
            if key in vibeGenreDict.keys():
                #print("inside if statement for haskey")
                #if key != 'pop rap':
                print(key)
                genre_exists_in_vibe = True
                break

        #print(genre_exists_in_vibe)
        return genre_exists_in_vibe

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
        vibeGenres = genreDict
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
                    #print("got here")

                    if (self.songGenreInVibe(spotifyObject=spotifyObject, songId=songId, songGenreDict=songGenreDict,
                                             vibeGenreDict=vibeGenres) == True):
                        #print("in if statement")
                        print(playlist['items'][i]['track']['name'])
                        song = [[songFeatures[0]['acousticness'],
                                   songFeatures[0]['danceability'], songFeatures[0]['energy'],
                                   songFeatures[0]['instrumentalness'], songFeatures[0]['liveness'],
                                songFeatures[0]['speechiness'], round(songFeatures[0]['tempo'] / 180, 6),
                                songFeatures[0]['valence']]]
                        distArray = cdist(song, clustersAndError[0], 'euclidean')
                        dist = min(distArray[0])
                        if float(dist) < float(clustersAndError[1]):
                            songsToAdd.append(songURI)
                            print("this was added")
                            print(playlist['items'][i]['track']['name'])
                        if len(songsToAdd) == 100 or i == len(playlist['items']) - 1:
                            listOfAllSongsToAdd.append(songsToAdd)
                            songsToAdd = []
                except:
                    print("spotify does not have this song anymore. Sorry")
            totalAdded = totalAdded + 100

        if (len(listOfAllSongsToAdd) < 1):
            print("in this part somehow")
            spotifyObject.user_playlist_add_tracks(user=username, playlist_id=playlist_to_add_to, tracks=songsToAdd)
        else:
            for songs in listOfAllSongsToAdd:
                spotifyObject.user_playlist_add_tracks(user=username, playlist_id=playlist_to_add_to, tracks=songs)
                time.sleep(5)

    def testPlaylist(self, token, playlistName):
        # get user
        spotifyObject = Spotify(auth=token)
        spotifyUser = spotifyObject.current_user()
        username = spotifyUser['id']

        #find playlist
        playlistID = playlistName

        """tracks = spotifyObject.user_playlist_tracks(user=username, playlist_id=playlistID)

        for i in range(0, len(tracks['items'])):
            songURI = tracks['items'][i]['track']['uri']
            print(tracks['items'][i]['track']['name'])
            #songFeatures = spotifyObject.audio_features(songURI)
            #pprint(songFeatures)"""

        playlist = spotifyObject.user_playlist_tracks(user=username, playlist_id=playlistID)
        numberOfSongs = int(playlist['total'])
        totalAdded = int(0)
        while (numberOfSongs > totalAdded):
            playlist = spotifyObject.user_playlist_tracks(user=username, playlist_id=playlistID, offset=totalAdded)
            for i in range(0, len(playlist['items'])):
                try:
                    print(playlist['items'][i]['track']['name'])
                except:
                    print("spotify does not have this song anymore. Sorry")
            totalAdded = totalAdded + 100

    def getGenres (self, token, playlistName):
        # get user
        spotifyObject = Spotify(auth=token)
        spotifyUser = spotifyObject.current_user()
        username = spotifyUser['id']

        # find playlist
        playlistID = playlistName

        playlist = spotifyObject.user_playlist_tracks(user=username, playlist_id=playlistID)
        numberOfSongs = int(playlist['total'])
        totalAdded = int(0)
        while (numberOfSongs > totalAdded):
            playlist = spotifyObject.user_playlist_tracks(user=username, playlist_id=playlistID, offset=totalAdded)
            for i in range(0, len(playlist['items'])):
                print(playlist['items'][i]['track']['name'])
                songId = playlist['items'][i]['track']['id']
                song = spotifyObject.track(songId)
                for artist in song['artists']:
                    artistInfo = spotifyObject.artist(artist_id=artist['id'])
                    genres = artistInfo['genres']
                    pprint(genres)
                songURI = playlist['items'][i]['track']['uri']
                songFeatures = spotifyObject.audio_features(songURI)
                song = [songFeatures[0]['acousticness'],
                                   songFeatures[0]['danceability'], songFeatures[0]['energy'],
                                   songFeatures[0]['instrumentalness'], songFeatures[0]['liveness'],
                                songFeatures[0]['speechiness'], round(songFeatures[0]['tempo'] / 180, 6),
                                songFeatures[0]['valence']]
                print(song)
            totalAdded = totalAdded + 100


    def buildPlaylist(self, playlistName, clustersAndError, token, newPlaylist):
        #get user
        spotifyObject = Spotify(auth=token)
        spotifyUser = spotifyObject.current_user()
        username = spotifyUser['id']

        # find playlist
        playlistID = playlistName

        #find playlist where we will add songs
        playlist_to_add_to = newPlaylist

        #get songs
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
                    songFeatures = spotifyObject.audio_features(songURI)
                    song = [[songFeatures[0]['acousticness'], songFeatures[0]['danceability'],
                            songFeatures[0]['energy'], round(songFeatures[0]['tempo'] / 200, 6),
                            songFeatures[0]['valence']]]
                    distArray = cdist(song, clustersAndError[0], 'euclidean')
                    dist = min(distArray[0])
                    if float(dist) < float(clustersAndError[1]):
                        songsToAdd.append(songURI)
                    if len(songsToAdd) == 100 or i == len(playlist['items']) - 1:
                        listOfAllSongsToAdd.append(songsToAdd)
                        songsToAdd = []
                except:
                    print("spotify does not have this song anymore. Sorry")
            totalAdded = totalAdded + 100


        if (len(listOfAllSongsToAdd) < 1):
            spotifyObject.user_playlist_add_tracks(user=username, playlist_id=playlist_to_add_to, tracks=songsToAdd)
        else:
            for songs in listOfAllSongsToAdd:
                spotifyObject.user_playlist_add_tracks(user=username, playlist_id=playlist_to_add_to, tracks=songs)


