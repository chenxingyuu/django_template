from django_filters import rest_framework as filters

from .models import User


class UserFilter(filters.FilterSet):
    email = filters.CharFilter(field_name='email', lookup_expr='contains', help_text='email')

    class Meta:
        model = User
        fields = ('email',)
