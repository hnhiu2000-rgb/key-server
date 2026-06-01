from flask import Flask, request, jsonify
import json, os, random, string

app = Flask(__name__)
DB = "keys.json"

def load():
    return json.load(open(DB)) if os.path.exists(DB) else {}

def save(data):
    json.dump(data, open(DB,"w"), indent=2)

def gen_key():
    c = string.ascii_uppercase + string.digits
    r = ''.join(random.choices(c, k=16))
    return '-'.join(r[i:i+4] for i in range(0,16,4))

@app.route("/check", methods=["POST"])
def check():
    d = request.json
    db = load()
    key = d.get("key")
    hwid = d.get("hwid")
    if key not in db:
        return jsonify({"valid": False})
    if db[key]["hwid"] is None:
        db[key]["hwid"] = hwid
        save(db)
        return jsonify({"valid": True})
    return jsonify({"valid": db[key]["hwid"] == hwid})

@app.route("/gen")
def gen():
    db = load()
    k = gen_key()
    db[k] = {"hwid": None}
    save(db)
    return jsonify({"key": k})

@app.route("/keys")
def keys():
    return jsonify(load())

if __name__ == "__main__":
import os
port = int(os.environ.get("PORT", 5000))
app.run(host="0.0.0.0", port=port)
