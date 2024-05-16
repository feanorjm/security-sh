from django.db import models
from datetime import datetime
from dpa_chile.models import Region, Provincia, Comuna


class Service(models.Model):
    name = models.CharField(max_length=100)
    sku = models.CharField(max_length=30)
    description = models.TextField(max_length=500)
    active = models.BooleanField(default=True)
    icon = models.CharField(max_length=200, null=True, blank=True)
    metadata = models.JSONField(null=True, default=dict)
    image = models.CharField(max_length=200, null=True, blank=True)
    requires_device = models.BooleanField(default=False)

    STATUS = (
        ('ninguno', 'ninguno'),
        ('indoorCamera', 'indoorCamera'),
        ('motionSensor', 'motionSensor'),
        ('multipurposeSensor', 'multipurposeSensor'),
        ('remoteControl', 'remoteControl'),
        ('siren', 'siren'),
        ('smartAlarmClock', 'smartAlarmClock'),
        ('smartLightBulb', 'smartLightBulb'),
        ('wallOutlet', 'wallOutlet')
    )
    device_category = models.CharField(max_length=50, choices=STATUS, default='indoorCamera')
    start_in = models.IntegerField(null=True, blank=True, default=0)

    def __str__(self):
        return self.name


class Plan(models.Model):
    PERIOD = (
        ('D', 'Diario'),
        ('M', 'Mensual'),
        ('A', 'Anual')
    )
    service = models.ForeignKey(Service, related_name='plans', on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=30)
    sku = models.CharField(max_length=30)
    description = models.CharField(max_length=100)
    price = models.IntegerField(default=0)
    iva = models.IntegerField(default=0)
    total_price = models.IntegerField(default=0)
    active = models.BooleanField(default=True)
    image = models.CharField(max_length=100, null=True, blank=True)
    periodicity = models.CharField(max_length=1, choices=PERIOD, default='M')
    metadata = models.JSONField(null=True, default=dict)

    def __str__(self):
        return str(self.name)


class Client(models.Model):
    uid = models.CharField(max_length=50)
    email = models.CharField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=30, null=True, blank=True)
    create_time = models.DateTimeField(null=True, blank=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    address = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    zip_code = models.IntegerField(null=True, blank=True)
    username = models.CharField(max_length=100, null=True, blank=True)
    password = models.CharField(max_length=50, null=True, blank=True)
    username_type = models.IntegerField(choices=((1, 'mobile phone number'), (2, 'email address')), null=True, blank=True)

    def __str__(self):
        return str(self.uid) + " - " + str(self.username)

    def save(self, *args, **kwargs):
        username = self.username
        email = self.email
        phone = self.phone
        if username is None or username == "":
            if email is not None and email != "":
                self.username = self.email
            elif phone is not None and phone != "":
                self.username = self.phone
            else:
                self.username = "--"

            print(self.username)

        super(Client, self).save(*args, **kwargs)


class Subscription(models.Model):
    STATUS = (
        ('active', 'active'),
        ('inactive', 'inactive'),
        ('cancel', 'cancel'),
        ('updated', 'updated'),
        ('failed', 'failed'),
        ('tester', 'tester')
    )

    client = models.ForeignKey(Client, related_name='subscriptions', on_delete=models.CASCADE)
    token_payment = models.CharField(max_length=100)
    subscription_id_gateway = models.CharField(max_length=50)
    plan_id = models.ForeignKey(Plan, on_delete=models.CASCADE)
    subtotal_iva = models.IntegerField(default=0)
    subtotal_iva0 = models.IntegerField(default=0)
    ice = models.IntegerField(default=0)
    iva = models.IntegerField(default=0)
    currency = models.CharField(max_length=10)
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS)
    devices = models.JSONField(null=True, default=list)
    cancellation_date = models.DateTimeField(null=True, blank=True)
    assigned_sim = models.BooleanField(default=False, null=True, blank=True)
    home = models.CharField(max_length=15, null=True)
    tester = models.BooleanField(default=False, null=True, blank=True)

    def __str__(self):
        return str(self.id)


class Payment(models.Model):
    id_subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE)
    uid = models.CharField(max_length=50, null=True, blank=True)
    plan_id = models.ForeignKey(Plan, on_delete=models.CASCADE)
    amount = models.CharField(max_length=10, null=True, blank=True)
    payment_date = models.DateTimeField(default=datetime.now)
    payment_gateway = models.CharField(max_length=30, null=True, blank=True)
    payment_method = models.CharField(max_length=30, null=True, blank=True)
    document_type = models.CharField(max_length=10, null=True, blank=True)
    document_number = models.CharField(max_length=30, null=True, blank=True)
    phone = models.CharField(max_length=30, null=True, blank=True)

    def __str__(self):
        return str(self.pk)


class KushkiToken(models.Model):
    AMBIENT_CHOICES = (
        ('PRD', 'Production'),
        ('TEST', 'Testing')
    )
    public_key = models.CharField(max_length=40)
    private_key = models.CharField(max_length=40)
    active = models.BooleanField(default=True)
    ambient = models.CharField(max_length=10, choices=AMBIENT_CHOICES, default='TEST')

    def __str__(self):
        return str(self.public_key)

    def clean(self):
        tokens = KushkiToken.objects.all()
        for token in tokens:
            token.active = False
            token.save()


class Commission(models.Model):
    COMM_TYPE = (
        ('percent', 'Porcentaje'),
        ('amount', 'Monto fijo'),
    )
    name = models.CharField(max_length=100)
    comm_subs_type = models.CharField(max_length=12, choices=COMM_TYPE, verbose_name='tipo comisión suscripción')
    subscription_comm = models.IntegerField(verbose_name='Comisión x susc mensual')
    subscription_comm_yearly = models.IntegerField(default=0, verbose_name='Comisión x susc Anual')
    comm_additional_type = models.CharField(max_length=12, choices=COMM_TYPE, verbose_name='tipo comisión adicionales')
    additional_comm = models.IntegerField()
    active = models.BooleanField(default=True, null=True)
    create_date = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        sub_type = ''
        add_type = ''
        if self.comm_subs_type == 'percent':
            sub_type = '%'
        if self.comm_additional_type == 'percent':
            add_type = '%'

        return self.name + ' [subs: ' + str(self.subscription_comm) + '/' + str(self.subscription_comm_yearly) + sub_type + \
               ' - adicional: ' + str(self.additional_comm) + add_type + ']'


class Partner(models.Model):
    PARTNER_TYPE = (
        ('seller', 'Vendedor'),
        ('client', 'Cliente'),
        ('installer', 'Instalador'),
        ('alliance', 'Alianza')

    )
    name = models.CharField(max_length=50)
    partner_type = models.CharField(max_length=12, choices=PARTNER_TYPE)
    rut = models.CharField(max_length=20)
    email = models.EmailField(null=True, blank=True)
    address = models.CharField(max_length=100, null=True, blank=True)
    region = models.ForeignKey(Region, to_field='codigo', on_delete=models.CASCADE, null=True, blank=True)
    provincia = models.ForeignKey(Provincia, to_field='codigo', on_delete=models.CASCADE, null=True, blank=True)
    comuna = models.ForeignKey(Comuna, to_field='codigo', on_delete=models.CASCADE, null=True, blank=True)
    active = models.BooleanField(default=True, null=True, blank=True)
    create_date = models.DateTimeField(auto_now_add=True, null=True)
    commission = models.ForeignKey(Commission, on_delete=models.DO_NOTHING, null=True, default=None, blank=True)

    def __str__(self, type=PARTNER_TYPE):
        d = dict(type)
        return self.name + " - " + d[self.partner_type]


class DiscountCode(models.Model):
    TYPE = (
        ('seller', 'Vendedor'),
        ('client', 'Cliente'),
        ('installer', 'Instalador'),
        ('alliance', 'Alianza')
    )

    DISCOUNT_TYPE = (
        ('percent', 'Porcentaje'),
        ('amount', 'Monto fijo'),
    )

    code = models.CharField(max_length=50)
    code_type = models.CharField(max_length=12, choices=TYPE)
    subscription_discount = models.BooleanField(default=False, verbose_name='Aplica en sub?')
    subscription_discount_type = models.CharField(max_length=12, choices=DISCOUNT_TYPE, null=True, blank=True, verbose_name='tipo_desc_sub')
    subscription_discount_amount = models.CharField(max_length=10, null=True, blank=True, verbose_name='monto_desc_sub')
    additional_discount = models.BooleanField(default=False, verbose_name='Aplica en adicionales?')
    additional_discount_type = models.CharField(max_length=12, choices=DISCOUNT_TYPE, null=True, blank=True, verbose_name='tipo_desc_adicional')
    additional_discount_amount = models.CharField(max_length=10, null=True, blank=True, verbose_name='monto_desc_adicional')
    assigned_to = models.ForeignKey(Partner, on_delete=models.CASCADE, null=True)
    create_date = models.DateTimeField(auto_now_add=True, null=True)
    active = models.BooleanField(default=True, null=True)
    unlimited = models.BooleanField(default=True, null=True)
    only_ondemand = models.BooleanField(default=False, null=True)

    def __str__(self):
        return self.code


class Coupon(models.Model):
    COUPON_TYPE = (
        ('seller', 'Vendedor'),
        ('client', 'Cliente'),
        ('installer', 'Instalador')

    )
    DISCOUNT_TYPE = (
        ('percent', 'Porcentaje'),
        ('amount', 'Monto fijo'),

    )

    code = models.CharField(max_length=20, null=True)
    coupon_type = models.CharField(max_length=12, choices=COUPON_TYPE)
    discount_type = models.CharField(max_length=12, choices=DISCOUNT_TYPE)
    discount_amount = models.CharField(max_length=10, null=True, blank=True)
    assigned_to = models.ForeignKey(Partner, on_delete=models.CASCADE, null=True)
    create_date = models.DateTimeField(auto_now_add=True, null=True)
    active = models.BooleanField(default=True, null=True)
    unlimited = models.BooleanField(default=True, null=True)

    def __str__(self):
        return self.code


class Discount(models.Model):
    discount_code = models.ForeignKey(DiscountCode, on_delete=models.CASCADE, default=None)
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE)
    create_date = models.DateTimeField(auto_now_add=True)
    subs_initial_amount = models.IntegerField(null=True, blank=True)
    subs_discount_amount = models.IntegerField(null=True, blank=True)
    subs_final_amount = models.IntegerField(null=True, blank=True)
    add_initial_amount = models.IntegerField(null=True, blank=True)
    add_discount_amount = models.IntegerField(null=True, blank=True)
    add_final_amount = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return str(self.id)


class CommissionPartner(models.Model):
    discount = models.ForeignKey(Discount, on_delete=models.CASCADE)
    partner = models.ForeignKey(Partner, on_delete=models.CASCADE)
    subs_commission = models.IntegerField()
    add_commission = models.IntegerField()
    total_commission = models.IntegerField()

    def __str__(self):
        return str(self.id)


class WebhookEvent(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True, default=None, )
    subscriptionId = models.CharField(max_length=50, default=None, null=True, blank=True)
    created = models.CharField(max_length=50, null=True, blank=True, default=None)
    periodicity = models.CharField(max_length=50, null=True, blank=True, default=None)
    lastFourDigits = models.CharField(max_length=50, null=True, blank=True, default=None)
    active = models.BooleanField(null=True, blank=True, default=None)
    ip = models.CharField(max_length=50, null=True, blank=True, default=None)
    token = models.CharField(max_length=100, null=True, blank=True, default=None)
    cardHolderName = models.CharField(max_length=50, null=True, blank=True, default=None)
    maskedCardNumber = models.CharField(max_length=50, null=True, blank=True, default=None)
    planName = models.CharField(max_length=50, null=True, blank=True, default=None)
    month = models.CharField(max_length=50, null=True, blank=True, default=None)
    dayOfWeek = models.CharField(max_length=50, null=True, blank=True, default=None)
    dayOfMonth = models.CharField(max_length=50, null=True, blank=True, default=None)
    startDate = models.CharField(max_length=50, null=True, blank=True, default=None)
    plccMetadataId = models.CharField(max_length=50, null=True, blank=True, default=None)
    event_id = models.CharField(max_length=50, null=True, blank=True, default=None)
    merchantId = models.CharField(max_length=50, null=True, blank=True, default=None)
    transactionReference = models.CharField(max_length=50, null=True, blank=True, default=None)
    deleteAt = models.CharField(max_length=50, null=True, blank=True, default=None)
    lastChargeDate = models.CharField(max_length=50, null=True, blank=True, default=None)
    metadata = models.JSONField(null=True, default=dict, blank=True)
    contactDetails = models.JSONField(null=True, default=dict, blank=True)
    amount = models.JSONField(null=True, default=dict, blank=True)
    binInfo = models.JSONField(null=True, default=dict, blank=True)
    created_hook = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return str(self.id)
