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
    response.text = f"Hello {name}"


@app.route('/books')
class Book:

    def get(self, request, response):
        response.text = "Books page"

    def post(self, request, response):
        response.text = "Endpoint to the create books"


def new_handler(request, response):
    response.text = "From new handler"


app.add_route("/new-handler", new_handler)


@app.route("/template")
def template_handler(req, resp):
    resp.body = app.template(
        "home.html",
        context={
            "new_title": "Best title",
            "new_body": "Best body"
        }
    )


def on_exception(req, resp, exc):
    resp.status_code = 500
    resp.text = str(exc)


app.add_exception(on_exception)


@app.route("/exception")
def exception_throwing_handler(req, resp):
    raise AttributeError("Some exception")
