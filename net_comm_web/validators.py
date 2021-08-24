import json
import os
import re
from pathlib import Path
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _, ungettext
from django_password_validators.password_history.password_validation import UniquePasswordsValidator

# Define the location for pass requirement file
parent_location = Path(__file__).resolve().parent.parent

with open(os.path.join(parent_location, 'GMB_NetComm/sec_pass_req.json')) as reqs:
    REQS = json.load(reqs)


def validate(password, user=None):
    try:
        UniquePasswordsValidator.validate(password)
        print(f'{password} is valid: past')
    except:
        return False
    return True


class PastPassValidator(object):
    def __init__(self):
        self.past_password = REQS['last_passwords']

    def validate(self, password, user=None):
        print(f'Starting validation for: {user}')
        try:
            UniquePasswordsValidator.validate(user, password)
            print(f'{password} is valid: past')
        except:
            print(UniquePasswordsValidator.validate(user, password))
        return True

    def get_help_text(self):
        return _(f'Your password must be different then your {self.past_password} last passwords.')


# Validate that the password has the required amount of numbers
class NumberValidator(object):
    def __init__(self):
        self.min_digits = REQS['password_content_requirements']['min_digits']

    def validate(self, password, user=None):
        if len([*re.findall('\d', password)]) < self.min_digits:
            raise ValidationError(
                _(f"The password must contain at least {self.min_digits} digit, 0-9."),
                code='password_no_number',
            )

    def get_help_text(self):
        return _(
            f"Your password must contain at least {self.min_digits} digit, 0-9."
        )


# Validate that the password has the required amount of uppercase characters
class UppercaseValidator(object):
    def __init__(self):
        self.min_uppercase = REQS['password_content_requirements']['min_capitals']

    def validate(self, password, user=None):
        if len([*re.findall('[A-Z]', password)]) < self.min_uppercase:
            raise ValidationError(
                _(f"The password must contain at least {self.min_uppercase} uppercase letter, A-Z."),
                code='password_no_upper',
            )

    def get_help_text(self):
        return _(
            f"Your password must contain at least {self.min_uppercase} uppercase letter, A-Z."
        )


# Validate that the password has the required amount of lowercase characters
class LowercaseValidator(object):
    def __init__(self):
        self.min_lowers = REQS['password_content_requirements']['min_lowers']

    def validate(self, password, user=None):
        if len([*re.findall('[a-z]', password)]) < self.min_lowers:
            raise ValidationError(
                _(f"The password must contain at least {self.min_lowers} lowercase letter, a-z."),
                code='password_no_lower',
            )

    def get_help_text(self):
        return _(
            f"Your password must contain at least {self.min_lowers} lowercase letter, a-z."
        )


# Validate that the password has the required amount of special characters
class SymbolValidator(object):
    def __init__(self):
        self.min_symbols = REQS['password_content_requirements']['min_specials']

    def validate(self, password, user=None):
        if len([*re.findall('[()[\]{}|\\`~!@#$%^&*_\-+=;:\'",<>./?]', password)]) < self.min_symbols:
            raise ValidationError(
                _(f"The password must contain at least {self.min_symbols} symbol: " +
                  "()[]{}|\`~!@#$%^&*_-+=;:'\",<>./?"),
                code='password_no_symbol',
            )

    def get_help_text(self):
        return _(
            f"Your password must contain at least {self.min_symbols} symbol: " +
            "()[]{}|\`~!@#$%^&*_-+=;:'\",<>./?"
        )


# Validate that the password has the required length
class LengthValidator(object):
    def __init__(self):
        self.min_length = REQS['min_pass_length']

    def validate(self, password, user=None):
        if len(password) < self.min_length:
            raise ValidationError(
                _(f'Your password must have at least {self.min_length} characters'),
                code='insufficient_length'
            )

    def get_help_text(self):
        return _(f'Your password must have at least {self.min_length} characters')


# Perform all password validations
def validate_password_complexity(password):
    valid_length = True
    num_valid = True
    upper_valid = True
    lower_valid = True
    special_valid = True

    try:
        LengthValidator().validate(password)
    except:
        valid_length = LengthValidator().get_help_text()
    try:
        NumberValidator().validate(password=password)
    except:
        num_valid = NumberValidator().get_help_text()
    try:
        UppercaseValidator().validate(password=password)
    except:
        upper_valid = UppercaseValidator().get_help_text()
    try:
        LowercaseValidator().validate(password=password)
    except:
        lower_valid = LowercaseValidator().get_help_text()
    try:
        SymbolValidator().validate(password=password)
    except:
        special_valid = SymbolValidator().get_help_text()

    return [valid_length, num_valid, upper_valid, lower_valid, special_valid]
