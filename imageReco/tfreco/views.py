from django.shortcuts import render
from tfreco.forms import DocumentForm
from tfreco.models import Document
from django.shortcuts import redirect
import os
import io
from base64 import b64decode
import tensorflow as tf
from PIL import Image
from django.core.files.temp import NamedTemporaryFile
import base64
from django.core.files.base import ContentFile
from django.http import JsonResponse
MAX_K = 10

TF_GRAPH = "{base_path}/inception_model/retrained_graph.pb".format(
    base_path=os.path.abspath(os.path.dirname(__file__)))
TF_LABELS = "{base_path}/inception_model/retrained_labels.txt".format(
    base_path=os.path.abspath(os.path.dirname(__file__)))

# Create your views here.

def load_graph():
    sess = tf.Session()
    with tf.gfile.FastGFile(TF_GRAPH, 'rb') as tf_graph:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(tf_graph.read())
        tf.import_graph_def(graph_def, name='')
    label_lines = [line.rstrip() for line in tf.gfile.GFile(TF_LABELS)]
    softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')
    return sess, softmax_tensor, label_lines

SESS, GRAPH_TENSOR, LABELS = load_graph(); 

def upload(request):
    context={}
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            imgForm = form.save()
            imgName = os.path.basename(imgForm.document.path)
            print(imgForm.document.url)
            context['img_name'] = imgName
            context['url'] = imgForm.document.url
            recognize_result = reko(imgForm)
            dataDir = dict()
            # for key,val in recognize_result:
            #     dataDir[key] = val
            context['result']=recognize_result
            print(recognize_result)
            return render(request,'detect.html',context)
    else:
        form = DocumentForm()
    return render(request,'home.html',{'form':form})        


def detect(request, img_name):
    print(img_name)

def image_to_byte_array(image:Image):
  imgByteArr = io.BytesIO()
  image.save(imgByteArr, format=image.format)
  imgByteArr = imgByteArr.getvalue()
  return imgByteArr

def reko(imgform):
    print('__________RECO______________')
    data = dict()
    image = Image.open(imgform.document.path)
    recognize_result = tf_recognize(image)
    #print(recognize_result)
    print('DATA____________CONF')    
    if recognize_result:
            # data["success"] = True
            #  data["confidence"] = {}
             for res in recognize_result:                
                 data[res[0]] = float(res[1])*100
             #print(data["confidence"])    
    return data

def tf_recognize(image_file, k=MAX_K):
    result = list()
    print('________________inside rf_recognize')
    image_data = tf.gfile.FastGFile(image_file.filename, 'rb').read()
    print('_____img data read____________________')
    predictions = SESS.run(GRAPH_TENSOR, {'DecodeJpeg/contents:0': image_data})
    print('session run')
    predictions = predictions[0][:len(LABELS)]
    print(predictions)
    top_k = predictions.argsort()[-k:][::-1]
    for node_id in top_k:
        label_string = LABELS[node_id]
        score = predictions[node_id]
        result.append([label_string, score])

    return result