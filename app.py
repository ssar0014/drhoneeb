# app.py
from flask import Flask, jsonify, request, Response
import json
import os
import boto3
#from config import S3_BUCKET, S3_KEY, S3_SECRET

import numpy as np
import tensorflow as tf
import keras
from keras.preprocessing import image
from keras.models import load_model
import cv2

graph = tf.get_default_graph()
# Set up the S3 bucket with our credentials
# s3 = boto3.resource('s3', aws_access_key_id=S3_KEY, aws_secret_access_key=S3_SECRET)
loaded_model = load_model('bee_healthy_or_not.h5')
unhealthy_model = load_model('unhealthy_status.h5')
healthy_or_not = ''
unhealthy_status = ''

app = Flask(__name__)

# curl -F "image=@bee_imgs/bee_imgs/041_066.png" http://127.0.0.1:5000/test
@app.route('/test', methods=['POST'])
# define auxilary functions to check the health condition of the bees
# if healthy, return the species and the health status of the bee
# if the bee is unhealthy, run the second neural net to classify the type of disease
# return the type of disease along with the species
def get_predictions():
    raw_image = image.load_img(request.files['image'],target_size=(50, 54))
    img = image.img_to_array(raw_image)
    img = np.expand_dims(img, axis=0)

    # create list for final response
    responses = list()

    with graph.as_default():
        prediction = loaded_model.predict(img)
    #prediction = prediction.tolist()
    if prediction[0][0] > 0.5:
        healthy_or_not = 'healthy'
    else:
        healthy_or_not = 'unhealthy'
        with graph.as_default():
            unhealthy_prediction = unhealthy_model.predict(img)
        unhealthy_prediction = unhealthy_prediction.tolist()
        if unhealthy_prediction[0][0] == 1:
            unhealthy_status = 'Varroa Mite Infestation'
        elif unhealthy_prediction[0][1] == 1:
            unhealthy_status = 'Ant Infestation'
        elif unhealthy_prediction[0][2] == 1:
            unhealthy_status = 'Robbed Hive'

    responses.append({'status': healthy_or_not,'problem': unhealthy_status,'species': 'dummy'})
    responses = json.dumps({'response':responses})
    try:
        with open('result.json','w+') as out:
            json.dump(responses, out, ensure_ascii=True, indent=4)
        return Response(response=responses, mimetype='text/plain', status=200)
    except FileNotFoundError:
        abort(404)

if __name__ == '__main__':
    app.run(debug = True)
