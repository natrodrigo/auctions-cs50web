from django import forms
from .models import AuctionListing, Comment

class AuctionListingForm(forms.ModelForm):
    class Meta:
        model = AuctionListing
        exclude = ['active','user']

    def __init__(self, *args, **kwargs):
        super(AuctionListingForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class CommentForm (forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']

    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'