from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello() :
    return 'hello world'

@app.route("/hello/")
def hello_flask() :
    return "Hello Flask!"

if __name__=="__main__":
    app.run()