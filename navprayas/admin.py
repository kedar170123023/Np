from django.contrib import admin

# Register your models here.

from .models import (MTSE, Transaction, PR, CC, RANGOTSAV, CHESS, FHS, Profile, Document)

admin.site.register(MTSE)
admin.site.register(Transaction)
admin.site.register(PR)
admin.site.register(CC)
admin.site.register(RANGOTSAV)
admin.site.register(CHESS)
admin.site.register(FHS)
admin.site.register(Profile)
admin.site.register(Document)