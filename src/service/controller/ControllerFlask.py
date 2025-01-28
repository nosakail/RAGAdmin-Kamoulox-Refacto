from crypt import methods

import flask as fl
from  uvicorn.middleware.wsgi import WSGIMiddleware

from handling_request import handling_request

app = fl.Flask(__name__)
modelPath = "./Meta-Llama-3.1-8B-Instruct"

@app.route("/")
def index():
    return {"data":"bonjour bienvenue sur ragadmin"}

@app.route("/<req>", methods=["POST"])
def request(req:str):
    req_handled = handling_request(req, modelPath)
    return {"data":req}

asgi_app = WSGIMiddleware(app)

if __name__=="__main__":
    app.run(debug=True)