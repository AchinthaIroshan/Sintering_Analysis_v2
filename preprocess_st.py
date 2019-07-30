from ij.plugin import FolderOpener
from ij import IJ,ImagePlus
import os
from script.imglib import ImgLib
from script.imglib.algorithm import Resample
from ij.io import FileSaver 

folder1 = "/media/aik19/Seagate Backup Plus Drive/ICIE16_Analysis_V2/Stage1/Raw_8bits/"
folder2 = "/media/aik19/Seagate Backup Plus Drive/ICIE16_Analysis_V2/Stage1/contrastad_and_cropped/" 

firstFolder = 74122 
folder3 = "/media/aik19/Seagate Backup Plus Drive/ICIE16_Analysis_V2/Stage1/RotatedNCropped/"
folder4 = "/media/aik19/Seagate Backup Plus Drive/ICIE16_Analysis_V2/Stage1/Resampled/"
folder5 = "/media/aik19/Seagate Backup Plus Drive/ICIE16_Analysis_V2/Stage1/Resampled_Slices/"

def prepros1(folder_in,folder_out,firstFolder):
	for x in range(1):
		fnum = firstFolder+x
		folder = folder_in+str(fnum)
		output = "nrrd=["+folder_out+str(fnum)+".nrrd]"
		imp = FolderOpener.open(folder)
		stack = imp.getImageStack()
		stackcropped  = stack.crop(404,644,538,1604,1476,1200)
		imp = ImagePlus("1",stackcropped)
		IJ.run(imp, "Stack Contrast Adjustment", "is")
		imp = IJ.getImage()
		IJ.run(imp, "Nrrd ... ", output);
		imp.close()
		IJ.run("Collect Garbage", "")
		

def prepros2(folder_in,folder_out):
	for filename in os.listdir(folder_in):
		imp =IJ.openImage(os.path.join(folder_in,filename))
		IJ.run(imp, "TransformJ Rotate", "z-angle=9 y-angle=-6 x-angle=0.0 interpolation=Linear background=0.0")
		imp = IJ.getImage()
		stack = imp.getImageStack()
		stackcropped  = stack.crop(118,98,70,1364,1304,904)
		imp = ImagePlus("2",stackcropped)
		output = "nrrd=["+folder_out+filename+"]"
		IJ.run(imp, "Nrrd ... ", output)
		imp.close()
		IJ.run("Collect Garbage", "")

def rescale(folder_in,folder_out):
	for filename in os.listdir(folder_in):
		imp =IJ.openImage(os.path.join(folder_in,filename))
		img = ImgLib.wrap(imp)
		img2 = Resample(img,0.25)
		imp=ImgLib.wrap(img2)
		output = "nrrd=["+folder_out+filename+"]"
		IJ.run(imp, "Nrrd ... ", output)
		IJ.run("Collect Garbage", "");

def stackToSlices(folder_in,folder_out,folder_num):
	for filename in os.listdir(folder_in):  
		imp = IJ.openImage(os.path.join(folder_in, filename))
		stack = imp.getImageStack()
		output=folder_out+str(folder_num)
		folder_num = folder_num+1
		os.makedirs(output)
		for i in xrange(1, imp.getNSlices()+1):
			ip = stack.getProcessor(i)
			imp = ImagePlus("imp", ip)
			fs= FileSaver(imp)
			filepath = os.path.join(output,str(i))
			fs.saveAsTiff(filepath)		

#prepros1(folder_in,folder_out,firstFolder)	
#prepros2(folder2,folder3)
#rescale(folder3,folder4)
stackToSlices(folder4,folder5,firstFolder)
		
		#IJ.run(imp, "TransformJ Rotate", "z-angle=9 y-angle=-6 x-angle=0.0 interpolation=Linear background=0.0");
		#stack = imp.getImageStack()
		#stackcropped  = stack.crop(118,98,70,1364,1304,904)
		#imp = ImagePlus("2",stackcropped)
		

	