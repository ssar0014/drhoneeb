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
global s3
s3 = boto3.resource('s3', aws_access_key_id=S3_KEY, aws_secret_access_key=S3_SECRET)

# get the models
global loaded_model
global unhealthy_model
global species_model
global graph
graph = tf.get_default_graph()
loaded_model = load_model("./bee_healthy_or_not.h5")
unhealthy_model = load_model("./unhealthy_status.h5")
species_model = load_model("./bee_species.h5")

# set the flags as being global in scope to be used inside the function
global healthy_or_not
global unhealthy_status
global species

# define a function to fetch the image from S3 and process it such that it is ready to be fed into the neural net
def getImage():
    image_file = s3.Bucket(S3_BUCKET).download_file('public/user_photo.png', '/tmp/user_photo.png')
    raw_image = image.load_img('/tmp/user_photo.png', grayscale=False, target_size=(50, 54))
    img = image.img_to_array(raw_image)
    img = np.expand_dims(img, axis=0)
    return img

def getSpecies(img_data):
    with graph.as_default():
        species_pred = species_model.predict(img_data)
    species_pred = species_pred.tolist()
    return species_pred
    if species_pred[0][0] > 0.95:
        return 'Italian Honey Bee'
    elif species_pred[0][1] > 0.95:
        return 'Russian Honey Bee'
    elif species_pred[0][2] > 0.95:
        return 'Carniolan Honey Bee'
    elif species_pred[0][3] > 0.95:
        return 'Hybrid Breed Honey Bee'
    else:
        return 'Unsure of Species'

def getBeeCondition(img_data):
    with graph.as_default():
        prediction = loaded_model.predict(img_data)
    prediction = prediction.tolist()
    return prediction
    if prediction[0][0] > 0.5:
        return ('healthy')
    else:
        return ('unhealthy')

def getBeeProblem(img_data):
    with graph.as_default():
        unhealthy_prediction = unhealthy_model.predict(img_data)
    unhealthy_prediction = unhealthy_prediction.tolist()
    return unhealthy_prediction
    if unhealthy_prediction[0][0] > 0.95:
        return ('Varroa Mite Infestation')
    elif unhealthy_prediction[0][1] > 0.95:
        return ('Ant Infestation')
    elif unhealthy_prediction[0][2] > 0.95:
        return ('Robbed Hive')
    else:
        return 'Unsure of condition'

app = Flask(__name__)

# set the app route and use the GET method to send response to the client
@app.route('/test', methods=['GET']) # change it to POST
def get_predictions():
    # initiate the flags for each classification
    healthy_or_not = ''
    unhealthy_status = ''
    species = ''

    # create list for final response
    responses = list()
    # get the image data in keras format
    img = getImage()

    # get the species of the bee from the first neural network trained to classify bee species
    species = getSpecies(img)
    # now run the 2nd neural net to get the health status - healthy or unhealthy
    # if healthy, return the species and the health status of the bee
    # if the bee is unhealthy, run the 3rd neural net to classify the type of disease
    # return the type of disease along with the species
    healthy_or_not = getBeeCondition(img)

    if healthy_or_not == 'healthy':
        unhealthy_status = 'Bee is Healthy'
    else:
        unhealthy_status = getBeeProblem(img)

    # attach all the responses to a list and format it as json
    responses.append({'status': healthy_or_not,'problem': unhealthy_status,'species': species})
    responses = json.dumps({'response':responses})
    # response from the API is sent as a json response
    try:
        return Response(response=responses, mimetype='text/plain', status=200)
    except FileNotFoundError:
        abort(404)

if __name__ == '__main__':
    app.run(debug = True)
