from django.utils import timezone

def get_expired_dates_util(fixed_item_id):
    from registry.models import Registry
    from orcamento.models import AbstractFixedItem, Periodicity

    fixed_item = AbstractFixedItem.objects.get(id=fixed_item_id)
    last_registry = Registry.objects.filter(item=fixed_item).last()
    if not last_registry:
        return [fixed_item.__next_expiracy_date()]

    last_date = last_registry.created_at.date()
    current_date = timezone.now().date()

    num_expired_periods = 0
    if fixed_item.periodicity == Periodicity.MONTHLY:
        num_expired_periods = (current_date.year - last_date.year) * 12 + (current_date.month - last_date.month)
    elif fixed_item.periodicity == Periodicity.WEEKLY:
        num_expired_periods = (current_date - last_date).days // 7
    elif fixed_item.periodicity == Periodicity.YEARLY:
        num_expired_periods = current_date.year - last_date.year

    expired_dates = [None] * (num_expired_periods + 1)

    expired_dates[0] = fixed_item.__next_expiracy_date(last_date)
    for i in range(1, num_expired_periods + 1):
        expired_dates[i] = fixed_item.__next_expiracy_date(expired_dates[i-1])

    return expired_dates

def next_expiracy_date(fixed_item, date):
    from orcamento.models import Periodicity

    if fixed_item.periodicity == Periodicity.MONTHLY:
        new_expiring_date = fixed_item.expiring_date.replace(year=date.year, month=date.month)
        if fixed_item.expire_work_day:
            if fixed_item.is_next_work_day:
                new_expiring_date = fixed_item.next_work_day(new_expiring_date)
            else:
                new_expiring_date = fixed_item.previous_work_day(new_expiring_date)
        return new_expiring_date

    if fixed_item.periodicity == Periodicity.WEEKLY:
        new_expiring_date = fixed_item.expiring_date.replace(year=date.year, month=date.month, day=date.day)
        if fixed_item.expire_work_day:
            if fixed_item.is_next_work_day:
                new_expiring_date = fixed_item.next_work_day(new_expiring_date)
            else:
                new_expiring_date = fixed_item.previous_work_day(new_expiring_date)
        return new_expiring_date

    new_expiring_date = fixed_item.expiring_date.replace(year=date.year)
    if fixed_item.expire_work_day:
        if fixed_item.is_next_work_day:
            new_expiring_date = fixed_item.next_work_day(new_expiring_date)
        else:
            new_expiring_date = fixed_item.previous_work_day(new_expiring_date)
    return new_expiring_date