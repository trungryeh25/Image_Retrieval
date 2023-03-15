from django.shortcuts import render, redirect
from rest_framework.views import APIView
from django.http import HttpResponse
from .forms import *

from numpy import load
import numpy as np
import time
import cv2
from tensorflow.keras.applications.efficientnet import EfficientNetB7
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.efficientnet import preprocess_input
from sklearn.neighbors import KDTree

feature_list = load(r'npy\feature_list.npy')
feature_id = load(r'npy\feature_id.npy')
feature_id = feature_id.tolist()

model = EfficientNetB7(include_top=False)
kd = KDTree(feature_list)

def feature_extract(img_path, model):
    img = image.load_img(img_path, target_size=(224, 224))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)

    features = model.predict(x)
    flattened_features = features.flatten()
    normalized_features = flattened_features / np.linalg.norm(flattened_features)
    return normalized_features.reshape(-1,1).T[0]

# Create your views here.


class HomePage(APIView):
    
    def get(self, request, *args, **kwargs):
        form = SearchForm()
        return render(request, template_name='homepage/index.html', context={
            'form': form,
        })

    def post(self, request, *args, **kwargs):
        form = SearchForm(request.POST, request.FILES)
        if form.is_valid(): 
            form.save()
            
            x = form.instance.x if form.instance.x > 0 else 0
            y = form.instance.y if form.instance.y > 0 else 0
            w = form.instance.w if form.instance.w > 0 else 0
            h = form.instance.h if form.instance.h > 0 else 0
            
            try:
                img_path = form.instance.img.url[1:]
            except:
                img_path = request.data['img_path']
                x=0 
                y=0
                w=0
                h=0
            
            img = cv2.imread(img_path)
            if not (x==0 and y==0 and w==0 and h==0):
                crop_img = img[y:y+h, x:x+w]
                img_path = img_path[:-4]+'_crop.jpg'
                cv2.imwrite(img_path, crop_img)
                       
            top_k = form.instance.topk
            start = time.time()
            dist, indx = kd.query(feature_extract(img_path, model).reshape(-1,1).T, top_k)
            end = time.time()

            # reading images
            images = []
            for i in range(top_k):
                images.append(feature_id[indx[0][i]].split('/')[-1][:-4])
            
            return render(request, template_name='homepage/index.html', context={
                'query': img_path, 
                'top_k': top_k, 
                'form': form, 
                'images': images,
                'time': round(end - start, 2),
                'x': x, 
                'y': y, 
                'w': w, 
                'h': h,
            })
        else:
            return HttpResponse('Uploaded fail!')
