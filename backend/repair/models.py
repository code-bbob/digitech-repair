from django.db import models
from datetime import datetime
import random
import string
# Create your models here.

class Repair(models.Model):

    status_choices = [
        ("Not repaired", "Not repaired"),
        ("Repaired","Repaired"),
        ("Unrepairable","Unrepairable"),
        ("Outrepaired", "Outrepaired"),
        ("Completed","Completed")
    ]

    accessory_choices = [
        ("Present","Present"),
        ("Absent","Absent"),
    ]

    repair_id = models.CharField(max_length=8,blank=True)
    customer_name = models.CharField(max_length=30)
    customer_phone_number = models.CharField(max_length=10)
    phone_model = models.CharField(max_length=30)   
    repair_problem = models.CharField(max_length=50)
    repair_description = models.TextField(null=True, blank=True)
    imei_number = models.CharField(max_length=30,null=True, blank=True)
    model_number = models.CharField(max_length=30,null=True, blank=True)
    sim_tray =models.CharField(max_length=20,choices=accessory_choices,default="Present")
    sim = models.CharField(max_length=20,choices=accessory_choices,default="Absent")
    SD_card = models.CharField(max_length=20,choices=accessory_choices,default="Absent")
    phone_cover = models.CharField(max_length=20,choices=accessory_choices,default="Absent")
    phone_condition = models.CharField(max_length=30,null=True, blank=True)
    total_amount = models.IntegerField()
    advance_paid = models.IntegerField()
    due = models.IntegerField()
    received_date = models.DateField(default=datetime.now)
    received_by = models.CharField(max_length=30)
    repaired_by = models.CharField(max_length=30,null=True, blank=True)
    delivery_date = models.DateField(default=datetime.now)
    repair_status=models.CharField(max_length=20,choices=status_choices,default="Not repaired")
    amount_paid = models.FloatField(null=True,blank=True)
    repair_cost_price = models.FloatField(null=True,blank=True)
    cost_price_description = models.CharField(max_length=50,null=True,blank=True)
    repair_profit = models.FloatField(null=True,blank=True)
    technician_profit = models.FloatField(null=True,blank=True)
    my_profit = models.FloatField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.pk:  # Check if the instance is new
            self.repair_id = self.generate_unique_repair_id()
        if self.repair_status=="Completed":
            self.amount_paid = self.amount_paid + self.advance_paid
        if self.repair_status=="Completed" and self.amount_paid is not None and self.repair_cost_price is not None:
            self.repair_profit = self.amount_paid - self.repair_cost_price
            self.technician_profit = (40/100) * self.repair_profit
            self.my_profit = (60/100) * self.repair_profit
        super(Repair, self).save(*args, **kwargs)

    def generate_unique_repair_id(self,length=8):
        characters = string.ascii_letters + string.digits
        while True:
            repair_id = ''.join(random.choice(characters) for _ in range(length))
            if not Repair.objects.filter(repair_id=repair_id).exists():
                return repair_id
            
    def __str__(self):
        return f"{self.phone_model} by {self.customer_name}"