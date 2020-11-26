from flask import Flask, render_template, redirect, url_for, request
from flask_cors import CORS, cross_origin
from matrix import *
import LED_display as LMD
import threading
from status import *
import time


app = Flask(__name__, static_url_path='/static') 
CORS(app, resources={r'*':{'origins':'*'}})
app.config['CORS_HEADERS'] = 'content-Type'

# sample
url_server = {
								"water" : "http://192.168.35.66:5000",
								"trafficlight1" : "http://192.168.43.79",
								"trafficlight2" : "http://192.168.35.39/5000",
						}

@app.route('/')
@app.route('/index.html')
@cross_origin()  
def home():

	return render_template('index.html', url_server=url_server, enumerate=enumerate)

@app.route('/squat.html')
@cross_origin()  
def squat():

	return render_template('squat.html', url_server=url_server, enumerate=enumerate)


@app.route('/side-legraise.html')
@cross_origin()  
def sideLegraise():
    
	return render_template('side-legraise.html', url_server=url_server, enumerate=enumerate)

@app.route('/push-up.html')
@cross_origin()  
def pushUp():
    
	return render_template('push-up.html', url_server=url_server, enumerate=enumerate)


''' ***************************************************************************'''

def LED_init():
	thread=threading.Thread(target=LMD.main, args=())
	print("[INFO] thread start")
	thread.setDaemon(True)
	thread.start()
	return

def draw_matrix(m):
	array = m.get_array()
	for y in range(m.get_dy()-4):
			for x in range(4, m.get_dx()-4):
					if array[y][x] == 0:
							LMD.set_pixel(y, 19-x, 0)
					elif array[y][x] == 1:
							LMD.set_pixel(y, 19-x, 4)
					else:
							continue
			print()

@app.route('/led')
@cross_origin()  
def led():
	led_count = request.args.get('count')
	led_count = int(led_count)
	
	if(led_count == 0):
			arrayScreen = Status.get_num0
	elif(led_count == 1):
			arrayScreen = Status.get_num1
	elif(led_count == 2):
			arrayScreen = Status.get_num2
	elif(led_count == 3):
			arrayScreen = Status.get_num3
	elif(led_count == 4):
			arrayScreen = Status.get_num4
	elif(led_count == 5):
			arrayScreen = Status.get_num5
	elif(led_count == 6):
			arrayScreen = Status.get_num6
	elif(led_count == 7):
			arrayScreen = Status.get_num7
	elif(led_count == 8):
			arrayScreen = Status.get_num8
	elif(led_count == 9):
			arrayScreen = Status.get_num9
	else:
			return "led count wrong"
	
	try: 
			iScreen = Matrix(arrayScreen)
			oScreen = Matrix(iScreen)
			draw_matrix(oScreen)
	except Exception as err:
			print("[Error] : ", err)
			return "led fail"
		
	return "led ok"

@app.route('/push-start')
@cross_origin()  
def pushStart():
	try:
		for i in range(0, 3):
    		arrayScreen = Status.get_pushUp
			iScreen = Matrix(arrayScreen)
			oScreen = Matrix(iScreen)
			draw_matrix(oScreen)
			time.sleep(0.4)
			arrayScreen = Status.get_pushDown
			iScreen = Matrix(arrayScreen)
			oScreen = Matrix(iScreen)
			draw_matrix(oScreen)
			time.sleep(0.4)
	except Exception as err:
		print("[Error] : ", err)
		return "led fail"

@app.route('/squat-start')
@cross_origin()  
def squattart():
	try:
		for i in range(0, 3):
    		arrayScreen = Status.get_squatStand
			iScreen = Matrix(arrayScreen)
			oScreen = Matrix(iScreen)
			draw_matrix(oScreen)
			time.sleep(0.4)
			arrayScreen = Status.get_squat
			iScreen = Matrix(arrayScreen)
			oScreen = Matrix(iScreen)
			draw_matrix(oScreen)
			time.sleep(0.4)
	except Exception as err:
		print("[Error] : ", err)
		return "led fail"

@app.route('/sidelegraise-start')
@cross_origin()  
def sideLegraiseStart():
	try:
		for i in range(0, 2):
    		arrayScreen = Status.get_sideHeadUp
			iScreen = Matrix(arrayScreen)
			oScreen = Matrix(iScreen)
			draw_matrix(oScreen)
			time.sleep(0.4)
			arrayScreen = Status.get_sideLeft
			iScreen = Matrix(arrayScreen)
			oScreen = Matrix(iScreen)
			draw_matrix(oScreen)
			time.sleep(0.4)
			arrayScreen = Status.get_sideHeadUp
			iScreen = Matrix(arrayScreen)
			oScreen = Matrix(iScreen)
			draw_matrix(oScreen)
			time.sleep(0.4)
			arrayScreen = Status.get_sideRight
			iScreen = Matrix(arrayScreen)
			oScreen = Matrix(iScreen)
			draw_matrix(oScreen)
			time.sleep(0.4)
	except Exception as err:
		print("[Error] : ", err)
		return "led fail"	

@app.route('/wrong-pose')
@cross_origin()  
def wrongPose():
    arrayScreen = Status.get_wrong
    try: 
		iScreen = Matrix(arrayScreen)
		oScreen = Matrix(iScreen)
		draw_matrix(oScreen)
	except Exception as err:
		print("[Error] : ", err)
		return "led fail"
		
	return "led ok"	

@app.route('/stop-all')
@cross_origin()  
def stopAll():
    arrayScreen = Status.arrayNone
    try: 
		iScreen = Matrix(arrayScreen)
		oScreen = Matrix(iScreen)
		draw_matrix(oScreen)
	except Exception as err:
		print("[Error] : ", err)
		return "led fail"
		
	return "led ok"		

''' ***************************************************************************'''


if __name__ == '__main__':
		LED_init()
		app.run(debug=False, threaded=True)
