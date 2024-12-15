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


"""
1. Duplicate routes -> Done
2. Class based handler
"""


@app.route('/books')
class Book:

    def get(self, request, response):
        response.text = "Books page"

    def post(self, request, response):
        response.text = "Endpoint to the create books"
