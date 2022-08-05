def main():
    import django

    django.setup()

    from django_q.tasks import Schedule

    Schedule.objects.create(
        func="elsa.users.utils.set_users_info_update_flag",
        schedule_type=Schedule.CRON,
        cron="0 0 * * MON",
    )
    Schedule.objects.create(
        func="elsa.users.utils.expire_users_membership",
        schedule_type=Schedule.CRON,
        cron="0 * * * *",
    )


if __name__ == "__main__":
    main()
