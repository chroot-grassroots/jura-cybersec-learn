from django.shortcuts import render
from django.http import JsonResponse
from .models import JuraUser
import hashlib

def register_view(request):
    if request.method == 'POST':
        # For testing - normally this would be done client-side
        username = request.POST.get('username')
        passphrase = request.POST.get('passphrase')
        recovery_enabled = request.POST.get('recovery_enabled') == 'on'
        
        # Simple hash for testing (normally done client-side with proper crypto)
        auth_hash = hashlib.sha256(f"{username}{passphrase}".encode()).hexdigest()
        
        try:
            user = JuraUser.objects.create(
                auth_hash=auth_hash,
                recovery_enabled=recovery_enabled
            )
            return JsonResponse({
                'status': 'User created',
                'masked_hash': f"{auth_hash[:8]}..."
            })
        except Exception as e:
            return JsonResponse({'status': 'Error', 'message': str(e)})
    
    return render(request, 'authentication/register.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        passphrase = request.POST.get('passphrase')
        
        # Generate same hash
        auth_hash = hashlib.sha256(f"{username}{passphrase}".encode()).hexdigest()
        
        if JuraUser.objects.filter(auth_hash=auth_hash).exists():
            return JsonResponse({'status': 'User found'})
        else:
            return JsonResponse({'status': 'User not found'})
    
    return render(request, 'authentication/login.html')