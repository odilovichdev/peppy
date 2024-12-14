from app import PeppyApp

app = PeppyApp()


# static routing
@app.route("/home")
def home(request, response):
    response.text = "Hello from the home page"

# static routing
@app.route("/about")
def about(request, response):
    response.text = "Hello from the about page"


# dynamic routing
@app.route('/hello/{name}')
def greeting(request, response, name):
    response.text=f"Hello {name}"