from django.contrib import admin
from requester_app.models import Request, Requester, AppliedRequest
# Register your models here.
admin.site.register(Request)
admin.site.register(Requester)
admin.site.register(AppliedRequest)