from django import forms


class ContactForm(forms.Form):
    name = forms.CharField(max_length=255)
    subject = forms.CharField(max_length=255)
    email = forms.EmailField()
    message = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 5, 'cols': 10})
    )

    def __str__(self):
        return self.subject
