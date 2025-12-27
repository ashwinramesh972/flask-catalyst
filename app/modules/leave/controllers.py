from flask import jsonify

def index():
    return jsonify({"message": "Welcome to leave module"})
