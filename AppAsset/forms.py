from django import forms
from AppAsset.models import *

WORKING_STATUS = (
    ('Functional', 'Functional'),
    ('Non-Functional', 'Non-Functional'),
)

STATUS_CONDITION = (
    ('Excellent', 'Excellent'),
    ('Good', 'Good'),
    ('Fair', 'Fair'),
    ('Poor', 'Poor'),
    ('Failing', 'Failing'),
)

CONTAINER_SIZE = (
    ('Small', 'Small'),
    ('Medium', 'Medium'),
    ('Large', 'Large')
)

STATUS_ARRAY = (
    ('Active', 'Active'),
    ('Block', 'Block'),
)


class FormContainer(forms.ModelForm):
    container_code = forms.CharField(max_length=100, required=False, widget=forms.TextInput(
        attrs={'autocomplete': 'off', 'class': 'form-control', 'readonly': 'true'}))
    container_name = forms.CharField(max_length=100, required=False, widget=forms.TextInput(
        attrs={'autocomplete': 'off', 'class': 'form-control', 'placeholder': 'Enter Container Name'}))
    address = forms.CharField(max_length=100, required=False, widget=forms.TextInput(
        attrs={'autocomplete': 'off', 'class': 'form-control', 'placeholder': 'Enter Address'}))
    area = forms.CharField(max_length=100, required=False, widget=forms.TextInput(
        attrs={'autocomplete': 'off', 'class': 'form-control', 'placeholder': 'Enter Area'}))
    size = forms.CharField(max_length=100, required=False, widget=forms.Select(
        choices=CONTAINER_SIZE, attrs={'class': 'default-select form-control form-control-sm wide'}))
    working_status = forms.CharField(max_length=100, required=False, widget=forms.Select(
        choices=WORKING_STATUS, attrs={'class': 'default-select form-control form-control-sm wide'}))
    status = forms.CharField(max_length=100, required=False, widget=forms.Select(
        choices=STATUS_ARRAY, attrs={'class': 'default-select form-control form-control-sm wide'}))

    class Meta:
        model = ContainerData
        fields = [
            'container_code',
            'container_name',
            'address',
            'area',
            'size',
            'working_status',
            'status',
        ]
