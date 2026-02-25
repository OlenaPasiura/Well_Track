from django import forms
from .models import SleepRecord

class SleepInputForm(forms.ModelForm):
    model = SleepRecord
    fields = ['start_time', 'end_time']
