from conftest import app, test_client
import pytest


def test_basic_route_adding(app):

    @app.route('/home')
    def home(req, resp):
        resp.text = "Hello from the home page"


def test_duplicate_routing(app):

    @app.route("/home")
    def home(req, resp):
        resp.text = "Hello from the home page"

    with pytest.raises(AssertionError):
        @app.route("/home")
        def home1(req, resp):
            resp.text = "Duplicate routing"


def test_default_response(app, test_client):

    resp = test_client.get("http://testserver/nonexistent")

    assert resp.text == "Not Found."
    assert resp.status_code == 404


def test_requests_can_be_send_by_test_client(app, test_client):

    @app.route("/home")
    def home(req, resp):
        resp.text = "Hello from the home page"

    assert test_client.get(
        'http://testserver/home').text == "Hello from the home page"


def test_parameterized_routing(app, test_client):

    @app.route("/hello/{name}")
    def greeting(req, resp, name):
        resp.text = f"Hello {name}"

    resp = test_client.get("http://testserver/hello/Fazliddin")

    assert resp.text == "Hello Fazliddin"


def test_class_based_get(app, test_client):

    @app.route("/books")
    class Book:

        def get(self, req, resp):
            resp.text = "Books page"

    assert test_client.get("http://testserver/books").text == "Books page"


def test_class_based_post(app, test_client):

    @app.route("/books")
    class Book:

        def post(self, req, resp):
            resp.text = "Endpoint to the create books"

    assert test_client.post(
        "http://testserver/books").text == "Endpoint to the create books"


def test_class_based_method_not_allowed(app, test_client):

    @app.route("/books")
    class Book:

        def get(self, req, resp):
            resp.text = "Books page"

    resp = test_client.post("http://testserver/books")

    assert resp.text == "Method Not Allowed."
    assert resp.status_code == 405


def test_alternative_add_routing(app, test_client):

    def new_handler(req, resp):
        resp.text = "From new handler"

    app.add_route("/new-handler", new_handler)

    assert test_client.get(
        "http://testserver/new-handler").text == "From new handler"


def test_template_handler(app, test_client):

    @app.route('/template')
    def template_handler(req, resp):
        resp.body = app.template(
            "test.html",
            context={
                "new_title": "Best title",
                "new_body": "Best body"
            }
        )
    resp = test_client.get("http://testserver/template")

    assert "Best title" in resp.text
    assert "Best body" in resp.text
    assert "text/html" in resp.headers["Content-type"]


def test_custom_exception_handler(app, test_client):

    def on_exception(req, resp, exc):
        resp.text = "Something bad exception"

    app.add_exception(on_exception)

    @app.route("/exception")
    def exception_throwing_handler(req, resp):
        raise AttributeError("Some exception")

    resp = test_client.get("http://testserver/exception")

    assert resp.text == "Something bad exception"


def test_non_existent_static_file(test_client):
    assert test_client.get(
        "http://testserver/nonexistent.css").status_code == 404


def test_static_file(test_client):
    resp = test_client.get("http://testserver/test.css")
    assert resp.text == "body {background-color: blue;}"
