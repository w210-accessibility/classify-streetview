# classify-streetview
CNN classification modeling on street view images
Classify pedestrian accessibility (and obstacle) features like curb ramps, surface problems, and obstructions. 

# Table of Contents
## crop-images

Notebooks and scripts to crop GSV images for training and inference

* `2020-03-08-CropWithDepth.ipynb` - initial experiements with the Depth data metadata and text files
* `2020-03-14-ABCropWithDepth.ipynb`
* `2020-03-15-Galen-make_new_city_csvs_sliding_window.ipynb` - copied from sidewalk-cv-assets19 repo with some modifications to try to run on our Milwaukee images

## exploratory

Experimental notebooks particularly with using models for inference and training. 
* `2020-02-19-SageMakerExperiments.ipynb`
* `2020-03-01-TestInference.ipynb`
* `2020-03-09-GPUInference.ipynb`

### images
Includes example, manually cropped Milwaukee images for testing with inference


## split-train-test
Preparing images to split into training and testing sets. Ideally, 80/20 train/test, but due to lack of examples for Obstruction and Surface Problem classes, getting 50/50 for those classes. Need to downsample the nulls for the overall set

* `2020-03-08-ExamineLabels.ipynb` - pulling in labels from EDA repo and reviewing to determine best split method

# Dependencies 
* [EDA repo for labels and data processing](https://github.com/w210-accessibility/EDA) 
* [Forked sidewalk-cv-assets19 repo](https://github.com/w210-accessibility/sidewalk-cv-assets19)
* AWS S3 Buckets with images 
