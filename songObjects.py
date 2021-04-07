import spotipy
class songObject:
    def __init__(self, uri, acousticness, danceability, energy, tempo, valence):
        self.uri = uri
        self.acousticness = acousticness
        self.danceability = danceability
        self.energy = energy
        self.tempo = tempo
        self.valence = valence
    def createObjectsList(self, songIDList, spotifyObject):
        songObjectsList = []
        for i in range (0, len(songIDList)):
            songFeatures = spotifyObject.audio_features(songIDList[i])
            songObject(songIDList[i], acousticness=songFeatures['acousticness'], danceability=songFeatures['danceability'],
                        energy=songFeatures['energy'], tempo=songFeatures['tempo'], valence=songFeatures['valence'])
            songObjectsList.append(songObject)
        return songObjectsList