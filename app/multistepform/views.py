from django.shortcuts import render
from formtools.wizard.views import SessionWizardView
from .forms import professionalform, personalform, orderdetailsform
# Create your views here.

def home(request):
    return render(request, 'msf/home.html')

class msfsubmission(SessionWizardView):
    template_name = 'msf/msf.html'
    form_list = [personalform, professionalform, orderdetailsform]

    def done(self, form_list, **kwargs):
        return render(self.request, 'msf/home.html', {
            'form_data': [form.cleaned_data for form in form_list],
        })
