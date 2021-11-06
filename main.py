from flask import Flask, render_template
app = Flask('app', template_folder = "templates", static_folder = "static")

@app.route('/')
def hello_world():
  return render_template('index.html')

app.run(host='0.0.0.0', port=8080)
