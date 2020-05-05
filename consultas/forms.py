from django import forms
from tempus_dominus.widgets import DatePicker


class ConsultasForms(forms.Form):
    dia_inicial = forms.DateField(label='Dia Inicial', widget=DatePicker())
    dia_final = forms.DateField(label='Dia Final', widget=DatePicker())
