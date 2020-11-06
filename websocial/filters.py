import django_filters

from django.contrib.auth.models import User

class userFilter(django_filters.FilterSet):
    class Meta:
        model = User

        fields = '__all__'