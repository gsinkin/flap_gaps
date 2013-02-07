import re
import locale
from datetime import timedelta
from datetime import datetime

locale.setlocale(locale.LC_ALL, "en_US.UTF-8")
NUMBER_RE = re.compile("\d+")


def format_phone(value):
    if not value:
        return value
    if len(value) == 10:
        return "(%s) %s-%s" % (value[0:3], value[3:6], value[6:])
    elif len(value) == 11:
        return "%s %s %s" % (value[0:5], value[5:8], value[8:])
    else:
        return value


def format_cash_money(value):
    if not value:
        return value
    if value.currency == "USD":
        return "${:,.2f}".format(value.amount)
    return "{:,.2f}".format(value) + " %" % value.currency


def format_date(value, f="%d/%m/%y"):
    return value.strftime(f)


def format_percent(value):
    return '{:g}%'.format(float(value) * 100)


def format_integer(value):
    return locale.format("%d", value, grouping=True)


def format_custom_charge_id(name):
    return "custom_%s" % int(NUMBER_RE.findall(name)[0])
