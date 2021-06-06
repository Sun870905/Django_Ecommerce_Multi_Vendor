from apps.products.models import Product
from django.core.mail import BadHeaderError, send_mail
from django.http import HttpResponse
from django.views.generic import FormView, ListView

from .forms import ContactForm
from .settings.production import CONTACT_EMAIL


class Contact(FormView):
    form_class = ContactForm
    template_name = "contact.html"

    def form_valid(self, form):
        subject = form.cleaned_data['subject']
        email = form.cleaned_data['email']
        message = form.cleaned_data['message']
        try:
            send_mail(subject, message, email, [CONTACT_EMAIL])
        except BadHeaderError:
            return HttpResponse('Invalid header found.')
        return super().form_valid(form)


class Home(ListView):
    model = Product
    queryset = Product.objects.all()[0:8]
    context_object_name = 'newest_products'
    template_name = "home.html"
