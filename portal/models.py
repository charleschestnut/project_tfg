import os

from django.db import models
from django.db.models import Avg
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator


# Create your models here.

class Profession(models.Model):
    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.name


class Administrator(models.Model):
    id_worker = models.PositiveIntegerField(unique=True)

    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE)


class BadWord(models.Model):
    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.name


class Banning(models.Model):
    start_datetime = models.DateField(auto_now_add=True)
    description = models.TextField(max_length=1000)
    finish_datetime = models.DateField()

    def __str__(self):
        return self.description + str(self.start_datetime) + "-->" + str(self.finish_datetime)


class Profile(models.Model):
    birthdate = models.DateField(null=True)
    dni = models.CharField(max_length=9, unique=True)
    city = models.TextField(max_length=30)
    description = models.TextField(default="Default description", null=True, blank=True, max_length=1000)

    banning = models.OneToOneField(Banning, null=True, blank=True, on_delete=True)

    professions = models.ManyToManyField(Profession)
    picture = models.ImageField(null=True, blank=True, upload_to=os.path.join(settings.MEDIA_ROOT, 'static/profile'))
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE)

    client_rating_avg = models.DecimalField(max_digits=4, decimal_places=2, default=0.0, null=True, blank=True)
    worker_rating_avg = models.DecimalField(max_digits=4, decimal_places=2, default=0.0, null=True, blank=True)

    def __str__(self):
        return self.user.first_name + " -- " + self.city

    def get_client_rating_avg(self):
        avg = ClientRating.objects.filter(rated_person__user_id=self.user_id).aggregate(Avg('punctuation')).get(
            'punctuation__avg')
        if avg:
            return avg
        else:
            return 0.0

    def get_worker_rating_avg(self):
        avg = WorkerRating.objects.filter(rated_person__user_id=self.user_id).aggregate(Avg('punctuation')).get(
            'punctuation__avg')
        if avg:
            return avg
        else:
            return 0.0


LABOUR_STATE_CHOICES = [
    'PENDING',
    'IN_PROCESS',
    'END_WORKER',
    'END_CLIENT',
    'FINISHED',
    'REJECTED',
    'CANCELLED',
    'PAID_OUT',
    'OFFER_WORKER',
    'OFFER_CLIENT',
]


class LabourOffer(models.Model):
    price = models.PositiveIntegerField(default=0, null=True, blank=True)


class LabourRequest(models.Model):
    title = models.TextField(max_length=100, null=False, blank=False)
    description = models.TextField(max_length=1000, null=True, blank=True)
    state = models.CharField(max_length=20)
    start_datetime = models.DateTimeField(null=True, blank=True)
    finish_datetime = models.DateTimeField(null=True, blank=True)
    price = models.PositiveIntegerField(default=0, null=True, blank=True)

    offer = models.OneToOneField(LabourOffer, null=True, blank=True, on_delete=True)
    creator = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='creator')
    worker = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='worker')


    def __str__(self):
        return "Labour request created by " + self.creator.user.first_name + "->" + self.worker.user.first_name


class LabourImage(models.Model):
    image = models.ImageField(null=False, blank=False, upload_to=os.path.join(settings.MEDIA_ROOT, 'static/labour_images'))
    labour = models.ForeignKey(LabourRequest, on_delete=models.CASCADE, related_name='labour')


class LabourChat(models.Model):
    creation_datetime = models.DateTimeField(null=False, blank=False)
    last_message_datetime = models.DateTimeField(null=False, blank=False)

    labour = models.OneToOneField(LabourRequest, on_delete=models.CASCADE)

    def last_message(self):
        chat_message = ChatMessage.objects.filter(chat__id=self.id).order_by('-send_datetime').first()
        if chat_message:
            return str(chat_message.content)
        else:
            return ' '


class ChatMessage(models.Model):
    content = models.TextField(max_length=500)
    send_datetime = models.DateTimeField(null=False, blank=False)
    is_read = models.BooleanField(default=False)

    chat = models.ForeignKey(LabourChat, on_delete=models.CASCADE)
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def __str__(self):
        return self.content[:10] + "..."


class ClientRating(models.Model):
    punctuation = models.IntegerField(
        default=0,
        validators=[
            MaxValueValidator(10),
            MinValueValidator(0)
        ])
    description = models.TextField(max_length=300, blank=True, null=True)

    banning = models.OneToOneField(Banning, null=True, blank=True, on_delete=True)
    labour = models.OneToOneField(LabourRequest, on_delete=models.CASCADE)

    rater_person = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='rater')
    rated_person = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='rated')

    def __str__(self):
        return self.rater_person.user.first_name + " -> " + self.rated_person.user.first_name + " -- " + str(
            self.punctuation)


class WorkerRating(models.Model):
    punctuation = models.IntegerField(
        default=0,
        validators=[
            MaxValueValidator(10),
            MinValueValidator(0)
        ])
    description = models.TextField(max_length=300, blank=True, null=True)

    banning = models.OneToOneField(Banning, null=True, blank=True, on_delete=True)
    labour = models.OneToOneField(LabourRequest, on_delete=models.CASCADE)

    rater_person = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='workerRater')
    rated_person = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='workerRated')

    def __str__(self):
        return self.rater_person.user.first_name + " -> " + self.rated_person.user.first_name + " -- " + str(
            self.punctuation)
