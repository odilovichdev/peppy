from webob import Request, Response
from parse import parse
import requests
import wsgiadapter
import inspect


class PeppyApp:

    def __init__(self):
        self.routes = dict()

    def __call__(self, environ, start_response):
        request = Request(environ)
        response = self.handler_request(request)
        return response(environ, start_response)

    def handler_request(self, request):
        response = Response()

        handler, kwargs = self.find_handler(request)
        if handler is not None:
            if inspect.isclass(handler):
                handler = getattr(handler(), request.method.lower(), None)
                if handler is None:
                    response.status_code = 405
                    response.text = "Method Not Allowed."
                    return response
            handler(request, response, **kwargs)
        else:
            self.default_response(response)

        return response

    def find_handler(self, request):
        """Find handlers"""
        for path, handler in self.routes.items():
            parsed_result = parse(path, request.path)
            if parsed_result is not None:
                return handler, parsed_result.named
        return None, None

    def default_response(self, response):
        response.status_code = 404
        response.text = "Not Found."

    def route(self, path):
        assert path not in self.routes, "Dublicate route. Please the achange url."

        def wrapper(handler):
            self.routes[path] = handler
            return handler
        return wrapper

    def test_session(self):
        session = requests.Session()
        session.mount("http://testserver", wsgiadapter.WSGIAdapter(self))
        return session
