from django.db import models



class RSVP(models.Model):
    ATTENDANCE_CHOICES = (
        ('yes', 'Yes, I will attend'),
        ('no', 'No, I cannot attend'),
    )

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    attendance = models.CharField(max_length=10, choices=ATTENDANCE_CHOICES, null=True, blank=True)
    number_of_guests = models.PositiveIntegerField(default=1)
    number_of_children = models.PositiveIntegerField(default=0)

    dietary_restrictions = models.TextField(null=True, blank=True)
    special_requests = models.TextField(null=True, blank=True)
    song_request_for_dj = models.CharField(max_length=255, null=True, blank=True)
    message = models.TextField(blank=True, null=True)
    is_vip = models.BooleanField(default=False)
    vip_token = models.CharField(max_length=50, blank=True, null=True, unique=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    


class WeddingMedia(models.Model):
    MEDIA_TYPES = (
        ('image', 'Image'),
        ('video', 'Video'),
    )
    official=  models.BooleanField(default=False)
    media_type = models.CharField(max_length=10, choices=MEDIA_TYPES)
    media_url = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.media_type}"
