from django.db import models

class GolfFile(models.Model):
    name = models.CharField(max_length=255)  # File name
    uploaded_at = models.DateTimeField(auto_now_add=True)  # Timestamp of upload
    file = models.FileField(upload_to='golf_files/')  # Upload directory

    def __str__(self):
        return self.name
