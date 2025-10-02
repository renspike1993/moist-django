from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import redirect

def group_required(group_name, redirect_url='/login/'):
    """
    Decorator to allow only users in a specific group.
    Superusers bypass the group check automatically.
    """
    def in_group(user):
        return user.is_superuser or user.groups.filter(name=group_name).exists()
    return user_passes_test(in_group, login_url=redirect_url)

def groups_required(group_names, redirect_url='/login/'):
    """
    Decorator to allow users in multiple groups.
    Usage: @groups_required(['Editors', 'Managers'])
    """
    def in_groups(user):
        return user.is_superuser or user.groups.filter(name__in=group_names).exists()
    return user_passes_test(in_groups, login_url=redirect_url)
