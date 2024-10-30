from django.db import models
from dietitian.models import Consultation
from users_account.models import Accounts

# Create your models here.
class Message(models.Model):
    consultation = models.ForeignKey(Consultation, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(Accounts, on_delete=models.CASCADE)
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.sender} at {self.timestamp}"