class Person():
    def __init__(self, name='unknown', role='unknown', photo_path=''):
        self.name = name
        self.photo_path = photo_path
        self.role = role

    def getAttributeList(self):
        return [self.name, self.role, self.photo_path]