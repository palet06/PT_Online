from django.shortcuts import render,redirect,reverse,HttpResponse
from django.core.files import File
from .forms import KullaniciKayitFormuInputlari
from .models import kullanici, kullanici_ayrinti, uretilen_kodlar,hocalar,okul,bolum
from django.contrib.auth import login,authenticate,logout
from django.contrib import messages
from django import forms
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.utils.dateparse import parse_datetime
import os
import random

# ----------------------------------------ŞİFRE DEĞİŞTİRME--------------------------------
def sifre(request):
    if request.method == "POST":
        ms = request.POST.get("mevcut_sifre")
        ys = request.POST.get('yeni_sifre')
        yst = request.POST.get('yeni_sifre_tekrar')
        ms_varmi = kullanici.objects.filter(id = request.session['id']).first()
        if (ms == "") or (ys == "") or (yst == ""):
            messages.warning(request, "Lütfen tüm alanları doldurun")
            return render(request, "sifre_degistir.html")
        elif (ms == ms_varmi.sifre):
            if (ys != yst):
                messages.warning(request, "Şifreleriniz eşleşmiyor")
                return render(request, "sifre_degistir.html")
            else:
                ms_varmi.sifre = ys
                ms_varmi.save()
                messages.success(request, "Şifreniz değiştirildi.")
                return render(request, "sifre_degistir.html")
        else:
            messages.warning(request, "Eski şifrenizi yanlış girdiniz")
            return render(request, "sifre_degistir.html")

    return render(request,"sifre_degistir.html")

# ------------------------------------------KULLANICI KAYIT--------------------------------


def kayit(request):
    if request.method == "POST":
        kim = request.POST.get("kim")
        if kim == "uye":
            ka = request.POST.get("kullanici_adi")
            si = request.POST.get('sifre')
            csi = request.POST.get('confirm')
            em = request.POST.get('email')
            ka_varmi = kullanici.objects.filter(kullanici_adi = ka).first()
            em_varmi = kullanici.objects.filter(email = em).first()
            if (ka == "") or (si == "") or (csi == "") or (em == ""):
                messages.warning(request, "Lütfen tüm alanları doldurun")
                print(kim)
                return render(request, "kayit.html",{"sayfa":kim,"kullanici_adi":ka,"email":em})
            if ka_varmi:
                messages.warning(request, "Bu kullanıcı adı zaten mevcut")
                return render(request,"kayit.html",{"sayfa":kim,"kullanici_adi":ka,"email":em})
            if (si and csi and si != csi):
                messages.warning(request, "Şifreleriniz eşleşmiyor")
                return render(request,"kayit.html",{"sayfa":kim,"kullanici_adi":ka,"email":em})
            if em_varmi:
                messages.warning(request, "Bu email adresi zaten kullanılıyor.")
                return render(request,"kayit.html",{"sayfa":kim,"kullanici_adi":ka,"email":em})
            k_ekle = kullanici(kullanici_adi=ka, sifre=si, email=em,hoca_mi="H")
            k_ekle.save()
            ayrinti_ekle = kullanici_ayrinti(id = k_ekle.id)
            ayrinti_ekle.save()
            request.session['member'] = ka
            request.session['id'] = k_ekle.id
            request.session['tip'] = "uye"
            return render(request,"index.html")
        if kim == "egitmen":
            ka = request.POST.get("hoca_kullanici_adi")
            si = request.POST.get("hoca_sifre")
            csi = request.POST.get("hoca_confirm")
            em = request.POST.get("hoca_email")
            hkod = request.POST.get("hoca_egitmen_kodu")
            if hkod == "":
                hkod =0
            ka_varmi = kullanici.objects.filter(kullanici_adi=ka).first()
            em_varmi = kullanici.objects.filter(email=em).first()
            kod_varmi = uretilen_kodlar.objects.filter(kod=hkod).first()
            if (ka == "") or (si == "") or (csi == "") or (em == "") or (hkod == ""):
                messages.warning(request, "Lütfen tüm alanları doldurun")
                return render(request, "kayit.html", {"sayfa": kim})
            if ka_varmi:
                messages.warning(request,"Bu kullanıcı adı zaten mevcut")
                return render(request, "kayit.html", {"sayfa": kim})
            if (si and csi and si != csi):
                messages.warning(request, "Şifreleriniz eşleşmiyor")
                return render(request, "kayit.html", {"sayfa": kim})
            if em_varmi:
                messages.warning(request, "Bu email adresi zaten kullanılıyor.")
                return render(request, "kayit.html", {"sayfa": kim})
            if not kod_varmi:
                messages.warning(request, "Eğitmen kodunuz yanlış. Lütfen İlkay KURU ile iletişime geçiniz")
                return render(request, "kayit.html", {"sayfa": kim})
            k_ekle = kullanici(kullanici_adi=ka, sifre=si, email=em,hoca_mi="E")
            k_ekle.save()
            ayrinti_ekle = hocalar(id=k_ekle.id)
            ayrinti_ekle.save()
            kod_varmi.delete()
            request.session['member'] = ka
            request.session['id'] = k_ekle.id
            request.session['tip'] = "hoca"
            return render(request, "index.html")
    else:
        return render(request, "kayit.html",{"sayfa":request.POST.get("kim")})

    # ------------------------------------------KULLANICI LOGİN İŞLEMİ--------------------------------

def giris(request):
    if request.method == "POST":
        m = kullanici.objects.filter(kullanici_adi=request.POST['kullanici_adi']).first()
        if m:
            if m.sifre == request.POST['sifre']:
                request.session['member'] = m.kullanici_adi
                request.session['id'] = m.id
                if m.hoca_mi == "E":
                    request.session['tip'] = "hoca"
                else:
                    request.session['tip'] = "uye"


                return render(request, "index.html")
            else:
                messages.warning(request, "Şifeniz hatalı")
                return render(request, "giris.html")
        else:
            messages.warning(request, "Kullanıcı adınız hatalı")
            return render(request, "giris.html")


    return render(request, "giris.html")


# -------------------------------RASGELE KOD ÜRETİLİYOR-------------------------------------------
""" burası veritabanına hoca kaydı için benzersiz sayı üretimi
def uretim(request):

    for i in range(100):
        k = uretilen_kodlar(kod = random.randint(1000, 9000))
        k.save()
    return render(request,"index.html")
"""

# ------------------------------------------KULLANICI LOGOUT İŞLEMİ--------------------------------

def cikis(request):

    del request.session['member']
    del request.session['id']
    del request.session['tip']
    return render(request, "index.html")

# ------------------------------------------KULLANICI PROFİL GÖRÜNTÜLEME İŞLEMİ--------------------
def profil_goruntule(request):
    if request.method == "POST":
        #---------------------------------formdan veriler alınıyor---------------------------------
        isim = request.POST.get("isim")
        soyisim = request.POST.get("soyisim")
        dogum_tarihi = request.POST.get("dogum_tarihi")
        telefon = request.POST.get("telefon")
        email = request.POST.get("email")
        cinsiyet = request.POST.get("cinsiyet")
        kilo = request.POST.get("kilo")
        boy = request.POST.get("boy")
        problem = request.POST.get("problem")
        resim = request.FILES.get('resimDosya')
        if (resim):
            if os.path.exists(os.getcwd() + "/static/veriler"):
                yol = os.getcwd() + "/static/veriler/" + request.session['member'] + resim.name[-4:]
                with open(yol,"wb+") as dosya:
                    for i in resim:
                        dosya.write(i)
                yol = "/static/veriler/" + request.session['member'] + resim.name[-4:]
                dosya.close()
        else:
            r_kontrol = kullanici_ayrinti.objects.filter(id = request.session['id']).first()
            if r_kontrol:
                yol = r_kontrol.resim
            else:
                yol=os.getcwd() + "static/img/default.png"

        #-------------------------işlemler yapılıyor -------------------------------------------------

        ayrinti_tablosu = kullanici_ayrinti.objects.get(id = request.session['id'])

        ayrinti_tablosu.isim = isim
        #ayrinti_tablosu.soyisim = soyisim
        sonuc_tarih = parse_datetime(dogum_tarihi + " 00:00:00")
        ayrinti_tablosu.dogum_tarihi = sonuc_tarih
        ayrinti_tablosu.telefon = telefon
        ayrinti_tablosu.cinsiyet = cinsiyet
        ayrinti_tablosu.resim = yol

        if kilo == "":
            ayrinti_tablosu.kilo = 0
        else:
            ayrinti_tablosu.kilo = int(kilo)

        if boy == "":
            ayrinti_tablosu.boy = 0
        else:
            ayrinti_tablosu.boy = int(boy)


        ayrinti_tablosu.problem = problem
        kullanici_tablosu = kullanici.objects.get(id = request.session['id'])
        kullanici_tablosu.email = email
        ayrinti_tablosu.save()
        kullanici_tablosu.save()
    email = kullanici.objects.filter(id = request.session['id']).first()
    veri = kullanici_ayrinti.objects.filter(id = email.id).first()

    tarih_cevir = veri.dogum_tarihi
    if tarih_cevir != None:
        sonuc = tarih_cevir.strftime("%Y-%m-%d")
    else:
        sonuc = ""


    return render(request,"profil_goruntule.html",{"email":email.email,"isim":veri.isim,"resim":veri.resim,"dogum_tarihi":str(sonuc),"kilo":veri.kilo,"boy":veri.boy,"problem":veri.problem,"pt_kontrol":veri.pt_kontrol,"trainer":veri.trainer,"telefon":veri.telefon,"cinsiyet":veri.cinsiyet})


def profilegitmen(request):

    if request.method == "POST":
        #---------------------------------formdan veriler alınıyor---------------------------------
        isim = request.POST.get("isim")
        soyisim = request.POST.get("soyisim")
        dogum_tarihi = request.POST.get("dogum_tarihi")
        telefon = request.POST.get("telefon")
        email = request.POST.get("email")
        cinsiyet = request.POST.get("cinsiyet")
        universite = request.POST.get("uni")
        uni_bolum = request.POST.get("bolum")
        resim = request.FILES.get('resimDosya')
        if (resim):
            if os.path.exists(os.getcwd() + "/static/veriler"):
                yol = os.getcwd() + "/static/veriler/" + request.session['member'] + resim.name[-4:]
                with open(yol,"wb+") as dosya:
                    for i in resim:
                        dosya.write(i)
                yol = "/static/veriler/" + request.session['member'] + resim.name[-4:]
                dosya.close()
        else:
            r_kontrol = hocalar.objects.filter(id = request.session['id']).first()
            if r_kontrol:
                yol = r_kontrol.resim
            else:
                yol=os.getcwd() + "static/img/default.png"

        #-------------------------işlemler yapılıyor -------------------------------------------------

        ayrinti_tablosu = hocalar.objects.get(id = request.session['id'])
        ayrinti_tablosu.isim = isim
        #ayrinti_tablosu.soyisim = soyisim
        sonuc_tarih = parse_datetime(dogum_tarihi + " 00:00:00")
        ayrinti_tablosu.dogum_tarihi = sonuc_tarih
        ayrinti_tablosu.telefon = telefon
        ayrinti_tablosu.cinsiyet = cinsiyet
        ayrinti_tablosu.resim = yol
        ayrinti_tablosu.universite = universite
        ayrinti_tablosu.bolum = uni_bolum
        kullanici_tablosu = kullanici.objects.get(id = request.session['id'])
        kullanici_tablosu.email = email
        ayrinti_tablosu.save()
        kullanici_tablosu.save()
    email = kullanici.objects.filter(id = request.session['id']).first()
    veri = hocalar.objects.filter(id = email.id).first()
    tarih_cevir = veri.dogum_tarihi
    if tarih_cevir != None:
        sonuc = tarih_cevir.strftime("%Y-%m-%d")
    else:
        sonuc = ""

    uni = okul.objects.all()
    neresi = bolum.objects.all()
    uni_hangisi = hocalar.objects.get(id=request.session['id'])


    return render(request,"profil_goruntule_egitmen.html",{"uni_secilen":uni_hangisi.universite,"bolum_hangisi":uni_hangisi.bolum,"uni":uni,"bolum":neresi,"email":email.email,"isim":veri.isim,"resim":veri.resim,"dogum_tarihi":str(sonuc),"telefon":veri.telefon,"cinsiyet":veri.cinsiyet})


def pt_al(request):
    egitmen = hocalar.objects.all()

    return render(request,"pt_al.html",{"egitmen":egitmen})
