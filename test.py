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
	return matched
def getMisMatchedLines():
	mismatched = []
	i = 301
	while (i < len(lines)):
		mismatched.extend(lines[i:i+300])
		i = i+600
	return mismatched
	


	
def getDistance(embedding_list1,embedding_list2):
	#print "embedding_list1" ,embedding_list1
	#print "embedding_list2" ,embedding_list2
	index = 0
	dist = 0.0
	for i in embedding_list1:
		dist = dist + (( float(embedding_list1[index])- float(embedding_list2[index]) )* (float(embedding_list1[index])- float(embedding_list2[index]) ))

		#print "Fark :", float(embedding_list1[index]) - float(embedding_list2[index])
		index = index +1
	dist = math.sqrt(dist)
	#print "Dist: ", dist
	return dist	
	




def evaluateMatchedFaces(database_name):
	matched = getMatchedLines()
	error60 = error65 = error70 = error75 = error80 = error85 = error90 = error95 = error96 = error97 = error98 = error99 = error100 = 0
	error105 = error110 = error115 = error120 = error1242 = 0
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
								
				#print "Matched name",name
				#print "Matched dataName", (datas[0] + x + datas[2])
				if name == datas[0] + x + datas[1]: 
					embedding_sql_list1 = embedding_sql.split(',')
				if name == datas[0] + y + datas[2]:
					embedding_sql_list2 = embedding_sql.split(',')
					
				if 	embedding_sql_list1 != None and embedding_sql_list2 != None:
					break
		if embedding_sql_list1 != None and embedding_sql_list2 != None:			
			dist = getDistance(embedding_sql_list1, embedding_sql_list2)
			#print "Matched Dist: ", dist	
			if dist > 0.60:
				error60 = error60 +1
			if dist > 0.65:
				error65 = error65 +1
			if dist > 0.70:
				error70 = error70 +1
			if dist > 0.75:
				error75 = error75 +1
			if dist > 0.80:
				error80 = error80 +1
			if dist > 0.85:
				error85 = error85 +1
			if dist > 0.90:
				error90 = error90 +1
			if dist > 0.95:
				error95 = error95 +1
			if dist > 0.96:
				error96 = error96 +1
			if dist > 0.97:
				error97 = error97 +1
			if dist > 0.98:
				error98 = error98 +1
			if dist > 0.99:
				error99 = error99 +1			
			if dist > 1.0:
				error100 = error100 +1
			if dist > 1.05:
				error105 = error105 +1
			if dist > 1.10:
				error110 = error110 +1
			if dist > 1.15:
				error115 = error115 +1			
			if dist > 1.20:
				error120 = error120 +1
			if dist > 1.242:
				error1242 = error1242 +1		
	return (error60, error65, error70, error75, error80, error85, error90, error95, error96, error97, error98, error99, error100, error105, error110, error115, error120, error1242)
	
def evaluateMisMatchedFaces(database_name):
	mismatched = getMisMatchedLines()
	error60 = error65 = error70 = error75 = error80 = error85 = error90 = error95 = error96 = error97 = error98 = error99 = error100 = 0
	error105 = error110 = error115 = error120 = error1242 = 0
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
			if dist < 0.60:
				error60 = error60 +1
			if dist < 0.65:
				error65 = error65 +1
			if dist < 0.70:
				error70 = error70 +1
			if dist < 0.75:
				error75 = error75 +1
			if dist < 0.80:
				error80 = error80 +1
			if dist < 0.85:
				error85 = error85 +1
			if dist < 0.90:
				error90 = error90 +1
			if dist < 0.95:
				error95 = error95 +1
			if dist < 0.96:
				error96 = error96 +1
			if dist < 0.97:
				error97 = error97 +1
			if dist < 0.98:
				error98 = error98 +1
			if dist < 0.99:
				error99 = error99 +1
			if dist < 1.0:
				error100 = error100 +1
			if dist < 1.05:
				error105 = error105 +1
			if dist < 1.10:
				error110 = error110 +1
			if dist < 1.15:
				error115 = error115 +1			
			if dist < 1.20:
				error120 = error120 +1
			if dist < 1.242:
				error1242 = error1242 +1		
	return (error60, error65, error70, error75, error80, error85, error90, error95, error96, error97, error98, error99, error100, error105, error110, error115, error120, error1242)

(merror60, merror65, merror70, merror75, merror80, merror85, merror90, merror95, merror96, merror97, merror98, merror99, merror100, merror105, merror110, merror115, merror120, merror1242) = evaluateMatchedFaces('Lfw_Database3.db')	
print "matched error60", merror60
print "matched error65", merror65
print "matched error70", merror70
print "matched error75", merror75
print "matched error80", merror80
print "matched error85", merror85
print "matched error90", merror90
print "matched error95", merror95
print "matched error96", merror96
print "matched error97", merror97
print "matched error98", merror98
print "matched error99", merror99
print "matched error100", merror100
print "matched error105", merror105
print "matched error110", merror110
print "matched error115", merror115
print "matched error120", merror120
print "matched error1242", merror1242


(mmerror60, mmerror65, mmerror70, mmerror75, mmerror80, mmerror85, mmerror90, mmerror95, mmerror96, mmerror97, mmerror98, mmerror99, mmerror100, mmerror105, mmerror110, mmerror115, mmerror120, mmerror1242) = evaluateMisMatchedFaces('Lfw_Database3.db')	
print "Mismatched error60", mmerror60
print "Mismatched error65", mmerror65
print "Mismatched error70", mmerror70
print "Mismatched error75", mmerror75
print "Mismatched error80", mmerror80
print "Mismatched error85", mmerror85
print "Mismatched error90", mmerror90
print "Mismatched error95", mmerror95
print "Mismatched error96", mmerror96
print "Mismatched error97", mmerror97
print "Mismatched error98", mmerror98
print "Mismatched error99", mmerror99
print "Mismatched error100", mmerror100
print "Mmatched error105", mmerror105
print "Mmatched error110", mmerror110
print "Mmatched error115", mmerror115
print "Mmatched error120", mmerror120
print "Mmatched error1242", mmerror1242

print "Accuracy for 0.60: " , (100.0 - ((merror60 + mmerror60) * 100.0) / 6000 )
print "Accuracy for 0.65: " , (100.0 - ((merror65 + mmerror65) * 100.0) / 6000 )
print "Accuracy for 0.70: " , (100.0 - ((merror70 + mmerror70) * 100.0) / 6000 )
print "Accuracy for 0.75: " , (100.0 - ((merror75 + mmerror75) * 100.0) / 6000 )
print "Accuracy for 0.80: " , (100.0 - ((merror80 + mmerror80) * 100.0) / 6000 )
print "Accuracy for 0.85: " , (100.0 - ((merror85 + mmerror85) * 100.0) / 6000 )
print "Accuracy for 0.90: " , (100.0 - ((merror90 + mmerror90) * 100.0) / 6000 )
print "Accuracy for 0.95: " , (100.0 - ((merror95 + mmerror95) * 100.0) / 6000 )
print "Accuracy for 0.96: " , (100.0 - ((merror96 + mmerror96) * 100.0) / 6000 )
print "Accuracy for 0.97: " , (100.0 - ((merror97 + mmerror97) * 100.0) / 6000 )
print "Accuracy for 0.98: " , (100.0 - ((merror98 + mmerror98) * 100.0) / 6000 )
print "Accuracy for 0.99: " , (100.0 - ((merror99 + mmerror99) * 100.0) / 6000 )
print "Accuracy for 1.00: " , (100.0 - ((merror100 + mmerror100) * 100.0) / 6000 )
print "Accuracy for 1.05: " , (100.0 - ((merror105 + mmerror105) * 100.0) / 6000 )
print "Accuracy for 1.10: " , (100.0 - ((merror110 + mmerror110) * 100.0) / 6000 )
print "Accuracy for 1.15: " , (100.0 - ((merror115 + mmerror115) * 100.0) / 6000 )
print "Accuracy for 1.20: " , (100.0 - ((merror120 + mmerror120) * 100.0) / 6000 )
print "Accuracy for 1.242: " , (100.0 - ((merror1242 + mmerror1242) * 100.0) / 6000 )




