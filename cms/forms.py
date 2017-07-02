from django import forms
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from cms.models import Material, Topic
from cms.validators import MaterialValidator

class AddMaterialForm(forms.ModelForm):
    user    = forms.ModelChoiceField(queryset = User.objects.first(), widget = forms.HiddenInput())
    topic   = forms.ModelChoiceField(queryset = Topic.objects.first(), widget = forms.HiddenInput())

    class Meta:
        model       = Material
        fields      = '__all__'
        validators  = {'link': MaterialValidator.validate_material_link}

        
