from django.conf import settings
from django.db import models

from users.models import User


class Course(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="courses",
        verbose_name="Владелец",
    )
    course_name = models.CharField(
        max_length=35,
        verbose_name="Название курса",
        blank=True,
        help_text="Введите название курса",
    )
    preview = models.ImageField(
        upload_to="educations/previews/",
        verbose_name="Превью курса",
        blank=True,
        help_text="Загрузите превью курса",
    )
    description = models.TextField(
        verbose_name="Описание",
        help_text="Введите описание курса",
    )
    last_notified = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"

    def __str__(self):
        return f"Название курса: {self.course_name}"


class Lesson(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="lessons",
        verbose_name="Владелец",
    )
    lesson_name = models.CharField(
        max_length=35,
        verbose_name="Название урока",
        blank=True,
        help_text="Введите название урока",
    )
    description = models.TextField(
        verbose_name="Описание",
        help_text="Введите описание курса",
    )
    preview = models.ImageField(
        upload_to="educations/previews/",
        verbose_name="Превью урока",
        blank=True,
        help_text="Загрузите превью урока",
    )
    video_url = models.URLField(
        verbose_name="Ссылка на видео",
        blank=True,
        help_text="Введите URL видео урока",
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="lessons",
        verbose_name="Курс",
        help_text="Курс, к которому относится урок",
    )

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"

    def __str__(self):
        return (
            f"Название урока: {self.lesson_name}" f"Описание урока: {self.description}"
        )


class Payment(models.Model):
    PAYMENT_CHOICES = [
        ("cash", "наличные"),
        ("transfer", "перевод на счет"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="payments",
        verbose_name="Пользователь",
        help_text="Пользователь, купивший курс или урок",
    )
    payment_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата платежа",
        help_text="Дата оплаты курса или урока",
    )
    paid_course = models.ForeignKey(
        "Course",
        on_delete=models.CASCADE,
        related_name="payments_for_course",
        verbose_name="Оплаченный курс",
        null=True,
        blank=True,
        help_text="Курс, за который произведена оплата",
    )
    paid_lesson = models.ForeignKey(
        "Lesson",
        on_delete=models.CASCADE,
        related_name="payments_for_lesson",
        verbose_name="Оплаченный урок",
        null=True,
        blank=True,
        help_text="Урок, за который произведена оплата",
    )
    payment_sum = models.PositiveIntegerField(
        verbose_name="Сумма оплаты",
        help_text="Введите сумму оплаты",
    )
    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_CHOICES,
        verbose_name="Способ оплаты",
        help_text="Выберите способ оплаты",
    )

    class Meta:
        verbose_name = "Платеж"
        verbose_name_plural = "Платежи"

    def __str__(self):
        return f"{self.user} - {self.payment_sum} ({self.payment_method})"


class Subscription(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="subscriptions",
        verbose_name="Пользователь",
    )
    course = models.ForeignKey(
        "educations.Course",
        on_delete=models.CASCADE,
        related_name="subscriptions",
        verbose_name="Курс",
    )

    class Meta:
        verbose_name = "Подписка пользователя"
        verbose_name_plural = "Подписки пользователей"
        unique_together = ("user", "course")

    def __str__(self):
        return f"Подписка {self.user} на курс {self.course}"
