"""
Management Command: Send Reminder Emails
Usage: python manage.py send_reminders

Sends reminder emails to all attendees registered for trainings happening tomorrow.
"""

from django.core.management.base import BaseCommand
from django.utils import timezone
from booking.utils import send_bulk_reminders


class Command(BaseCommand):
    help = 'Send reminder emails to attendees for trainings scheduled tomorrow'

    def add_arguments(self, parser):
        # Optional: Add --dry-run flag to test without sending emails
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Simulate sending emails without actually sending them',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        
        if dry_run:
            self.stdout.write(self.style.WARNING('DRY RUN MODE - No emails will be sent'))
        
        self.stdout.write(self.style.SUCCESS(f'Starting reminder email process...'))
        self.stdout.write(f'Current time: {timezone.now().strftime("%Y-%m-%d %H:%M:%S")}')
        
        if not dry_run:
            # Send reminders
            result = send_bulk_reminders()
            
            # Display results
            self.stdout.write(self.style.SUCCESS('\n✅ Reminder Email Summary:'))
            self.stdout.write(f'  📅 Date: {result["date"]}')
            self.stdout.write(f'  📚 Bookings processed: {result["bookings_processed"]}')
            self.stdout.write(f'  ✅ Emails sent: {result["emails_sent"]}')
            self.stdout.write(f'  ❌ Emails failed: {result["emails_failed"]}')
            
            if result["emails_sent"] > 0:
                self.stdout.write(self.style.SUCCESS(f'\n🎉 Successfully sent {result["emails_sent"]} reminder emails!'))
            else:
                self.stdout.write(self.style.WARNING('\n⚠️  No reminder emails were sent. No trainings scheduled for tomorrow.'))
        else:
            # Dry run - just show what would be sent
            from booking.models import Booking
            from datetime import timedelta
            
            tomorrow = timezone.now() + timedelta(days=1)
            tomorrow_start = tomorrow.replace(hour=0, minute=0, second=0, microsecond=0)
            tomorrow_end = tomorrow.replace(hour=23, minute=59, second=59, microsecond=999999)
            
            tomorrow_bookings = Booking.objects.filter(
                start__gte=tomorrow_start,
                start__lte=tomorrow_end,
                status='Approved'
            )
            
            self.stdout.write(f'\n📋 Bookings scheduled for tomorrow ({tomorrow.strftime("%Y-%m-%d")}):')
            
            if not tomorrow_bookings.exists():
                self.stdout.write(self.style.WARNING('  No bookings found for tomorrow'))
            else:
                for booking in tomorrow_bookings:
                    attendees = booking.attendee_set.filter(reminder_sent=False)
                    self.stdout.write(f'\n  • {booking.title}')
                    self.stdout.write(f'    Time: {booking.start.strftime("%I:%M %p")} - {booking.end.strftime("%I:%M %p")}')
                    self.stdout.write(f'    Room: {booking.room.name}')
                    self.stdout.write(f'    Attendees to notify: {attendees.count()}')
                    
                    for attendee in attendees:
                        self.stdout.write(f'      - {attendee.name} ({attendee.email})')