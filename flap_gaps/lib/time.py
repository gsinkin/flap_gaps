from datetime import datetime

from sqlalchemy import text


server_now = text("(NOW() AT TIME ZONE 'UTC')")


def _pluralize(value):
    return "s" if value > 1 else ""


def time_from_now(timestamp):
    now = datetime.utcnow()
    time_diff = now - timestamp

    if time_diff.days > 0:
        return "%s day%s ago" % (time_diff.days, _pluralize(time_diff.days))
    else:
        hours = time_diff.seconds / 3600
        minutes = time_diff.seconds / 60
        if hours > 0:
            return "%s hour%s ago" % (hours, _pluralize(hours))
        elif minutes > 0:
            return "%s minute%s ago" % (minutes, _pluralize(minutes))
        return "%s seconds ago" % time_diff.seconds
