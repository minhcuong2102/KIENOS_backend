from django.db import models
from datetime import timedelta

class Service(models.Model):
    discount = models.IntegerField(default=0)
    name = models.CharField(max_length=256, null=False, blank=False, default='Gói tập luyện ...')
    discount_start = models.DateTimeField(null=True, blank=True)
    discount_end = models.DateTimeField(null=True, blank=True)
    details = models.TextField(null=True, blank=True)

    class Meta:
        abstract = True  


class PTService(Service):

    session_duration = models.IntegerField(default=0)
    cost_per_session = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    validity_period = models.IntegerField(default=45) # Thời hạn sử dụng, vd: 45 ngày

    @property
    def total_cost(self):
        return self.number_of_session * self.cost_per_session
    
    # def save(self, *args, **kwargs):
    #     if not self.expire_date:  
    #         self.expire_date = self.start_date + timedelta(days=self.validity_period)
    #     super().save(*args, **kwargs)

    class Meta:
        db_table = 'pt_service'


class NonPTService(Service):
    number_of_month = models.IntegerField(default=0)
    cost_per_month = models.DecimalField(max_digits=10, decimal_places=2)

    @property
    def total_cost(self):
        return self.number_of_month * self.cost_per_month
    
    # def save(self, *args, **kwargs):
    #     if not self.expire_date:  
    #         self.expire_date = self.start_date + timedelta(days=self.number_of_month * 30)  # 1 tháng = 30 ngày
    #     super().save(*args, **kwargs)

    class Meta:
        db_table = 'nonpt_service'


