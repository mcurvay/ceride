import locale
import pytz
from datetime import datetime, timedelta

from django.contrib.auth.models import User
from django.db import models

try:
    locale.setlocale(locale.LC_ALL, "tr_TR.utf8")
except locale.Error:
    locale.setlocale(locale.LC_ALL, "tr_TR")

LEVEL = [
    (1, '1: Sınırlı etkili - Nöbet heyeti çözebilir'),
    (2, '2: Sınırlı etkili - Nöbet heyeti çözemez'),
    (3, '3: Geneli etkileyen etkisi yüksek arıza')]

TYPE = [
    (1, '1: Donanımın kalıcı hasara uğrama riski'),
    (2, '2: Kurumsal verinin kaybedilme riski'),
    (3, '3: Görevin yapılamama/vatandaşa sunulamama riski'),
    (4, '4: Kritik uygulamaların devredışı kalma riski'),
    (5, '5: Kurumun imajını olumsuz etkileme riski'),
    (6, '6: Diğer')]

DETECTION_METHOD = [
    ('SOME İzleme Ekranları', 'SOME İzleme Ekranları'),
    ('GÜVERCİNLİK İzleme Ekranları', 'GÜVERCİNLİK İzleme Ekranları'),
    ('KASTAMONU İzleme Ekranı', 'KASTAMONU İzleme Ekranı'),
    ('Kurum İçi', 'Kurum İçi (Diğer Birlikler, İç Hatlar, E-Posta, Telefon, vb.)'),
    ('Kurum Dışı', 'Kurum Dışı')]

FAILURE_SOURCE = [
    ('Yazılım', 'Yazılım'),
    ('Donanım', 'Donanım'),
    ('Konfigürasyon', 'Konfigürasyon'),
    ('Alt Yapı', 'Alt Yapı'),
    ('Kurum Dışı', 'Kurum Dışı')]

SOLUTION_BY = [
    ('Nöbetçi heyeti', 'Nöbetçi heyeti'),
    ('İlgili personel', 'İlgili personel'),
    ('Firma Personeli', 'Firma Personeli')]


class Event(models.Model):
    # İlk Bilgiler
    title = models.CharField(
        'Olay *',
        max_length=200,
        help_text='''Yeni olay oluşturmadan önce devam eden çözülmemiş olayları mutlaka kontrol ediniz.
        Olay başlığını belirlerken problemi doğru anlatan anahtar kelimeler kullanılmalıdır.''')
    description = models.TextField('Ön İnceleme *')
    dateTime = models.DateTimeField(
        'Tespit Tarihi ve Saati *',
        default=datetime.now)

    # Tespit Bilgileri
    detection_method = models.CharField(
        'Tespit Yöntemi *',
        choices=DETECTION_METHOD,
        max_length=30)
    detection_method_text = models.TextField(
        'Tespit Yöntemi Açıklama',
        null=True,
        blank=True,
        help_text='Tespit yönteminde ek açıklama alanı olarak kullanabilirsiniz.')
    detection_by = models.CharField(
        'Tespit Eden *',
        max_length=200,
        help_text='İlgili Birim, İsim Soyisim, Telefon, E-Posta, vb.')

    # Etki Bilgileri
    level = models.IntegerField(
        'Seviye *',
        choices=LEVEL,
        default=3)
    type = models.IntegerField(
        'Tip *',
        choices=TYPE,
        default=4)
    type_text = models.CharField(
        'Tip Açıklama',
        max_length=200,
        null=True,
        blank=True,
        help_text='Tip 6 seçildiğinde ek açıklama alanı olarak kullanabilirsiniz.')

    # Çözüm Bilgileri
    solved_at = models.DateTimeField(
        'Çözüm Tarihi ve Saati',
        blank=True,
        null=True,
        default=None,
        help_text='Çözüm tarihi ve saati girilmediyse olay çözülmedi olarak kabul edilecektir.')
    failure_source = models.CharField(
        'Arıza Kaynağı',
        choices=FAILURE_SOURCE,
        null=True,
        blank=True,
        max_length=15)
    solution_by = models.CharField(
        'Çözüm Geliştiren',
        choices=SOLUTION_BY,
        null=True,
        blank=True,
        max_length=20)
    notes = models.TextField(
        'Ek Açıklama',
        null=True,
        blank=True,
        help_text='Komutan emri, bilir kişi raporu, öneriler vb. ek açıklamaları buraya yazabilirsiniz.')

    # Otomatik Bilgiler
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='%(class)s_created_by')
    updated_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='%(class)s_updated_by', null=True,
        blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def formatted_date(self):
        date_time = self.dateTime.astimezone(pytz.timezone('Europe/Istanbul'))
        if date_time.date() == datetime.now().date():
            return 'Bugün ' + date_time.strftime("%H:%M")
        elif date_time.date() == datetime.now().date() - timedelta(days=1):
            return 'Dün ' + date_time.strftime("%H:%M")
        elif date_time.date() >= datetime.now().date() - timedelta(days=7):
            return date_time.strftime("%A")
        elif date_time.year == datetime.now().year:
            return date_time.strftime("%d %B")
        else:
            return date_time.strftime("%d %B %Y")

    def is_today(self):
        date_time = self.dateTime.astimezone(pytz.timezone('Europe/Istanbul'))
        return date_time.date() == datetime.now().date()

    class Meta:
        verbose_name = 'Olay'
        verbose_name_plural = 'Olaylar'
        ordering = ['-dateTime']


class Step(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    description = models.TextField('Yapılan İşlemler')
    dateTime = models.DateTimeField('İşlem Tarihi ve Saati', default=datetime.now)

    def __str__(self):
        date_time = self.dateTime.astimezone(pytz.timezone('Europe/Istanbul'))
        return date_time.strftime("%H:%M - %d %B %y %A")

    def formatted_date(self):
        date_time = self.dateTime.astimezone(pytz.timezone('Europe/Istanbul'))
        if self.dateTime.date() == self.event.dateTime.date():
            return date_time.strftime("%H:%M")
        else:
            return date_time.strftime("%d %B %y - %H:%M")

    class Meta:
        verbose_name = 'Adım'
        verbose_name_plural = 'Adımlar'
        ordering = ['dateTime']
