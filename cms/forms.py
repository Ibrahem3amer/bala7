from django import forms
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from cms.models import Material, Topic
from cms.validators import MaterialValidator

class AddMaterialForm(forms.ModelForm):
    user    = forms.ModelChoiceField(queryset = User.objects.all(), widget = forms.HiddenInput())
    topic   = forms.ModelChoiceField(queryset = Topic.objects.all(), widget = forms.HiddenInput())

    class Meta:
        model       = Material
        fields      = '__all__'

    def clean(self):

        # Parent validation.
        super(AddMaterialForm, self).clean()
        form_cleaned_data = self.cleaned_data

        # Validate material link validity.
        link_validation = MaterialValidator.validate_material_link(form_cleaned_data['link'])
        if link_validation != 1:
            raise forms.ValidationError("Material link should lead to pdf file, should not be broken link.")

        # Validate that date is not future date.
        date_validation = MaterialValidator.validate_date(form_cleaned_data['year'])
        if date_validation != 1:
            raise forms.ValidationError("Material date should not be in the future.")

        return form_cleaned_data


        
