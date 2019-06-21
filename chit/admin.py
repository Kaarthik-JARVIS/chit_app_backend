from django.contrib import admin

from .models import User,Type,Chit,Group,Members,GroupMembers,Transaction,Expense,ExpenseCategory, GroupAuction, PayableAuction

admin.site.register(User)
admin.site.register(Chit)
admin.site.register(Type)
admin.site.register(Members)
admin.site.register(Group)
admin.site.register(GroupMembers)
admin.site.register(Transaction)
admin.site.register(ExpenseCategory)
admin.site.register(Expense)
admin.site.register(GroupAuction)
admin.site.register(PayableAuction)