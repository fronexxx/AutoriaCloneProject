from django.db import models


class CurrencyChoices(models.TextChoices):
    UAH = 'UAH', 'UAH'
    USD = 'USD', 'USD'
    EUR = 'EUR', 'EUR'

class StatusChoices(models.TextChoices):
    PENDING = 'pending', 'pending'
    ACTIVE = 'active', 'active'
    INACTIVE = 'inactive', 'inactive'

class RegionChoices(models.TextChoices):
    VINNYTSIA = 'Vinnytsia', 'Vinnytsia'
    VOLYN = 'Volyn', 'Volyn'
    DNIPROPETROVSK = 'Dnipropetrovsk', 'Dnipropetrovsk'
    DONETSK = 'Donetsk', 'Donetsk'
    ZHYTOMYR = 'Zhytomyr', 'Zhytomyr'
    ZAKARPATTIA = 'Zakarpattia', 'Zakarpattia'
    ZAPORIZHZHIA = 'Zaporizhzhia', 'Zaporizhzhia'
    IVANO_FRANKIVSK = 'Ivano-Frankivsk', 'Ivano-Frankivsk'
    KYIV = 'Kyiv', 'Kyiv'
    KYIV_REGION = 'Kyiv region', 'Kyiv region'
    KIROVOHRAD = 'Kirovohrad', 'Kirovohrad'
    LUHANSK = 'Luhansk', 'Luhansk'
    LVIV = 'Lviv', 'Lviv'
    MYKOLAIV = 'Mykolaiv', 'Mykolaiv'
    ODESA = 'Odesa', 'Odesa'
    POLTAVA = 'Poltava', 'Poltava'
    RIVNE = 'Rivne', 'Rivne'
    SUMY = 'Sumy', 'Sumy'
    TERNOPIL = 'Ternopil', 'Ternopil'
    KHARKIV = 'Kharkiv', 'Kharkiv'
    KHERSON = 'Kherson', 'Kherson'
    KHMELNYTSKYI = 'Khmelnytskyi', 'Khmelnytskyi'
    CHERKASY = 'Cherkasy', 'Cherkasy'
    CHERNIVTSI = 'Chernivtsi', 'Chernivtsi'
    CHERNIHIV = 'Chernihiv', 'Chernihiv'
    CRIMEA = 'Crimea', 'Crimea'