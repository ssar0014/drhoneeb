# app.py
from flask import Flask, jsonify, request, Response
import json
import os
import boto3
from config import S3_BUCKET, S3_KEY, S3_SECRET

import numpy as np
import tensorflow as tf
import keras
from keras.preprocessing import image
from keras.models import load_model

# Set up the S3 bucket with our credentials
s3 = boto3.resource('s3', aws_access_key_id=S3_KEY, aws_secret_access_key=S3_SECRET)

# get the models
graph = tf.get_default_graph()
loaded_model = load_model("./bee_healthy_or_not.h5")
unhealthy_model = load_model("./unhealthy_status.h5")
species_model = load_model("./bee_species.h5")

# set the flags as being global in scope to be used inside the function
global healthy_or_not
global unhealthy_status
global species

# initiate the flags for each classification
healthy_or_not = ''
unhealthy_status = 'The Bee is healthy'
species = ''

# define a function to fetch the image from S3 and process it such that it is ready to be fed into the neural net
def getImage():
    #image_file = request.files['image']
    image_file = s3.Bucket(S3_BUCKET).download_file('public/user_photo.png', '/tmp/user_photo.png')
    #image_file.save('/tmp/user_photo.png')
    raw_image = image.load_img('/tmp/user_photo.png',target_size=(50, 54))
    img = image.img_to_array(raw_image)
    img = np.expand_dims(img, axis=0)
    return img


app = Flask(__name__)

# curl -F "image=@bee_imgs/bee_imgs/041_066.png" http://127.0.0.1:5000/test
@app.route('/test', methods=['GET']) # change it to POST
def get_predictions():
    # create list for final response
    responses = list()

    # get the image data
    img = getImage()

    # get the species of the bee from the first neural network trained to classify bee species
    with graph.as_default():
        species_pred = species_model.predict(img)
    if species_pred[0][0] == 1:
        species = 'Italian Honey Bee'
    elif species_pred[0][1] == 1:
        species = 'Russian Honey Bee'
    elif species_pred[0][2] == 1:
        species = 'Carniolan Honey Bee'
    elif species_pred[0][3] == 1:
        species = 'Hybrid Breed Honey Bee'
    # now run the 2nd neural net to get the health status - healthy or unhealthy
    # if healthy, return the species and the health status of the bee
    # if the bee is unhealthy, run the 3rd neural net to classify the type of disease
    # return the type of disease along with the species
    with graph.as_default():
        prediction = loaded_model.predict(img)
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
    # attach all the responses to a list and format it as json
    responses.append({'status': healthy_or_not,'problem': unhealthy_status,'species': species})
    responses = json.dumps({'response':responses})

    # response from the API is sent as a json response, and the same is written to a file
    # the file is then sent to S3
    try:
        with open('result.json','w+') as out:
            json.dump(responses, out, ensure_ascii=True, indent=4)
        s3Obj = s3.Object(S3_BUCKET, 'result.json')
        s3Obj.put(Body=(bytes(json.dumps(responses).encode('UTF-8'))))
        return Response(response=responses, mimetype='text/plain', status=200)
    except FileNotFoundError:
        abort(404)

if __name__ == '__main__':
    app.run(debug = True)
