import Pairs_helper

matched = Pairs_helper.getMatchedLines()
mismatched = Pairs_helper.getMisMatchedLines()
print "Matched " ,matched
print "MisMatched " ,mismatched

index=0
for i in matched:
	print index,i
	index = index+1
index=0
for i in mismatched:
	print index,i
	index = index+1
