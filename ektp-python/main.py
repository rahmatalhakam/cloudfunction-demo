import sys
import io
import os
import json
import re

from google.cloud import vision
from google.cloud.vision import types
from flask import escape

def hello_get(request):
    """HTTP Cloud Function.
    Args:
        request (flask.Request): The request object.
        <http://flask.pocoo.org/docs/1.0/api/#flask.Request>
    Returns:
        The response text, or any set of values that can be turned into a
        Response object using `make_response`
        <http://flask.pocoo.org/docs/1.0/api/#flask.Flask.make_response>.
    """
    return 'Hello World!'
# [END functions_helloworld_get]

def extract_ektp(request):
    if 'ektp' in request.files:
        ektp = request.files['ektp']
        if ektp.filename != '': 
            # save file to local storage
            path = os.path.join('/tmp', ektp.filename)
            ektp.save(path)
                    
            # call vision api to extract text from image
            client = vision.ImageAnnotatorClient()
            with io.open(path, 'rb') as image_file:
                content = image_file.read()        
            image = vision.types.Image(content=content)
            response = client.text_detection(image=image)
            texts = response.text_annotations

            # extract ektp information from text detector
            text = texts[0].description
            lines = text.split("\n")
            res = []
            for line in lines:
                line = re.sub('gol. darah|nik|kewarganegaraan|nama|status perkawinan|berlaku hingga|alamat|agama|tempat/tgl lahir|jenis kelamin|gol darah|rt/rw|kel|desa|kecamatan', '', line, flags=re.IGNORECASE)
                line = line.replace(":","").strip()
                if line != "":
                    res.append(line)                        
            p = {
                "province": res[0],
                "city": res[1],
                "id": res[2],
                "name": res[3],
                "birthdate": res[4],
            }

            resp_json = json.dumps(p)
            return '{}'.format(resp_json)
    return 'No data'         
