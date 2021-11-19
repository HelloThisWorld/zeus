import tornado.web
import tornado.ioloop

from thunder import load_data
from thunder.controller.RequestHandlers import BasicRequstHandler, SearchRequestHandler

if __name__ == "__main__":
    app = tornado.web.Application([
        (r"/", BasicRequstHandler),
        (r"/search", SearchRequestHandler)
    ])

    # load data from remote
    load_data()

    app.listen(5000)
    print("Listening on port 5000")
    tornado.ioloop.IOLoop.current().start()
