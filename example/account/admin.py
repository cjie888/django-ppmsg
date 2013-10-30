# -*- coding: utf-8 -*-

from django.contrib import admin
from django.contrib.auth.models import User as DjangoUser


class DjangoUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'date_of_last_login',
                    'date_of_date_joined', 'is_superuser', 'is_staff')
    ordering = ('username',)
    list_filter = ('is_staff', 'is_superuser')
    search_fields = ('username', 'email')
    filter_horizontal = ('user_permissions',)

    def date_of_last_login(self, obj):
        new_last_login = obj.last_login.strftime("%Y-%m-%d %H:%M:%S")
        return new_last_login
    date_of_last_login.short_description = u'最后登入时间'

    def date_of_date_joined(self, obj):
        new_date_joined = obj.date_joined.strftime("%Y-%m-%d %H:%M:%S")
        return new_date_joined
    date_of_date_joined.short_description = u'加入时间'


admin.site.unregister(DjangoUser)
admin.site.register(DjangoUser, DjangoUserAdmin)
