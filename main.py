#import Pandas and Geopy Library
import pandas as pd
from geopy.distance import geodesic

#Method to Calculate Levenshtein Distance or Minimum Number of Updation for Similarity 
def Levenshtein_distance(str1, str2):
    #Creating a Matrix of m+1 x n+1 and initlize all the values infinity
    mat = [[float("inf")] * (len(str2) + 1) for i in range(len(str1) + 1)]
 
    for j in range(len(str2)+1):
        mat[len(str1)][j] = len(str2) - j

    for i in range(len(str1)+1):
        mat[i][len(str2)] = len(str1) - i

    #For Checking Each Character
    for i in range(len(str1)-1, -1, -1):
        for j in range(len(str2)-1, -1, -1):
    
            if str1[i] == str2[j]:            #If Charecter of both string matches
                mat[i][j] = mat[i+1][j+1]

            else:
                mat[i][j] = 1 + min(
                    mat[i][j+1],          #Deletion
                    mat[i+1][j],          #Insertion
                    mat[i+1][j+1]         #Updation
                )

    return mat[0][0]        

# Method for calculating distance between two points
def Geopy_distance(s_point, e_point):
    dis = geodesic(s_point, e_point).m
    return dis

#Read CSV File
df = pd.read_csv('assignment_data.csv')

#Make a new columns named is_similar and initilize all the values 0
df['is_similar'] = 0

#Initialize Starting Point
s_point = (df.loc[0, 'latitude'], df.loc[0, 'longitude'])
#Check each and Every Row
for i in range(1, len(df)):
    #Initilize Ending Point
    e_point = (df.loc[i, 'latitude'], df.loc[i, 'longitude'])
    #If Points are with in 200 meters
    if Geopy_distance(s_point, e_point) <= 200:
        #If Both the name are similar 
        if Levenshtein_distance(df.loc[i-1, 'name'], df.loc[i, 'name']) < 5:
            df.loc[i-1, 'is_similar'] = 1
            df.loc[i, 'is_similar'] = 1
    #Update the starting point
    s_point = e_point
print(df)
df.to_csv('output.csv')
