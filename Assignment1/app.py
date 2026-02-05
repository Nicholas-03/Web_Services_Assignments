from url import Url
from flask import Flask, request, jsonify, redirect
import re

app = Flask(__name__)
# Url.addUrl("https://facebook.com/")
# Url.addUrl("https://google.com/")

@app.get("/<id>")
def returnUrl(id):
    if id in Url.urls:
        url = Url.urls[id]
        return jsonify({"value": url}), 301
    else:
        return jsonify("Not Found"), 404
    
@app.put("/<id>")
def update(id):    
    data = request.get_json(force=True)
    url = data.get('url')
    
    if id not in Url.urls:
        return jsonify("Not Found"), 404
    
    url_pattern = re.compile(
        "((http|https)://)" # Group: http:// or https:// (required)
        "(www.)?" # www. optional
        "[a-zA-Z0-9@:%._\\+~#?&//=]" # One character that can be letter, digit, or these special chars
        "{2,256}" # The domain part must be 2-256 characters long
        "\\.[a-z]" # Dot + a single lowercase letter
        "{2,6}" # Must be 2-6 characters long
        "\\b" # Word boundary
        "([-a-zA-Z0-9@:%._\\+~#?&//=]" # Group: start of path characters
        "*)" # Optional path (0 or more characters)
    )
    if not url_pattern.match(url):
        return jsonify("Error"), 400

    Url.urls[id] = url
    return "", 200

@app.delete("/<id>")
def deleteUrl(id):
    if id in Url.urls:
        del Url.urls[id]
        return "", 204
    else:
        return jsonify("Not found"), 404

@app.get("/")
def getUrls():
    keys = list(Url.getUrls())

    if len(keys) == 0:
        return jsonify({"value": None}), 200
    
    return jsonify({"value": keys}), 200

@app.post("/")
def addUrl():
    if not request.is_json:
        return jsonify("Error"), 400
    
    data = request.get_json()
    url = data.get('value')

    if not url:
        return jsonify("Error"), 400
    
    url_pattern = re.compile(
        "((http|https)://)" # Group: http:// or https:// (required)
        "(www.)?" # www. optional
        "[a-zA-Z0-9@:%._\\+~#?&//=]" # One character that can be letter, digit, or these special chars
        "{2,256}" # The domain part must be 2-256 characters long
        "\\.[a-z]" # Dot + a single lowercase letter
        "{2,6}" # Must be 2-6 characters long
        "\\b" # Word boundary
        "([-a-zA-Z0-9@:%._\\+~#?&//=]" # Group: start of path characters
        "*)" # Optional path (0 or more characters)
    )
    if not url_pattern.match(url):
        return jsonify("Error"), 400
    
    id = Url.addUrl(url)
    return jsonify({"id": id}), 201

@app.delete("/")
def deleteNull():
    Url.urls.clear()
    return jsonify("Not Found"), 404