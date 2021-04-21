from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers


class ForeignKeyField(serializers.RelatedField):
    default_error_messages = {
        # 'required': _('This field is required.'),
        'does_not_exist': _('Invalid {filter_by} {data}, object does not exist.'),
        'incorrect_type': _('Incorrect type. Expected {filter_by} value, received {data_type}.'),
    }

    filter_by = 'id'

    def __init__(self, **kwargs):
        self.filter_by = kwargs.pop('filter_by', self.filter_by)
        super().__init__(**kwargs)

    def to_internal_value(self, data):
        try:
            return self.get_queryset().get(**{self.filter_by: data})
        except ObjectDoesNotExist:
            self.fail('does_not_exist', data=data, filter_by=self.filter_by)
        except (TypeError, ValueError):
            self.fail('incorrect_type', filter_by=self.filter_by, data_type=type(data).__name__)

    def to_representation(self, value):
        return str(value)
