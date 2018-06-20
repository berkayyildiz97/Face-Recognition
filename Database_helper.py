import cv2
import numpy as np 
import sqlite3
import os
import math
import argparse

maxOfMinDistances = 0.0
database_name =	""

def setDatabase(database):
	global database_name
	database_name = database

def record(embeddings, face_name):
	print "database in record :", database_name
	print "embeddings", embeddings
	conn = sqlite3.connect(database_name)
	c = conn.cursor()
	#uname = face_name.split('.')[0]
	#print(face_name)
	stringEmb = ','.join(map(str, embeddings))
	print "stringEmb : ", stringEmb
	c.execute('INSERT INTO users (name,embedding) VALUES (?,?);',(face_name , stringEmb,))
	#print(stringEmb)
	#c.execute('INSERT INTO users (embeddings) VALUES (?);', (stringEmb,))
	conn.commit()
	conn.close()

def findMinDistance(embedding):
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
				#print "embedding_sql_list", float(embedding_sql_list[index])
				#print "embedding", float(embedding[index])
				#print "Fark :", float(embedding_sql_list[index]) - float(embedding[index])
 				index = index+1
			dist = math.sqrt(dist)
			if dist < minDist:
				minDist = dist
				minDistName = name
		return (minDist, minDistName)

def findMinDistanceForCalculatingThresholdValue(embedding):
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
			stringEmb = ','.join(map(str, embedding))
			if stringEmb == embedding_sql:
				continue
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

def findInitialThresholdValue():
	print "Computing Initial Threshold Value..."
	global maxOfMinDistances
	con = sqlite3.connect(database_name)
	with con:    
		cur = con.cursor()    
		cur.execute("SELECT * FROM users")
		rows = cur.fetchall()
		maxOfMinDistances = 0.0
		for row in rows:
			print "Threshold :", (maxOfMinDistances * 0.8)
			(id,name,embedding_sql) = row
			embedding_sql_list = embedding_sql.split(',')
			minDist = findMinDistanceForCalculatingThresholdValue(embedding_sql_list)[0]
			if maxOfMinDistances < minDist:
				maxOfMinDistances = minDist
		if maxOfMinDistances == 4.0:
			maxOfMinDistances = 0
		if maxOfMinDistances == 0:
			return 0.8
		return 0.8 * maxOfMinDistances


def findThresholdValue(embedding):
	global maxOfMinDistances
	minDist = findMinDistance(embedding)[0]
	if maxOfMinDistances < minDist:
		maxOfMinDistances = minDist
	if maxOfMinDistances == 4.0:
		maxOfMinDistances = 0
	if maxOfMinDistances == 0:
		return 0.8
	return 0.8 * maxOfMinDistances

def recognize(embedding, thresholdValue):
	(minDist, minDistName) = findMinDistance(embedding)
	print "thresholdValue", thresholdValue
	print "minDist :", minDist
	if minDist < thresholdValue:
		print "Face Found :", minDistName
	else:
		print "Face Not Found :", -1
			
def isFound(embedding):
	stringEmb = ','.join(map(str, embedding))
	con = sqlite3.connect(database_name)
	with con:    
		cur = con.cursor()    
		cur.execute("SELECT * FROM users")
		rows = cur.fetchall()
		for row in rows:
			(id,name,embedding_sql) = row
			if stringEmb == embedding_sql:
				return True
	return False


