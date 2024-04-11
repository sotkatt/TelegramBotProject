from django.db import models


class TelegramUser(models.Model):
    user_id = models.BigIntegerField(
        unique=True,
        verbose_name="ID пользователя",
        help_text="Уникальный идентификатор пользователя в Telegram.",
    )
    username = models.CharField(
        max_length=120,
        blank=True,
        null=True,
        verbose_name="Имя пользователя",
        help_text="Имя пользователя в Telegram.",
    )
    first_name = models.CharField(
        max_length=120,
        blank=True,
        null=True,
        verbose_name="Имя",
        help_text="Имя пользователя в Telegram.",
    )
    last_name = models.CharField(
        max_length=120,
        blank=True,
        null=True,
        verbose_name="Фамилия",
        help_text="Фамилия пользователя в Telegram.",
    )
    language_code = models.CharField(
        max_length=10,
        blank=True,
        null=True,
        verbose_name="Код языка",
        help_text="Код языка, используемый пользователем в Telegram.",
    )
    is_bot = models.BooleanField(
        default=False,
        verbose_name="Бот",
        help_text="Указывает, является ли пользователь ботом.",
    )
    
    balance = models.BigIntegerField(
        default=0,
        verbose_name="Баланс",
        help_text="Баланс пользователя.",
    )
    
    chart = models.FileField(
        upload_to="chart/",
        blank=True,
        null=True,
        verbose_name="График",
        help_text="Файл с графиком пользователя.",
    )
    
    is_admin = models.BooleanField(
        default=False,
        verbose_name="Админ",
        help_text="Указывает, является ли пользователь админом.",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Создан",
        help_text="Временная метка, указывающая, когда был создан пользователь.",
    )

    def get_name(self):
        if self.username:
            return self.username
        
        elif self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        
        elif self.first_name:
            return self.first_name
        
        else:
            return str(self.user_id)
    
    def __str__(self):
        return f"{self.user_id}: {self.get_name()}"
    
    class Meta:
        verbose_name = "Пользователь Telegram"
        verbose_name_plural = "Пользователи Telegram"
        ordering = ["-created_at"]


class TelegramUserIncome(models.Model):
    user = models.ForeignKey(
        TelegramUser,
        on_delete=models.CASCADE,
        verbose_name="Пользователь Telegram",
        help_text="Пользователь Telegram, которому принадлежит доход.",
    )
    name = models.CharField(
        max_length=100,
        verbose_name="Название дохода.",
        help_text="От куда пришли даеньги",
    )
    amount = models.BigIntegerField(
        verbose_name="Сумма",
        help_text="Сумма дохода.",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Создан",
        help_text="Временная метка, указывающая, когда был создан доход.",
    )

    def __str__(self):
        return f"{self.user.get_name()}: {self.amount} ₸"

    class Meta:
        verbose_name = "Доход Telegram"
        verbose_name_plural = "Доходы Telegram"
        ordering = ["-created_at"]


class TelegramSupport(models.Model):
    user = models.ForeignKey(
        TelegramUser,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
        help_text="Пользователь, которому принадлежит вопрос.",
    )
    message = models.TextField(
        verbose_name="Сообщение",
        help_text="Сообщение пользователя.",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Создан",
        help_text="Временная метка, указывающая, когда был создан.",
    )

    def __str__(self):
        return f"{self.user.get_name()}: {self.message}"

    class Meta:
        verbose_name = "Поддержка Telegram"
        verbose_name_plural = "Поддержка Telegram"
        ordering = ["-created_at"]


class TelegramAnswers(models.Model):
    admin_user = models.ForeignKey(
        TelegramUser,
        on_delete=models.CASCADE,
        verbose_name="Администратор",
        help_text="Пользователь, которому выдана права администратора.",
    )
    questions = models.ForeignKey(
        TelegramSupport,
        on_delete=models.CASCADE,
        verbose_name="Вопрос",
        help_text="Вопрос пользователя.",
    )
    answer = models.TextField(
        verbose_name="Ответ",
        help_text="Ответ на вопрос пользователя.",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Создан",
        help_text="Временная метка, указывающая, когда был создан.",
    )
    
    def __str__(self):
        return f"{self.admin_user.get_name()}: {self.answer}"
    
    class Meta:
        verbose_name = "Ответы на вопросы Telegram"
        verbose_name_plural = "Ответы на вопросы Telegram"
        ordering = ["-created_at"]


class TelegramExpense(models.Model):
    user = models.ForeignKey(
        TelegramUser,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
        help_text="Пользователь, которому принадлежит расход.",
    )
    name = models.CharField(
        max_length=100,
        verbose_name="Название расхода",
        help_text="Расхода, куда потратилась деньги.",
    )
    amount = models.BigIntegerField(
        default=0,
        verbose_name="Сумма",
        help_text="Сумма расхода.",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Создан",
        help_text="Временная метка, указывающая, когда был создан.",
    )

    def __str__(self):
        return f"{self.user.get_name()} - {self.amount} ₸ ({self.name})"

    class Meta:
        verbose_name = "Расход Telegram"
        verbose_name_plural = "Расходы Telegram"
        ordering = ["-created_at"]