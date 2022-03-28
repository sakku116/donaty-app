# this file is just like the database

from person import Person

def getList():
    return [
        Person('Steven Doe', 'Content Creator', './assets/creators/steven_doe.png'),
        Person('Ze', 'Digital Artist', './assets/creators/ze.jpg'),
        Person('Andre Rio', 'UI/UIX Designer', './assets/creators/andre_rio.jpg'),
        Person('Ky Craft 116', 'Content Creator', './assets/creators/ky_craft_116.jpg'),
        Person('Irwansyah Saputra', 'Influencer', './assets/creators/irwansyah_saputra.jpg'),
        Person('Aspect30', 'Content Creator', './assets/creators/aspect30.jpg'),
        Person('Rayen', 'Digital Artist', './assets/creators/rayen.jpg'),
        Person('Nino', 'Digital Artist', './assets/creators/nino.jpg'),
        Person('Windo Anggara', 'Content Creator', './assets/creators/windo_anggara.jpg')
    ]

def getNameAttrList(*args):
    lst = []
    for i in getList():
        lst.append(i.name)
    return lst

def search(n, *args):
    name_found = []

    def match(string, substring):
        if substring.lower() in string.lower():
            return True
        else:
            return False
    
    for i in getNameAttrList():
        if match(i, n):
            name_found.append(i)
            status = 'found'

    return [status, name_found]


