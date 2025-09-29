from django import forms
from django.core.exceptions import ValidationError
from .models import *


class VTCSForm(forms.ModelForm):
    class Meta:
        model = APITripData
        fields = [
            'vehicle_code',
            'before_weight',
            'after_weight',
            'time_in',
            'time_out',
            'trip_date',
            'before_picture',
            'after_picture',
            'roof_before_picture',
            'roof_after_picture',
            'slip_id',
            'lat',
            'long',
            'site_name',
            'site_id',
        ]

    def clean(self):
        cleaned_data = super().clean()

        # 1. Validate before_weight must be greater than after_weight
        before_weight = cleaned_data.get('before_weight')
        after_weight = cleaned_data.get('after_weight')

        if before_weight is not None and after_weight is not None:
            if before_weight <= after_weight:
                self.add_error('after_weight', 'After weight must be less than before weight')

        # 2. Validate time_in must be less than time_out
        time_in = cleaned_data.get('time_in')
        time_out = cleaned_data.get('time_out')

        if time_in is not None and time_out is not None:
            if time_in >= time_out:
                self.add_error('time_out', 'Exit time must be after entry time')

        # 3. Validate trip_date must match time_in date
        trip_date = cleaned_data.get('trip_date')

        if time_in is not None and trip_date is not None:
            if trip_date != time_in.date():
                self.add_error('trip_date', 'Trip date must match the entry time date')

        return cleaned_data