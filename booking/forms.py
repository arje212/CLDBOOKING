from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Booking, Trip, Holiday, Profile, PasswordChangeRequest


ALL_COLOR_CHOICES = [
    ("#F1F50B", 'Yellow'),
    ('#3B82F6', 'Blue'),
    ('#10B981', 'Green'),
    ('#EF4444', 'Red'),
    ('#8B5CF6', 'Violet'),
    ('#6366F1', 'Indigo'),
    ('#F472B6', 'Pink'),
    ('#6B7280', 'Gray'),
    ('#374151', 'Dark Gray'),
    ('#D97706', 'Amber'),
    ('#14B8A6', 'Teal'),
    ('#0EA5E9', 'Sky'),
    ('#A3E635', 'Lime'),
    ('#84CC16', 'Light Green'),
    ('#22C55E', 'Emerald'),
    ('#EAB308', 'Gold'),
    ('#C026D3', 'Purple'),
    ('#F43F5E', 'Rose'),
    ('#BE123C', 'Dark Red'),
    ('#1E3A8A', 'Dark Blue'),
    ('#ffffff', 'White'),
]


def get_available_colors():
    """Return only colors not yet taken by existing users."""
    used_colors = set(Profile.objects.values_list('color', flat=True))
    return [
        (hex_val, label)
        for hex_val, label in ALL_COLOR_CHOICES
        if hex_val not in used_colors
    ]


class SimplePasswordField(forms.CharField):
    """Password field with no Django validators — accept anything."""
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('widget', forms.PasswordInput)
        kwargs.setdefault('min_length', 1)
        super().__init__(*args, **kwargs)

    def validate(self, value):
        # Only check that it's not empty
        if not value:
            raise ValidationError("Password cannot be empty.")


class RegisterForm(forms.Form):
    username   = forms.CharField(max_length=150)
    email      = forms.EmailField(required=True)
    password1  = SimplePasswordField(label="Password")
    password2  = SimplePasswordField(label="Confirm Password")
    color      = forms.ChoiceField(choices=get_available_colors)

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError("This username is already taken.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("This email is already registered.")
        return email

    def clean(self):
        cleaned = super().clean()
        p1 = cleaned.get('password1')
        p2 = cleaned.get('password2')
        if p1 and p2 and p1 != p2:
            self.add_error('password2', "Passwords do not match.")
        return cleaned

    def save(self, commit=True):
        user = User(
            username=self.cleaned_data['username'],
            email=self.cleaned_data['email'],
            is_staff=True,
            is_active=False,  # needs admin approval
        )
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
            profile, _ = Profile.objects.get_or_create(user=user)
            profile.color = self.cleaned_data['color']
            profile.save()
        return user


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ('room', 'title', 'attendees', 'start', 'end', 'status')
        widgets = {
            'start':  forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end':    forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }


class TripForm(forms.ModelForm):
    class Meta:
        model = Trip
        fields = ('destination', 'date', 'notes')
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }


class HolidayForm(forms.ModelForm):
    class Meta:
        model = Holiday
        fields = ['date', 'name']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }


class PasswordChangeRequestForm(forms.ModelForm):
    class Meta:
        model = PasswordChangeRequest
        fields = ['new_password']
        widgets = {
            'new_password': forms.PasswordInput(attrs={'class': 'input input-bordered w-full'}),
        }
