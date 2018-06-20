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
		
def findMinDistance(embedding, database_name):
	con = sqlite3.connect(database_name)
	with con:    
		cur = con.cursor()    
		cur.execute("SELECT * FROM users")
		rows = cur.fetchall()
		minDist = 4.0
		minDistName = None
		for row in rows:
			#print "row",row
			(id,name,embedding_sql) = row
			embedding_sql_list = embedding_sql.split(',')
			index = 0
			dist = 0
			for i in embedding_sql_list:
				dist = dist + (( float(embedding_sql_list[index])- float(embedding[index]) ) * (float(embedding_sql_list[index])- float(embedding[index]) ))
 				index = index+1
			dist = math.sqrt(dist)
			if dist < minDist:
				minDist = dist
				minDistName = name
		return (minDist, minDistName)
	
def evaluateMatchedFaces(database_name):
	matched = getMatchedLines()
	error = 0
	for line in matched:
		datas = line.split('\t')
		con = sqlite3.connect(database_name)
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
		print "Current Data:", (datas[0] + x + datas[1])
		embedding_sql_list1 = None
		embedding_sql_list2 = None
		with con:    
			cur = con.cursor()    
			cur.execute("SELECT * FROM users")
			rows = cur.fetchall()
			for row in rows:
				#print "row",row
				(id,name,embedding_sql) = row
								
				#print "Matched name",name
				#print "Matched dataName", (datas[0] + x + datas[2])
				if name == datas[0] + x + datas[1]: 
					embedding_sql_list1 = embedding_sql.split(',')
					break
		if embedding_sql_list1 != None:			
			(minDist, minDistName) = findMinDistance(embedding_sql_list1, database_name)
			if ( minDist < 0.91 and minDistName == datas[0] + y + datas[2] ) == False:
				print "Error in match"
				error = error +1
			else:
				print "Pass in match"
		else:
			print "Couldnt find this image in database:"
			error = error +1		
	return error
	
def evaluateMisMatchedFaces(database_name):
	mismatched = getMisMatchedLines()
	error = 0
	for line in mismatched:
		datas = line.split('\t')
		con = sqlite3.connect(database_name)
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
		print "Current Data:", (datas[0] + x + datas[1])		
		embedding_sql_list1 = None
		embedding_sql_list2 = None
		with con:
			cur = con.cursor()    
			cur.execute("SELECT * FROM users")
			rows = cur.fetchall()
			for row in rows:
				#print "row",row
				(id,name,embedding_sql) = row
								
				#print "Matched name",name
				#print "Matched dataName", (datas[0] + x + datas[2])
				if name == datas[0] + x + datas[1]: 
					embedding_sql_list1 = embedding_sql.split(',')
					break
		if embedding_sql_list1 != None:			
			(minDist, minDistName) = findMinDistance(embedding_sql_list1, database_name)
			if ( minDist < 0.91 and minDistName == datas[2] + y + datas[3] ):
				print "Error in mismatch"
				error = error +1
			else:
				print "Pass in mismatch"
		else:
			print "Couldnt find this image in database:", (datas[0] + x + datas[1])
			error = error +1		
	return error
	
matchedError = evaluateMatchedFaces('Lfw_Database3.db')	
print "matched error", matchedError

mismatchedError = evaluateMisMatchedFaces('Lfw_Database3.db')	
print "mismatchedError",mismatchedError

print "Accuracy: " , (100.0 - ((matchedError + mismatchedError) * 100.0) / (len(lines)-1) )




