from django import forms

class QRCodeForm(forms.Form):
    num_qr_codes = forms.IntegerField(label='عدد أكواد QR', min_value=1)
    num_uses = forms.IntegerField(label='عدد مرات الاستخدام المسموح بها', min_value=1)