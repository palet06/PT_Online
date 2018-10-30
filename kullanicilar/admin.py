from django.contrib import admin
from .models import kullanici_ayrinti,kullanici,uretilen_kodlar,hocalar

# Register your models here.
@admin.register(kullanici_ayrinti)
class KullaniciAyrintiTablosuAdmin(admin.ModelAdmin):
    list_display = ["id","isim","kayit_tarihi","pt_kontrol","trainer"]
    list_display_links = ["isim","kayit_tarihi","pt_kontrol","trainer"]
    search_fields = ["isim"]
    list_filter = ["kayit_tarihi","trainer"]
    class Meta:
        model = kullanici_ayrinti



@admin.register(kullanici)
class KullaniciTablosuAdmin(admin.ModelAdmin):
    list_display = ["id","kullanici_adi","sifre","email",]
    list_display_links = ["id","kullanici_adi","sifre","email",]
    search_fields = ["kullanici_adi"]
    list_filter = ["kullanici_adi","email"]
    class Meta:
        model = kullanici

@admin.register(uretilen_kodlar)
class UretilenKodlarAdmin(admin.ModelAdmin):
    list_display = ["id","kod"]
    list_display_links = ["id","kod"]
    class Meta:
        model = uretilen_kodlar

@admin.register(hocalar)
class HocalarAdmin(admin.ModelAdmin):
    list_display = ["id","isim"]
    list_display_links = ["id","isim"]
    search_fields = ["isim"]
    list_filter = ["isim"]
    class Meta:
        model = hocalar

