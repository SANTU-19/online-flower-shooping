from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Profile

@login_required
def profile_view(request):
    # This ensures the profile exists
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        # Update profile image if uploaded
        if request.FILES.get('image'):
            profile.image = request.FILES['image']

        # Update username, email, phone
        request.user.username = request.POST.get('username')
        request.user.email = request.POST.get('email')
        profile.phone = request.POST.get('phone')

        # Save changes
        request.user.save()
        profile.save()

        return redirect('profile')   

    return render(request, 'profile/profilee.html', {'profile': profile})

@login_required
def remove_photo(request):
    profile = request.user.profile
    profile.image.delete(save=True)
    return redirect('profile')
