from wtforms import Form
from wtforms import TextField
from wtforms import validators


class EchoForm(Form):
    echo = TextField("Echo", [validators.Required()])
