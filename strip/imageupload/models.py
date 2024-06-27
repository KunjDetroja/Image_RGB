from django.db import models

class UrineStrip(models.Model):
    image = models.ImageField(upload_to='urine_strips/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Urine Strip uploaded at {self.uploaded_at}"
