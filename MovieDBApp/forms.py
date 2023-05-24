from django.forms import ModelForm
from .models import *


class DirectorForm(ModelForm):
    class Meta:
        model = Director
        fields = '__all__'

class AudienceForm(ModelForm):
    class Meta:
        model = Audience
        fields = '__all__'