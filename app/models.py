from datetime import datetime
from django.db import models

# TODO: Model genişletilecek.
# TODO: Viriyi kimin girdiği ve düzelttiği zaman bilgisi ile birlikte kaydedilecek.
# TODO: TextField veri girişlerinde markdown desteği eklenecek.

class Event(models.Model):
  """
  Olaylar için model. title, description, dateTime, solution_dateTime, detection_method, detection_by, level, type
  """  
  LEVEL = [
      (3, 'Seviye 3'),
    ]
  TYPE = [
      (1, 'Tür 1'),
      (2, 'Tür 2'),
      (3, 'Tür 3'),
      (4, 'Tür 4'),
      (5, 'Tür 5'),
      (6, 'Tür 6'),
    ]
  title = models.CharField('Olay', max_length=200)
  description = models.TextField('Ön İnceleme')
  dateTime = models.DateTimeField('Tespit Tarihi ve Saati', default=datetime.now)
  solution_dateTime = models.DateTimeField(
    'Çözüm Tarihi ve Saati',
    blank=True,
    null=True,
    default=None,
    help_text='Çözüm tarihi ve saati girilmediyse olay çözülmedi olarak kabul edilecektir.')
  detection_method = models.CharField('Tespit Yöntemi', max_length=200, help_text='Telefonla, SOME Ekranı, vb...')
  detection_by = models.CharField('Tespit Eden', max_length=200, help_text='SOME Nöbetçi Heyeti')
  level = models.IntegerField(choices=LEVEL, default=3)
  type = models.IntegerField(choices=TYPE, default=4)

  def __str__(self):
    return self.title

class Step(models.Model):
  """
  Olaylara ait adımlar için model. event, description, dateTime.
  """
  event = models.ForeignKey(Event, on_delete=models.CASCADE)
  description = models.TextField('Yapılan İşlemler')
  dateTime = models.DateTimeField('İşlem Tarihi ve Saati', default=datetime.now)

  def __str__(self):
    return self.dateTime.__str__()
