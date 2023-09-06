# DL oncology repo

## MSI_CRC
MSI status prediction on WSI of colorectal patients.    
HIA repository: https://github.com/KatherLab/HIA

### Preprocessing
- detect_blur.py: file to detect blurry tiles
- Export_ROI_at_tile_level_select_tissue.groovy: script to select tissue of a Whole Slide Image and to generate tiles
- preProcessing: scripts to perform image normalization
- HIA_custom: folder containing modified HIA (KatherLab) scripts to load models from file and not from URL
- The folder also contains the CLINI and SLIDE files needed to run experiments on HIA
- Examples to run fine-tuning and deployment of models in the HIA required format are also provided


## CXR_LC
Lung cancer classification of chest X-Ray images.
- The folder contains examples of classification models (ResNet, ViT, densenet) and a python script to recreate the multiple AUC and PR curves plot.
