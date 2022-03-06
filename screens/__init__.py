from .first_screen import FirstScreen
from .second_screen import SecondScreen

# this is my first time organizing modules into a package.
# so what this file does is include the class form some modules to one file.
# and im wondering why this file called __init__.py. so in my opinion (maybe this is a fact)
# is you will be able to import classes that included in this file to main code using
# name of directory or we can call it a 'package' and then import the classes directly
# from dir/package name.
# for example, in root/main.py you can import class that imported in here with:
# `
# from screens import FirstScreen
# from screens import SecondScreen
# `
# so, you dont need to import the class with `from screens.[name of file] import [class]`
