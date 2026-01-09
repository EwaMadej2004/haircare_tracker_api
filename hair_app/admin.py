from django.contrib import admin
from .models import (
    HairProfile,
    HairProduct,
    HairRoutineEntry,
    HairTip,
)

admin.site.register(HairProfile)
admin.site.register(HairProduct)
admin.site.register(HairRoutineEntry)
admin.site.register(HairTip)

