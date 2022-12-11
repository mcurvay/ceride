from datetime import datetime
from django.db import models
from django.contrib.auth.models import User

# TODO: Model genişletilecek.
# TODO: TextField veri girişlerinde markdown desteği eklenecek.

class Event(models.Model):
  """
  Olaylar için model. title, description, dateTime, solved_at, detection_method, detection_by, level, type, created_by, created_at, updated_by, updated_at.
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
  solved_at = models.DateTimeField(
    'Çözüm Tarihi ve Saati', blank=True, null=True, default=None,
    help_text='Çözüm tarihi ve saati girilmediyse olay çözülmedi olarak kabul edilecektir.'
    )
  detection_method = models.CharField('Tespit Yöntemi', max_length=200, help_text='Telefonla, SOME Ekranı, vb...')
  detection_by = models.CharField('Tespit Eden', max_length=200, help_text='SOME Nöbetçi Heyeti')
  level = models.IntegerField(choices=LEVEL, default=3)
  type = models.IntegerField(choices=TYPE, default=4)
  created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='%(class)s_created_by')
  created_at = models.DateTimeField(auto_now_add=True)
  updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='%(class)s_updated_by', null=True, blank=True)
  updated_at = models.DateTimeField(auto_now=True)

  def __str__(self):
    return self.title

class Step(models.Model):
  """
  Olaylara ait adımlar için model. event, description, dateTime, created_by, created_at, updated_by, updated_at.
  """
  event = models.ForeignKey(Event, on_delete=models.CASCADE)
  description = models.TextField('Yapılan İşlemler')
  dateTime = models.DateTimeField('İşlem Tarihi ve Saati', default=datetime.now)
  created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='%(class)s_created_by')
  created_at = models.DateTimeField(auto_now_add=True)
  updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='%(class)s_updated_by', null=True, blank=True)
  updated_at = models.DateTimeField(auto_now=True)

  def __str__(self):
    return self.dateTime.__str__()
