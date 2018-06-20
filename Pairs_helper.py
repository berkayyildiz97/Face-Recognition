
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
		
	
	
