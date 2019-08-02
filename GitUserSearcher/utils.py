
def log_message(thing, message):
    """:returns: detailed error message using reflection"""
    return '{} {}'.format(repr(thing), message)


class LogUtilMixin(object):

    def log(self, message):
        """:returns: Log message formatting"""
        if message is None:
            message = ''

        return log_message(thing=self, message=message)


def get_non_field_error(message):

    return {
        'non_field_errors': [
            message
        ]
    }
