import json

import tornado.web
import urllib.parse

from thunder import get_connection, PackageContentService


class BasicRequstHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("../template/html/index.html")


class SearchRequestHandler(tornado.web.RequestHandler):
    def get(self):
        header = "Content-Type"
        body = "application/json"
        self.set_header(header, body)
        conn = get_connection()
        package_service = PackageContentService(conn)
        query_package = urllib.parse.unquote(self.get_argument("q"))
        package = package_service.fetch_by_name(pack_name=query_package)
        self.write(json.dumps(package))
