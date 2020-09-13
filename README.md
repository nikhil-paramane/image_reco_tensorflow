
### Student Project for using image recognition for Cranes and other Heavy Construction Equipment
* Uses [Python](https://www.python.org) language
* Uses [Django](https://www.djangoproject.com) Web Framework
* Uses [TensorFlow](https://www.tensorflow.org) Machine Learning Framework


### Instructions for how to setup:
* Install Python 3.8.5
* Install pip3
* And then:
```
pip3 install virtualenv
python3 -m venv env
source env/bin/activate
git clone https://github.com/nikhil-paramane/image_reco_tensorflow.git
cd image_reco_tensorflow/imageReco
python manage.py makemigrations
```

### Instructions for how to Demo:
* Go to: http://craneimagereco.herokuapp.com/
* Click on `Choose file`  and select the JPEG file you want to process
* Click on `Upload and Detect`
* Wait for the image to be processed
* Output should show the results of processing
* Click on `Image Detector` Button the top left corner to repeat the demo
