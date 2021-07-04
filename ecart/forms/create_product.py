from django import forms
from ecart.models import Product, Category, SubCategory
from ckeditor.widgets import CKEditorWidget

class Create_Product_Form(forms.ModelForm):
    
    # product_description = forms.CharField(widget = CKEditorWidget())

    class Meta:
        model = Product

        # fields = ['product_name', 'product_description', 'mrp', 'selling_price', 'stock', 'thumbnail', 'img1', 'img2', 'img3']
        fields = '__all__'

        widgets = {
            'product_name' : forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off'}),
            'product_description' : forms.CharField(widget=CKEditorWidget()),
            # 'product_description' : forms.Textarea(attrs={'rows': 5, 'class': 'form-control'}),
            'mrp' : forms.NumberInput(attrs={'class': 'form-control'}),
            'selling_price' : forms.NumberInput(attrs={'class': 'form-control'}),
            'stock' : forms.NumberInput(attrs={'class': 'form-control'}),
            'category_name' : forms.Select(attrs={'class': 'form-select'}),
            'sub_category' : forms.Select(attrs={'class': 'form-select'}),
            # 'size' : forms.Select(attrs={'class': 'form-select'}),
            # 'color' : forms.Select(attrs={'class': 'form-select'}),
            'thumbnail' : forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'img1' : forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'img2' : forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'img3' : forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

        help_texts = {
                'thumbnail': 'Resolution must be 1500x1500',
                'img1': 'Resolution must be 1500x1500',
                'img2': 'Resolution must be 1500x1500',
                'img3': 'Resolution must be 1500x1500',
        }

    def clean(self):
        super(Create_Product_Form, self).clean()

        product_name = self.cleaned_data.get('product_name')
        product_description = self.cleaned_data.get('product_description')
        mrp = self.cleaned_data.get('mrp')
        selling_price = self.cleaned_data.get('selling_price')
        stock = self.cleaned_data.get('stock')
        category_name = self.cleaned_data.get('category_name')
        sub_category = self.cleaned_data.get('sub_category')
        thumbnail = self.cleaned_data.get('thumbnail')
        img1 = self.cleaned_data.get('img1')
        img2 = self.cleaned_data.get('img2')
        img3 = self.cleaned_data.get('img3')

        print(thumbnail)
    
        if len(product_name) <= 10:
            self.add_error('product_name', 'Product name must be greater than 10 charachter.')

        if not product_description:
            self.add_error('product_description', 'Please write description for product.') 

        data = Category.objects.values('id').filter(name = category_name)
        check_subcat = SubCategory.objects.filter(category_id=data[0]['id'])

        if sub_category not in check_subcat:
            self.add_error('sub_category', 'Please select valid sub-category for category.')

        if stock <= 0:
            self.add_error('stock', 'Stock must not be 0.')

        if mrp <= 0:
            self.add_error('mrp', 'MRP not equal to 0.')

        if mrp <= selling_price:
            self.add_error('mrp', 'MRP must be greater than selling price.')

        if selling_price <= 0:
            self.add_error('selling_price', 'Selling price not equal to 0.')

        if selling_price >= mrp:
            self.add_error('selling_price', 'Selling price must be smaller than MRP price.')

        if not thumbnail:
            self.add_error('thumbnail', 'Please select image for thumbnail.')

        if thumbnail:
            if thumbnail.size >= 4194304:
                self.add_error('thumbnail', 'Thumbnail must be less than 4 MB.')

        if img1:
            if img1.size >= 4194304:
                self.add_error('img1', 'Image must be less than 4 MB.')
        
        if img2:
            if img2.size >= 4194304:
                self.add_error('img2', 'Image must be less than 4 MB.')
        
        if img3:
            if img3.size >= 4194304:
                self.add_error('img3', 'Image must be less than 4 MB.')

        return self.cleaned_data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['sub_category'].queryset = SubCategory.objects.all().distinct('name').order_by('name')
