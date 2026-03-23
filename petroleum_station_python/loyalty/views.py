from django.shortcuts import render, redirect
from .models import LoyaltyReward, LoyaltyRedemption
from .forms import LoyaltyRewardForm
from users.decorators import role_required

@role_required('admin', 'accountant', 'staff', 'receptionist')
def reward_list(request):
    rewards = LoyaltyReward.objects.all()
    redemptions = LoyaltyRedemption.objects.all().order_by('-redeemed_date')
    return render(request, 'loyalty/reward_list.html', {
        'rewards': rewards,
        'redemptions': redemptions
    })

@role_required('admin')
def reward_create(request):
    if request.method == 'POST':
        form = LoyaltyRewardForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('loyalty:reward_list')
    else:
        form = LoyaltyRewardForm()
    return render(request, 'loyalty/reward_form.html', {'form': form})
