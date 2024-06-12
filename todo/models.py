from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone

# Create your models here.

class Status(models.Model):
  status = models.CharField('ステータス', max_length=20)

  def __str__(self):
    return self.status

def validate_task_name(value):
  if not value:
    raise ValidationError(('タスク名は必須です。'),
                          code='invalid', params={'value': value})
    
def validate_status_id(value):
  if not value:
    raise ValidationError(('ステータスの選択は必須です。'),
                          code='invalid', params={'value': value})

class TaskManager(models.Manager):
  def get_queryset(self):
    return super().get_queryset().filter(deleted_flg=False)

class Task(models.Model):
  task_name = models.CharField('タスク名', max_length=20, validators=[validate_task_name])
  status_id = models.ForeignKey(Status,
                      verbose_name='ステータス',
                      on_delete=models.CASCADE,
                      validators=[validate_status_id])
  start_date = models.DateField('作成日時', auto_now_add=True)
  end_date = models.DateField('完了日時', null=True, blank=True)
  deleted_flg = models.BooleanField('削除フラグ', default=False)
  objects = TaskManager()

  def clean(self):
    # タスク名が空白でないことを確認
    if not self.task_name:
      raise ValidationError('タスク名は必須です。')

  def save(self, *args, **kwargs):
    self.full_clean()
    # 新しいステータスを取得
    completed_status = Status.objects.get(status='完了')

    if self.status_id == completed_status and not self.end_date:
      self.end_date = timezone.now()
    elif self.status_id != completed_status and self.end_date:
      self.end_date = None
    super().save(*args, **kwargs)

  def __str__(self):
    return self.task_name
