from dao.director import DirectorDAO


class DirectorNotFound(Exception):
    pass


class DirectorService:
    def __init__(self, dao: DirectorDAO):
        self.dao = dao

    def get_one(self, bid):

        if bid == 0:
            raise DirectorNotFound
        return self.dao.get_one(bid)

    def get_all(self):
        return self.dao.get_all()

    def create(self, director_d):
        return self.dao.create(director_d)

    def update(self, director_d):
        self.dao.update(director_d)

    def partially_update(self, director_d):
        director = self.dao.get_one(director_d["id"])
        if "name" in director_d:
            director['name'] = director_d.get("name")
        self.dao.update(director)

    def delete(self, rid):
        self.dao.delete(rid)
