#import libraries
import csv

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import random as rd
import kmeans1d
from sklearn.preprocessing import MinMaxScaler
from sklearn.cluster import KMeans


#make sure there are no skipped lines / empty blanks in the Total Emissions rows
#delete Cluster column

errorVar = '#NUM!'

def load_data(filename):
    """
    Reads the contents of a file, with data given in the following tab-delimited format,
    Company   Values

    Parameters:
    filename - the name of the data file as a string

    Returns:
    a list of companies and values
    """

    data = pd.read_csv(filename)
    data.head()
    
            
    return (data)


def find_null(companies, values):
    """
    Parameters:
    company - company list of panda dataframe
    values - value list of panda dataframe

    Returns:
    list of companies with no information
    """
    nullComp = []
    nullVal = []
    for i in range(len(values)):
        if values[i] == errorVar: #100 is placeholder for blanks
            nullVal.append(values[i])
            nullComp.append(companies[i])
            #print(values[i])
        #print(values[i])
    return nullComp

def clean_data(companies, values):
    """
    Parameters:
    company - company list of panda dataframe
    values - value list of panda dataframe

    Returns:
    two lists: of companies and values that are valid and have information
    """
    cleanCompanies = list(companies)
    cleanValues  = list(values)
    for i in range(len(values)):
        if values[i] == errorVar:
            cleanCompanies.remove(companies[i])
            cleanValues.remove(values[i])

                       
    cleanValues = [float(val) for val in list(cleanValues)] # convert to float

    return cleanCompanies, cleanValues

def get_cluster(values):
    """
    gets clusters of companies with values, leaves companies without values with blanks

    Parameters:
    company - company list of panda dataframe
    values - value list of panda dataframe

    Returns:
    list of clusters
    """
    k=1
    sumsquare = []
    lamda = 0
    while k <= len(values):
        clusters, centroids = kmeans1d.cluster(values, k)

        dict = {}
        i = 1
        while i < len(clusters):
            if clusters[i] not in dict:
                dict[clusters[i]] = [i]
            else:
                    dict[clusters[i]].append(i)
            i += 1
#    print(dict)
#    print("\n")

        sum = 0
        for key in dict:
            indices = dict[key]
            for x in indices:
                sum += (values[x]-centroids[key])**2
        if k == 1:
            lamda = (1 / 70)*sum
        sumsquare.append(sum + lamda*(k - 1))
        k += 1

    #print("SumSquare: ", sumsquare)
#with open('Sumsquare.csv', 'w') as f:
 #       writer = csv.writer(f)
  #      for val in sumsquare:
   #         writer.writerow([val])

    bestK = sumsquare.index(min(sumsquare))+1
    clusters, centroids = kmeans1d.cluster(values, bestK)
    
    return clusters

def write_file(cleanComp, cleanVal, clusters, nullComp):
    """
    writes csv file with company names, their clusters. Puts companies with no info at the end

    Parameters:
    cleanComp - list of company names, all have values
    cluster - list of clusters for companies with information
    nullComp - list of company names without values

    """
    with open('cluster.csv', 'w') as f:
        writer = csv.writer(f, lineterminator = '\n')
        writer.writerow(["Company", "Value", "Cluster"])
        for i in range(len(clusters)):
            writer.writerow([cleanComp[i], cleanVal[i], clusters[i]+1]) #add one bc want to index from 1-5 instead of 0-4
        for name in nullComp:
            writer.writerow([name])
    
    
data = load_data('Total Emissions.csv')                             # loads the csv data into a pd dataframe
nullComp = find_null(data['Companies'], data['values'])             # returns list of companies without information
cleanComp, cleanVal = clean_data(data['Companies'], data['values']) # returns two lists: of companies/values that have data
clusters = get_cluster(cleanVal)                                    # returns clusters
write_file(cleanComp, cleanVal, clusters, nullComp)                 # makes a cluster csv with groups 






