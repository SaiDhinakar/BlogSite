from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserSettingsForm

@login_required
def settings_view(request):
    if request.method == 'POST':
        form = UserSettingsForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            user = form.save(commit=False)
            
            # Handle profile image
            if 'profile_image' in request.FILES:
                old_image = user.profile_image if user.profile_image else None
                user.profile_image = request.FILES['profile_image']
                if old_image:
                    import os
                    if os.path.exists(old_image.path):
                        os.remove(old_image.path)
            
            user.save()
            messages.success(request, 'Profile updated successfully')
            return redirect('settings')
    else:
        form = UserSettingsForm(instance=request.user)
    
    return render(request, 'settings/settings.html', {'form': form})