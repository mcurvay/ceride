from datetime import datetime
from django.db import models
from django.contrib.auth.models import User

# TODO: TextField veri girişlerinde markdown desteği eklenecek.

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
  (1, 'Yazılım'),
  (2, 'Donanım'),
  (3, 'Altyapı'),
  ]

SOLUTION = [
  (1, 'Nöbetçi heyeti'),
  (2, 'İlgili personel'),
  (3, 'Firma Personeli')
  ]

class Event(models.Model): 
  title = models.CharField('Olay', max_length=200)
  description = models.TextField('Ön İnceleme')
  dateTime = models.DateTimeField('Tespit Tarihi ve Saati', default=datetime.now)
  detection_method = models.CharField('Tespit Yöntemi', max_length=200, help_text='Telefonla, SOME Ekranı, vb...')
  detection_by = models.CharField('Tespit Eden', max_length=200, help_text='SOME Nöbetçi Heyeti')
  level = models.IntegerField("Seviye", choices=LEVEL, default=3)
  type = models.IntegerField("Tip", choices=TYPE, default=4)
  source = models.IntegerField("Arıza Kaynağı", choices=SOURCE, null=True, blank=True)
  solution_method = models.IntegerField("Çözüm Yöntemi", choices=SOLUTION, null=True, blank=True )

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


class Step(models.Model):
  event = models.ForeignKey(Event, on_delete=models.CASCADE)
  description = models.TextField('Yapılan İşlemler')
  dateTime = models.DateTimeField('İşlem Tarihi ve Saati', default=datetime.now)

  def __str__(self):
    return self.dateTime.__str__()
