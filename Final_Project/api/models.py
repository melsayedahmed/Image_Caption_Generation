from django.db import models


class ApiImage(models.Model):
    name = models.TextField()
    Main_Img = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.name
