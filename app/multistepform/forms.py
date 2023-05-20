from django import forms
from core.models import personal, professional , orderdetails

class personalform(forms.ModelForm):
    class Meta:
        model =  personal
        fields = '__all__'

class professionalform(forms.ModelForm):
    class Meta:
        model = professional
        fields = '__all__'

class orderdetailsform(forms.ModelForm):
    class Meta:
        model = orderdetails
        fields = '__all__'





