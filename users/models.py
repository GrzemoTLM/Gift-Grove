import bcrypt
from django.db import models

class AppUser(models.Model):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    role = models.CharField(max_length=30, choices=[
        ("organizer", "Organizer"),
        ("participant", "Participant")
    ], default="participant")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.username} ({self.role})"

    def set_password(self, raw_password):
        hashed = bcrypt.hashpw(raw_password.encode(), bcrypt.gensalt())
        self.password = hashed.decode()

    def check_password(self, raw_password):
        return bcrypt.checkpw(raw_password.encode(), self.password.encode())
