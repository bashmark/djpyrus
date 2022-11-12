from django import forms


class AskVersionForm(forms.Form):
    scheme = forms.CharField(max_length=200, help_text='scheme')
    address = forms.CharField(max_length=200, help_text='address')
    port = forms.IntegerField(max_value=60000, help_text='port')


class AskForAllForm(forms.Form):
    pass


class LoadJsonForm(forms.Form):
    pass
