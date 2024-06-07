from django.db import models
from django.utils import timezone

# Create your models here.

class Status(models.Model):
  status = models.CharField('ステータス', max_length=20)

  def __str__(self):
    return self.status

class Task(models.Model):
  task_name = models.CharField('タスク名', max_length=20)
  status_id = models.ForeignKey(Status,
                      verbose_name='ステータス',
                      on_delete=models.CASCADE)
  start_date = models.DateField('作成日時', auto_now_add=True)
  end_date = models.DateField('完了日時', null=True, blank=True)
  deleted_flg = models.BooleanField('削除フラグ', default=False)

  def save(self, *args, **kwargs):
    # 新しいステータスを取得
    completed_status = Status.objects.get(status='完了')

    if self.status_id == completed_status and not self.end_date:
      self.end_date = timezone.now()
    elif self.status_id != completed_status and self.end_date:
      self.end_date = None

    super().save(*args, **kwargs)

  def __str__(self):
    return self.task_name
