from django.db import models


# Create your models here.

class PITBApiData(models.Model):
    ACTIVE = 'active'
    BLOCKED = 'blocked'

    STATUS_CHOICES = [
        (ACTIVE, 'active'),
        (BLOCKED, 'blocked'),
    ]

    MULTIPLE = 'multiple'
    SINGLE = 'single'

    HIT_TYPE_CHOICES = [
        (MULTIPLE, 'multiple'),
        (SINGLE, 'single'),
    ]
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=20, unique=True)  # PTA-1
    name = models.CharField(max_length=100)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=ACTIVE)
    description = models.TextField()
    function_name = models.CharField(max_length=100, null=True)
    hit_type = models.CharField(max_length=10, choices=HIT_TYPE_CHOICES, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=100, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    updated_by = models.CharField(max_length=100, null=True)

    def save(self, *args, **kwargs):
        if not self.code:
            # Getting the last code from DB
            last_record = PITBApiData.objects.all().order_by('-code').first()
            if last_record:
                last_number = int(last_record.code.split('-')[1])  # Returns ['PTA', '123'] and returns 123
                self.code = f"PTA-{last_number + 1}"
            else:
                self.code = "PTA-1"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.code} - {self.name}"

    class Meta:
        db_table = 'tbl_pitb_api_data'


class PITBApiBulkVTMSLog(models.Model):
    id = models.AutoField(primary_key=True)
    method = models.CharField(max_length=100)
    push_body = models.TextField(null=True)
    push_date = models.DateField(auto_now_add=True)
    push_time = models.TimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=100, null=True)

    class Meta:
        db_table = 'tbl_pitb_api_bulk_vtms_log'

    def __str__(self):
        return f"{self.push_date} - {self.push_time}"
