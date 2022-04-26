import inspect
from typing import Callable

from wunderbar.requests import Request
from wunderbar.templating import DefaultIndex, PageNotFound404


class WunderbarApp:
    """My custom framework class"""

    def __init__(self, routes: dict = None):
        """
        Framework class initialization function
        Pass server routes for accessing them later
        :param routes: server routes
        """
        self.routes = routes if routes else {'/': DefaultIndex()}
        self._not_found_view = PageNotFound404

    def __call__(self, environ, start_response):
        """
        Framework callable
        :param environ: a WSGI environment
        :param start_response: a callable accepting a status code,
            a list of headers, and an optional exception context to
            start the response
        :return: response body
        """
        request = Request(environ['REQUEST_METHOD']).get_request(environ)
        print(f'Got {request["method"]} request with data '
              f'{request["data"] if "data" in request else request["request_params"]}')
        code, body = self._get_view(environ['PATH_INFO'], request)
        start_response(code, [('Content-Type', 'text/html')])
        return [body.encode('utf-8')]

    def _get_view(self, path: str, request):
        """
        Calls view via corresponding resource
        path and returns response code and body
        :param path: resource path
        :param request: request
        :return: (response code, body)
        """
        path = f'{path}/' if not path.endswith('/') else path
        if path in self.routes:
            view = self.routes[path]
        else:
            view = self.not_found_view
        return view(request)

    @property
    def not_found_view(self):
        """Not found view getter"""
        # Return a callable class instance or a function object
        return self._not_found_view() if inspect.isclass(self._not_found_view) else self._not_found_view

    @not_found_view.setter
    def not_found_view(self, not_found_cls: Callable):
        """
        Not found view setter
        :param not_found_cls: a callable function
        """
        self._not_found_view = not_found_cls


def main():
    app = WunderbarApp()
    app.run()


if __name__ == '__main__':
    main()
