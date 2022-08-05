from django.contrib import admin

import elsa.memberships.models as models

# Register your models here.
admin.site.register(
    [models.Membership, models.Payment, models.Coupon, models.CouponToUser]
)
