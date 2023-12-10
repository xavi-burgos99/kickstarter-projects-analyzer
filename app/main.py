import eel;
import os;

eel.init('www')
eel.start('templates/index.html', size=(1000, 600), port=8800, jinja_templates='templates')