#Accuracies for Lwf_Database3.db


merror60 = 2590
merror65 = 2387
merror70 = 2162
merror75 = 1900
merror80 = 1640
merror85 = 1376
merror90 = 1139
merror95 = 889
merror100 = 664

mmerror60 = 18
mmerror65 = 42
mmerror70 = 79
mmerror75 = 145
mmerror80 = 221
mmerror85 = 375
mmerror90 = 537
mmerror95 = 765
mmerror100 = 1006




print "Accuracy for 0.60: " , (100.0 - ((merror60 + mmerror60) * 100.0) / 6000 )
print "Accuracy for 0.65: " , (100.0 - ((merror65 + mmerror65) * 100.0) / 6000 )
print "Accuracy for 0.70: " , (100.0 - ((merror70 + mmerror70) * 100.0) / 6000 )
print "Accuracy for 0.75: " , (100.0 - ((merror75 + mmerror75) * 100.0) / 6000 )
print "Accuracy for 0.80: " , (100.0 - ((merror80 + mmerror80) * 100.0) / 6000 )
print "Accuracy for 0.85: " , (100.0 - ((merror85 + mmerror85) * 100.0) / 6000 )
print "Accuracy for 0.90: " , (100.0 - ((merror90 + mmerror90) * 100.0) / 6000 )
print "Accuracy for 0.95: " , (100.0 - ((merror95 + mmerror95) * 100.0) / 6000 )
print "Accuracy for 1.00: " , (100.0 - ((merror100 + mmerror100) * 100.0) / 6000 )


'''
matched error60 2590
matched error65 2387
matched error70 2162
matched error75 1900
matched error80 1640
matched error85 1376
matched error90 1139
matched error95 889
matched error96 841
matched error97 792
matched error98 752
matched error99 698
matched error100 664
Mismatched error60 18
Mismatched error65 42
Mismatched error70 79
Mismatched error75 145
Mismatched error80 221
Mismatched error85 375
Mismatched error90 537
Mismatched error95 765
Mismatched error96 810
Mismatched error97 865
Mismatched error98 916
Mismatched error99 958
Mismatched error100 1006
Accuracy for 0.60:  56.5333333333
Accuracy for 0.65:  59.5166666667
Accuracy for 0.70:  62.65
Accuracy for 0.75:  65.9166666667
Accuracy for 0.80:  68.9833333333
Accuracy for 0.85:  70.8166666667
Accuracy for 0.90:  72.0666666667
Accuracy for 0.95:  72.4333333333
Accuracy for 0.96:  72.4833333333
Accuracy for 0.97:  72.3833333333
Accuracy for 0.98:  72.2
Accuracy for 0.99:  72.4
Accuracy for 1.00:  72.1666666667s
'''

