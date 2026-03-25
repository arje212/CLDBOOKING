from django.contrib import admin
from .models import Room, Booking, Trip, Profile, Todo, ChatMessage, FutureProject, Attendee


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'capacity', 'projector', 'speaker', 'price_per_hour')
    search_fields = ('name',)


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display  = ('title', 'room', 'start', 'end', 'created_by', 'status', 'hours_used', 'total_cost', 'get_attendee_count')
    list_filter   = ('room', 'status', 'start')
    search_fields = ('title', 'created_by__username')
    readonly_fields = ('qr_code_preview', 'registration_url')
    
    def get_attendee_count(self, obj):
        return obj.get_attendee_count()
    get_attendee_count.short_description = 'Registered'
    
    def qr_code_preview(self, obj):
        if obj.qr_code:
            return f'<img src="{obj.qr_code.url}" width="200" />'
        return "No QR Code"
    qr_code_preview.short_description = 'QR Code'
    qr_code_preview.allow_tags = True
    
    def registration_url(self, obj):
        url = obj.get_registration_url()
        return f'<a href="{url}" target="_blank">{url}</a>'
    registration_url.short_description = 'Registration Link'
    registration_url.allow_tags = True


# ════════════════════════════════════════════════════════════════
# 🆕 ATTENDEE ADMIN
# ════════════════════════════════════════════════════════════════

@admin.register(Attendee)
class AttendeeAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'booking', 'registered_at', 'confirmation_sent', 'reminder_sent')
    list_filter = ('confirmation_sent', 'reminder_sent', 'registered_at', 'booking__room')
    search_fields = ('name', 'email', 'booking__title')
    readonly_fields = ('registered_at',)
    
    fieldsets = (
        ('Personal Information', {
            'fields': ('name', 'email', 'phone', 'notes')
        }),
        ('Booking', {
            'fields': ('booking',)
        }),
        ('Email Status', {
            'fields': ('confirmation_sent', 'reminder_sent', 'registered_at')
        }),
    )
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('booking', 'booking__room')


@admin.register(Trip)
class TripAdmin(admin.ModelAdmin):
    list_display = ('destination', 'date', 'created_by')
    list_filter  = ('date',)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'color')


@admin.register(Todo)
class TodoAdmin(admin.ModelAdmin):
    list_display  = ('title', 'user', 'priority', 'due_date', 'is_done')
    list_filter   = ('priority', 'is_done')
    search_fields = ('title', 'user__username')


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display  = ('sender', 'message', 'created_at', 'is_deleted')
    list_filter   = ('is_deleted',)
    search_fields = ('sender__username', 'message')


@admin.register(FutureProject)
class FutureProjectAdmin(admin.ModelAdmin):
    list_display  = ('title', 'provider', 'status', 'target_date', 'budget', 'created_by')
    list_filter   = ('status',)
    search_fields = ('title', 'provider')