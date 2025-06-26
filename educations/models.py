from django.db import models

class Course(models.Model):
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
        null=True,
        help_text="Загрузите превью курса",
    )
    description = models.TextField(
        verbose_name="Описание",
        help_text="Введите описание курса",
    )

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"

    def __str__(self):
        return f"Название курса: {self.course_name}"


class Lesson(models.Model):
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
        null=True,
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
        return (f"Название урока: {self.lesson_name}"
                f"Описание урока: {self.description}")
