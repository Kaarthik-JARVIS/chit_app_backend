"""my_site URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from chit import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/login', views.LoginView.as_view()),
    path('api/user', views.UserView.as_view()),
    path('api/user/<int:userId>', views.UserView.as_view()),
    path('api/chitType', views.ChitTypeView.as_view()),
    path('api/chitType/<int:id>', views.ChitTypeView.as_view()),
    path('api/chitAmount', views.ChitAmountView.as_view()),
    path('api/chitAmount/<int:id>', views.ChitAmountView.as_view()),
    path('api/chitGroup', views.ChitGroupView.as_view()),
    path('api/chitTypeGroup/<int:typeId>', views.ChitTypeGroupView.as_view()),
    path('api/chitGroup/<int:id>', views.ChitGroupView.as_view()),
    path('api/expenseCategory', views.ExpenseCategoryView.as_view()),
    path('api/expenseCategory/<int:id>', views.ExpenseCategoryView.as_view()),
    path('api/members', views.MemberView.as_view()),
    path('api/members/<int:id>', views.MemberView.as_view()),

    path('api/addGroupMember/<int:groupId>', views.AddGroupMemberView.as_view()),
    path('api/groupMember/<int:id>', views.AddGroupMemberView.as_view()),
    path('api/addExpense', views.ExpenseView.as_view()),
    path('api/viewExpense', views.ShowExpenseView.as_view()),
    
    path('api/commission', views.ChitCommissionView.as_view()),
    
    path('api/viewMembers', views.ActiveMember.as_view()),
    path('api/viewExpenseCategory', views.ActiveExpenseCategory.as_view()),
    path('api/viewChitType', views.ActiveChitType.as_view()),
    path('api/viewChitAmount', views.ActiveChitAmount.as_view()),

    path('api/removeChitType/<int:id>', views.DeleteChitType.as_view()),
    path('api/removeMembers/<int:id>', views.DeleteChitMember.as_view()),
    path('api/removeChitAmount/<int:id>', views.DeleteChitAmount.as_view()),
    path('api/removeExpenseCategory/<int:id>', views.DeleteExpenseCategory.as_view()),

    path('api/removeGroupMember/<int:id>', views.DeleteGroupMember.as_view()),
    path('api/removeUser/<int:id>', views.DeleteUser.as_view()),

    path('api/auction', views.AuctionView.as_view()),
    path('api/transaction', views.TransactionView.as_view()),
    path('api/transaction/<int:id>', views.TransactionView.as_view()),

    path('api/groupDetail/<int:id>', views.GroupDataView.as_view()),

    path('api/memberDetail/<int:id>', views.MemberDetailView.as_view()),
]
