import json
import os
import re
from pathlib import Path

from django.core.exceptions import ValidationError

from django.utils.translation import ugettext as _, ungettext

parent_location = Path(__file__).resolve().parent.parent
print(parent_location)

with open(os.path.join(parent_location, 'GMB_NetComm/sec_pass_req.json')) as reqs:
    REQS = json.load(reqs)


class NumberValidator(object):
    def __init__(self):
        self.min_digits = REQS['password_content_requirements']['min_digits']

    def validate(self, password, user=None):
        if not re.findall('\d', password):
            raise ValidationError(
                _(f"The password must contain at least {self.min_digits} digit, 0-9."),
                code='password_no_number',
            )
        else:
            return True

    def get_help_text(self):
        return _(
            f"Your password must contain at least {self.min_digits} digit, 0-9."
        )


class UppercaseValidator(object):
    def __init__(self):
        self.min_uppercase = REQS['password_content_requirements']['min_capitals']

    def validate(self, password, user=None):
        if not re.findall('[A-Z]', password):
            raise ValidationError(
                _(f"The password must contain at least {self.min_uppercase} uppercase letter, A-Z."),
                code='password_no_upper',
            )
        else:
            return True

    def get_help_text(self):
        return _(
            f"Your password must contain at least {self.min_uppercase} uppercase letter, A-Z."
        )


class LowercaseValidator(object):
    def __init__(self):
        self.min_lowers = self.min_uppercase = REQS['password_content_requirements']['min_lowers']

    def validate(self, password, user=None):
        if not re.findall('[a-z]', password):
            raise ValidationError(
                _(f"The password must contain at least {self.min_lowers} lowercase letter, a-z."),
                code='password_no_lower',
            )
        else:
            return True

    def get_help_text(self):
        return _(
            f"Your password must contain at least {self.min_lowers} lowercase letter, a-z."
        )


class SymbolValidator(object):
    def __init__(self):
        self.min_symbols = REQS['password_content_requirements']['min_specials']

    def validate(self, password, user=None):
        if not re.findall('[()[\]{}|\\`~!@#$%^&*_\-+=;:\'",<>./?]', password):
            raise ValidationError(
                _(f"The password must contain at least {self.min_symbols} symbol: " +
                  "()[]{}|\`~!@#$%^&*_-+=;:'\",<>./?"),
                code='password_no_symbol',
            )
        else:
            return True

    def get_help_text(self):
        return _(
            f"Your password must contain at least {self.min_symbols} symbol: " +
            "()[]{}|\`~!@#$%^&*_-+=;:'\",<>./?"
        )

def validate_password_complexity(password):
    validation_result = [NumberValidator().validate(password=password),
                         UppercaseValidator().validate(password=password),
                         LowercaseValidator().validate(password),
                         SymbolValidator().validate(password)]
    return validation_result
