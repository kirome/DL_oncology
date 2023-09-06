"""
@author: Narmin Ghaffari Laleh <narminghaffari23@gmail.com> - Nov 2020

"""
##############################################################################
from multiprocessing.dummy import Pool as ThreadPool
import stainNorm_Macenko
import multiprocessing
import os
import cv2
import numpy  as np

global inputPath
global outputPath
global normalizer

                   
##############################################################################
                        
def poolcontext(*args, **kwargs):
    pool = multiprocessing.Pool(*args, **kwargs)
    yield pool
    pool.terminate()

###############################################################################
    
def Normalization(inputPath, outputPath, sampleImagePath, num_threads = 8):
    
    inputPathContent = os.listdir(inputPath)
    normPathContent = os.listdir(outputPath)
    
    remainlList = []
    for i in inputPathContent:
        if not i in normPathContent:
            remainlList.append(i)
            
    inputPathContent = [i for i in remainlList if not i.endswith('.bat')]
    inputPathContent = [i for i in inputPathContent if not i.endswith('.txt')]
    
    target = cv2.imread(sampleImagePath)
    target = cv2.cvtColor(target, cv2.COLOR_BGR2RGB)
    #print(target)
    normalizer = stainNorm_Macenko.Normalizer()
    normalizer.fit(target) 
    #print(normalizer) 
        
    pool = ThreadPool(num_threads)
    pool.map(Normalize_Main, inputPathContent) 
    pool.close()
    pool.join()

##############################################################################

def Normalize_Main(item): 
           
    outputPathRoot = os.path.join(outputPath, item)
    inputPathRoot = os.path.join(inputPath, item)
    inputPathRootContent = os.listdir(inputPathRoot)
    target = cv2.imread(sampleImagePath)
    target = cv2.cvtColor(target, cv2.COLOR_BGR2RGB)
    #print(target)
    normalizer = stainNorm_Macenko.Normalizer()
    normalizer.fit(target) 
    #print(normalizer) 
    print()
    if not len(inputPathRootContent) == 0:
        if not os.path.exists(outputPathRoot):
            os.mkdir(outputPathRoot)
            temp = os.path.join(inputPath, item)
            tempContent = os.listdir(temp)
            tempContent = [i for i in tempContent if i.endswith('.png')] #jpg
            print(temp)
            for tempItem in tempContent:
                img = cv2.imread(os.path.join(inputPathRoot, tempItem))
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) 
                edge  = cv2.Canny(img, 40, 40) 
                edge = edge / np.max(edge)               
                edge = (np.sum(np.sum(edge)) / (img.shape[0] *img.shape[1])) * 100
                print(edge)
                #print(os.path.join(outputPathRoot, tempItem))
                if edge > 2:
                    try:
                        nor_img = normalizer.transform(img)
                        cv2.imwrite(os.path.join(outputPathRoot, tempItem), cv2.cvtColor(nor_img, cv2.COLOR_RGB2BGR))
                    except:
                        print('Failed to normalize the tile {}.'.format(tempItem))

###############################################################################
#-inputPath "/mnt/isilon/Lung_HMAR_TCGA/train_Level1/LUAD/14B004030_1_T3_2_1_1498399048828/" -outputPath /mnt/isilon/Lung_HMAR_TCGA/train_Level1/LUAD_norm/14B004030_1_T3_2_1 --sampleImagePath /mnt/isilon/Lung_HMAR_TCGA/train_Level1/LUAD/14B004030_1_T3_2_1_1498399048828/14B004030_1_T3_2_1_1498399048828_2_1024-9216-1536-9728_.png
#TUMICC and lung project
#inputPath = r"/mnt/isilon/TUMICC_project/NEW_samples_with_Relapse_270422/New_tiles"
#outputPath = r"/mnt/isilon/TUMICC_project/NEW_samples_with_Relapse_270422/New_tiles_normalized"
#sampleImagePath = r"/mnt/isilon/Lung_HMAR_TCGA/train_Level1/LUAD/14B004030_1_T3_2_1_1498399048828/14B004030_1_T3_2_1_1498399048828_2_1024-9216-1536-9728_.png"
#Breast_project
#inputPath =  r"/mnt/isilon/Breast_HMAR/HoverNet/Tests/NEW_TEST_SET/"
#outputPath =  r"/mnt/isilon/Breast_HMAR/HoverNet/Tests/NEW_TEST_SET_normalized/"  
#sampleImagePath = r"/mnt/isilon/Breast_HMAR/HoverNet/Lizard_dataset/Lizard_images/ALL_images/pannuke_1.png"
#SCLC project
#inputPath = r"/mnt/isilon/SCLC_project/Slides/OK/Tiles_40X_Level_1"
#inputPath = r"/mnt/isilon/SCLC_project/Slides/OK/Rerun_030522/qupath/tiles"
#inputPath = r"/mnt/isilon/SCLC_project/Slides/OK/Tiles_20X_Level_0"
sampleImagePath = r"/data/home/xmonzonis/MSI_PSMAR/normalization_template.jpg"
inputPath = r"/data/home/xmonzonis/MSI_PSMAR/QuPath_MSI_PSMAR/BLOCKS_NORM_MACENKO"
outputPath = r"/data/home/xmonzonis/MSI_PSMAR/QuPath_MSI_PSMAR/NORM_tiles"
#sampleImagePath = r"/mnt/isilon/Joan/SCLC_project/Slides/OK/s_20X_Level_0/16B006343_2_T1_1_1_1462289486267/16B006343_2_T1_1_1_1462289486267_0_6656-5632-7168-6144_.png"
Normalization(inputPath, outputPath,sampleImagePath, num_threads = 6)

