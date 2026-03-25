"""
TrainRoom Booking System - Email Utilities
Handles confirmation and reminder emails for attendees
"""

from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from datetime import datetime, timedelta
from django.utils import timezone


def send_confirmation_email(attendee):
    """
    Send confirmation email immediately after registration
    
    Args:
        attendee: Attendee instance
    
    Returns:
        bool: True if email sent successfully, False otherwise
    """
    booking = attendee.booking
    
    subject = f"✅ Registration Confirmed: {booking.title}"
    
    # HTML message
    html_message = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
            .header {{ background: #4f46e5; color: white; padding: 20px; text-align: center; border-radius: 8px 8px 0 0; }}
            .content {{ background: #f8fafc; padding: 30px; border-radius: 0 0 8px 8px; }}
            .info-box {{ background: white; padding: 15px; margin: 15px 0; border-left: 4px solid #4f46e5; }}
            .footer {{ text-align: center; color: #666; font-size: 12px; margin-top: 20px; }}
            h1 {{ margin: 0; font-size: 24px; }}
            h2 {{ color: #4f46e5; font-size: 18px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🎉 Registration Confirmed!</h1>
            </div>
            <div class="content">
                <p>Hi <strong>{attendee.name}</strong>,</p>
                
                <p>You have successfully registered for the following training:</p>
                
                <div class="info-box">
                    <h2>📅 Training Details</h2>
                    <p><strong>Training:</strong> {booking.title}</p>
                    <p><strong>Date:</strong> {booking.start.strftime('%B %d, %Y')}</p>
                    <p><strong>Time:</strong> {booking.start.strftime('%I:%M %p')} - {booking.end.strftime('%I:%M %p')}</p>
                    <p><strong>Room:</strong> {booking.room.name}</p>
                </div>
                
                <p>Please mark your calendar and arrive 10 minutes before the start time.</p>
                
                <p>We look forward to seeing you!</p>
                
                <div class="footer">
                    <p>This is an automated message from TrainRoom Booking System.</p>
                    <p>If you have questions, please contact your training coordinator.</p>
                </div>
            </div>
        </div>
    </body>
    </html>
    """
    
    # Plain text fallback
    plain_message = f"""
    Registration Confirmed!
    
    Hi {attendee.name},
    
    You have successfully registered for:
    
    Training: {booking.title}
    Date: {booking.start.strftime('%B %d, %Y')}
    Time: {booking.start.strftime('%I:%M %p')} - {booking.end.strftime('%I:%M %p')}
    Room: {booking.room.name}
    
    Please mark your calendar and arrive 10 minutes early.
    
    We look forward to seeing you!
    
    ---
    TrainRoom Booking System
    """
    
    try:
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[attendee.email],
            html_message=html_message,
            fail_silently=False,
        )
        
        # Mark as sent
        attendee.confirmation_sent = True
        attendee.save(update_fields=['confirmation_sent'])
        
        return True
    except Exception as e:
        print(f"Error sending confirmation email to {attendee.email}: {e}")
        return False


def send_reminder_email(attendee):
    """
    Send reminder email 1 day before the training
    
    Args:
        attendee: Attendee instance
    
    Returns:
        bool: True if email sent successfully, False otherwise
    """
    booking = attendee.booking
    
    subject = f"⏰ Reminder: {booking.title} - Tomorrow"
    
    # HTML message
    html_message = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
            .header {{ background: #f59e0b; color: white; padding: 20px; text-align: center; border-radius: 8px 8px 0 0; }}
            .content {{ background: #fffbeb; padding: 30px; border-radius: 0 0 8px 8px; }}
            .info-box {{ background: white; padding: 15px; margin: 15px 0; border-left: 4px solid #f59e0b; }}
            .alert {{ background: #fef3c7; padding: 15px; border-radius: 6px; margin: 15px 0; }}
            .footer {{ text-align: center; color: #666; font-size: 12px; margin-top: 20px; }}
            h1 {{ margin: 0; font-size: 24px; }}
            h2 {{ color: #f59e0b; font-size: 18px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>⏰ Training Reminder</h1>
            </div>
            <div class="content">
                <p>Hi <strong>{attendee.name}</strong>,</p>
                
                <div class="alert">
                    <p><strong>📢 Your training is TOMORROW!</strong></p>
                </div>
                
                <div class="info-box">
                    <h2>📅 Training Details</h2>
                    <p><strong>Training:</strong> {booking.title}</p>
                    <p><strong>Date:</strong> {booking.start.strftime('%B %d, %Y')} (TOMORROW)</p>
                    <p><strong>Time:</strong> {booking.start.strftime('%I:%M %p')} - {booking.end.strftime('%I:%M %p')}</p>
                    <p><strong>Room:</strong> {booking.room.name}</p>
                </div>
                
                <p><strong>Quick Reminders:</strong></p>
                <ul>
                    <li>Please arrive 10 minutes before the start time</li>
                    <li>Bring any required materials or notebooks</li>
                    <li>Make sure you know where {booking.room.name} is located</li>
                </ul>
                
                <p>See you tomorrow!</p>
                
                <div class="footer">
                    <p>This is an automated reminder from TrainRoom Booking System.</p>
                    <p>If you have questions, please contact your training coordinator.</p>
                </div>
            </div>
        </div>
    </body>
    </html>
    """
    
    # Plain text fallback
    plain_message = f"""
    Training Reminder - Tomorrow!
    
    Hi {attendee.name},
    
    This is a friendly reminder that your training is TOMORROW:
    
    Training: {booking.title}
    Date: {booking.start.strftime('%B %d, %Y')} (TOMORROW)
    Time: {booking.start.strftime('%I:%M %p')} - {booking.end.strftime('%I:%M %p')}
    Room: {booking.room.name}
    
    Quick Reminders:
    - Arrive 10 minutes early
    - Bring required materials
    - Know the room location
    
    See you tomorrow!
    
    ---
    TrainRoom Booking System
    """
    
    try:
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[attendee.email],
            html_message=html_message,
            fail_silently=False,
        )
        
        # Mark as sent
        attendee.reminder_sent = True
        attendee.save(update_fields=['reminder_sent'])
        
        return True
    except Exception as e:
        print(f"Error sending reminder email to {attendee.email}: {e}")
        return False


def send_bulk_reminders():
    """
    Find all bookings scheduled for tomorrow and send reminders
    Called by management command: python manage.py send_reminders
    
    Returns:
        dict: Summary of emails sent
    """
    from .models import Booking, Attendee
    
    # Get tomorrow's date range
    tomorrow = timezone.now() + timedelta(days=1)
    tomorrow_start = tomorrow.replace(hour=0, minute=0, second=0, microsecond=0)
    tomorrow_end = tomorrow.replace(hour=23, minute=59, second=59, microsecond=999999)
    
    # Find bookings happening tomorrow
    tomorrow_bookings = Booking.objects.filter(
        start__gte=tomorrow_start,
        start__lte=tomorrow_end,
        status='Approved'  # Only send for approved bookings
    )
    
    total_sent = 0
    total_failed = 0
    bookings_processed = 0
    
    for booking in tomorrow_bookings:
        # Get all attendees who haven't received a reminder yet
        attendees = booking.attendee_set.filter(reminder_sent=False)
        
        for attendee in attendees:
            success = send_reminder_email(attendee)
            if success:
                total_sent += 1
            else:
                total_failed += 1
        
        if attendees.exists():
            bookings_processed += 1
    
    return {
        'bookings_processed': bookings_processed,
        'emails_sent': total_sent,
        'emails_failed': total_failed,
        'date': tomorrow.strftime('%Y-%m-%d')
    }