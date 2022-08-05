from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from elsa.commons.models import UUIDPrimaryKeyModel, TimeStampedModel


# Create your models here.
class Membership(UUIDPrimaryKeyModel, TimeStampedModel):
    """Represents a paid subscription to a training plan."""

    class MembershipTiers(models.IntegerChoices):
        """Membership length tiers. Expressed in months"""

        TRIMESTER = 3, _("Trimester")
        SEMESTER = 6, _("Semester")
        YEAR = 12, _("Year")

    tier = models.IntegerField(
        choices=MembershipTiers.choices, default=MembershipTiers.TRIMESTER
    )
    price = models.DecimalField(max_digits=19, decimal_places=4)


class Payment(UUIDPrimaryKeyModel, TimeStampedModel):
    """Represents a membership subscription payment transaction."""

    class PaymentStatus(models.IntegerChoices):
        """Transaction status.
        All of these except 'PENDING' are taken from the PayU Documentation.
        """

        PENDING = 0, _("Pending")
        APPROVED = 4, _("Approved")
        DECLINED = 6, _("Declined")
        EXPIRED = 5, _("Expired")

    class AllowedCoins(models.TextChoices):
        """List of coins allowed for payment."""

        ARS = "ARS", _("Argentine Peso")
        BRL = "BRL", _("Brazilian Real")
        CLP = "CLP", _("Chilean Peso")
        COP = "COP", _("Colombian Peso")
        MXN = "MXN", _("Mexican Peso")
        PEN = "PEN", _("Peruvian New Sol")
        USD = "USD", _("American Dollar")

    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    membership_purchased = models.ForeignKey(
        to=Membership, on_delete=models.SET_NULL, null=True
    )
    status = models.IntegerField(
        choices=PaymentStatus.choices, default=PaymentStatus.PENDING
    )
    reference_code = models.CharField(max_length=32)
    amount = models.DecimalField(max_digits=19, decimal_places=4)
    currency = models.CharField(
        max_length=3, choices=AllowedCoins.choices, default=AllowedCoins.USD
    )


class Coupon(UUIDPrimaryKeyModel, TimeStampedModel):
    class CouponNames(models.TextChoices):
        LANZAMIENTO = "ELSA50P"
        ACTIVACIONES_25 = "ELSA25P"
        ACTIVACIONES_15 = "ELSA15P"
        PEOPLE_X_BIKE = "PXB15ELSA"
        GORIGOGO = "GRG15ELSA"
        WHATSAPP_50 = "ELSA50WP"
        WHATSAPP_25 = "ELSA25WT"
        WHATSAPP_15 = "ELSA15WG"
        SOCIOS = "ELSA36020"
        LUIS_FER_SALDARRIAGA = "ELSA25LFS"
        LA_RUTA_COL = "ELSALRC25"
        FONDO_JARLINSO = "ELSAFJP25"
        FONDO_GORIGOGO = "ELSAGRG25"
        FONDO_NAIRO = "ELSAFNQ25"
        EVENTO_20221 = "ELSAEV221"
        EVENTO_20222 = "ELSAEV222"
        EVENTO_20223 = "ELSAEV223"
        REGALO_0001 = "ELSA3F0001"
        REGALO_0002 = "ELSA3F0002"
        REGALO_0003 = "ELSA3F0003"
        REGALO_0004 = "ELSA3F0004"
        REGALO_0005 = "ELSA3F0005"
        REGALO_0006 = "ELSA3F0006"
        REGALO_0007 = "ELSA3F0007"
        REGALO_0008 = "ELSA3F0008"
        REGALO_0009 = "ELSA3F0009"
        REGALO_0010 = "ELSA3F0010"
        REGALO_0011 = "ELSA3F0011"
        REGALO_0012 = "ELSA3F0012"
        REGALO_0013 = "ELSA3F0013"
        REGALO_0014 = "ELSA3F0014"
        REGALO_0015 = "ELSA3F0015"
        REGALO_0016 = "ELSA3F0016"
        REGALO_0017 = "ELSA3F0017"
        REGALO_0018 = "ELSA3F0018"
        REGALO_0019 = "ELSA3F0019"
        REGALO_0020 = "ELSA3F0020"
        REGALO_0021 = "ELSA3F0021"
        REGALO_0022 = "ELSA3F0022"
        REGALO_0023 = "ELSA3F0023"
        REGALO_0024 = "ELSA3F0024"
        REGALO_0025 = "ELSA3F0025"
        REGALO_0026 = "ELSA3F0026"
        REGALO_0027 = "ELSA3F0027"
        REGALO_0028 = "ELSA3F0028"
        REGALO_0029 = "ELSA3F0029"
        REGALO_0030 = "ELSA3F0030"
        REGALO_0031 = "ELSA3F0031"
        REGALO_0032 = "ELSA3F0032"
        REGALO_0033 = "ELSA3F0033"
        REGALO_0034 = "ELSA3F0034"
        REGALO_0035 = "ELSA3F0035"
        REGALO_0036 = "ELSA3F0036"
        REGALO_0037 = "ELSA3F0037"
        REGALO_0038 = "ELSA3F0038"
        REGALO_0039 = "ELSA3F0039"
        REGALO_0040 = "ELSA3F0040"
        REGALO_0041 = "ELSA3F0041"
        REGALO_0042 = "ELSA3F0042"
        REGALO_0043 = "ELSA3F0043"
        REGALO_0044 = "ELSA3F0044"
        REGALO_0045 = "ELSA3F0045"
        REGALO_0046 = "ELSA3F0046"
        REGALO_0047 = "ELSA3F0047"
        REGALO_0048 = "ELSA3F0048"
        REGALO_0049 = "ELSA3F0049"
        REGALO_0050 = "ELSA3F0050"
        REGALO_0051 = "ELSA3F0051"
        REGALO_0052 = "ELSA3F0052"
        REGALO_0053 = "ELSA3F0053"
        REGALO_0054 = "ELSA3F0054"
        REGALO_0055 = "ELSA3F0055"
        REGALO_0056 = "ELSA3F0056"
        REGALO_0057 = "ELSA3F0057"
        REGALO_0058 = "ELSA3F0058"
        REGALO_0059 = "ELSA3F0059"
        REGALO_0060 = "ELSA3F0060"
        REGALO_0061 = "ELSA3F0061"
        REGALO_0062 = "ELSA3F0062"
        REGALO_0063 = "ELSA3F0063"
        REGALO_0064 = "ELSA3F0064"
        REGALO_0065 = "ELSA3F0065"
        REGALO_0066 = "ELSA3F0066"
        REGALO_0067 = "ELSA3F0067"
        REGALO_0068 = "ELSA3F0068"
        REGALO_0069 = "ELSA3F0069"
        REGALO_0070 = "ELSA3F0070"
        REGALO_0071 = "ELSA3F0071"
        REGALO_0072 = "ELSA3F0072"
        REGALO_0073 = "ELSA3F0073"
        REGALO_0074 = "ELSA3F0074"
        REGALO_0075 = "ELSA3F0075"
        REGALO_0076 = "ELSA3F0076"
        REGALO_0077 = "ELSA3F0077"
        REGALO_0078 = "ELSA3F0078"
        REGALO_0079 = "ELSA3F0079"
        REGALO_0080 = "ELSA3F0080"

    name = models.CharField(
        max_length=20,
        choices=CouponNames.choices,
        default=CouponNames.REGALO_0001,
        unique=True,
    )
    discount = models.FloatField()
    valid_start_date = models.DateTimeField()
    valid_end_date = models.DateTimeField()

    def is_valid_date(self, date):
        return self.valid_start_date <= date <= self.valid_end_date


class CouponToUser(UUIDPrimaryKeyModel, TimeStampedModel):
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    coupon = models.ForeignKey(to=Coupon, on_delete=models.CASCADE)

    class Meta:
        unique_together = ["user", "coupon"]
