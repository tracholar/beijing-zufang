# coding:utf-8
# 基本特征提取
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt


import re
import numpy as np



def get_area(x):
	pt = re.compile(r'(\d+)㎡')
	res = pt.search(x)
	if res:
		return float(res.groups()[0])
	else:
		return np.inf
def get_state(x):
	pt = re.compile(r'^.+?-(.+?)-')
	res = pt.search(x)
	if res:
		return res.groups()[0]
	else:
		return '-'
		
def get_ts(x):
	pt = re.compile(r'(\d+室\d+厅)')
	res = pt.search(x)
	if res:
		return res.groups()[0]
	else:
		return '-'

		
def get_orient(x):
	res = re.search(r'朝(.+)$',x)
	if res:
		return res.groups()[0]
	else:
		return '-'

def GenInfo(fn):
	df = pd.read_csv(fn, sep='\t',names=['title','URL','INFO','ADDR','price'], header=False)
	df['region'] = df.ADDR.map(lambda x: x[:x.find('-')])
	df['area'] = df.INFO.map(get_area)
	df['orient'] = df.INFO.map(get_orient)
	df['type'] = df.INFO.map(lambda x: x.decode('utf-8')[:2])
	df['state'] = df.ADDR.map(get_state)
	
	return df
	