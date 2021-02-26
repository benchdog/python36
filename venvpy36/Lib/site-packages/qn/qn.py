import re
import csv
from scipy.misc import comb
from sklearn.decomposition import PCA
from sklearn.manifold import MDS
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from collections import OrderedDict
import numpy as np
from scipy.stats import rankdata
import pandas as pd

from .diskIO import *


def pinsplit(string,pattern,rangeValue):
	# split a string by pattern at designated point
	# e.g. pinsplit('a,b,ccd-5,6',',',3) outputs ['a,b,ccd-5','6']
	# e.g. pinaplit('a,b,ccd-5,6',',',[1,-1]) outputs ['a','b,ccd-5','6']

	patternIdx = [m.start() for m in re.finditer(pattern,string)]
	# if string doesn't contain any pattern
	if not patternIdx:
		return string
	if type(rangeValue) is int:
		if rangeValue>0:
			rangeValue = rangeValue - 1
		output = []
		output.append(string[:patternIdx[rangeValue]])
		output.append(string[patternIdx[rangeValue]+1:])
		return output
	else:
		patternCount = len(patternIdx)
		rangeValue = map(lambda x: x-1 if x>0 else patternCount+x,rangeValue)
		rangeValue = sorted(rangeValue)
		output = []
		startIdx = 0
		for val in rangeValue:
			endIdx = patternIdx[val]
			output.append(string[startIdx:endIdx])
			startIdx = endIdx+1
		output.append(string[startIdx:len(string)])
		return output


def getNumber(s):
	# parse string to number without raising error
	try:
		return float(s)
	except ValueError:
		return False

def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i+n]

copydict = lambda dct, *keys: {key: dct[key] for key in keys}

def flatList(listOfLists):
	return [item for sublist in listOfLists for item in sublist]

def printEvery(unit,n,string=None):
	if n%unit==0:
		if string:
			print(string)
		else:
			print(n)

def csv2list(pathx,delim='\t'):
    res = []
    with open(pathx,'r') as pf:
        for line in pf:
            line = line.strip('\r\n\t')
            res.append(line.split(delim))
    return res

def plotPCA(mat,labels):
    # columns are samples and rows are genes
    pca = PCA(n_components=3)
    pca.fit(mat)
    ax = scatter3(pca.components_.T,labels)
    ax.set_xlabel('PC1 ('+format(pca.explained_variance_ratio_[0],'.2')+')')
    ax.set_ylabel('PC2 ('+format(pca.explained_variance_ratio_[1],'.2')+')')
    ax.set_zlabel('PC3 ('+format(pca.explained_variance_ratio_[2],'.2')+')')

def plotMDS(distMat,groups=None,labels=None):
	# input should be distance matrix
	mds = MDS(dissimilarity="precomputed",
	max_iter=10000,eps=1e-6)
	mds.fit(distMat)
	coordinates = mds.embedding_
	fig = plt.figure()
	ax = fig.add_subplot(111)
	if groups:
		colors = ['r','y','b','c']
		uniqGroups = list(set(groups))
		groupColors = []
		for group in groups:
			idx = uniqGroups.index(group)
			groupColors.append(colors[idx])
		ax.scatter(coordinates[:,0],coordinates[:,1],c=groupColors)
	else:
		ax.scatter(coordinates[:,0],coordinates[:,1])
	if labels:
		for i,label in enumerate(labels):
			ax.annotate(label,xy=(coordinates[i,0],coordinates[i,1]),
			xytext=(coordinates[i,0],coordinates[i,1]+0.05))
	return ax


def scatter3(mat,labels):
    colors = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd", "#8c564b", "#e377c2", "#7f7f7f", "#bcbd22", "#17becf"]
    # colors = ['r','b','g','c','m','y',]
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    plottedLabels = []
    for i, label in enumerate(set(labels)):
        plottedLabels.append(label)
        idx = np.array([True if item==label else False for item in labels])
        print(label,colors[i])
        subMat = mat[idx,:]
        xs = subMat[:,0]
        ys = subMat[:,1]
        zs = subMat[:,2]
        ax.scatter(xs, ys, zs, c=colors[i], marker='o')
    plt.show()
    plt.legend(plottedLabels)
    return ax

def tidy_split(df, column, sep='|', keep=False):
    """
    Split the values of a column and expand so the new DataFrame has one split
    value per row. Filters rows where the column is missing.

    Params
    ------
    df : pandas.DataFrame
        dataframe with the column to split and expand
    column : str
        the column to split and expand
    sep : str
        the string used to split the column's values
    keep : bool
        whether to retain the presplit value as it's own row

    Returns
    -------
    pandas.DataFrame
        Returns a dataframe with the same columns as `df`.

	Author
	--------
	Daniel Himmelstein @ stackflow
    """
    indexes = list()
    new_values = list()
    df = df.dropna(subset=[column])
    for i, presplit in enumerate(df[column].astype(str)):
        values = presplit.split(sep)
        if keep and len(values) > 1:
            indexes.append(i)
            new_values.append(presplit)
        for value in values:
            indexes.append(i)
            new_values.append(value)
    new_df = df.iloc[indexes, :].copy()
    new_df[column] = new_values
    return new_df

def groupby(iterable,keyFunc):
	res = OrderedDict()
	for item in iterable:
		key = keyFunc(item)
		if key not in res:
			res[key] = []
		res[key].append(item)
	return res

def inferSchema(coll,exclude=['_id']):
	projection = {}
	if exclude:
		for key in exclude:
			projection[key] = False

	summary = {}
	total = 0
	for doc in coll.find(projection=projection):
		total+=1
		for key in doc:
			if key not in summary:
				summary[key] = {'count':0,'type':set()}
			summary[key]['count'] += 1
			summary[key]['type'].add(type(doc[key]))

	for key in summary:
		summary[key]['ratio'] = summary[key]['count']/total
		summary[key]['count'] = str(summary[key]['count'])+'/'+str(total)
		summary[key]['type'] = list(summary[key]['type'])

	return summary

def averageByIndex(series):
	return series.groupby(level=0).mean()


def addToDict(target,source,keys):
	for key in keys:
		if isinstance(key,str):
			if key in source:
				target[key] = source[key]
		else:
			if key[1] in source:
				target[key[0]] = source[key[1]]
	return target

def rpSort(objects,functions):
	# vals smaller the better
	ranks = []
	for function in functions:
		vals =[function(x) for x in objects]
		ranks.append(rankdata(vals))
	ranks = np.vstack(ranks).T
	rps = np.prod(ranks,axis=1).tolist()
	sortedObjects, _ = zip(*sorted(zip(objects,rps),key=lambda x:x[1]))
	return sortedObjects

def correct_pvals(pvalues, correction_type = "Benjamini-Hochberg"):
    """
    consistent with R - print correct_pvalues_for_multiple_testing([0.0, 0.01, 0.029, 0.03, 0.031, 0.05, 0.069, 0.07, 0.071, 0.09, 0.1])
    """
    from numpy import array, empty
    pvalues = array(pvalues)
    n = float(pvalues.shape[0])
    new_pvalues = empty(n)
    if correction_type == "Bonferroni":
        new_pvalues = n * pvalues
    elif correction_type == "Bonferroni-Holm":
        values = [ (pvalue, i) for i, pvalue in enumerate(pvalues) ]
        values.sort()
        for rank, vals in enumerate(values):
            pvalue, i = vals
            new_pvalues[i] = (n-rank) * pvalue
    elif correction_type == "Benjamini-Hochberg":
        values = [ (pvalue, i) for i, pvalue in enumerate(pvalues) ]
        values.sort()
        values.reverse()
        new_values = []
        for i, vals in enumerate(values):
            rank = n - i
            pvalue, index = vals
            new_values.append((n/rank) * pvalue)
        for i in range(0, int(n)-1):
            if new_values[i] < new_values[i+1]:
                new_values[i+1] = new_values[i]
        for i, vals in enumerate(values):
            pvalue, index = vals
            new_pvalues[index] = new_values[i]
    return new_pvalues


def vectorize(targets):
    targets_flat = flatList(targets)
    uniq = pd.Series(list(set(targets_flat)))
    arr = []
    for item in targets:
        vec = uniq.isin(item).values.tolist()
        arr.append(vec)
    mat = np.array(arr).astype(np.int)
    return mat
