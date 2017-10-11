from django import forms
from django.contrib.auth.models import User
from cms.models import Material, Task
from cms.validators import MaterialValidator

class SupervisiorMaterialForm(forms.ModelForm):

    TYPE_CHOICES = ((1, 'Lecture'), (2, 'Asset'))
    content_type = forms.ChoiceField(choices=TYPE_CHOICES)

    class Meta:
        model = Material
        fields = '__all__'


class SupervisiorTaskForm(forms.ModelForm):

    TYPE_CHOICES = ((3, 'Task'), )
    content_type = forms.ChoiceField(choices=TYPE_CHOICES)

    class Meta:
        model = Task
        fields = '__all__'



