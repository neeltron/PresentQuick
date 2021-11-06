from flask import Flask, render_template, request
app = Flask('app', template_folder = "templates", static_folder = "static")

@app.route('/')
def hello_world():
  return render_template('index.html')

@app.route('/try')
def longText():
  return render_template('tryitout.html')

@app.route('/try', methods = ['POST'])
def process():
  title = request.form['title']
  presenter = request.form['presenter']
  back = request.form['back']
  intro = request.form['intro']
  literature = request.form['literature']
  method = request.form['method']
  result = request.form['result']
  conc = request.form['conc']
  ack = request.form['ack']
  cite = request.form['cite']
  end = request.form['end']
  return render_template('tryitout.html')

app.run(host='0.0.0.0', port=8080)
