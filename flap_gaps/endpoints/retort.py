from flask import request

from flap_gaps import app
from flap_gaps.forms.retort_forms import EchoForm
from flap_gaps.lib.rendering import render_json


@app.endpoint("retort.echo")
def echo():
    form = EchoForm(request.values)
    if form.validate():
        return render_json(form.echo.data)
    return render_json("YOU HAD ONE JOB TO DO!", success=False,
                       status=400)
