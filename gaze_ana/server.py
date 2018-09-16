# -*- coding: utf-8 -*-
# app.py
"""
 Using SQLAlchemy and Flask get db record.(GET)
"""
import os
from flask import Flask, render_template
from flaski.models import WikiContent
from flask_restful import Resource, Api
from flask_cors import CORS
from flaski.app import db, app
from flaski.app import Choice
from functools import wraps

# app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
api = Api(app)
# datasetpart = {}
# datasetparthourly = {}


# def cors(func, allow_origin=None, allow_headers=None, max_age=None):
#     if not allow_origin:
#         allow_origin = "*"
#     if not allow_headers:
#         allow_headers = "content-type, accept"
#     if not max_age:
#         max_age = 60
#
#     @wraps(func)
#     def wrapper(*args, **kwargs):
#         response = func(*args, **kwargs)
#         cors_headers = {
#             "Access-Control-Allow-Origin": allow_origin,
#             "Access-Control-Allow-Methods": func.__name__.upper(),
#             "Access-Control-Allow-Headers": allow_headers,
#             "Access-Control-Max-Age": max_age,
#         }
#         if isinstance(response, tuple):
#             if len(response) == 3:
#                 headers = response[-1]
#             else:
#                 headers = {}
#             headers.update(cors_headers)
#             return (response[0], response[1], headers)
#         else:
#             return response, 200, cors_headers
#     return wrapper
#
#
# def abortIfNotExist(fileName):
#     filepath = '../data/json/' + fileName
#     if not os.path.exists(filepath):
#         abort(404, message="{} doesn't exist".format(fileName))
#
#
# class Resource(Resource):
#     method_decorators = [cors]
#
#
def write(array):
    post = Choice(array[0], array[1], array[2], array[3], array[4], array[5], array[6], array[7], array[8], array[9], array[10])
    print(post, array)
    db.session.add(post)
    db.session.commit()

class Hello(Resource):
    def get(self, params):
        param = params.split('&')
        param = [p.split('=')[1] for p in param]
        print(param)
        write(param)
        return param

api.add_resource(Hello, '/data/<params>')

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='127.0.0.1', port=port)
