from string import ascii_letters
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import pyodbc
sns.set(style="white")
dbName = 'Kello'

dbTableNames = ['[SKCA]']

conn = pyodbc.connect('DRIVER={SQL Server};SERVER=dokelu.kst.fri.uniza.sk;DATABASE=' + dbName + ';UID=read;PWD=read')

for dbTableName in dbTableNames:
	a = []
	r = []
	step = 5
	for snow in np.arange(0, 56, step):
		#q = '''select [Delay] from ''' + dbTableName + ''' where (TrainType = 'Nex' or TrainType = 'Pn' or TrainType = 'Lv') and Delay < 2000 and Delay > -2000 and ROUND(Temp, 0) = ''' + str(temp)
		q = '''select [Delay] from ''' + dbTableName + ''' where Delay < 200 and Delay > -200 and Snow >= ''' + str(snow) + " and Snow < "+str((snow+step-0.1))
		print(q)
		x = pd.read_sql_query(q, conn)['Delay'].values.tolist()
		if (len(x) != 0):
			a.append(x)
			r.append(str(snow) + "-" + str((snow+step-0.1)))
	print(len(a))
	print(len(r))
	d = pd.DataFrame([*zip(*a)], columns=r)
	d.plot.box(grid='True', showfliers=False)
	plt.xlabel('Snow [mm]')
	plt.ylabel('Delay [s]')
	plt.show()