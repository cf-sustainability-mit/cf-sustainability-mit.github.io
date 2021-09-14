# First created by Chris Noga and Vivian Song in 2020
# Last Update by Alejandro Diaz in 2021 September 14th contact at: adiaz@alum.mit.edu

# had to run these commands to make it work

# pip install xlrd
# pip install openpyxl

import pandas as pd
import math

import numpy as np
import random as rd
import kmeans1d
from sklearn.preprocessing import MinMaxScaler
from sklearn.cluster import KMeans


# used in run_clustering
def clean_values(values):
	clean_values = list()
	null_indices = list()
	for index, value in enumerate(values):
		if math.isnan(value) == False:
			clean_values.append(value)
		else:
			null_indices.append(index)
	return clean_values, null_indices


def run_clustering(values, unit): # returns clusters for each company
    """
    gets clusters of companies with values, leaves companies without values with blanks

    Parameters:
    company - company list of panda dataframe
    values - value list of panda dataframe

    Returns:
    list of clusters
    """
    values, null_indices = clean_values(values)
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

        sum = 0
        for key in dict:
            indices = dict[key]
            for x in indices:
                sum += (values[x]-centroids[key])**2
        if k == 1:
            lamda = (1 / 70)*sum
        sumsquare.append(sum + lamda*(k - 1))
        k += 1

    # bestK = sumsquare.index(min(sumsquare))+1 # USE THIS IF YOU WANT THE OPTIMAL # OF GROUPS
    bestK = 6                                   # USE THIS IF YOU WANT AN EXACT # OF GROUPS
    clusters, centroids = kmeans1d.cluster(values, bestK)

    # make a dictionary that contains all values for a cluster
    avg_dict = {}
    for index, cluster in enumerate(clusters):
        if cluster in avg_dict:
            avg_dict[cluster].append(int(10**values[index]))
        else:
            avg_dict[cluster] = [int(10**values[index])]
    
    # convert that dictionary into an average for each cluster
    for key in avg_dict:
        sum_ = 0
        for val in avg_dict[key]:   # sum values (for some reason the sum function was not working)
            sum_ += val
        answer = sum_ /len(avg_dict[key])
        avg_dict[key] = answer


    for index in range(len(clusters)): 		                       # make the clusters not zero-indexed
        ballpark = " ~" + str(int(avg_dict[clusters[index]])) + " " + unit # gets ballpark number for each group
        clusters[index] = str(int(clusters[index] + 1)) + ballpark

    for index in null_indices:
    	clusters.insert(index, errorVar) 	# adds null values back in

    return clusters





# specify paths to main excel sheets
path_to_master_excel_sheet = "./master-data-clusters2021.xlsx"
path_to_intensity_excel_sheet = "./Operating Costs Analysis.xlsx"
errorVar = '#NUM!'

# read in master excel sheet
read_file = pd.read_excel (path_to_master_excel_sheet)
read_file.to_csv ("raw_master.csv", index = False, header=True) # does not add a column of indices
data = pd.read_csv("raw_master.csv")

# take emissions intensity and make clusters based off of the data
column_name = "LOG(2016-2020 AVG CO2 Emissions Intensity (emissions) / ($B operating costs))"
log_intensities = data.loc[:,column_name]
cluster_numbers = run_clustering(log_intensities, "tons per dollar")
cluster_column_name = "Cluster Emissions Intensity Based on 2016-2020 LOG(AVG)"
data = data.drop(columns=cluster_column_name)
data.insert(7, cluster_column_name, cluster_numbers, True)

# take emissions and make clusters based off of the data
column_name = "LOG(2016-2020 AVG CO2 Emissions (million metric tons))"
log_emissions = data.loc[:,column_name]
cluster_numbers = run_clustering(log_emissions, "tons")
cluster_column_name = "Cluster Total Emissions Based on 2016-2020 LOG(AVG)"
data = data.drop(columns=cluster_column_name)
data.insert(4, cluster_column_name, cluster_numbers, True)
data.to_csv('final.csv')                # make a final csv to put into Tableau

data.drop(data.columns[[2, 3]], axis = 1, inplace = True)
data.to_csv('final_toshow.csv')         # make a final csv to put into the Website


# pull out data for intensities over time and condense into an excel
xls = pd.ExcelFile(path_to_intensity_excel_sheet)
data = pd.read_excel(xls, '2 Comparisons')

# delete a range of rows and columns
data = data.drop(labels=range(24,26), axis=0)
data = data.drop(labels=range(1, 14), axis=0)
data.drop(columns=data.columns[0], 
        axis=1, 
        inplace=True)
data.to_csv("final_intensities.csv", index = False, header=False) # this drops the first row and does not add a column of indices


print("Successful!")
