from django import forms

class SleepInputForm(forms.Form):
    hours = forms.FloatField(label='Скільки годин?')
