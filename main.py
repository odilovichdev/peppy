from app import PeppyApp

app = PeppyApp()


@app.route("/home")
def home(request, response):
    response.text = "Hello from the home page"


@app.route("/about")
def about(request, response):
    response.text = "Hello from the about page"


@app.route("/hello/{name}")
def greeting(request, response, name):
    response.text = f"Hello {name}"
