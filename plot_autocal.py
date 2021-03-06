import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.cm as cm
from matplotlib.colors import ListedColormap
import argparse
import math

import plot_analysis as analysis


def plot_autocal(data1, data2):

	if data2.autocal == 1:
		auto_plot_1(data1, data2)
	elif data2.autocal == 6:
		auto_plot_6(data1, data2)
	elif data2.autocal == 7:
		auto_plot_7c(data1, data2)
	elif data2.autocal == 8:
		auto_plot_8(data1, data2)


def auto_plot_1(data1, data2):
	ecm = data2.data_extra[0]

	#Extracción de la media inicial del ecm
	segundos_ini = 5
	aux=[]
	for i in range(len(ecm)):
		if i>0:
			if ecm[i]!=ecm[i-1] and data1.time[i]<segundos_ini:
				aux.append(ecm[i])
	ini = sum(aux) / len (aux)
	
	#Plot
	f, axarr = plt.subplots(3, sharex=True, figsize=(8.5,5.1))

	#Voltaje
	axarr[0].plot(data1.time, data1.v_model_scaled, label="Model neuron", linewidth=0.4)
	axarr[0].plot(data1.time, data1.v_live, label="Real neuron", linewidth=0.4)
	axarr[0].set_title("Voltage")
	axarr[0].legend(loc=1)

	axarr[1].plot(data1.time, ecm)
	axarr[1].set_title("MSE")
	axarr[1].axhline(y=ini, color='r', linestyle='--', linewidth=0.4, label="Initial MSE")
	axarr[1].axhline(y=ini*0.4, color='g', linestyle='--', linewidth=0.4, label="Target MSE")
	#axarr[1].axvline(x=segundos_ini, color='b', linestyle='--', linewidth=0.4, label="Start")
	axarr[1].legend(loc=1)

	axarr[2].plot(data1.time, data2.data_extra[1])
	axarr[2].set_title("Conductance")
	axarr[2].legend(loc=1)

	plt.xlim([0, 20])
	plt.xlabel("Time (s)")
	plt.tight_layout()
	plt.show()


def auto_plot_6(data1, data2):
	f, axarr = plt.subplots(3, sharex=True, figsize=(8.5,5.1))

	axarr[0].plot(data1.time, data1.v_model_scaled, label="Model", linewidth=0.4)
	axarr[0].plot(data1.time, data1.v_live, label="Live", linewidth=0.4)
	axarr[0].set_title("Voltage")
	axarr[0].legend()

	axarr[1].plot(data2.time, data2.data_extra[0])
	axarr[1].set_title("MSE")
	axarr[1].legend()

	axarr[2].plot(data2.time, data2.data_extra[1])
	axarr[2].set_title("Parameter")
	axarr[2].legend()

	plt.xlabel("Time (s)")
	plt.tight_layout()
	plt.show()


def auto_plot_7a(data1, data2):
	g0 = data2.data_extra[2]
	g1 = data2.data_extra[3]
	g2 = data2.data_extra[4]
	g3 = data2.data_extra[5]

	f, axarr = plt.subplots(2, sharex=True, figsize=(8.5,4.1))

	axarr[0].plot(data1.time, data1.v_model_scaled, label="Model", linewidth=0.4)
	axarr[0].plot(data1.time, data1.v_live, label="Live", linewidth=0.4)
	axarr[0].set_title("Voltage")
	axarr[0].legend()

	axarr[1].plot(data2.time, g0)
	axarr[1].plot(data2.time, g3)
	axarr[1].set_title("Conductance")
	axarr[1].legend()

	plt.xlabel("Time (s)")
	plt.tight_layout()
	plt.show()


def auto_plot_7b(data1, data2):
	segundos=100000
	old=50000
	new=150000

	matrix = [[0 for x in range(12)] for y in range(5)] 
	a=0
	b=0

	g0 = data2.data_extra[2]
	g1 = data2.data_extra[3]
	g2 = data2.data_extra[4]
	g3 = data2.data_extra[5]

	for i in range(5*12):
		matrix[a][b] = analysis.analisis_para_mapa(data1.v_live[old:new-200], data1.v_model_scaled[old:new-200], g0[old:new-200], g3[old:new-200])
		old=new
		new=old+segundos
		a+=1
		if a==5:
			a=0
			b+=1

	x=[]
	y=[]
	for i in range(5):
		for j in range(12):
			if matrix[i][j]==1:
				x.append(i)
				y.append(j)

	fig = plt.figure()  # create a figure object
	ax = fig.add_subplot(1, 1, 1)  # create an axes object in the figure
	my_xticks = ['0', '0.2', '0.4', '0.6', '0.8']
	my_yticks = ['0', '0.01', '0.02', '0.03', '0.04', '0.05', '0.06', '0.07', '0.08', '0.09', '0.10', '0.11']
	#locs, labels = plt.xticks(x, my_xticks)
	#plt.setp(labels, 'rotation')
	plt.plot(x, y, "o")
	ax.set_xticks(range(5))
	ax.set_xticklabels(my_xticks)
	ax.set_yticks(range(12))
	ax.set_yticklabels(my_yticks)
	plt.show()


def auto_plot_7c(data1, data2):
	print("Plot 7c")
	segundos=100000
	old=50000
	new=150000

	eje_x=12
	eje_y=5

	matrix = [[0 for x in range(eje_x)] for y in range(eje_y)] 
	a=0
	b=0

	g0 = data2.data_extra[2]
	g1 = data2.data_extra[3]
	g2 = data2.data_extra[4]
	g3 = data2.data_extra[5]

	result=[]
	print(g3)
	for i in range(eje_x*eje_y):
		result.append( analysis.analisis_para_mapa_2(data1.v_model_scaled[old:new-200], data1.v_live[old:new-200], g3[old:new-200], g0[old:new-200]) )
		old=new
		new=old+segundos
		a+=1
		if a==5:
			a=0
			b+=1
	print("Plot 7c.")
	result = np.array(result)
	matrix = result.reshape((5, 12))

	x=[]
	y=[]
	for i in range(5):
		for j in range(12):
			if matrix[i][j]==1:
				x.append(i)
				y.append(j)
			#if matrix[i][j]==990.7333333333331:
				#matrix[i][j]=0

	print("Plot 7c..")
	min_a=999
	for i in range(5):
		for j in range(12):
			if matrix[i][j]!=0 and matrix[i][j]<min_a:
				min_a=matrix[i][j]
	for i in range(5):
		for j in range(12):
			if matrix[i][j]==0 :
				matrix[i][j]=min_a-1


	print("Plot 7c...")
	#####Mapa
	fig, ax = plt.subplots()
	cMap = ListedColormap(['white', 'green', 'blue','red'])

	# define the colormap
	cmap = plt.cm.jet
	# extract all colors from the .jet map
	cmaplist = [cmap(i) for i in range(cmap.N)]
	# force the first color entry to be grey
	cmaplist[0] = (.5,.5,.5,1.0)
	# create the new map
	cmap = cmap.from_list('Custom cmap', cmaplist, cmap.N)


	#heatmap = ax.pcolor(matrix, cmap=plt.get_cmap('Blues'))
	heatmap = ax.pcolor(matrix, cmap=cmap)
	cbar = plt.colorbar(heatmap)
	cbar.ax.set_ylabel('Distancia entre disparos (ms)')

	my_yticks = ['0', '0.2', '0.4', '0.6', '0.8']
	my_xticks = ['0', '0.01', '0.02', '0.03', '0.04', '0.05', '0.06', '0.07', '0.08', '0.09', '0.10', '0.11']
	ax.set_xticks(np.arange(12)+0.5)
	ax.set_xticklabels(my_xticks)
	ax.set_yticks(np.arange(5)+0.5)
	ax.set_yticklabels(my_yticks)

	plt.xlabel("Conductancia sinapsis lenta")
	plt.ylabel("Conductancia sinapsis rápida")
	plt.title("Mapa de conductancias - Sinapsis química")
	plt.show()


def auto_plot_8(data1, data2):
	g0 = data2.data_extra[2]
	g1 = data2.data_extra[3]
	g2 = data2.data_extra[4]
	g3 = data2.data_extra[5]

	f, axarr = plt.subplots(3, sharex=True, figsize=(8.5,6.1))

	time_a, res_a, min_a, max_a = analysis.periodo(data1.v_live)
	time_b, res_b, min_b, max_b = analysis.periodo(data1.v_model_scaled)

	res_times = []
	#Recorremos elementos
	for i in range(len(time_a)):
		#Para cada elementos recorremos su entorno
		tmp_min = 99999
		for j in range(50):
			if i-j>=0 and i-j<len(time_b):
				tmp = abs(time_a[i]-time_b[i-j])
				if tmp<tmp_min:
					tmp_min=tmp
			if i+j<len(time_b):
				tmp = abs(time_a[i]-time_b[i+j])
				if tmp<tmp_min:
					tmp_min=tmp
		res_times.append(tmp_min)

	axarr[0].plot(data1.time, data1.v_model_scaled, label="Model", linewidth=0.4)
	axarr[0].plot(data1.time, data1.v_live, label="Live", linewidth=0.4)
	axarr[0].plot(time_a, res_a, 'o', linewidth=0.4)
	axarr[0].plot(time_b, res_b, 'o', linewidth=0.4)
	axarr[0].axhline(y=max_a, color='C1', linestyle='--', linewidth=0.2)
	axarr[0].axhline(y=min_a, color='C1', linestyle='--', linewidth=0.2)
	axarr[0].axhline(y=max_b, color='C2', linestyle='--', linewidth=0.2)
	axarr[0].axhline(y=min_b, color='C2', linestyle='--', linewidth=0.2)
	axarr[0].set_title("Voltage")
	axarr[0].legend()

	axarr[1].plot(data2.time, data2.data_extra[0])
	axarr[1].plot(data2.time, data2.data_extra[1])
	axarr[1].set_title("Conductances")
	axarr[1].legend()

	t2 = np.linspace(0, t[len(t)-1], num=len(res_times))
	axarr[2].plot(t2, res_times)
	axarr[2].set_title("Phase")
	axarr[2].legend()

	plt.xlabel("Time (s)")
	plt.tight_layout()
	plt.show()
