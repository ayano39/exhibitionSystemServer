class RouteInfo:

    def __init__(self,grade,path):
        self.grade = grade
        self.path = path

    def toJson(self):
        return self.path