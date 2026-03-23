from django.db import models
from users.models import Customer

class LoyaltyReward(models.Model):
    reward_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    points_cost = models.IntegerField()

    class Meta:
        db_table = 'loyalty_reward'
        managed = False

    def __str__(self):
        return self.name

class LoyaltyRedemption(models.Model):
    redemption_id = models.AutoField(primary_key=True)
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Fulfilled', 'Fulfilled'),
    )
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    reward = models.ForeignKey(LoyaltyReward, on_delete=models.CASCADE)
    redeemed_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')

    class Meta:
        db_table = 'loyalty_redemption'
        managed = False

    def __str__(self):
        return f"Redemption {self.redemption_id} - {self.customer.name}"

