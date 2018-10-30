from django.db import models
from django.utils import timezone

# Create your models here.
class kullanici(models.Model):
    kullanici_adi = models.CharField(max_length=16, verbose_name="Kullanıcı Adı")
    sifre = models.CharField(max_length=21,verbose_name="Şifre")
    email = models.EmailField(default="",max_length=51,verbose_name="Email")
    hoca_mi = models.CharField(default="",max_length=1,verbose_name="Eğitmen mi?")
    def __int__(self):
        return self.id


class kullanici_ayrinti(models.Model):
    isim = models.CharField(default="",max_length=200,null=True,verbose_name="İsim")
    #soyisim = models.CharField(default="",max_length=51, null=True, verbose_name="Soysim")
    resim = models.CharField(default="/static/img/default.png",null=True,max_length=701,verbose_name="Resim")
    kayit_tarihi = models.DateTimeField(default=timezone.now)
    dogum_tarihi = models.DateTimeField(null=True)
    telefon= models.CharField(default="",max_length=11,blank=True,verbose_name="Telefon No")
    cinsiyet = models.CharField(max_length=1, blank=True, default="")
    kilo = models.IntegerField(default=0)
    boy = models.IntegerField(default=0)
    problem = models.CharField(default="",blank=True,max_length=700)
    pt_kontrol = models.IntegerField(default=0)
    trainer = models.CharField(default="", max_length=50)
    def __str__(self):
        return self.isim


class hocalar(models.Model):
    isim = models.CharField(default="", max_length=200, null=True, verbose_name="İsim")
    #soyisim = models.CharField(default="", max_length=51, null=True, verbose_name="Soysim")
    kayit_tarihi = models.DateTimeField(default=timezone.now)
    dogum_tarihi = models.DateTimeField(null=True)
    telefon= models.CharField(default="",max_length=11,blank=True,verbose_name="Telefon No")
    cinsiyet = models.CharField(max_length=1, blank=True, default="")
    universite = models.CharField(default="", max_length=100, null=True, verbose_name="Üniversite")
    bolum = models.CharField(default="", max_length=100, null=True, verbose_name="Bölüm")
    resim = models.CharField(default="/static/img/default.png",null=True,max_length=701,verbose_name="Resim")
    ogrenci = models.CharField(default="", max_length=51,null=True,verbose_name="PT Verilen Öğrenci(ler)")
    #deneme = models.ForeignKey(kullanici_ayrinti,on_delete=models.CASCADE, null=True) #BURANIN İŞARET ETTİĞİ KAYIT SİLİİNİRSE. BU KAYITTA TAMAMEN SİLİNİYOR.
    def __str__(self):
        return self.isim

"""
class pt_alan_ogrenciler(models.Model):
    isim = models.ForeignKey(kullanici_ayrinti,on_delete=models.CASCADE,verbose_name="isim")
    saat = models.IntegerField(default=0,null=True,verbose_name="aldığı saat")
    paket = models.CharField(default="",max_length=50,null=True,verbose_name="Alınan Paket")
    egitmen = models.ForeignKey(hocalar,on_delete=models.CASCADE,verbose_name="Eğitmen")
    tarih = models.DateTimeField(default=timezone.now)
    ogr_id = models.ForeignKey(kullanici,on_delete=models.CASCADE)
    def __str__(self):
        return self.isim"""



class uretilen_kodlar(models.Model):
    kod = models.IntegerField()
    def __int__(self):
        return self.kod


class okul(models.Model):
    okul = models.CharField(max_length=100)
    def __str__(self):
        return self.okul

class bolum(models.Model):
    bolum = models.CharField(max_length=100)
    def __str__(self):
        return self.bolum
