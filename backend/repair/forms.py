from django.forms import ModelForm
from .models import Repair

class RepairForm(ModelForm):
     class Meta:
        model = Repair
        fields = ['customer_name','customer_phone_number','phone_model','repair_problem','repair_description','imei_number','model_number','sim_tray','sim','SD_card','phone_cover','phone_condition','total_amount','advance_paid','due','received_date','received_by','repaired_by','delivery_date','repair_status']

class SubmitForm(ModelForm):
    class Meta:
        model=Repair
        fields = ['amount_paid']

class OutsideForm(ModelForm):
    class Meta:
        model = Repair
        fields = ['outside_name','outside_desc','taken_by','outside_cost']