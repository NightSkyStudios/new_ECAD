from django.db import models
from datetime import datetime
from django.utils.safestring import mark_safe
from PIL import Image
from io import BytesIO
from django.core.files import File
from django.db.models.signals import post_delete, pre_delete
from django.dispatch import receiver
from datetime import date
from tinymce import models as tinymce_models


# Create your models here.

def compress(image):
    im = Image.open(image)
    im_io = BytesIO()
    im.save(im_io, 'JPEG', quality=50)
    new_image = File(im_io, name=image.name)
    return new_image


class Post(models.Model):
    title = models.CharField('Назва',
                             max_length=225,
                             help_text='Назва публікації')
    image = models.ImageField('Зображення',
                              upload_to='img',
                              null=True,
                              blank=True,
                              default='default.jpg',
                              help_text="Основне зображення публікації")
    preview_text = models.TextField('Опис',
                                    max_length=300,
                                    help_text='Невеликий опис для попереднього перегляду, який відображається на '
                                              'сторінці з усіма публікаціями (максимально 300 символів)')

    text = tinymce_models.HTMLField('Текст',
                                    help_text='Цей текст буде з форматуванням відображатись на океремій сторінці '
                                              'відведеній для цієї публікації')
    date = models.DateTimeField('Дата публікації проекту',
                                default=datetime.now,
                                blank=True,
                                help_text='Ця дата використовується виключно для сортування і не показується на '
                                          'сторінках сайту')
    isHidden = models.BooleanField('Приховати публікацію',
                                   default=False,
                                   help_text="Поставте галочку для того что <b>приховати</b> цей пост у блозі")

    def save(self, *args, **kwargs):
        if bool(self.image):
            new_image = compress(self.image)
            self.image = new_image
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Пост Блогу'
        verbose_name_plural = 'Пости Блогу'


class Event(models.Model):
    title = models.CharField('Назва',
                             max_length=225,
                             help_text='Назва події')
    event_date = models.DateTimeField('Дата проведення події',
                                      default=datetime.now,
                                      blank=True,
                                      help_text='Дата проведення події, яка відображається на сторінці')
    image = models.ImageField('Зображення',
                              upload_to='img',
                              null=True,
                              blank=True,
                              default='default.jpg',
                              help_text="Основне зображення публікації")
    video = models.FileField(upload_to='videos',
                             null=True,
                             blank=True,
                             help_text=mark_safe("Якщо для публікації потрібне відео"))
    preview_text = models.TextField('Опис',
                                    max_length=300,
                                    help_text='Невеликий опис для попереднього перегляду, який відображається на '
                                              'сторінці з усіма подіями (максимально 300 символів)')
    text = tinymce_models.HTMLField('Текст',
                                    help_text='Цей текст буде з форматуванням відображатись на океремій сторінці '
                                              'відведеній для цієї події')
    date = models.DateTimeField('Дата публікації проекту',
                                default=datetime.now,
                                blank=True,
                                help_text='Ця дата використовується виключно для сортування і не показується на '
                                          'сторінках сайту')
    isHidden = models.BooleanField('Приховати публікацію',
                                   default=False,
                                   help_text="Поставте галочку для того что <b>приховати</b> цю подію у списку подій")

    def save(self, *args, **kwargs):
        if bool(self.image):
            new_image = compress(self.image)
            self.image = new_image
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    @property
    def is_past(self):
        return date.today() > self.event_date.date()

    class Meta:
        verbose_name = 'Подія'
        verbose_name_plural = 'Події'


class Project(models.Model):

    CHERKASY = 'CK'
    CHERNIHIV = 'CH'
    CHERNITVTSI = 'CV'
    DNIPRO = 'DP'
    DONETSK = 'DT'
    IVANO_FRANKIVSK = 'IF'
    KHARKIV = 'KK'
    KHERSON = 'KS'
    KHMELNYTSKYI = 'KM'
    KIEV = 'KV'
    KIEV_CITY = 'KC'
    KIROVOHRAD = 'KH'
    LUHANSK = 'LH'
    LVIV = 'LV'
    MYKOLAIV = 'MY'
    ODESSA = 'OD'
    POLTAVA = 'PL'
    RIVNE = 'RV'
    SUMY = 'SM'
    TERNOPIL = 'TP'
    VINNYTSIA = 'VI'
    VOLYN = 'VO'
    ZAKARPATTIA = 'ZK'
    ZAPORIZHIA = 'ZP'
    ZHYTOMYR = 'ZT'
    CRIMEA = 'CR'
    SEVASTOPOL = 'SV'

    AREA_CHOICES = (
        (VINNYTSIA, 'Вінницька'),
        (VOLYN, 'Волинська'),
        (DNIPRO, 'Дніпропетровська'),
        (DONETSK, 'Донецька'),
        (ZHYTOMYR, 'Житомирська'),
        (ZAKARPATTIA, 'Закарпатська'),
        (ZAPORIZHIA, 'Запорізька'),
        (IVANO_FRANKIVSK, 'Івано-Франківська'),
        (KIEV, 'Київська'),
        (KIEV_CITY, 'Київ'),
        (KIROVOHRAD, 'Кіровоградська'),
        (LUHANSK, 'Луганська'),
        (LVIV, 'Львівська'),
        (MYKOLAIV, 'Миколаївська'),
        (ODESSA, 'Одеська'),
        (POLTAVA, 'Полтавська'),
        (RIVNE, 'Рівнинська'),
        (SUMY, 'Сумська'),
        (TERNOPIL, 'Тернопільська'),
        (KHARKIV, 'Харківська'),
        (KHERSON, 'Херсонська'),
        (KHMELNYTSKYI, 'Хмельницька'),
        (CHERKASY, 'Черкаська'),
        (CHERNIHIV, 'Чернігівська'),
        (CHERNITVTSI, 'Черівецька'),
        (CRIMEA, 'АР Крим'),
        (SEVASTOPOL, 'Севастополь'),
    )

    title = models.CharField('Назва',
                             max_length=225,
                             help_text='Назва проекту')
    image = models.ImageField('Зображення',
                              upload_to='img',
                              null=True,
                              blank=True,
                              default='default.jpg',
                              help_text='Зображення для цього проекту')
    area = models.CharField('Область',
                            max_length=2,
                            choices=AREA_CHOICES,
                            default=VINNYTSIA,
                            help_text='Виберіть область у якій знаходиться цей проект',)
    text = tinymce_models.HTMLField('Текст',
                                    help_text='Цей текст буде з форматуванням відображатись на океремій сторінці '
                                              'відведеній для цього проекту')
    power = models.IntegerField('Потужність',
                                help_text="Потужність у ватах даного проекту")
    date = models.DateTimeField('Дата публікації проекту',
                                default=datetime.now,
                                blank=True,
                                help_text='Ця дата використовується виключно для сортування і не показується на '
                                          'сторінках сайту')
    isHidden = models.BooleanField('Приховати публікацію',
                                   default=False,
                                   help_text="Поставте галочку для того что <b>приховати</b> цей проект у списку "
                                             "проектів")

    def save(self, *args, **kwargs):
        if bool(self.image):
            new_image = compress(self.image)
            self.image = new_image
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Проект'
        verbose_name_plural = 'Проекти'


class Slider(models.Model):
    image = models.ImageField('Зображення',
                              upload_to='img',
                              null=True,
                              blank=True,
                              default='default.jpg',
                              help_text='Зображення буде відображатись на слайдері головної сторінки')

    def save(self, *args, **kwargs):
        new_image = compress(self.image)
        self.image = new_image
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Фотографія Слайдеру'
        verbose_name_plural = 'Фотографії Сладеру'


class Partner(models.Model):
    name = models.CharField('Назва компанії-партнера',
                            max_length=64,
                            help_text='Допомагає для SEO')
    image = models.ImageField('Зображення',
                              upload_to='img',
                              null=False,
                              blank=False,
                              help_text='Логотип для відображення на головній сторінці у блоці партнерів')

    class Meta:
        verbose_name = 'Партнер'
        verbose_name_plural = 'Партнери'


@receiver(post_delete)
def submission_delete(sender, instance, **kwargs):
    try:
        instance.image.delete(False)
    except AttributeError:
        pass
    try:
        instance.video.delete(False)
    except AttributeError:
        pass



