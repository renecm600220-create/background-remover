from flask import Flask, render_template, request, jsonify
import os
from PIL import Image
import io
import base64
from rembg import remove

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/remove_background", methods=["POST"])
def remove_background():
    if "image" not in request.files:
        return jsonify({"error": "No hay imagen"}), 400
    file = request.files["image"]
    if file.filename == "":
        return jsonify({"error": "No hay imagen"}), 400
    try:
        input_image = file.read()
        output_image = remove(input_image)
        img = Image.open(io.BytesIO(output_image))
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format="PNG")
        img_base64 = base64.b64encode(img_byte_arr.getvalue()).decode("utf-8")
        return jsonify({"success": True, "image": "data:image/png;base64," + img_base64})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
