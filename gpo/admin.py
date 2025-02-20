from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Group

class CustomUserAdmin(UserAdmin):
    model = User

    # Cấu hình các trường trong form tạo và chỉnh sửa người dùng
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('uid',)}),  # Thêm trường `uid` nếu cần
    )

# Đăng ký User với Django Admin
admin.site.register(User, CustomUserAdmin)
admin.site.register(Group)
