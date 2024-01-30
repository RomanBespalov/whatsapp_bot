from django.db import models
from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from django.utils.html import format_html

from send_post.parser_rss import get_rss_news, RSS_URL


class Account(models.Model):
    """Модель аккаунт - номер телефона
    с которого отправляются новости."""
    account_name = models.CharField(
        max_length=200,
        verbose_name='Название аккаунта',
    )
    number = models.CharField(
        max_length=20,
        verbose_name='Номер телефона аккаунта',
    )
    groups = models.ManyToManyField(
        'Group',
        verbose_name=format_html('Название группы/ групп<br>'
                                 '(Cоздается, редактируется и удаляется '
                                 'в разделе Группы'),
        blank=True,
    )

    class Meta:
        verbose_name = 'Аккаунт'
        verbose_name_plural = 'Аккаунты'
        ordering = ['-id']

    def __str__(self):
        return f"{self.account_name} {self.number}"


class Group(models.Model):
    """Модель групп ватсап."""
    group_name = models.CharField(
        max_length=200,
        verbose_name='Название группы ватсап',
    )
    group_account = models.ForeignKey(
        Account,
        on_delete=models.PROTECT,
        verbose_name='Привязанный аккаунт',
        related_name='group_accounts',
    )
    group_id = models.TextField(
        verbose_name='ID группы',
        null=True,
    )
    rss_for_group = models.ManyToManyField(
        'RSS',
        verbose_name='RSS ленты связанные с группой',
    )

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'
        ordering = ['-id']

    def __str__(self):
        return self.group_name


class RSS(models.Model):
    """"Модель RSS ленты."""
    rss_name = models.CharField(
        max_length=200,
        verbose_name='Название RSS ленты',
    )
    rss_url = models.TextField(
        verbose_name='Ссылка на RSS ленту',
    )
    group_rss = models.ManyToManyField(
        Group,
        verbose_name=format_html('Группы связанные с RSS лентой<br>'
                                 '(Cоздается, редактируется и удаляется '
                                 'в разделе Группы'),
        blank=True,
    )

    class Meta:
        verbose_name = 'RSS лента'
        verbose_name_plural = 'RSS ленты'
        ordering = ['-id']

    def __str__(self):
        return self.rss_name


class Post(models.Model):
    post_name = models.CharField(
        max_length=300,
        verbose_name='Название новости',
    )
    poster = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        verbose_name='Аккаунт отправителя новости',
    )
    post_to_group = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
        verbose_name='Группа, куда отправилась новость',
    )
    created_at = models.DateTimeField(
        verbose_name='Дата отправки новости',
        auto_now_add=True
    )

    def save(self, *args, **kwargs):
        if not self.post_name:
            self.post_name = get_rss_news(RSS_URL)['title']
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Новостной пост'
        verbose_name_plural = 'Новостные посты'
        ordering = ['-id']

    def __str__(self):
        return self.post_name


@receiver(post_save, sender=Group)
def update_account_groups(sender, instance, **kwargs):
    """При сохранении группы обновим связи в аккаунтах"""
    instance.group_account.groups.add(instance)


@receiver(m2m_changed, sender=Group.rss_for_group.through)
def update_group_rss(sender, instance, action, **kwargs):
    """При изменении связей между Group и RSS, обновим связи в лентах"""
    if (action == "post_add" or action == "post_remove"
       or action == "post_clear"):
        for rss_id in instance.rss_for_group.values_list("id", flat=True):
            rss = RSS.objects.get(pk=rss_id)
            rss.group_rss.add(instance)
