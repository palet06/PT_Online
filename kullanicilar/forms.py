from django import forms
from .models import kullanici



class KullaniciKayitFormuInputlari(forms.Form):
    kullanici_adi = forms.CharField(max_length=15,label="Kullanıcı Adı")
    sifre = forms.CharField(max_length=20,label="Şifre",widget=forms.PasswordInput)
    confirm = forms.CharField(max_length=20,label="Şifreyi Doğrula",widget=forms.PasswordInput)
    email = forms.EmailField(max_length=50,label="Email Adresi",widget=forms.EmailInput)
    def clean(self):
        kullanici_adi = self.cleaned_data.get('kullanici_adi')
        sifre = self.cleaned_data.get('sifre')
        confirm = self.cleaned_data.get('confirm')
        email = self.cleaned_data.get('email')
        gonder =  {"kullanici_adi":kullanici_adi,"sifre":sifre,"confirm":confirm,"email":email}
        return gonder

class PostForm(forms.ModelForm):
    class Meta:
        model = kullanici
        fields = ('kullanici_adi','email',)










