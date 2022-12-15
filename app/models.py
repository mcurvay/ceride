from datetime import datetime, timedelta

import locale, pytz

from django.db import models
from django.contrib.auth.models import User

locale.setlocale(locale.LC_ALL, "tr_TR.utf8")

LEVEL = [
    (1, '1: Lorem ipsum'),
    (2, '2: Dolor sit amet'),
    (3, '3: Nöbetçi heyeti tarafından çözülemeyen ve geneli etkileyen, etkisi yüksek arıza')
    ]

TYPE = [
    (1, '1: Acilen müdahale edilmemesi durumunda donanımın kalıcı hasara uğraması'),
    (2, '2: Kurumsal verinin kaybedilme ihtimali'),
    (3, '3: Görevin yapılmasına, hizmetin vatandaşa sunulmasına mani bir durum oluşması'),
    (4, '4: Kritik uygulamaların tamamen devredışı kalması'),
    (5, '5: Kurumun imajını olumsuz etkileyecek hususlar'),
    (6, '6: Diğer'),
    ]

SOURCE = [
    ('Yazılım', 'Yazılım'),
    ('Donanım', 'Donanım'),
    ('Konfigürasyon', 'Konfigürasyon'),
    ]

SOLUTIONBY = [
    ('Nöbetçi heyeti', 'Nöbetçi heyeti'),
    ('İlgili personel', 'İlgili personel'),
    ('Firma Personeli', 'Firma Personeli')
    ]

class Event(models.Model): 
    title = models.CharField('Olay', max_length=200, help_text='Yeni olay oluşturmadan önce devam eden çözülmemiş olayları mutlaka kontrol ediniz. Olay başlığını belirlerken problemi doğru anlatan anahtar kelimeler kullanılmalıdır.')
    description = models.TextField('Ön İnceleme')
    dateTime = models.DateTimeField('Tespit Tarihi ve Saati', default=datetime.now)
    detection_method = models.CharField('Tespit Yöntemi', max_length=200, help_text='Telefonla, SOME Ekranı, vb...')
    detection_by = models.CharField('Tespit Eden', max_length=200, help_text='SOME Nöbetçi Heyeti')
    level = models.IntegerField("Seviye", choices=LEVEL, default=3)
    type = models.IntegerField("Tip", choices=TYPE, default=4)
    suggestions = models.TextField('Öneriler', help_text='Problemin yeniden gerçekleşmemesi için alınabilecek tedbirler.', null=True, blank=True)
    source = models.CharField("Arıza Kaynağı", choices=SOURCE, null=True, blank=True, max_length=15)
    solution_by = models.CharField("Çözüm Geliştiren", choices=SOLUTIONBY, null=True, blank=True, max_length=20)

    solved_at = models.DateTimeField(
        'Çözüm Tarihi ve Saati', blank=True, null=True, default=None,
        help_text='Çözüm tarihi ve saati girilmediyse olay çözülmedi olarak kabul edilecektir.'
        )

    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='%(class)s_created_by')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='%(class)s_updated_by', null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def formatted_date(self):
        dateTime = self.dateTime.astimezone(pytz.timezone('Europe/Istanbul'))
        if dateTime.date() == datetime.now().date():
            return 'Bugün ' + dateTime.strftime("%H:%M")
        elif dateTime.date() == datetime.now().date() - timedelta(days=1):
            return 'Dün ' + dateTime.strftime("%H:%M")
        elif dateTime.date() >= datetime.now().date() - timedelta(days=7):
            return dateTime.strftime("%A")
        elif dateTime.year == datetime.now().year:
            return dateTime.strftime("%d %B")
        else:
            return dateTime.strftime("%d %B %Y")

    def is_today(self):
        dateTime = self.dateTime.astimezone(pytz.timezone('Europe/Istanbul'))
        return dateTime.date() == datetime.now().date()

    class Meta:
        verbose_name = 'Olay'
        verbose_name_plural = 'Olaylar'
        ordering = ['-dateTime']


class Step(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    description = models.TextField('Yapılan İşlemler')
    dateTime = models.DateTimeField('İşlem Tarihi ve Saati', default=datetime.now)

    def __str__(self):
        dateTime = self.dateTime.astimezone(pytz.timezone('Europe/Istanbul'))
        return dateTime.strftime("%H:%M - %d %B %y %A")

    def formatted_date(self):
        dateTime = self.dateTime.astimezone(pytz.timezone('Europe/Istanbul'))
        if self.dateTime.date() == self.event.dateTime.date():
            return dateTime.strftime("%H:%M")
        else:
            return dateTime.strftime("%d %B %y - %H:%M")

    class Meta:
        verbose_name = 'Adım'
        verbose_name_plural = 'Adımlar'
        ordering = ['dateTime']
