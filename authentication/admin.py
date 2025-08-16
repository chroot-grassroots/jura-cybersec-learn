from django.contrib import admin
from .models import JuraUser

@admin.register(JuraUser)
class JuraUserAdmin(admin.ModelAdmin):
    list_display = ('masked_auth_hash', 'has_recovery')
    readonly_fields = ('auth_hash', 'recover_hash', 'recovery_enabled', 'encrypted_secret_key')
    list_filter = ('recovery_enabled',)
    
    # Disable all modifications
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False
    
    # Mask all sensitive data
    def masked_auth_hash(self, obj):
        """Mask actual hash"""
        return "********"
    masked_auth_hash.short_description = "Auth Hash (Masked)"
    
    def has_recovery(self, obj):
        """Boolean indicator without showing actual recovery hash"""
        return "✓" if obj.recover_hash else "✗"
    has_recovery.short_description = "Recovery Set"