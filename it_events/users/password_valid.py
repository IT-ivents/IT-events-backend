import re
from difflib import SequenceMatcher

from django.contrib.auth import password_validation as pw
from django.utils.translation import gettext as _
from rest_framework.exceptions import NotAcceptable


class NumericPasswordValid(pw.NumericPasswordValidator):
    def validate(self, password, user=None):
        if password.isdigit():
            raise NotAcceptable(
                'Введённый пароль состоит только из цифр'
            )

    def get_help_text(self):
        return _("Your password can’t be entirely numeric.")


class CommonPasswordValidator(pw.CommonPasswordValidator):
    def validate(self, password, user=None):
        if password.lower().strip() in self.passwords:
            raise NotAcceptable(
                'Введённый пароль слишком распространен.'
            )

    def get_help_text(self):
        return _("Your password can’t be a commonly used password.")


class UserAttributeSimilarityValidator(pw.UserAttributeSimilarityValidator):
    def validate(self, password, user=None):
        if not user:
            return

        password = password.lower()
        for attribute_name in self.user_attributes:
            value = getattr(user, attribute_name, None)
            if not value or not isinstance(value, str):
                continue
            value_lower = value.lower()
            value_parts = re.split(r"\W+", value_lower) + [value_lower]
            for value_part in value_parts:
                if pw.exceeds_maximum_length_ratio(
                    password, self.max_similarity, value_part
                ):
                    continue
                if (
                    SequenceMatcher(a=password, b=value_part).quick_ratio()
                    >= self.max_similarity
                ):
                    raise NotAcceptable(
                        _('Введённый пароль слишком похож на email address.'),
                    )

    def get_help_text(self):
        return _(
            "Your password can’t be too similar to your other personal "
            "information."
        )
