path = r'C:\Users\cldto\OneDrive\Desktop\trainroom\booking\views.py'

new_code = """

# ================================================================
# ATTENDEE REGISTRATION VIEWS
# ================================================================

def attendee_register(request, booking_id):
    from .forms import AttendeeForm
    from .utils import send_confirmation_email
    from .models import Attendee
    booking = get_object_or_404(Booking, id=booking_id)
    if booking.start < timezone.now():
        return render(request, 'booking/registration_closed.html', {'booking': booking})
    if request.method == 'POST':
        form = AttendeeForm(request.POST, booking=booking)
        if form.is_valid():
            attendee = form.save(commit=False)
            attendee.booking = booking
            attendee.save()
            send_confirmation_email(attendee)
            return redirect('attendee_success', attendee_id=attendee.id)
    else:
        form = AttendeeForm(booking=booking)
    return render(request, 'booking/attendee_form.html', {
        'form': form, 'booking': booking,
        'attendee_count': booking.get_attendee_count(),
    })


def attendee_success(request, attendee_id):
    from .models import Attendee
    attendee = get_object_or_404(Attendee, id=attendee_id)
    return render(request, 'booking/success.html', {
        'attendee': attendee, 'booking': attendee.booking,
    })


from django.contrib.auth.decorators import login_required, user_passes_test

@login_required
def booking_detail(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    attendees = booking.attendee_set.all().order_by('registered_at')
    attendee_count = attendees.count()
    return render(request, 'booking/booking_detail.html', {
        'booking': booking, 'attendees': attendees, 'attendee_count': attendee_count,
    })


@login_required
def download_qr_code(request, booking_id):
    from django.http import Http404
    booking = get_object_or_404(Booking, id=booking_id)
    if not booking.qr_code:
        raise Http404("QR code not found")
    qr_file = booking.qr_code.open('rb')
    from django.http import HttpResponse
    response = HttpResponse(qr_file.read(), content_type='image/png')
    response['Content-Disposition'] = 'attachment; filename="booking_{}_qr.png"'.format(booking.id)
    qr_file.close()
    return response


@login_required
@user_passes_test(lambda u: u.is_staff or u.is_superuser)
def attendee_list(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    attendees = booking.attendee_set.all().order_by('registered_at')
    return render(request, 'booking/attendee_list.html', {
        'booking': booking, 'attendees': attendees,
    })


@login_required
@user_passes_test(lambda u: u.is_superuser)
def regenerate_qr_code(request, booking_id):
    from django.contrib import messages
    booking = get_object_or_404(Booking, id=booking_id)
    if request.method == 'POST':
        booking.generate_qr_code()
        booking.save()
        messages.success(request, 'QR code regenerated for {}'.format(booking.title))
    return redirect('booking_detail', booking_id=booking.id)
"""

with open(path, 'a', encoding='utf-8') as f:
    f.write(new_code)
print("Done - functions appended successfully.")
