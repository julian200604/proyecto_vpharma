from django import forms
from .models import Order

class OrderCreateForm(forms.ModelForm):
    # Define las opciones de forma de pago
    PAYMENT_METHOD_CHOICES = [
        ('contraentrega', 'Pago Contraentrega'),
        ('retiro', 'Yo lo retiro'),
    ]
    
    # Cambia el campo de pago a MultipleChoiceField
    payment_method = forms.MultipleChoiceField(
        choices=PAYMENT_METHOD_CHOICES,
        widget=forms.CheckboxSelectMultiple,  # Muestra las opciones como checkboxes
        required=True,  # Puedes ajustar esto según si es obligatorio o no
    )

    class Meta:
        model = Order
        fields = [
            'first_name',
            'last_name',
            'address',
            'neighborhood',
            'phone_number',
            'instructions',
            'payment_method',
        ]
        widgets = {
            'instructions': forms.Textarea(attrs={'rows': 5, 'cols': 30}),
        }