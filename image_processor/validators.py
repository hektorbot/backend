from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_neural_content_weight_blend(value):
    if value < 0 or value > 1.0:
        raise ValidationError(
            _("%(value)s should be in range [0.0; 1.0]"), params={"value": value}
        )

