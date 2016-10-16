from pyramid.config import Configurator
from wsgiref.simple_server import make_server

import os

def main(global_config, **settings):
    os.chdir('/home/ubuntu/workspace/ex50')

    config = Configurator(settings=settings)
    config.add_route('view_hello', '/')
    config.add_route('view_verify', '/verify')
    config.add_route('view_webhook', '/webhook')
    config.scan('.views')
    return config.make_wsgi_app()
    

'''
if __name__ == '__main__':
    config = Configurator()
    config.add_route('hello', '/')
    config.scan('.')
    app = config.make_wsgi_app()
    server = make_server('0.0.0.0', 8080, app)
    server.serve_forever()
'''