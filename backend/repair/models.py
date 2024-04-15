from django.db import models
from datetime import datetime
import random
import string
# Create your models here.

class Repair(models.Model):
    repair_id = models.CharField(max_length=8,blank=True)
    customer_name = models.CharField(max_length=30)
    customer_phone_number = models.CharField(max_length=10)
    phone_model = models.CharField(max_length=30)   
    repair_problem = models.CharField(max_length=50)
    repair_description = models.TextField()
    imei_number = models.CharField(max_length=30)
    model_number = models.CharField(max_length=30)
    sim_tray = models.BooleanField(default=1)
    sim = models.BooleanField(default=0)
    SD_card = models.BooleanField(default=0)
    phone_cover = models.BooleanField(default=0)
    phone_condition = models.CharField(max_length=30)
    total_amount = models.IntegerField()
    advance_paid = models.IntegerField()
    due = models.IntegerField()
    received_date = models.DateField(default=datetime.now)
    received_by = models.CharField(max_length=30)
    repaired_by = models.CharField(max_length=30)
    delivery_date = models.DateField()
    repair_status = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        self.repair_id = self.generate_unique_repair_id()
        super(Repair, self).save(*args, **kwargs)

    def generate_unique_repair_id(self,length=8):
        characters = string.ascii_letters + string.digits
        while True:
            repair_id = ''.join(random.choice(characters) for _ in range(length))
            if not Repair.objects.filter(repair_id=repair_id).exists():
                return repair_id
            
    def __str__(self):
        return f"{self.phone_model} by {self.customer_name}"