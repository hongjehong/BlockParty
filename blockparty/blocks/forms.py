from django import forms
from .models import Party, Participate

class PartyForm(forms.ModelForm):

    class Meta:
        model = Party
        fields = '__all__'
        exclude = ('user', )


class ParticipateForm(forms.ModelForm):

    class Meta:
        model = Participate
        fields = '__all__'
        exclude = ('user', 'party', )
