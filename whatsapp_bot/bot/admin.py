from django.contrib import admin

from bot.models import Account, Group, RSS, Post


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = (
        'account_name',
        'number',
        'get_groups_display',
    )
    readonly_fields = ('groups',)

    def get_groups_display(self, obj):
        groups = obj.groups.all()
        return ', '.join([group.group_name for group in groups])
    get_groups_display.short_description = ('Группы связанные '
                                            'с данным аккаунтом')


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = (
        'group_name',
        'group_account',
        'group_url',
        'get_rss_for_group_display',
    )

    def get_rss_for_group_display(self, obj):
        rss_names = obj.rss_for_group.all()
        return ', '.join([rss_name.rss_name for rss_name in rss_names])
    get_rss_for_group_display.short_description = ('RSS ленты связанные '
                                                   'с данной группой')


@admin.register(RSS)
class RSSAdmin(admin.ModelAdmin):
    list_display = (
        'rss_name',
        'rss_url',
        'get_group_rss_display',
    )
    readonly_fields = ('group_rss',)

    def get_group_rss_display(self, obj):
        groups = obj.group_rss.all()
        return ', '.join([group.group_name for group in groups])
    get_group_rss_display.short_description = ('Группы связанные '
                                               'с данной RSS лентой')


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        'post_name',
        'poster',
        'post_to_group',
        'created_at',
    )
    # readonly_fields = ('post_name', 'poster', 'post_to_group', 'created_at',)
