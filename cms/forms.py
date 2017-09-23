import datetime
from django import forms
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.forms.widgets import SelectDateWidget
from django.shortcuts import get_object_or_404
from cms.models import Material, Topic, UserContribution, Professor, UserPost
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

        return form_cleaned_data


class UserContributionForm(forms.ModelForm):

    # Fields 
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control nj-input'}))
    content = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control nj-textarea'}))
    link = forms.URLField(widget=forms.URLInput(attrs={'class': 'form-control nj-input'}))
    term = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control select nj-select'}), choices=UserContribution.term_choices)
    content_type = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control select nj-select'}), choices=UserContribution.type_choices)
    week_number = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control nj-input'}))
    deadline = forms.DateField(widget=forms.SelectDateWidget(attrs={'class': 'form-control nj-input'}))
    professor = forms.ModelMultipleChoiceField(queryset=Professor.objects.all(), required=False)
    topic = forms.CharField(widget=forms.HiddenInput())
    user = forms.CharField(widget=forms.HiddenInput())

    class Meta:
        model = UserContribution
        exclude = ['user', 'topic', 'year', 'status', 'supervisior_id']

    def __init__(self, *args, **kwargs):
        super(UserContributionForm, self).__init__(*args, **kwargs)
        initial_arguments = kwargs.get('initial', None)
        if initial_arguments:
            self.instance.topic = get_object_or_404(Topic, pk=initial_arguments.get('topic', -1))
            self.instance.user = get_object_or_404(User, pk=initial_arguments.get('user', -1))
            self.instance.year = datetime.datetime.now()
            self.instance.supervisior_id = -1

        # Filtering professors to the ones who lays in same user topics.
        try:
            professor_query = Professor.objects.filter(id__in=self.instance.topic.professors.all())
            self.fields['professor'].queryset = professor_query
        except:
            self.fields['professor'].queryset = []
        
class UserPostForm(forms.ModelForm):
    
    # Fields
    title = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control nj-input'}))
    content = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control nj-textarea'}))
    topic = forms.CharField(widget=forms.HiddenInput())
    user = forms.CharField(widget=forms.HiddenInput())

    class Meta:
        model = UserPost
        fields = ['title', 'content']

    def __init__(self, *args, **kwargs):
        super(UserPostForm, self).__init__(*args, **kwargs)
        initial_arguments = kwargs.get('initial', None)
        if initial_arguments:
            self.instance.topic = get_object_or_404(Topic, pk=initial_arguments.get('topic', -1))
            self.instance.user = get_object_or_404(User, pk=initial_arguments.get('user', -1))