from django.contrib import admin
from main.models import (
    TelegramUser, TelegramUserIncome, 
    TelegramSupport, TelegramAnswers, 
    TelegramExpense
)


@admin.register(TelegramExpense)
class TelegramExpenseAdmin(admin.ModelAdmin):
    list_display = ['get_username', 'name', 'amount', 'created_at']
    list_filter = ['user__username', 'name', 'created_at']
    search_fields = ['user__user_id', 'user__username', 'user__first_name', 'user__last_name']
    readonly_fields = ['created_at',]

    def get_username(self, obj):
        return obj.user.get_name()
    
    get_username.short_description = 'Пользователь'


@admin.register(TelegramAnswers)
class TelegramAnswersAdmin(admin.ModelAdmin):
    list_display = ['get_admin_username', 'get_user_username', 'answer', 'created_at']
    list_filter = ['admin_user__username', 'questions__user__username', 'created_at']
    search_fields = [
        'admin_user__user_id', 'admin_user__username', 
        'admin_user__first_name', 'admin_user__last_name', 'questions__message', 'answer']
    readonly_fields = ['created_at',]
    ordering = ['-created_at']

    def get_admin_username(self, obj):
        return obj.admin_user.get_name()

    def get_user_username(self, obj):
        return obj.questions.user.get_name()

    get_admin_username.short_description = 'Администратор'
    get_user_username.short_description = 'Пользователь с вопросом'


@admin.register(TelegramSupport)
class TelegramSupportAdmin(admin.ModelAdmin):
    list_display = ['get_username', 'message', 'created_at']
    list_filter = ['user__username', 'created_at']
    search_fields = [
        'user__user_id', 'user__username', 'user__first_name', 'user__last_name', 'message'
    ]
    readonly_fields = ['created_at',]
    ordering = ['-created_at']

    def get_username(self, obj):
        return obj.user.get_name()
    
    get_username.short_description = 'Пользователь'


@admin.register(TelegramUserIncome)
class TelegramUserIncomeAdmin(admin.ModelAdmin):
    list_display = ['get_username', 'name', 'amount', 'created_at']
    list_filter = ['user__username', 'name', 'created_at']
    search_fields = [
        'user__user_id', 
        'user__username', 
        'user__first_name', 
        'user__last_name',
        'name', 'amount']
    readonly_fields = ['created_at']

    def get_username(self, obj):
        return obj.user.username
    
    get_username.short_description = 'Пользователь'


@admin.register(TelegramUser)
class TelegramUserAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'get_name', 'balance', 'is_bot', 'is_admin', 'created_at')
    list_filter = ('is_bot', 'is_admin', 'created_at')
    search_fields = ('user_id', 'username', 'first_name', 'last_name')
    readonly_fields = ('created_at',)
    fieldsets = (
        ('Информация о пользователе', {
            'fields': ('user_id', 'username', 'first_name', 'last_name', 'language_code', 'is_bot', 'created_at')
        }),
        ('Финансовая информация', {
            'fields': ('balance',)
        }),
        ('Информация о файле', {
            'fields': ('chart',)
        }),
        ('Информация об администраторе', {
            'fields': ('is_admin',)
        }),
    )
    ordering = ['-created_at']

    def get_name(self, obj):
        return obj.get_name()

    get_name.short_description = 'Name'
    get_name.admin_order_field = 'username'

