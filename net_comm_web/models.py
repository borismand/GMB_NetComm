from django.db import models


# Create your models here.


class Customer(models.Model):
    PROGRAM = [
        ('200', '200 Mbps'),
        ('500', '500 Mbps'),
        ('1000', '1Gbps')
    ]
    f_name = models.CharField(max_length=15)
    l_name = models.CharField(max_length=15)
    personal_id = models.BigIntegerField()
    mobile_num = models.CharField(max_length=15)
    email = models.EmailField(max_length=254)
    subscription = models.CharField(max_length=4, choices=PROGRAM, default='200')
    charge_from = models.DateField(auto_now_add=True)
    program_cost = models.IntegerField()

    def __str__(self):
        return f'{self.f_name} {self.l_name}'
