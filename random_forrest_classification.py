
from ij import IJ

from trainableSegmentation import WekaSegmentation


def training_Classifier():
	
	input_im = IJ.openImage("/home/aik19/Achintha/Sintering analysis/Scripts/Sintering_Analysis_The_New_Approach/training_sample_1.tif")
	labels = IJ.openImage("/home/aik19/Achintha/Sintering analysis/Scripts/Sintering_Analysis_The_New_Approach/Filtered_training_Sample.labels.tif")
	# for all slices in input2, add white pixels as labels for class 2 and 
 	#black pixels as labels for class 1
	segmentator =  WekaSegmentation( input_im )
	segmentator.addBinaryData( input_im, labels, "class 2", "class 1" )
	segmentator.trainClassifier()
	testImage = IJ.openImage( "/home/aik19/Achintha/Sintering analysis/Scripts/Sintering_Analysis_The_New_Approach/74122_micro_test_3.tif" )
	result = segmentator.applyClassifier( testImage )
	result.show()

	
training_Classifier()