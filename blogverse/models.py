from django.db import models
from django.conf import settings  # Use settings.AUTH_USER_MODEL
from django.contrib.auth.models import AbstractUser, BaseUserManager

# Custom user manager
class AppUserManager(BaseUserManager):
    def create_user(self, email, name, phone, address, gender, password=None ,birthdate=None, **extra_fields):
        if not email:
            raise ValueError('The Email field is mandatory')

        email = self.normalize_email(email)
        user = self.model(
            email=email,
            name=name,
            phone=phone,
            address=address,
            gender=gender,
            birthdate = birthdate,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, phone, address, gender,password=None, birthdate=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if not password:
            raise ValueError("Superusers must have a password.")

        return self.create_user(email, name, phone, address, gender, password, birthdate, **extra_fields)


# Custom user model
class AppUser(AbstractUser):
    GENDER_CHOICES = (
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    )

    # Remove username field as we use email as the unique identifier
    username = None  
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    address = models.TextField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    birthdate = models.DateField(null=True, blank=True)
    objects = AppUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'phone', 'address', 'gender', 'birthdate' ]

    def __str__(self):
        return self.email


class Profile(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    gender = models.CharField(max_length=6)
    birthdate = models.DateField(null=True, blank=True)
    address = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=10)
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)


    def _str_(self):
        return self.name
class BlogPost(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='blog_images/', blank=True, null=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)

    def _str_(self):
        return self.title


    
class Like(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name="likes")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')

    def _str_(self):
        return self.title