import json
import urllib
from flask import request, session, Response
from flask import render_template

from flap_gaps.lib import time
from flap_gaps.lib import formatting_utils


def render_html_template(template, context=None):
    if not context:
        context = {}

    context["request"] = request
    context["session"] = session

    return render_template(template, **context)


def render_json(python_obj=None, success=True, status=200, pretty=False):
    if python_obj is None:
        python_obj = {}
    if type(python_obj) == dict:
        python_obj["success"] = success
    else:
        python_obj = {"success": success,
                      "result": python_obj}

    if pretty:
        json_response = json.dumps(python_obj, indent=2)
    else:
        json_response = json.dumps(python_obj)

    return Response(json_response, mimetype="application/json",
                    content_type="application/json; charset=utf-8",
                    status=status)


def urlencode(value, key):
    return urllib.urlencode({key: value})


FILTERS = {
    "format_cash_money": formatting_utils.format_cash_money,
    "format_phone": formatting_utils.format_phone,
    "format_date": formatting_utils.format_date,
    "format_percent": formatting_utils.format_percent,
    "format_integer": formatting_utils.format_integer,
    "format_custom_charge_id": formatting_utils.format_custom_charge_id,
    "time_from_now": time.time_from_now,
    "urlencode": urlencode}

JINJA_ENV = None


def load_filters(jinja_env):
    global JINJA_ENV
    JINJA_ENV = jinja_env
    jinja_env.filters.update(FILTERS)


def template_filter(name=None):
    return JINJA_ENV.filters[name]
