from django.contrib import admin
from django.urls import path
from booking import views

urlpatterns = [
    # ── Django Admin ──────────────────────────────────────────────
    path("admin/", admin.site.urls),

    # ── Dashboard ─────────────────────────────────────────────────
    path("", views.dashboard, name="dashboard"),

    # ── Authentication ────────────────────────────────────────────
    path("login/",    views.login_view,          name="login"),
    path("logout/",   views.logout_view,         name="logout"),
    path("register/", views.register_view,        name="register"),
    path("redirect/", views.redirect_after_login, name="redirect_after_login"),

    # ── Password Reset Flow ───────────────────────────────────────
    path("custom-reset-password/",              views.reset_password_view,      name="custom_reset_password"),
    path("staff/request-password-change/",      views.request_password_change,  name="request_password_change"),
    path("dashboard-admin/approve-password/<int:request_id>/", views.approve_password_change, name="approve_password_change"),
    path("dashboard-admin/reject-password/<int:request_id>/",  views.reject_password_change,  name="reject_password_change"),

    # ── User Approval ─────────────────────────────────────────────
    path("dashboard-admin/approve-user/<int:user_id>/", views.approve_user, name="approve_user"),
    path("dashboard-admin/reject-user/<int:user_id>/",  views.reject_user,  name="reject_user"),

    # ── Delete / Deactivate User ──────────────────────────────────
    path("dashboard-admin/delete-user/<int:user_id>/",     views.delete_user,     name="delete_user"),
    path("dashboard-admin/deactivate-user/<int:user_id>/", views.deactivate_user, name="deactivate_user"),

    # ── Bookings ──────────────────────────────────────────────────
    path("bookings/new/",                    views.booking_create, name="booking_create"),
    path("bookings/",                        views.booking_list,   name="booking_list"),
    path("cancel-booking/<int:booking_id>/", views.cancel_booking, name="cancel_booking"),
    path("rooms/choose/",                    views.choose_room,    name="choose_room"),

    # ── Trips ─────────────────────────────────────────────────────
    path("trips/new/", views.trip_create, name="trip_create"),

    # ── Holidays ──────────────────────────────────────────────────
    path("holidays/new/",    views.holiday_create, name="holiday_create"),
    path("api/ph_holidays/", views.ph_holidays,    name="api_ph_holidays"),

    # ── APIs ──────────────────────────────────────────────────────
    path("api/bookings/",                    views.api_bookings,                  name="api_bookings"),
    path("api/pending-password-requests/",   views.pending_password_requests_api, name="pending_password_requests_api"),
    path("api/pending-user-registrations/",  views.pending_user_registrations_api, name="pending_user_registrations_api"),

    # ── Chat ──────────────────────────────────────────────────────
    path("chat/",                             views.chat_view,           name="chat_view"),
    path("chat/messages/",                    views.chat_messages_api,   name="chat_messages_api"),
    path("chat/send/",                        views.chat_send,           name="chat_send"),
    path("chat/delete/<int:msg_id>/",         views.chat_delete_message, name="chat_delete_message"),

    # ── Admin Dashboard ───────────────────────────────────────────
    path("dashboard-admin/",                        views.admin_dashboard,      name="admin_dashboard"),
    path("dashboard-admin/export-bookings/",        views.export_bookings_excel, name="export_bookings"),
    path("dashboard-admin/bookings/",               views.booking_history,      name="booking_history"),
    path("dashboard-admin/staff/",                  views.staff_accounts,       name="staff_accounts"),
    path("dashboard-admin/staff/edit/<int:user_id>/", views.edit_staff,         name="edit_staff"),

    # ── Room Management ───────────────────────────────────────────
    path("dashboard-admin/rooms/",                      views.manage_rooms, name="manage_rooms"),
    path("dashboard-admin/rooms/add/",                  views.add_room,     name="add_room"),
    path("dashboard-admin/rooms/update/<int:room_id>/", views.update_room,  name="update_room"),
    path("dashboard-admin/rooms/delete/<int:room_id>/", views.delete_room,  name="delete_room"),

    # ── Room Billing ──────────────────────────────────────────────
    path("dashboard-admin/billing/",        views.room_billing_report, name="room_billing_report"),
    path("dashboard-admin/billing/export/", views.export_billing_excel, name="export_billing_excel"),
    path("dashboard-admin/room-cost/export/",  views.export_room_cost_excel, name="export_room_cost"),

    # ── Login Page Settings ───────────────────────────────────────
    path("dashboard-admin/update-login-bg/", views.update_login_bg, name="update_login_bg"),

    # ── Todo List ─────────────────────────────────────────────────
    path("todos/",                      views.todo_list,   name="todo_list"),
    path("todos/create/",               views.todo_create, name="todo_create"),
    path("todos/toggle/<int:todo_id>/", views.todo_toggle, name="todo_toggle"),
    path("todos/delete/<int:todo_id>/", views.todo_delete, name="todo_delete"),

    # ── Future Projects ───────────────────────────────────────────
    path("projects/",                         views.project_list,          name="project_list"),
    path("projects/create/",                  views.project_create,        name="project_create"),
    path("projects/status/<int:project_id>/", views.project_update_status, name="project_update_status"),
    path("projects/delete/<int:project_id>/", views.project_delete,        name="project_delete"),
]
