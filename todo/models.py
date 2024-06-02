from django.db import models

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

  def __str__(self):
    return self.task_name
