import sqlite3
import math
lines = []

with open('pairs.txt') as f:
	lines = f.readlines()
	lines = [x.strip() for x in lines] 	

def getMatchedLines():
	matched = []
	i = 1
	while (i < len(lines)):
		matched.extend(lines[i:i+300])
		i = i+600
	print "matched len ",len(matched)
	return matched
def getMisMatchedLines():
	mismatched = []
	i = 301
	while (i < len(lines)):
		mismatched.extend(lines[i:i+300])
		i = i+600
	print "mismatched len ",len(mismatched)
	return mismatched
		
def getDistance(embedding_list1,embedding_list2):

	index = 0
	dist = 0.0
	for i in embedding_list1:
		dist = dist + (( float(embedding_list1[index])- float(embedding_list2[index]) )* (float(embedding_list1[index])- float(embedding_list2[index]) ))

		#print "Fark :", float(embedding_list1[index]) - float(embedding_list2[index])
		index = index +1
	dist = math.sqrt(dist)
	return dist	
	
def evaluateMatchedFaces(database_name):
	matched = getMatchedLines()
	errors = [0]*201
	for line in matched:
		datas = line.split('\t')
		con = sqlite3.connect(database_name)
		embedding_sql_list1 = None
		embedding_sql_list2 = None
		with con:    
			cur = con.cursor()    
			cur.execute("SELECT * FROM users")
			rows = cur.fetchall()
			for row in rows:
				#print "row",row
				(id,name,embedding_sql) = row
				x  = ""
				y = ""
				if int(datas[1]) < 10:
					x = "_000"
				elif int(datas[1]) < 100:
					x =  "_00"
				else:
					x = "_0"
						
				if int(datas[2]) < 10:
					y = "_000"
				elif int(datas[2]) < 100:
					y = "_00"
				else: 
					y = "_0"
								
				if name == datas[0] + x + datas[1]: 
					embedding_sql_list1 = embedding_sql.split(',')
				if name == datas[0] + y + datas[2]:
					embedding_sql_list2 = embedding_sql.split(',')
					
				if embedding_sql_list1 != None and embedding_sql_list2 != None:
					break
		if embedding_sql_list1 != None and embedding_sql_list2 != None:			
			dist = getDistance(embedding_sql_list1, embedding_sql_list2)
			index = 0
			for count in range(50,251,1):
				if dist > count/100.0:
					errors[index] = errors[index] + 1
				index = index + 1
	return errors
	
	
def evaluateMisMatchedFaces(database_name):
	mismatched = getMisMatchedLines()

	errors = [0] * 201
	for line in mismatched:
		datas = line.split("\t")
		con = sqlite3.connect(database_name)
		embedding_sql_list1 = None
		embedding_sql_list2 = None
		with con:   
			cur = con.cursor()    
			cur.execute("SELECT * FROM users")
			rows = cur.fetchall()
			for row in rows:
				#print "row",row
				(id,name,embedding_sql) = row
				x  = ""
				y = ""
				if int(datas[1]) < 10:
					x = "_000"
				elif int(datas[1]) < 100:
					x =  "_00"
				else:
					x = "_0"
						
				if int(datas[3]) < 10:
					y = "_000"
				elif int(datas[3]) < 100:
					y = "_00"
				else: 
					y = "_0"
	
				if name == datas[0] + x + datas[1]: 
					embedding_sql_list1 = embedding_sql.split(',')
				if name == datas[2] + y + datas[3]:
					embedding_sql_list2 = embedding_sql.split(',')
					
				if 	embedding_sql_list1 != None and embedding_sql_list2 != None:
					break
		if embedding_sql_list1 != None and embedding_sql_list2 != None:			
			dist = getDistance(embedding_sql_list1, embedding_sql_list2)	
			index = 0
			for count in range(50,251,1):
				if dist < count/100.0:
					errors[index] = errors[index] + 1
				index = index + 1
	return errors

def findF1Score(matchedError,mismatchedError):
	tp = 3000.0- matchedError
	fp = float(mismatchedError)
	fn = float(matchedError)
	tn = 3000.0- mismatchedError
	precision = tp / (tp + fp) 
	recall = tp / (tp + fn)
	f1 = 2.0*(precision * recall) / (precision +recall)
	accuracy = (100.0 - ((fn + fp) * 100.0) / 6000 )
	return (f1,accuracy)
		
	
matchedErrors = evaluateMatchedFaces('Lfw_Database4.db')	
#[2683, 2660, 2628, 2581, 2548, 2507, 2469, 2415, 2357, 2308, 2242, 2201, 2139, 2075, 2029, 1968, 1918, 1866, 1820, 1762, 1700, 1634, 1576, 1506, 1434, 1379, 1329, 1269, 1218, 1154, 1107, 1052, 1000, 950, 909, 851, 799, 758, 713, 672, 649, 605, 568, 527, 494, 460, 429, 391, 361, 334, 317, 295, 272, 245, 229, 213, 202, 183, 170, 155, 140, 130, 117, 108, 103, 99, 96, 89, 83, 81, 73, 66, 62, 59, 55, 52, 46, 45, 40, 35, 33, 30, 30, 28, 27, 25, 25, 25, 22, 20, 20, 19, 18, 14, 13, 12, 11, 8, 5, 4, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

print "Matched Errors: ",matchedErrors

mismatchedErrors = evaluateMisMatchedFaces('Lfw_Database4.db')	
#mismatchedErrors = [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 3, 4, 4, 5, 6, 8, 12, 14, 16, 18, 18, 19, 24, 28, 39, 42, 46, 53, 59, 64, 70, 77, 90, 101, 112, 121, 143, 156, 170, 192, 209, 224, 250, 268, 289, 310, 334, 353, 372, 397, 424, 462, 496, 543, 576, 613, 648, 686, 724, 764, 811, 863, 914, 975, 1029, 1067, 1115, 1178, 1253, 1327, 1386, 1441, 1507, 1573, 1636, 1694, 1750, 1821, 1895, 1957, 2029, 2095, 2146, 2221, 2283, 2354, 2403, 2454, 2525, 2571, 2622, 2663, 2721, 2752, 2773, 2806, 2827, 2851, 2870, 2889, 2900, 2918, 2927, 2936, 2943, 2951, 2956, 2957, 2961, 2963, 2967, 2968, 2970, 2971, 2971, 2971, 2971, 2971, 2972, 2972, 2972, 2972, 2972, 2972, 2972, 2972, 2972, 2972, 2972, 2972, 2972, 2972, 2972, 2972, 2972, 2972, 2972, 2972, 2972, 2972, 2972, 2972, 2972, 2972, 2972, 2972, 2972, 2972, 2972, 2972, 2972, 2972, 2972, 2972, 2972, 2972, 2972, 2972, 2972, 2972, 2972, 2972, 2972, 2972, 2972, 2972, 2972, 2972, 2972, 2972, 2972, 2972, 2972, 2972, 2972, 2972, 2972, 2972, 2972, 2972, 2972, 2972, 2972, 2972, 2972, 2972, 2972, 2972]

print "Mismatched Errors: ",mismatchedErrors
f1Scores = [0]* 201
accuracy = [0]*201
index = 0

for i in range(50,251,1):
	( f1Scores[index],accuracy[index] ) = findF1Score( matchedErrors[index],mismatchedErrors[index])
	index = index + 1
	
count = 0
print "F1 Scores: "
for i in range(50,251,1):
	print "Threshold ", str(i/100.0)
	print "--F1 Score: ", f1Scores[count]
	print "--Accuracy: ", accuracy[count]
	count = count + 1


'''
Threshold  0.5
--F1 Score:  0.191136569189
--Accuracy:  55.2833333333
Threshold  0.51
--F1 Score:  0.203531876684
--Accuracy:  55.65
Threshold  0.52
--F1 Score:  0.220575155648
--Accuracy:  56.1833333333
Threshold  0.53
--F1 Score:  0.245029239766
--Accuracy:  56.9666666667
Threshold  0.54
--F1 Score:  0.261801332175
--Accuracy:  57.5166666667
Threshold  0.55
--F1 Score:  0.282198053807
--Accuracy:  58.2
Threshold  0.56
--F1 Score:  0.300679501699
--Accuracy:  58.8333333333
Threshold  0.57
--F1 Score:  0.326268823201
--Accuracy:  59.7333333333
Threshold  0.58
--F1 Score:  0.352908891328
--Accuracy:  60.7
Threshold  0.59
--F1 Score:  0.374763065259
--Accuracy:  61.5166666667
Threshold  0.6
--F1 Score:  0.403298749667
--Accuracy:  62.6166666667
Threshold  0.61
--F1 Score:  0.420526315789
--Accuracy:  63.3
Threshold  0.62
--F1 Score:  0.445882962196
--Accuracy:  64.3333333333
Threshold  0.63
--F1 Score:  0.471217524198
--Accuracy:  65.4
Threshold  0.64
--F1 Score:  0.4889224572
--Accuracy:  66.1666666667
Threshold  0.65
--F1 Score:  0.511777832879
--Accuracy:  67.1833333333
Threshold  0.66
--F1 Score:  0.53000244918
--Accuracy:  68.0166666667
Threshold  0.67
--F1 Score:  0.548488512696
--Accuracy:  68.8833333333
Threshold  0.68
--F1 Score:  0.564458263573
--Accuracy:  69.65
Threshold  0.69
--F1 Score:  0.583962264151
--Accuracy:  70.6
Threshold  0.7
--F1 Score:  0.604370060437
--Accuracy:  71.6333333333
Threshold  0.71
--F1 Score:  0.625457875458
--Accuracy:  72.7333333333
Threshold  0.72
--F1 Score:  0.643470402169
--Accuracy:  73.7
Threshold  0.73
--F1 Score:  0.664442961975
--Accuracy:  74.85
Threshold  0.74
--F1 Score:  0.68533916849
--Accuracy:  76.0333333333
Threshold  0.75
--F1 Score:  0.700972972973
--Accuracy:  76.95
Threshold  0.76
--F1 Score:  0.714713430282
--Accuracy:  77.7666666667
Threshold  0.77
--F1 Score:  0.730842305256
--Accuracy:  78.75
Threshold  0.78
--F1 Score:  0.744050104384
--Accuracy:  79.5666666667
Threshold  0.79
--F1 Score:  0.759983532318
--Accuracy:  80.5666666667
Threshold  0.8
--F1 Score:  0.771550845731
--Accuracy:  81.3166666667
Threshold  0.81
--F1 Score:  0.784850926672
--Accuracy:  82.2
Threshold  0.82
--F1 Score:  0.797130330809
--Accuracy:  83.0333333333
Threshold  0.83
--F1 Score:  0.808997632202
--Accuracy:  83.8666666667
Threshold  0.84
--F1 Score:  0.818395303327
--Accuracy:  84.5333333333
Threshold  0.85
--F1 Score:  0.830852503383
--Accuracy:  85.4166666667
Threshold  0.86
--F1 Score:  0.841843564735
--Accuracy:  86.2166666667
Threshold  0.87
--F1 Score:  0.849081613331
--Accuracy:  86.7166666667
Threshold  0.88
--F1 Score:  0.858322386939
--Accuracy:  87.4166666667
Threshold  0.89
--F1 Score:  0.866393747674
--Accuracy:  88.0333333333
Threshold  0.9
--F1 Score:  0.870096225019
--Accuracy:  88.3
Threshold  0.91
--F1 Score:  0.878254492116
--Accuracy:  88.9333333333
Threshold  0.92
--F1 Score:  0.88500727802
--Accuracy:  89.4666666667
Threshold  0.93
--F1 Score:  0.892296590294
--Accuracy:  90.05
Threshold  0.94
--F1 Score:  0.897725237328
--Accuracy:  90.4833333333
Threshold  0.95
--F1 Score:  0.902309058615
--Accuracy:  90.8333333333
Threshold  0.96
--F1 Score:  0.906558533145
--Accuracy:  91.1666666667
Threshold  0.97
--F1 Score:  0.912078307988
--Accuracy:  91.6166666667
Threshold  0.98
--F1 Score:  0.916319444444
--Accuracy:  91.9666666667
Threshold  0.99
--F1 Score:  0.917886038905
--Accuracy:  92.05
Threshold  1.0
--F1 Score:  0.91899297825
--Accuracy:  92.1166666667
Threshold  1.01
--F1 Score:  0.92085106383
--Accuracy:  92.25
Threshold  1.02
--F1 Score:  0.921621621622
--Accuracy:  92.2666666667
Threshold  1.03
--F1 Score:  0.923876592891
--Accuracy:  92.4333333333
Threshold  1.04
--F1 Score:  0.924437030859
--Accuracy:  92.45
Threshold  1.05
--F1 Score:  0.923306277953
--Accuracy:  92.2833333333
Threshold  1.06
--F1 Score:  0.922518958127
--Accuracy:  92.1666666667
Threshold  1.07
--F1 Score:  0.922698984605
--Accuracy:  92.1333333333
Threshold  1.08
--F1 Score:  0.921824104235
--Accuracy:  92.0
Threshold  1.09
--F1 Score:  0.920860980741
--Accuracy:  91.85
Threshold  1.1
--F1 Score:  0.920650249477
--Accuracy:  91.7833333333
Threshold  1.11
--F1 Score:  0.919577058635
--Accuracy:  91.6333333333
Threshold  1.12
--F1 Score:  0.918152866242
--Accuracy:  91.4333333333
Threshold  1.13
--F1 Score:  0.915769474351
--Accuracy:  91.1333333333
Threshold  1.14
--F1 Score:  0.911149551816
--Accuracy:  90.5833333333
Threshold  1.15
--F1 Score:  0.906987650461
--Accuracy:  90.0833333333
Threshold  1.16
--F1 Score:  0.900884132154
--Accuracy:  89.35
Threshold  1.17
--F1 Score:  0.897487282257
--Accuracy:  88.9166666667
Threshold  1.18
--F1 Score:  0.893415007657
--Accuracy:  88.4
Threshold  1.19
--F1 Score:  0.888990406578
--Accuracy:  87.85
Threshold  1.2
--F1 Score:  0.885226069862
--Accuracy:  87.35
Threshold  1.21
--F1 Score:  0.881345749474
--Accuracy:  86.8333333333
Threshold  1.22
--F1 Score:  0.876753207998
--Accuracy:  86.2333333333
Threshold  1.23
--F1 Score:  0.8711492891
--Accuracy:  85.5
Threshold  1.24
--F1 Score:  0.865158636898
--Accuracy:  84.7
Threshold  1.25
--F1 Score:  0.859224715826
--Accuracy:  83.9
Threshold  1.26
--F1 Score:  0.852648289797
--Accuracy:  82.9833333333
Threshold  1.27
--F1 Score:  0.846219931271
--Accuracy:  82.1
Threshold  1.28
--F1 Score:  0.842464778711
--Accuracy:  81.55
Threshold  1.29
--F1 Score:  0.837570621469
--Accuracy:  80.8333333333
Threshold  1.3
--F1 Score:  0.830510846746
--Accuracy:  79.8166666667
Threshold  1.31
--F1 Score:  0.822372975218
--Accuracy:  78.6166666667
Threshold  1.32
--F1 Score:  0.814033164314
--Accuracy:  77.3833333333
Threshold  1.33
--F1 Score:  0.807828214189
--Accuracy:  76.4333333333
Threshold  1.34
--F1 Score:  0.801996223361
--Accuracy:  75.5333333333
Threshold  1.35
--F1 Score:  0.795241913927
--Accuracy:  74.4666666667
Threshold  1.36
--F1 Score:  0.788288288288
--Accuracy:  73.3666666667
Threshold  1.37
--F1 Score:  0.78176323742
--Accuracy:  72.3166666667
Threshold  1.38
--F1 Score:  0.776329509906
--Accuracy:  71.4
Threshold  1.39
--F1 Score:  0.771021992238
--Accuracy:  70.5
Threshold  1.4
--F1 Score:  0.764004614793
--Accuracy:  69.3166666667
Threshold  1.41
--F1 Score:  0.756983240223
--Accuracy:  68.1
Threshold  1.42
--F1 Score:  0.751228114372
--Accuracy:  67.0833333333
Threshold  1.43
--F1 Score:  0.745102932002
--Accuracy:  65.95
Threshold  1.44
--F1 Score:  0.739173471913
--Accuracy:  64.8666666667
Threshold  1.45
--F1 Score:  0.734693877551
--Accuracy:  64.0333333333
Threshold  1.46
--F1 Score:  0.728136419001
--Accuracy:  62.8
Threshold  1.47
--F1 Score:  0.723141993958
--Accuracy:  61.8166666667
Threshold  1.48
--F1 Score:  0.717451191759
--Accuracy:  60.6833333333
Threshold  1.49
--F1 Score:  0.713418264079
--Accuracy:  59.8833333333
Threshold  1.5
--F1 Score:  0.709265175719
--Accuracy:  59.05
Threshold  1.51
--F1 Score:  0.703812316716
--Accuracy:  57.9166666667
Threshold  1.52
--F1 Score:  0.70003500175
--Accuracy:  57.15
Threshold  1.53
--F1 Score:  0.695894224078
--Accuracy:  56.3
Threshold  1.54
--F1 Score:  0.692600715687
--Accuracy:  55.6166666667
Threshold  1.55
--F1 Score:  0.687994496044
--Accuracy:  54.65
Threshold  1.56
--F1 Score:  0.685557586837
--Accuracy:  54.1333333333
Threshold  1.57
--F1 Score:  0.683916562179
--Accuracy:  53.7833333333
Threshold  1.58
--F1 Score:  0.68135362253
--Accuracy:  53.2333333333
Threshold  1.59
--F1 Score:  0.679732638496
--Accuracy:  52.8833333333
Threshold  1.6
--F1 Score:  0.677889504011
--Accuracy:  52.4833333333
Threshold  1.61
--F1 Score:  0.676437429538
--Accuracy:  52.1666666667
Threshold  1.62
--F1 Score:  0.674991562605
--Accuracy:  51.85
Threshold  1.63
--F1 Score:  0.674157303371
--Accuracy:  51.6666666667
Threshold  1.64
--F1 Score:  0.672796591164
--Accuracy:  51.3666666667
Threshold  1.65
--F1 Score:  0.67211829282
--Accuracy:  51.2166666667
Threshold  1.66
--F1 Score:  0.671441360788
--Accuracy:  51.0666666667
Threshold  1.67
--F1 Score:  0.670915800067
--Accuracy:  50.95
Threshold  1.68
--F1 Score:  0.670316165792
--Accuracy:  50.8166666667
Threshold  1.69
--F1 Score:  0.669941938365
--Accuracy:  50.7333333333
Threshold  1.7
--F1 Score:  0.669867143017
--Accuracy:  50.7166666667
Threshold  1.71
--F1 Score:  0.669568128557
--Accuracy:  50.65
Threshold  1.72
--F1 Score:  0.66941872141
--Accuracy:  50.6166666667
Threshold  1.73
--F1 Score:  0.669120107059
--Accuracy:  50.55
Threshold  1.74
--F1 Score:  0.669045495094
--Accuracy:  50.5333333333
Threshold  1.75
--F1 Score:  0.66889632107
--Accuracy:  50.5
Threshold  1.76
--F1 Score:  0.668821759001
--Accuracy:  50.4833333333
Threshold  1.77
--F1 Score:  0.668821759001
--Accuracy:  50.4833333333
Threshold  1.78
--F1 Score:  0.668821759001
--Accuracy:  50.4833333333
Threshold  1.79
--F1 Score:  0.668821759001
--Accuracy:  50.4833333333
Threshold  1.8
--F1 Score:  0.668821759001
--Accuracy:  50.4833333333
Threshold  1.81
--F1 Score:  0.668747213553
--Accuracy:  50.4666666667
Threshold  1.82
--F1 Score:  0.668747213553
--Accuracy:  50.4666666667
Threshold  1.83
--F1 Score:  0.668747213553
--Accuracy:  50.4666666667
Threshold  1.84
--F1 Score:  0.668747213553
--Accuracy:  50.4666666667
Threshold  1.85
--F1 Score:  0.668747213553
--Accuracy:  50.4666666667
Threshold  1.86
--F1 Score:  0.668747213553
--Accuracy:  50.4666666667
Threshold  1.87
--F1 Score:  0.668747213553
--Accuracy:  50.4666666667
Threshold  1.88
--F1 Score:  0.668747213553
--Accuracy:  50.4666666667
Threshold  1.89
--F1 Score:  0.668747213553
--Accuracy:  50.4666666667
Threshold  1.9
--F1 Score:  0.668747213553
--Accuracy:  50.4666666667
Threshold  1.91
--F1 Score:  0.668747213553
--Accuracy:  50.4666666667
Threshold  1.92
--F1 Score:  0.668747213553
--Accuracy:  50.4666666667
Threshold  1.93
--F1 Score:  0.668747213553
--Accuracy:  50.4666666667
Threshold  1.94
--F1 Score:  0.668747213553
--Accuracy:  50.4666666667
Threshold  1.95
--F1 Score:  0.668747213553
--Accuracy:  50.4666666667
Threshold  1.96
--F1 Score:  0.668747213553
--Accuracy:  50.4666666667
Threshold  1.97
--F1 Score:  0.668747213553
--Accuracy:  50.4666666667
Threshold  1.98
--F1 Score:  0.668747213553
--Accuracy:  50.4666666667
Threshold  1.99
--F1 Score:  0.668747213553
--Accuracy:  50.4666666667
Threshold  2.0
--F1 Score:  0.668747213553
--Accuracy:  50.4666666667
Threshold  2.01
--F1 Score:  0.668747213553
--Accuracy:  50.4666666667
Threshold  2.02
--F1 Score:  0.668747213553
--Accuracy:  50.4666666667
Threshold  2.03
--F1 Score:  0.668747213553
--Accuracy:  50.4666666667
Threshold  2.04
--F1 Score:  0.668747213553
--Accuracy:  50.4666666667
Threshold  2.05
--F1 Score:  0.668747213553
--Accuracy:  50.4666666667
Threshold  2.06
--F1 Score:  0.668747213553
--Accuracy:  50.4666666667
Threshold  2.07
--F1 Score:  0.668747213553
--Accuracy:  50.4666666667
Threshold  2.08
--F1 Score:  0.668747213553
--Accuracy:  50.4666666667
Threshold  2.09
--F1 Score:  0.668747213553
--Accuracy:  50.4666666667
Threshold  2.1
--F1 Score:  0.668747213553
--Accuracy:  50.4666666667
Threshold  2.11
--F1 Score:  0.668747213553
--Accuracy:  50.4666666667
Threshold  2.12
--F1 Score:  0.668747213553
--Accuracy:  50.4666666667
Threshold  2.13
--F1 Score:  0.668747213553
--Accuracy:  50.4666666667
Threshold  2.14
--F1 Score:  0.668747213553
--Accuracy:  50.4666666667
Threshold  2.15
--F1 Score:  0.668747213553
--Accuracy:  50.4666666667
Threshold  2.16
--F1 Score:  0.668747213553
--Accuracy:  50.4666666667
Threshold  2.17
--F1 Score:  0.668747213553
--Accuracy:  50.4666666667
Threshold  2.18
--F1 Score:  0.668747213553
--Accuracy:  50.4666666667
Threshold  2.19
--F1 Score:  0.668747213553
--Accuracy:  50.4666666667
Threshold  2.2
--F1 Score:  0.668747213553
--Accuracy:  50.4666666667
Threshold  2.21
--F1 Score:  0.668747213553
--Accuracy:  50.4666666667
Threshold  2.22
--F1 Score:  0.668747213553
--Accuracy:  50.4666666667
Threshold  2.23
--F1 Score:  0.668747213553
--Accuracy:  50.4666666667
Threshold  2.24
--F1 Score:  0.668747213553
--Accuracy:  50.4666666667
Threshold  2.25
--F1 Score:  0.668747213553
--Accuracy:  50.4666666667
Threshold  2.26
--F1 Score:  0.668747213553
--Accuracy:  50.4666666667
Threshold  2.27
--F1 Score:  0.668747213553
--Accuracy:  50.4666666667
Threshold  2.28
--F1 Score:  0.668747213553
--Accuracy:  50.4666666667
Threshold  2.29
--F1 Score:  0.668747213553
--Accuracy:  50.4666666667
Threshold  2.3
--F1 Score:  0.668747213553
--Accuracy:  50.4666666667
Threshold  2.31
--F1 Score:  0.668747213553
--Accuracy:  50.4666666667
Threshold  2.32
--F1 Score:  0.668747213553
--Accuracy:  50.4666666667
Threshold  2.33
--F1 Score:  0.668747213553
--Accuracy:  50.4666666667
Threshold  2.34
--F1 Score:  0.668747213553
--Accuracy:  50.4666666667
Threshold  2.35
--F1 Score:  0.668747213553
--Accuracy:  50.4666666667
Threshold  2.36
--F1 Score:  0.668747213553
--Accuracy:  50.4666666667
Threshold  2.37
--F1 Score:  0.668747213553
--Accuracy:  50.4666666667
Threshold  2.38
--F1 Score:  0.668747213553
--Accuracy:  50.4666666667
Threshold  2.39
--F1 Score:  0.668747213553
--Accuracy:  50.4666666667
Threshold  2.4
--F1 Score:  0.668747213553
--Accuracy:  50.4666666667
Threshold  2.41
--F1 Score:  0.668747213553
--Accuracy:  50.4666666667
Threshold  2.42
--F1 Score:  0.668747213553
--Accuracy:  50.4666666667
Threshold  2.43
--F1 Score:  0.668747213553
--Accuracy:  50.4666666667
Threshold  2.44
--F1 Score:  0.668747213553
--Accuracy:  50.4666666667
Threshold  2.45
--F1 Score:  0.668747213553
--Accuracy:  50.4666666667
Threshold  2.46
--F1 Score:  0.668747213553
--Accuracy:  50.4666666667
Threshold  2.47
--F1 Score:  0.668747213553
--Accuracy:  50.4666666667
Threshold  2.48
--F1 Score:  0.668747213553
--Accuracy:  50.4666666667
Threshold  2.49
--F1 Score:  0.668747213553
--Accuracy:  50.4666666667
Threshold  2.5
--F1 Score:  0.668747213553
--Accuracy:  50.4666666667
'''



