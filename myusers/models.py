from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.core.validators import RegexValidator
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
# Create your models here.


class HMUserManager(BaseUserManager):

    def create_user(self, email, first_name, last_name, password=None):
        if not email:
            raise ValueError('User needs a username')

        user = self.model(email=email, first_name=first_name,
                          last_name=last_name)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password, first_name, last_name):
        user = self.create_user(email, password=password,
                                first_name=first_name, last_name=last_name)
        user.is_admin = True
        user.save(using=self._db)
        return user


class Client(models.Model):
    name = models.CharField(
        verbose_name=_('Client Name'),
        max_length=355,
        unique=True,
    )
    email = models.EmailField(
        verbose_name=_('email address'),
        max_length=255,
        unique=True,
        blank=True,
        null=True,
    )
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+233200000000' or '0200000000'. Up to 15 digits allowed.")
    hospital_name = models.CharField(max_length=255, blank=True, null=True)
    hospital_branch = models.CharField(max_length=255, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_edit = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name


class HMUser(AbstractBaseUser):

    STATUS_TYPES = (
        ('0', 'Dev SuperUser'),
        ('1', 'HM Admin SuperUser'),
        ('2', 'HM Administrator'),
        ('3', 'HM Auditor'),
        ('4', 'Doctor'),
        ('5', 'Pharmacy'),
        ('6', 'Finance'),
        ('7', 'Residence'),
        ('8', 'Patient'),
    )

    email = models.EmailField(
        verbose_name=_('email address'),
        max_length=255,
        unique=True,
    )
    username = models.CharField(
        verbose_name=_('username'),
        max_length=100,
        default='User'
    )
    first_name = models.CharField(max_length=100)
    unique_code = models.CharField(max_length=200, blank=True, null=True)
    last_name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    first_passwd = models.BooleanField(default=True)
    is_returned = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_blocked = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    lastlogin = models.DateTimeField(blank=True, null=True)
    location = models.CharField(max_length=1000, blank=True, null=True)
    country = models.CharField(max_length=1000, default='Ghana')
    hospital = models.CharField(max_length=1000, blank=True, null=True)
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+233200000000' or '0200000000'. Up to 15 digits allowed.")
    phone_number = models.CharField(
        validators=[phone_regex], max_length=100, null=True, blank=True)
    permission = models.CharField(
        max_length=100, default='0', choices=STATUS_TYPES)
    lastupdatedtime = models.DateTimeField(blank=True, null=True)
    lastupdatedby_id = models.IntegerField(default=0)
    name_of_client = models.CharField(max_length=255, blank=True, null=True)
    client = models.ForeignKey(
        Client, blank=True, null=True, related_name='myusers')
    return_message = models.TextField(blank=True, null=True)
    temporal_login_fails = models.IntegerField(default=0)
    permanent_login_fails = models.IntegerField(default=0)

    objects = HMUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def get_full_name(self):
        return '''{} {}'''.format(self.first_name, self.last_name)

    def get_short_name(self):
        return self.first_name

    @property
    def is_staff(self):
        return self.is_admin

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    # On Python 3: def __str__(self):
    def __unicode__(self):
        return self.email.encode("utf8")

    class Meta:
        ordering = ('id', 'first_name',)
        verbose_name = _('HM users')
        verbose_name_plural = _('HM users')

    def update_last_login(self):
        self.lastlogin = timezone.now()
        self.save()


class EditClient(models.Model):
    name = models.CharField(max_length=500, blank=True, null=True)
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+233200000000' or '0200000000'. Up to 15 digits allowed.")
    created = models.DateTimeField(auto_now_add=True)
    hmuser = models.ForeignKey(
        HMUser, blank=True, null=True, related_name='myuluser')
    is_editing = models.BooleanField(default=False)
    is_edit = models.BooleanField(default=False)
    is_edited = models.BooleanField(default=False)
    hospital_name = models.CharField(max_length=255, blank=True, null=True)
    hospital_branch = models.CharField(max_length=255, blank=True, null=True)

    def __unicode__(self):
        return str(self.hmuser)


class UserActivity(models.Model):
    module = models.CharField(max_length=1000, blank=True, null=True)
    action = models.CharField(max_length=1000, blank=True, null=True)
    description = models.CharField(max_length=1000, blank=True, null=True)
    user = models.ForeignKey(HMUser, related_name='user_activities')
    client = models.ForeignKey(
        Client, related_name='user_activities', blank=True, null=True)
    device = models.CharField(max_length=1000, blank=True, null=True)
    ip_address = models.CharField(max_length=1000, blank=True, null=True)
    country = models.CharField(max_length=1000, blank=True, null=True)
    longitude = models.CharField(max_length=1000, blank=True, null=True)
    latitude = models.CharField(max_length=1000, blank=True, null=True)
    datecreated = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'User Activities'
        ordering = ('-id', )

    def __str__(self):
        return self.description
