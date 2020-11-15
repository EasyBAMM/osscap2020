from flask import Flask, render_template, redirect, url_for
from flask_cors import CORS, cross_origin

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




if __name__ == '__main__':
    app.run(debug=True)
