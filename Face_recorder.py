import cv2
import numpy as np 
import sqlite3

def record(embeddings, face_name):
	print(embeddings)
	conn = sqlite3.connect('database.db')
	c = conn.cursor()
	#uname = face_name.split('.')[0]
	print(face_name)
	stringEmb = ','.join(map(str, embeddings))
	c.execute('INSERT INTO users (name,embeddings) VALUES (?,?);',(face_name , stringEmb,))
	print(stringEmb)
	#c.execute('INSERT INTO users (embeddings) VALUES (?);', (stringEmb,))
	conn.commit()
	conn.close()
