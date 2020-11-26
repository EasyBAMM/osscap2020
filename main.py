from flask import Flask, render_template, redirect, url_for, request
from flask_cors import CORS, cross_origin
from matrix import *
import LED_display as LMD
import threading
from status import *

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
				arrayScreen = Status.arrayNum0
		elif(led_count == 1):
				arrayScreen = Status.arrayNum1
		elif(led_count == 2):
				arrayScreen = Status.arrayNum2
		elif(led_count == 3):
				arrayScreen = Status.arrayNum3
		elif(led_count == 4):
				arrayScreen = Status.arrayNum4
		elif(led_count == 5):
				arrayScreen = Status.arrayNum5
		elif(led_count == 6):
				arrayScreen = Status.arrayNum6
		elif(led_count == 7):
				arrayScreen = Status.arrayNum7
		elif(led_count == 8):
				arrayScreen = Status.arrayNum8
		elif(led_count == 9):
				arrayScreen = Status.arrayNum9
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

''' ***************************************************************************'''


if __name__ == '__main__':
		LED_init()
		app.run(debug=False, threaded=True)
