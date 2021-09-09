"""
  Author : Balram Chaudhary
  Connect : linkedin.com/in/balram-chaudhary-855926195/
"""

from flask import Flask, render_template, request,send_from_directory
from mdetect import run
import os

PATH = os.getcwd()

model_path= "models/last.pt"

app = Flask(__name__)

def predict_label(img_path):
	s= run(weights=model_path, source=img_path,conf_thres=0.9)

	return s

@app.route("/", methods=['GET', 'POST'])
def main():
	return render_template("index.html")

@app.route("/submit", methods = ['GET', 'POST'])
def get_output():
	if request.method == 'POST':
		img = request.files['my_image']
		img_path = "static/" + img.filename
		img.save(img_path)
		p= predict_label(img_path)
		prediction= p['present']
		all= ['Resistor', 'Cap3', 'Transformer', 'Transformer', 'Cap4', 'Cap1', 'Cap2', 'MOSFET', 'Mov']
		present = [x.split(" ")[0] for x in prediction]
		absent = [x for x in all if x not in present]
		if len(absent) ==0:
			absent = "[All components present]"
		global op_image_path
		op_image_path = os.path.join(PATH,str(p['save_dir']))
		pic_name = img.filename

	return render_template("index.html", prediction = present, img_path = pic_name, absent=absent )

@app.route("/<filename>")
def send_image(filename):
	return send_from_directory(op_image_path,filename)

if __name__ =='__main__':
	app.run(debug = True)