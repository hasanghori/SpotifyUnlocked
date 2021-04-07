from sklearn.cluster import KMeans
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from matplotlib import pyplot as plt
from scipy.spatial.distance import cdist
import math
from statistics import mean
from statistics import stdev




"""
def averageError(data):
    dataset = []
    for d in data:
        dataset.append(min(d[0], d[1]))

    error = stdev(dataset) + mean(dataset)
    print("vvvvvv")
    print(stdev(dataset))
    print(mean(dataset))
    print(error)
    print("^^^^^")
    return error

data = [[0.881, 0.387, 0.374, 116.661/174.059, 0.393],
                  [0.0213, 0.716, 0.875, 109.991/174.059, 0.099],
                  [0.0403, 0.849, 0.799, 108.056/174.059, 0.561],
                  [0.0887, 0.719, 0.367, 160.044/174.059, 0.392],
                  [0.281, 0.751, 0.303, 79.533/174.059, 0.471],
                  [0.0926, 0.781, 0.512, 142.939/174.059, 0.149],
                  [0.423, 0.769, 0.541, 160.055/174.059, 0.439],
                  [0.494, 0.699, 0.521, 114.996/174.059, 0.208],
                   [0.492, 0.765, 0.497, 112.195/174.059, 0.457],
                    [0.182, 0.495, 0.726, 174.059/174.059, 0.458],
                    [0.136, 0.829, 0.539, 99.96/174.059, 0.388],
                    [0.729, 0.563, 0.322, 81.077/174.059, 0.511],
                    [0.392, 0.628, 0.407, 99.916/174.059, 0.574],
                    [0.636, 0.726, 0.375, 106.854/174.059, 0.762],
                    [0.691, 0.446, 0.189, 70.053/174.059, 0.481],
                    [0.899, 0.576, 0.173, 124.973/174.059, 0.354],
                        [0.0917, 0.761, 0.612, 77.003/174.059, 0.896],
                        [0.836, 0.455, 0.228, 118.499/174.059, 0.142],
                        [0.964, 0.66, 0.139, 79.976/174.059, 0.306],
                        [0.785, 0.732, 0.322, 114.977/174.059, 0.428],
                        [0.0371, 0.764, 0.705, 101.003/174.059, 0.672],
                        [0.756, 0.77, 0.19, 90.123/174.059, 0.918],
                        [0.609, 0.806, 0.289, 89.958/174.059, 0.457],
                           ]

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
    print("v this is k")
    print(k)
    print(sse)
    print(" ^ this is k")
    if k > 1:
        if (sse[k - 2] - sse[k - 1] < 1):
            centroidsAndError.append(centroids[k - 2])
            avgError = math.sqrt(sse[k - 2] / len(data))
            centroidsAndError.append(avgError)
            print("v if statement")
            print(k - 1)
            print(centroidsAndError)
            print("^ if statement")
            break

print("vvvvv")
print(cdist(data, centroidsAndError[0]))

print(averageError(data = cdist(data, centroidsAndError[0])))

"""
"""
print(len(data))
print(len(data[0]))
df = pd.DataFrame(data=data)
#print(df)
#plt.scatter(df['acousticness'], df['danceability'])
#plt.show()



print("struggling")
km = KMeans(n_clusters=2)
print("struggling")
y_predicted = km.fit_predict(df)
print("struggling")
print(y_predicted)
print(km.cluster_centers_)
print(km.inertia_)


df['cluster'] = y_predicted
print(df.head())

df1 = df[df.cluster==0]
df2 = df[df.cluster==1]
df3 = df[df.cluster==2]

plt.scatter(df1['tempo'], df1['valence'], color='green')
plt.scatter(df2['tempo'], df2['valence'], color='red')
plt.scatter(df3['tempo'], df3['valence'], color='black')
plt.scatter(km.cluster_centers_[:,1], km.cluster_centers_[:,3], label = 'centroid')

plt.show()

k_rng = range(1,10)
sse = []
for k in k_rng:
    km = KMeans(n_clusters=k)
    km.fit_predict(df)
    sse.append(km.inertia_)
    print(k)
    print(km.cluster_centers_)
    print(sse)
print("finalmente")
print(sse)

plt.plot(k_rng, sse)

plt.show()
"""

"""print("I am here")
        newVibe = {"name" : request.form["VibeName"], "acousticness" : request.form["acousticness"], "danceability" : request.form["danceability"],
        "energy" : request.form["energy"], "tempo" : request.form["tempo"], "valence" : request.form["valence"]}

        print(newVibe)
        session["vibe"] = newVibe
        spotifyObject = Spotify(auth=session["token"])
        spotifyUser = spotifyObject.current_user()
        spotifyID = "YOOP"
        found_user = users.query.filter_by(username = spotifyID).first() #how to make a new user!!!?
        if found_user:
            if len(found_user.mood) > 0:
                print("found user")
                print(found_user.mood)
                print("i did it")

        else:
            print("what")
            newUser = users(username=spotifyID)
            db.session.add(newUser)
            db.session.commit()
            found_user = users.query.filter_by(username=spotifyID).first()
            mood1 = Mood(request.form["VibeName"], int(request.form["acousticness"]), int(request.form["danceability"]),
                        int(request.form["energy"]), int(request.form["tempo"]), int(request.form["valence"]), user_id=found_user.id)
            print("up")
            db.session.add(mood1)
            print("yall")
            db.session.commit()
            print("work?")
        return redirect(url_for("user", usr=session["vibe"]["name"]))"""

