from django.db import models

# TODO: Model genişletilecek.
# TODO: Model içerisindeki gerekli alanlar için default değerler ve help_text değerleri verilecek.
# TODO: Model isilendirmeleri için daha anlamlı isimler verilecek.
# TODO: Sınıflar için docstringler eklenecek.
# TODO: TextField veri girişlerinde markdown desteği eklenecek.

class Event(models.Model):
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
  event_name = models.CharField('Olay', max_length=200)
  examination = models.TextField('Ön İnceleme')
  detection_date = models.DateTimeField('Tespit Tarihi ve Saati')
  solution_date = models.DateTimeField('Çözüm Tarihi ve Saati', blank=True, null=True, default=None, help_text='Çözüm tarihi ve saati girilmediyse olay çözülmedi olarak kabul edilecektir.')
  detection_method = models.CharField('Tespit Yöntemi', max_length=200, help_text='Telefonla, SOME Ekranı, vb...')
  first_detecter = models.CharField('İlk Tespit Eden', max_length=200, help_text='SOME Nöbetçi Heyeti')
  level = models.IntegerField(choices=LEVEL, default=3)
  theType = models.IntegerField(choices=TYPE, default=4)

  def __str__(self):
    return self.event_name

class EventStep(models.Model):
  event = models.ForeignKey(Event, on_delete=models.CASCADE)
  step = models.TextField('Yapılan İşlemler')
  step_date = models.DateTimeField('İşlem Tarihi ve Saati')

  def __str__(self):
    return self.step_date
