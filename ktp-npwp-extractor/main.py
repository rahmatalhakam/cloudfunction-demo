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


def extract_file(request):
    if 'file' in request.files and request.args.get('type') != None:
        filePhoto = request.files['file']
        typePhoto = request.args.get('type').lower()
        if typePhoto != 'ktp' and typePhoto != 'npwp':
            return 'Wrong params'
        if filePhoto.filename != '':
            # save file to local storage
            path = os.path.join('/tmp', filePhoto.filename)
            filePhoto.save(path)

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
            npwp = ''
            name = ''
            nik = ''
            kpp = ''
            nikIndex = 0
            address = ''
            ttl = ''
            gender = ''
            if typePhoto == 'ktp':
                for i in range(len(lines)):
                    lineLower = lines[i].lower()
                    if len(re.findall('\d', lines[i])) > 14:
                        nik = re.sub(':', '', lines[i],
                                     flags=re.IGNORECASE).strip()
                    if 'laki' in lineLower or 'perempuan' in lineLower:
                        gender = re.sub(':', '', lines[i],
                                        flags=re.IGNORECASE).strip()
                    if re.search('^(?=.*Lahir)(?=.*\d+|,\d+.{8}| \d+.{8}).*$',
                                 lines[i]):
                        ttl = re.sub('^.*?: |^.*?:|^.*Lahir ',
                                     '',
                                     lines[i],
                                     flags=re.IGNORECASE)
                    if re.search(
                            'islam|christian|konghucu|katolik|budha|buddha|kristen|hindu',
                            lineLower):
                        religion = re.sub(':',
                                          '',
                                          lines[i],
                                          flags=re.IGNORECASE).strip()
                p = {
                    "province": lines[0],
                    "city": lines[1],
                    "nik": nik,
                    "gender": gender,
                    "birthdate": ttl,
                    "religion": religion
                }
            elif typePhoto == 'npwp':
                for i in range(len(lines)):
                    lineLower = lines[i].lower()
                    if 'nik' in lineLower:
                        nik = re.sub('nik|\.|:| ',
                                     '',
                                     lines[i],
                                     flags=re.IGNORECASE)
                        nikIndex = i
                    elif 'npwp' in lineLower and i != len(lines) - 1:
                        npwp = re.sub('npwp|:| ',
                                      '',
                                      lines[i],
                                      flags=re.IGNORECASE)
                        nama = lines[i + 1]
                    elif 'kpp' in lineLower:
                        kpp = lines[i]
                    if lines[i] != "":
                        res.append(lines[i])
                address = lines[nikIndex +
                                1] + ' ' + lines[nikIndex +
                                                 2] + ' ' + lines[nikIndex + 3]
                p = {
                    "npwp": npwp,
                    "name": nama,
                    "nik": nik,
                    "address": address,
                    "KPP": kpp,
                }
            resp_json = json.dumps(p)
            return '{}'.format(resp_json)
    return 'No data'
