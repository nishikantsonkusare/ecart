from django import forms
from ecart.models import Banner

class BannerForm(forms.ModelForm):
    class Meta:
        model = Banner
        fields = ['image']

        widgets = {
            'image' : forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
    
    def clean(self):
        super(BannerForm, self).clean()
        image = self.cleaned_data.get('image')
        if image.size >= 4*1024*1024:
            self.add_error('image', 'Image must be less than 4MB.')
        return self.cleaned_data