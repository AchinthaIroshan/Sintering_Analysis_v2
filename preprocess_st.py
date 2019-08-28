from ij.plugin import FolderOpener
from ij import IJ,ImagePlus,ImageStack
import os
from script.imglib import ImgLib
from script.imglib.algorithm import Resample
from ij.io import FileSaver 
import csv
from mpicbg.ij.plugin import NormalizeLocalContrast  
from ij.plugin.filter import ParticleAnalyzer as PA
from ij.measure import ResultsTable



folder1 = "/media/aik19/Seagate Backup Plus Drive/ICIE16_Analysis_V2/Stage1/Raw_8bits/"
folder2 = "/media/aik19/Seagate Backup Plus Drive/ICIE16_Analysis_V2/Stage1/contrastad_and_cropped/" 

firstFolder = 74126 
folder3 = "/media/aik19/Seagate Backup Plus Drive/ICIE16_Analysis_V2/Stage1/RotatedNCropped/"
folder4 = "/media/aik19/Seagate Backup Plus Drive/ICIE16_Analysis_V2/Stage1/Resampled/"
folder5 = "/media/aik19/Seagate Backup Plus Drive/ICIE16_Analysis_V2/Stage1/Resampled_Slices/"
folder6 = "/media/aik19/Seagate Backup Plus Drive/ICIE16_Analysis_V2/Stage1/strutSlice_8bit/"
folder7 = "/media/aik19/Seagate Backup Plus Drive/ICIE16_Analysis_V2/Stage1/SegmentedStrutSlices/" 
folder8 = "/media/aik19/Seagate Backup Plus Drive/ICIE16_Analysis_V2/Stage1/SegmentedStruts_tifs/"
folder9 = "/media/aik19/Seagate Backup Plus Drive/ICIE16_Analysis_V2/Stage1/rm_smallCC/"


file3 = "/media/aik19/Seagate Backup Plus Drive/ICIE16_Analysis_V2/Stage1/RotatedNCropped/74126.nrrd"
file4 = "/media/aik19/Seagate Backup Plus Drive/ICIE16_Analysis_V2/Stage1/Resampled/74126.nrrd"
file5 = "/media/aik19/Seagate Backup Plus Drive/ICIE16_Analysis_V2/Stage1/strutSlice_8bit/74126.nrrd"
file6 = "/media/aik19/Seagate Backup Plus Drive/ICIE16_Analysis_V2/Stage1/rm_smallCC/74126.nrrd"





v2_folder_1 = "/media/aik19/Seagate Expansion Drive/ICIE16-S1/"
v2_folder_2 = "/media/aik19/Seagate Backup Plus Drive/ICIE16_Analysis_V2/Stage2/8bit_raw_2/"

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

#prepros1(folder1,folder2,firstFolder)

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

#prepros2(folder2,folder3)

def rescale(folder_in,folder_out):
	for filename in os.listdir(folder_in):
		imp =IJ.openImage(os.path.join(folder_in,filename))
		img = ImgLib.wrap(imp)
		img2 = Resample(img,0.25)
		imp=ImgLib.wrap(img2)
		output = "nrrd=["+folder_out+filename+"]"
		IJ.run(imp, "Nrrd ... ", output)
		IJ.run("Collect Garbage", "");

def rescaleimp(file_inpath,file_outpath):

	imp = IJ.openImage(file_inpath)
	img = ImgLib.wrap(imp)
	img2 = Resample(img,0.25)
	imp = ImgLib.wrap(img2)
	output = "nrrd=["+file_outpath+"]"
	IJ.run(imp, "Nrrd ... ", output)

#rescaleimp(file3,file4)
	

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

def covertTo8bits(folder_in,folder_out):
	for filename in os.listdir(folder_in):  
		imp = IJ.openImage(os.path.join(folder_in, filename))
		IJ.run(imp, "8-bit", "") 
		output = "nrrd=["+folder_out+filename+"]"
		IJ.run(imp, "Nrrd ... ", output)


def covertTo8bitsBatch(folder_in,folder_out):
	for folder in os.listdir(folder_in):
		infolderpath = folder_in+folder
		outfolderpath = folder_out + folder 
		os.mkdir(outfolderpath)
		for filename in os.listdir(infolderpath):
			imp = IJ.openImage(os.path.join(infolderpath, filename))
			IJ.run(imp, "8-bit", "") 
			fs = FileSaver(imp) 
			filepath = os.path.join(outfolderpath, filename)
			fs.saveAsTiff(filepath)


#covertTo8bitsBatch(v2_folder_1,v2_folder_2)


def getLabels():
	with open('/home/aik19/Achintha/Sintering analysis/Scripts/Sintering_Analysis_The_New_Approach/sliceLabels.csv','r') as csv_file:
		csv_reader = csv.reader(csv_file, delimiter=',')
		line_count=0
		rows = []
		for row in csv_reader:
			if line_count==0:
				file_names = row
				line_count +=1
			else:
				rows.append(row)
				line_count +=1
		return file_names,rows

#file_names,rows = getLabels()
#print(file_names)
#print(rows)


def ProcessSlices(folder_in,folder_out):
	
	file_names,rows = getLabels()
	for i in range(len(file_names)):
		imp = IJ.openImage(os.path.join(folder_in, file_names[i]))
		stack = imp.getImageStack()
		stack2 = ImageStack(imp.width,imp.height)
		
		for j in range(imp.getNSlices()):
			if rows[j][i]== '0':
				ip = stack.getProcessor(j+1)
				NormalizeLocalContrast.run(ip, 341, 326, 4, True, True)
				imagep = ImagePlus("imp",ip)
				IJ.run(imagep, "Non-local Means Denoising", "sigma=15 smoothing_factor=1 slice")
				imagep.setRoi(2,0,336,320);
				IJ.run(imagep, "Level Sets", "method=[Active Contours] use_level_sets grey_value_threshold=50 distance_threshold=0.50 advection=2.20 propagation=1 curvature=1 grayscale=30 convergence=0.0025 region=inside")
				fimp = IJ.getImage()
				#fip  = fimp.getProcessor()
				fimp = removeSmallCCs(fimp)
				fip  = fimp.getProcessor()
				stack2.addSlice(fip)
				print("process")
		
			else:
				ip = stack.getProcessor(j+1)
				stack2.addSlice(ip)
		
		final_imp = ImagePlus("image",stack2)
		output = "nrrd=["+folder_out+file_names[i]+"]"
		IJ.run(final_imp, "Nrrd ... ", output)

def preprocess_slices_giv_im(image_num,file_inpath,file_outpath):

	imp = IJ.openImage(file_inpath)
	file_names,rows = getLabels()
	stack = imp.getImageStack()
	stack2 = ImageStack(imp.width,imp.height)
	 
	for j in range(imp.getNSlices()):
		if rows[j][image_num]== '0':
			ip = stack.getProcessor(j+1)
			NormalizeLocalContrast.run(ip, 341, 326, 4, True, True)
			imagep = ImagePlus("imp",ip)
			IJ.run(imagep, "Non-local Means Denoising", "sigma=15 smoothing_factor=1 slice")
			imagep.setRoi(2,0,336,320);
			IJ.run(imagep, "Level Sets", "method=[Active Contours] use_level_sets grey_value_threshold=50 distance_threshold=0.50 advection=2.20 propagation=1 curvature=1 grayscale=30 convergence=0.0025 region=inside")
			fimp = IJ.getImage()
			#fip  = fimp.getProcessor()
			fimp = removeSmallCCs(fimp)
			fip  = fimp.getProcessor()
			stack2.addSlice(fip)
			print("process")
		
		else:
			ip = stack.getProcessor(j+1)
			stack2.addSlice(ip)


	final_imp = ImagePlus("image",stack2)
	output = "nrrd=["+file_outpath+"]"
	IJ.run(final_imp, "Nrrd ... ", output)




def removeSmallCCs(image):

	MINSIZE = 1000
	MAXSIZE = 1000000

	options = PA.SHOW_ROI_MASKS 
			
	
	results = ResultsTable()
	
	p = PA(options, PA.STACK_POSITION + PA.LABELS + PA.AREA + PA.PERIMETER + PA.CIRCULARITY, results, MINSIZE, MAXSIZE)
	p.setHideOutputImage(True)
	p.analyze(image)
	mmap = p.getOutputImage()
	mip = mmap.getProcessor() 
	mip.threshold(0)
	img = ImagePlus("rods_processed", mip)
	IJ.run(img, "8-bit", "") 
	IJ.run(img, "Make Binary", "method=Default background=Dark black")
	

	return img



def microRoI(input_folder,folder_centers,output_folder):
		
	

#preprocess_slices_giv_im(4,file5,file6)
#ProcessSlices(folder7,folder8)
#imp = IJ.openImage("/media/aik19/Seagate Backup Plus Drive/ICIE16_Analysis_V2/Stage1/SegmentedStruts_tifs/74122/221")
#imp.show()
#imp1 = analyzeParticles(imp)
#imp1.show()


#stackToSlices(folder7,folder8,firstFolder)
#imp = IJ.getImage()
#ip  = imp.getProcessor()
#NormalizeLocalContrast.run(ip, 341, 326, 4, True, True)  
#imp2 = ImagePlus("imp",ip)
#imp2.show()

#IJ.run(imp, "Enhance Contrast", "saturated=0.35")
#IJ.run(imp, "Apply LUT", "stack")
#IJ.run(imp, "Non-local Means Denoising", "sigma=15 smoothing_factor=1 stack")
#ProcessSlices(folder6,folder7)
#file_names,rows = getLabels()



#print(len(rows))
#print(rows[220][0])




#prepros1(folder_in,folder_out,firstFolder)	
#prepros2(folder2,folder3)
#rescale(folder3,folder4)
#stackToSlices(folder4,folder5,firstFolder)
		
		#IJ.run(imp, "TransformJ Rotate", "z-angle=9 y-angle=-6 x-angle=0.0 interpolation=Linear background=0.0");
		#stack = imp.getImageStack()
		#stackcropped  = stack.crop(118,98,70,1364,1304,904)
		#imp = ImagePlus("2",stackcropped)
		

	