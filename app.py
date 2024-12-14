from webob import Request, Response


class PeppyApp:

    def __init__(self):
        self.routes = dict()

    def __call__(self, environ, start_response):
        request = Request(environ)
        response = self.handler_request(request)
        return response(environ, start_response)

    def handler_request(self, request):
        response = Response()

        handler = self.find_handler(request)
        if handler is not None:
            handler(request, response)
        else:
            self.default_response(response)

        return response

    def find_handler(self, request):
        for path, handle in self.routes.items():
            if request.path == path:
                return handle

    def default_response(self, response):
        response.status_code = 404
        response.text = "Not Found."

    def route(self, path):
        def wrapper(handler):
            self.routes[path] = handler
            return handler
        return wrapper
