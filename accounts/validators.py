from django.core.exceptions import ValidationError


def validate_phone_numbers(value):
    telephone_chars = ("+", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9")
    if value[0] != "+":
        raise ValidationError(
                "The first character should be '+'."
            )
    for x in value:
        if x not in telephone_chars:
            raise ValidationError(
                "Please, enter a number, which contains digits and '+' sign."
                "Do not include spaces or other symbols."
            )