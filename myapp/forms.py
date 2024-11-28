from django import forms

class UserInputForm(forms.Form):
    equation = forms.CharField(label='Differential Equation f(x, y)', max_length=100)
    x0 = forms.FloatField(label='Initial x0')
    y0 = forms.FloatField(label='Initial y0')
    x_end = forms.FloatField(label='End of Interval (x_end)')
    h = forms.FloatField(label='Step Size (h)')
    method = forms.ChoiceField(choices=[('euler', 'Euler'), ('euler-cauchy', 'Euler-Cauchy')], label='Method')
