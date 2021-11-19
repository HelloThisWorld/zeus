class Package:
    def __init__(self, pack_name: str, version: str, ):
        self.body = dict()
        self.body["pack_name"] = pack_name
        self.body["version"] = version

    def set(self, key: str, value: str):
        self.body[key] = value

    def get(self, key) -> str:
        if key in self.body:
            return self.body.get(key)
        else:
            return None

    def get_tar_name(self):
        return f"{self.get('pack_name')}_{self.get('version')}.tar.gz"

    def to_dict(self) -> dict:
        return self.body

