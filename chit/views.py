from django.http import JsonResponse
from .models import User, Type, Chit, Group, Members, GroupMembers, ExpenseCategory, Expense, Transaction, Commission, GroupAuction, PayableAuction
from rest_framework import views
from django.contrib.auth.hashers import PBKDF2PasswordHasher
import logging
from django.db.models import F,Q
from django.db.models import Count, Sum
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt

import jwt,json
from datetime import datetime

from chit.permissions import JSONWebTokenAuthentication
from rest_framework import exceptions
from rest_framework.authentication import get_authorization_header
from rest_framework.authtoken.models import Token

class LoginView(views.APIView):

    def post(self,request):
        username = request.data["username"]
        pwd = request.data["password"]
        
        user = authenticate(username=username, password=pwd)

        if user is not None:
            user = User.objects.filter(name=username).get()
            
            # if user.auth_token is not None:
            #     user.auth_token.delete()

            # token = Token.objects.create(user=user)
            
            return JsonResponse({'status': True,'message': 'Login Success',
                                'userId': user.id,
                                'name': user.name,
                                'phone': user.phone_number,
                                'role': user.role,
                                'token': 'token'}, status=200)
        else:
            return JsonResponse({'message': 'Invalid Username / Password', 'status': False})


""" Users 
"""
class UserView(views.APIView):

    def post(self, request,userId=0):
        if userId == 0:
            try:
                hasher = PBKDF2PasswordHasher()
                user = User(
                    name=request.data['name'],
                    phone_number=request.data['phone_number'],
                    role=request.data['role'],
                    password=hasher.encode(password=request.data['pin'],
                                        salt='salt',
                                        iterations=50000))

                user.save()

                return JsonResponse({'status': True,'id': user.id, 'message': 'New user added successfully'}, status=200)
            
            except Exception as e:
                return JsonResponse({'message' : str(e),'status': False},status=200)
        else:
            try:
                user = User.objects.filter(id=userId).update(
                    name=request.data['name'],
                    phone_number=request.data['phone_number'],
                    role=request.data['role'])

                return JsonResponse({'status': True,'id': id, 'message': 'Information updated successfully'}, status=200)
            except Exception as e:
                return JsonResponse({'message' : str(e),'status': False},status=200)

    def get(self, request, userId=0):
        """
        """
        if userId == 0:
            users = User.objects.all()
        else:
            users = User.objects.filter(id=userId)
            
        result = []

        for user in users:
            status = True
            if user.is_active == 0:
                status = False

            result .append({
                'id':user.id,
                'name':user.name,
                'phone_number':user.phone_number,
                'role':user.role,
                'status':status
            })
        return JsonResponse(result, safe=False, status=200)


""" Chit Type 
"""
class ChitTypeView(views.APIView):
    def post(self, request,id = 0):
        if id == 0:
            try:
                data = Type(name=request.data['name'],color=request.data['color'])
                data.save()

                return JsonResponse({'status': True, 'id': data.id ,'message': 'Information added successfully'}, status=200)
            
            except Exception as e:
                return JsonResponse({'message' : str(e),'status': False},status=200)
        
        else:
            try:
                data = Type.objects.filter(id=id).update(name=request.data['name'],color=request.data['color'])

                return JsonResponse({'status': True,'id': id , 'message': 'Information updated successfully'}, status=200)
            
            except Exception as e:
                return JsonResponse({'message' : str(e),'status': False},status=200)

    def get(self, request, id=0):
        """ Get Details
        """
        if id == 0:
            datas = Type.objects.all()
        else:
            datas = Type.objects.filter(id=id)
            
        result = []

        for typeData in datas:
            status = True
            if typeData.status == 0:
                status = False

            result .append({
                'id':typeData.id,
                'name':typeData.name,
                'color':typeData.color,
                'status':status
            })
        return JsonResponse(result, safe=False, status=200)


""" Chit Amount 
"""
class ChitAmountView(views.APIView):
    def post(self, request,id = 0):
        if id == 0:
            try:
                data = Chit(amount=request.data['amount'], remarks=request.data['remarks'])
                data.save()

                return JsonResponse({'status': True,'id': data.id, 'message': 'Information added successfully'}, status=200)
            
            except Exception as e:
                return JsonResponse({'message' : str(e),'status': False},status=200)
        
        else:
            try:
                data = Chit.objects.filter(id=id).update(amount=request.data['amount'], remarks=request.data['remarks'])

                return JsonResponse({'status': True,'id': id, 'message': 'Information updated successfully'}, status=200)
            
            except Exception as e:
                return JsonResponse({'message' : str(e),'status': False},status=200)

    def get(self, request, id=0):
        """ Get Details
        """
        if id == 0:
            datas = Chit.objects.all()
        else:
            datas = Chit.objects.filter(id=id)
            
        result = []

        for data in datas:
            status = True
            if data.status == 0:
                status = False
            result .append({
                'id':data.id,
                'amount':data.amount,
                'remarks':data.remarks,
                'status':status
            })
        return JsonResponse(result, safe=False, status=200)


""" Chit Group 
"""
class ChitGroupView(views.APIView):

    def post(self, request,id = 0):
        """ POST method handler to store user data
        """
        if id == 0:
            try:
                data = Group(name=request.data['name'], 
                            type_id=Type.objects.filter(id=request.data['typeId']).get(),
                            remarks=request.data['remarks'],
                            chit_id=Chit.objects.filter(id=request.data['chitId']).get(),
                            start_date=request.data['startDate'])
                data.save()

                return JsonResponse({'status': True, 'id': data.id, 'message': 'Information added successfully'}, status=200)
            
            except Exception as e:
                return JsonResponse({'message' : str(e),'status': False},status=200)
        
        else:
            try:
                data = Group.objects.filter(id=id).update(name=request.data['name'], 
                            type_id=Type.objects.filter(id=request.data['typeId']).get(),
                            remarks=request.data['remarks'],
                            chit_id=Chit.objects.filter(id=request.data['chitId']).get(),
                            start_date=request.data['startDate'])

                return JsonResponse({'status': True,'id': id,  'message': 'Information updated successfully'}, status=200)
            
            except Exception as e:
                return JsonResponse({'message' : str(e),'status': False},status=200)

    def get(self, request, id=0):
        """ Get Details
        """
        try:
            if id != 0:
                datas = Group.objects.filter(id=id)
            else:
                datas = Group.objects.all()

            result = []

            for data in datas:
                members = []
                groupMem = GroupMembers.objects.filter(group_id=data.id)

                for member in groupMem:
                    members.append({
                        'id':member.id,
                        'memberId':member.member_id.id,
                        'name':member.member_id.name,
                        'phoneNo':member.member_id.phone_number
                    })

                result.append({
                    'id':data.id,
                    'name':data.name,
                    'typeId':data.type_id.id,
                    'type':data.type_id.name,
                    'chitId':data.chit_id.id,
                    'chitAmount':data.chit_id.amount,
                    'startDate':data.start_date,
                    'remarks':data.remarks,
                    'members': members
                })
            return JsonResponse(result, safe=False, status=200)
        except Exception as e:
            return JsonResponse({'message' : str(e),'status': False},status=200)


class ChitTypeGroupView(views.APIView):
    def get(self, request, typeId=0):
        """ Get Details
        """
        try:
            if typeId != 0:
                datas = Group.objects.filter(type_id=Type.objects.get(id=typeId),status=1)
            else:
                datas = Group.objects.all()

            result = []

            for data in datas:
                members = []
                groupMem = GroupMembers.objects.filter(group_id=data.id)

                for member in groupMem:
                    members.append({
                        'id':member.id,
                        'memberId':member.member_id.id,
                        'name':member.member_id.name,
                        'phoneNo':member.member_id.phone_number
                    })

                result.append({
                    'id':data.id,
                    'name':data.name,
                    'typeId':data.type_id.id,
                    'type':data.type_id.name,
                    'chitId':data.chit_id.id,
                    'chitAmount':data.chit_id.amount,
                    'startDate':data.start_date,
                    'remarks':data.remarks,
                    'members': members
                })
            return JsonResponse(result, safe=False, status=200)
        except Exception as e:
            return JsonResponse({'message' : str(e),'status': False},status=200)

""" Chit Type 
"""
class ChitCommissionView(views.APIView):
    def post(self, request):

        commission = Commission.objects.all()

        if not commission:
            try:
                data = Commission(profit_commission=request.data['profitCommission'],
                    auction_commission=request.data['auctionCommission'])
                data.save()

                return JsonResponse({'status': True, 'message': 'Information added successfully'}, status=200)
            
            except Exception as e:
                return JsonResponse({'message' : str(e),'status': False},status=200)
        
        else:
            try:
                data = Commission.objects.update(profit_commission=request.data['profitCommission'],
                    auction_commission=request.data['auctionCommission'])

                return JsonResponse({'status': True, 'message': 'Information updated successfully'}, status=200)
            
            except Exception as e:
                return JsonResponse({'message' : str(e),'status': False},status=200)

    def get(self, request):
        """ Get Details
        """
        commission = Commission.objects.all()
        
        if not commission:
            result = {
                'profitCommission':0,
                'auctionCommission':0,
            }
        else:
            data = Commission.objects.get()
            result = {
                'profitCommission':data.profit_commission,
                'auctionCommission':data.auction_commission,
            }

        return JsonResponse(result, safe=False, status=200)

 

""" Members
"""
class MemberView(views.APIView):
    def post(self, request,id = 0):
        if id == 0:
            try:
                data = Members(name=request.data['name'],
                                phone_number=request.data['phoneNo'],
                                note=request.data['note'])
                data.save()

                return JsonResponse({'status': True,'id':data.id, 'message': 'Information added successfully'}, status=200)
            
            except Exception as e:
                return JsonResponse({'message' : str(e),'status': False},status=200)
        
        else:
            try:
                data = Members.objects.filter(id=id).update(name=request.data['name'],
                                phone_number=request.data['phoneNo'],
                                note=request.data['note'])

                return JsonResponse({'status': True,'id':id, 'message': 'Information updated successfully'}, status=200)
            
            except Exception as e:
                return JsonResponse({'message' : str(e),'status': False},status=200)

    def get(self, request, id=0):
        """ Get Details
        """
        if id == 0:
            datas = Members.objects.all()
        else:
            datas = Members.objects.filter(id=id)
            
        result = []

        for data in datas:
            status = True
            if data.status == 0:
                status = False
            result .append({
                'id':data.id,
                'name':data.name,
                'phoneNo':data.phone_number,
                'note':data.note,
                'status':status
            })
        return JsonResponse(result, safe=False, status=200)

""" GroupMembers
"""
class AddGroupMemberView(views.APIView):
    def post(self, request, groupId = 0):
        try:
            if groupId == 0:
                return JsonResponse({'status': False,'message': 'Invalid Group Id'}, status=200)

            mem = json.loads(request.data['members'])

            for member in mem:
                memberId = member['memberId']
                groupMem = GroupMembers.objects.filter(group_id=Group.objects.get(id=groupId),
                            member_id=Members.objects.get(id=memberId))

                if not groupMem :
                    data = GroupMembers(group_id=Group.objects.get(id=groupId),
                            member_id=Members.objects.get(id=memberId))
                    data.save()

            return JsonResponse({'status': True,'message': 'Members added successfully'}, status=200)
        
        except Exception as e:
            return JsonResponse({'message' : str(e),'status': False},status=200)

    def get(self, request, id=0):
            """ Get Details
            """
            try:
                if id == 0:
                    return JsonResponse({'status': False, 'message':'Invalid Group'}, safe=False, status=200)
                
                group = group_id=Group.objects.filter(id=id).get()
                auctionMember = GroupAuction.objects.filter(group_id=group)

                members = []
                for auction in auctionMember:
                    members.append(str(auction.member_id.id))

                datas = GroupMembers.objects.filter(group_id=group).exclude(member_id=tuple(members))
                
                result = []

                for data in datas:
                    result .append({
                        'id':data.member_id.id,
                        'name':data.member_id.name,
                        'phoneNo':data.member_id.phone_number,
                        'note':data.member_id.note,
                    })
                return JsonResponse(result, safe=False, status=200)

            except Exception as e:
                return JsonResponse({'message' : str(e),'status': False},status=200)

""" Expense Category
"""
class ExpenseCategoryView(views.APIView):

    def post(self, request,id= 0):
        if id == 0:
            try:
                data = ExpenseCategory(name=request.data['name'],
                                remarks=request.data['remarks'])
                data.save()

                return JsonResponse({'status': True, 'message': 'Information added successfully'}, status=200)
            
            except Exception as e:
                return JsonResponse({'message' : str(e),'status': False},status=200)
        
        else:
            try:
                data = ExpenseCategory.objects.filter(id=id).update(name=request.data['name'],
                                remarks=request.data['remarks'])

                return JsonResponse({'status': True, 'message': 'Information updated successfully'}, status=200)
            
            except Exception as e:
                return JsonResponse({'message' : str(e),'status': False},status=200)

    def get(self, request, id=0):
        """ Get Details
        """
        if id == 0:
            datas = ExpenseCategory.objects.all()
        else:
            datas = ExpenseCategory.objects.filter(id=id)
            
        result = []

        for data in datas:
            status = True
            if data.status == 0:
                status = False
            result .append({
                'id':data.id,
                'name':data.name,
                'remarks':data.remarks,
                'status':status
            })
        return JsonResponse(result, safe=False, status=200)


""" Expense View
"""
class ExpenseView(views.APIView):

    def post(self, request):
        try:
            date = request.data['date']
            expenses = json.loads(request.data['expenses'])
            for expense in expenses:
                if expense['id'] == 0:

                    data = Expense(date=date,amount=expense['amount'],
                            category_id=ExpenseCategory.objects.get(id=expense['categoryId']))
                    data.save()
                else:
                    data = Expense.objects.filter(id=expense['id']).update(date=date,amount=expense['amount'],
                            category_id=ExpenseCategory.objects.get(id=expense['categoryId']))

            return JsonResponse({'message' : 'Expense updated successfully','status': True},status=200)

        except Exception as e:
            return JsonResponse({'message' : str(e),'status': False},status=200)


""" Show Expense
"""
class ShowExpenseView(views.APIView):

    def post(self, request):
        try:
            date = request.data['date']

            result = []

            datas = Expense.objects.filter(date=date)

            for data in datas:
                result.append({
                    'id':data.id,
                    'amount':data.amount,
                    'categoryId':data.category_id.id,
                    'categoryName':data.category_id.name,
                })

            return JsonResponse(result, safe=False, status=200)

        except Exception as e:
            return JsonResponse({'message' : str(e),'status': False},status=200)



class ActiveExpenseCategory(views.APIView):

    def get(self, request):
        """ Get Details
        """
        datas = ExpenseCategory.objects.filter(status=1)
            
        result = []

        for data in datas:
            result .append({
                'id':data.id,
                'name':data.name,
                'remarks':data.remarks,
            })
        return JsonResponse(result, safe=False, status=200)

class ActiveMember(views.APIView):

    def get(self, request):
        """ Get Details
        """
        datas = Members.objects.filter(status=1).order_by('name')
            
        result = []

        for data in datas:
            result .append({
                'id':data.id,
                'name':data.name,
                'phoneNo':data.phone_number,
                'note':data.note,
            })
        return JsonResponse(result, safe=False, status=200)

class ActiveGroup(views.APIView):
    def get(self, request):
        """ Get Details
        """
        datas = Group.objects.filter(status=1)
            
        result = []

        for data in datas:
            result .append({
                'id':data.id,
                'name':data.name,
                'typeId':data.type_id.id,
                'type':Type.objects.get(id=data.type_id).name,
                'chitId':data.chit_id.id,
                'chitAmount':Chit.objects.get(id=data.chit_id).amount,
                'startDate':data.startDate,
                'remarks':data.remarks,
            })
        return JsonResponse(result, safe=False, status=200)

class ActiveChitAmount(views.APIView):
    def get(self, request):
        """ Get Details
        """
        datas = Chit.objects.filter(status=1)
            
        result = []

        for data in datas:
            result .append({
                'id':data.id,
                'amount':data.amount,
                'remarks':data.remarks,
            })
        return JsonResponse(result, safe=False, status=200)

class ActiveChitType(views.APIView):
    def get(self, request):
        """ Get Details
        """
        datas = Type.objects.filter(status=1)
            
        result = []

        for typeData in datas:
            result .append({
                'id':typeData.id,
                'name':typeData.name,
            })
        return JsonResponse(result, safe=False, status=200)


class DeleteUser(views.APIView):
    def get(self, request, id = 0):
        """ Get Details
        """
        try:
            data = User.objects.filter(id=id).get()
            if data.is_active == 0:
                User.objects.filter(id=id).update(is_active=1)
            else:
                User.objects.filter(id=id).update(is_active=0)

            return JsonResponse({
                'status': True,
                'message':"Status Updated Successfully",
            }, safe=False, status=200)

        except Exception as e:
            return JsonResponse({
                'status': False,
                'message': e.data,
            }, safe=False, status=200)
 
class DeleteChitType(views.APIView):
    def get(self, request, id = 0):
        """ Get Details
        """
        try:
            data = Type.objects.filter(id=id).get()
            
            if data.status == 0:
                Type.objects.filter(id=id).update(status=1)
            else:
                Type.objects.filter(id=id).update(status=0)

            return JsonResponse({
                'status': True,
                'message':"Status Updated Successfully",
            }, safe=False, status=200)

        except Exception as e:
            return JsonResponse({
                'status': False,
                'message': e.data,
            }, safe=False, status=200)
   
class DeleteExpenseCategory(views.APIView):
    def get(self, request, id = 0):
        """ Get Details
        """
        try:
            data = ExpenseCategory.objects.filter(id=id).get()
            
            if data.status == 0:
                ExpenseCategory.objects.filter(id=id).update(status=1)
            else:
                ExpenseCategory.objects.filter(id=id).update(status=0)

            return JsonResponse({
                'status': True,
                'message':"Status Updated Successfully",
            }, safe=False, status=200)

        except Exception as e:
            return JsonResponse({
                'status': False,
                'message': e.data,
            }, safe=False, status=200)

class DeleteChitAmount(views.APIView):
    def get(self, request, id = 0):
        """ Get Details
        """
        try:
            data = Chit.objects.filter(id=id).get()
            
            if data.status == 0:
                Chit.objects.filter(id=id).update(status=1)
            else:
                Chit.objects.filter(id=id).update(status=0)

            return JsonResponse({
                'status': True,
                'message':"Status Updated Successfully",
            }, safe=False, status=200)

        except Exception as e:
            return JsonResponse({
                'status': False,
                'message': e.data,
            }, safe=False, status=200)

class DeleteChitMember(views.APIView):
    def get(self, request, id = 0):
        """ Get Details
        """
        try:
            data = Members.objects.filter(id=id).get()
            
            if data.status == 0:
                Members.objects.filter(id=id).update(status=1)
            else:
                Members.objects.filter(id=id).update(status=0)

            return JsonResponse({
                'status': True,
                'message':"Status Updated Successfully",
            }, safe=False, status=200)

        except Exception as e:
            return JsonResponse({
                'status': False,
                'message': e.data,
            }, safe=False, status=200)

class DeleteGroupMember(views.APIView):
    def get(self, request, id = 0):
        """ Get Details
        """
        try:
            data = GroupMembers.objects.filter(id=id).get()

            if not data:
                return JsonResponse({
                    'status': False,
                    'message':"Member not Found",
                }, safe=False, status=200)

            data.delete()
            
            return JsonResponse({
                'status': True,
                'message':"Member removed Successfully",
            }, safe=False, status=200)

        except Exception as e:
            return JsonResponse({
                'status': False,
                'message': e.data,
            }, safe=False, status=200)
    
""" Chit Auction 
"""
class AuctionView(views.APIView):
    def post(self, request):
        try:
            groupMembers = GroupMembers.objects.filter(group_id=Group.objects.filter(id=request.data['groupId']).get())

            if not groupMembers.count() < 20:
                return JsonResponse({'status': False, 'message': 'Insufficient Members in Group'}, status=200)

            data = GroupAuction(date=request.data['date'], 
                            group_id=Group.objects.filter(id=request.data['groupId']).get(),
                            member_id=Members.objects.filter(id=request.data['memberId']).get(),
                            auction_amount=request.data['auctionAmount'],
                            month=request.data['month'],
                            payable=request.data['payable'],
                            createdBy=User.objects.filter(id=request.data['createdBy']).get(),
                            remarks=request.data['remarks'])
            data.save()

            for member in groupMembers:
                payable = PayableAuction(auction_id=data,
                                    group_id=Group.objects.filter(id=request.data['groupId']).get(),
                                    member_id=member.member_id,
                                    total_payable=request.data['payable'],
                                    paid_amount=0,
                                    payment_status=0)
                payable.save()

            GroupAuction.objects.filter(id=data.id).update(status=1)

            return JsonResponse({'status': True, 'id': data.id, 'message': 'Information added successfully'}, status=200)
        
        except Exception as e:
            return JsonResponse({'message' : str(e),'status': False},status=200)


""" Chit Transaction 
"""
class TransactionView(views.APIView):
    def post(self, request,id = 0):
        if id == 0:
            try:
                payableData = PayableAuction.objects.filter(member_id=Members.objects.filter(id=request.data['memberId']).get()).exclude(total_payable=F('paid_amount'))

                if payableData.count() == 0:
                    return JsonResponse({'status': False, 'message': 'No Outstanding for Payment.'}, status=200)

                currentAmount = int(request.data['amount'])
                
                """ Inside For Loop -- Adding Transaction to PayableAuction
                """
                for payable in payableData:
                    payAmount = payable.total_payable - payable.paid_amount
                    paying = 0
                    if currentAmount == 0:
                        break
                    elif payAmount >= currentAmount:
                        paying = payable.paid_amount + currentAmount
                        currentAmount = 0
                    elif payAmount < currentAmount:
                        currentAmount = currentAmount - payAmount
                        paying = payable.paid_amount + payAmount

                    PayableAuction.objects.filter(id=payable.id).update(paid_amount=paying)

                data = Transaction(date=request.data['date'],
                                member_id=Members.objects.filter(id=request.data['memberId']).get(),
                                amount=request.data['amount'],
                                remarks=request.data['remarks'],
                                payment_mode=request.data['paymentMode'],
                                createdBy=User.objects.filter(id=request.data['createdBy']).get())
                data.save()
                
                return JsonResponse({'status': True,'id': data.id, 'message': 'Information added successfully'}, status=200)
            
            except Exception as e:
                return JsonResponse({'message' : str(e),'status': False},status=200)
        
        else:
            try:
                transData = Transaction.objects.filter(id=id).get()
                """ Checking Updation of Member
                """
                if transData.member_id.id != int(request.data['memberId']):
                    """ Checking Outstanding of New Member in PayableAuction
                    """
                    payableData = PayableAuction.objects.filter(member_id=Members.objects.filter(id=request.data['memberId']).get()).exclude(total_payable=F('paid_amount'))

                    if payableData.count() == 0:
                        return JsonResponse({'status': False, 'message': 'No Outstanding for Payment this Member.'}, status=200)

                    """ Making Zero of Previous Transaction in PayableAuction
                    """
                    prevPayData = PayableAuction.objects.filter(member_id=transData.member_id).order_by(Lower('id').desc())
                    currentAmount = int(request.data('amount'))
                    for payable in prevPayData:
                        payAmount = payable.paid_amount
                        paying = 0
                        if currentAmount == 0:
                            break
                        elif payAmount > currentAmount:
                            paying = payAmount - currentAmount
                            currentAmount = 0
                        elif payAmount <= currentAmount:
                            paying = 0
                            currentAmount = currentAmount - payAmount

                        PayableAuction.objects.filter(id=payable.id).update(paid_amount=paying)

                    """ Adding Transaction in Payable Auction
                    """
                    currentAmount = int(request.data['amount'])
                    for payable in payableData:
                        payAmount = payable.total_payable - payable.paid_amount
                        paying = 0
                        if currentAmount == 0:
                            break
                        elif payAmount >= currentAmount:
                            paying = payable.paid_amount + currentAmount
                            currentAmount = 0
                        elif payAmount < currentAmount:
                            currentAmount = currentAmount - payAmount
                            paying = payable.paid_amount + payAmount

                        PayableAuction.objects.filter(id=payable.id).update(paid_amount=paying)
                    
                elif int(request.data['amount']) != transData.amount:

                    currentAmount = int(request.data['amount'])
                    if transData.amount < currentAmount:
                        payableData = PayableAuction.objects.filter(member_id=Members.objects.filter(id=request.data['memberId']).get()).exclude(total_payable=F('paid_amount'))
                        for payable in payableData:
                            payAmount = payable.total_payable - payable.paid_amount
                            paying = 0
                            if currentAmount == 0:
                                break
                            elif payAmount >= currentAmount:
                                paying = payable.paid_amount + currentAmount
                                currentAmount = 0
                            elif payAmount < currentAmount:
                                currentAmount = currentAmount - payAmount
                                paying = payable.paid_amount + payAmount

                            PayableAuction.objects.filter(id=payable.id).update(paid_amount=paying)
                    
                    elif transData.amount > currentAmount:
                        currentAmount = transData.amount - currentAmount
                        prevPayData = PayableAuction.objects.filter(member_id=transData.member_id).order_by(Lower('id').desc())

                        for payable in prevPayData:
                            payAmount = payable.paid_amount
                            paying = 0
                            if currentAmount == 0:
                                break
                            elif payAmount > currentAmount:
                                paying = payAmount - currentAmount
                                currentAmount = 0
                            elif payAmount <= currentAmount:
                                paying = 0
                                currentAmount = currentAmount - payAmount

                            PayableAuction.objects.filter(id=payable.id).update(paid_amount=paying)

                data = Transaction.objects.filter(id=id).update(date=request.data['date'],
                                member_id=Members.objects.filter(id=request.data['memberId']).get(),
                                amount=request.data['amount'],
                                remarks=request.data['remarks'],
                                payment_mode=request.data['paymentMode'],
                                createdBy=User.objects.filter(id=request.data['createdBy']).get())

                return JsonResponse({'status': True,'id': id, 'message': 'Information updated successfully'}, status=200)
            
            except Exception as e:
                return JsonResponse({'message' : str(e),'status': False},status=200)

    def get(self, request, id=0):
        """ Get Details
        """
        try:
            if id == 0:
                datas = Transaction.objects.all()
            else:
                datas = Transaction.objects.filter(id=id)
                
            result = []

            for data in datas:
                result.append({
                    'id':data.id,
                    'date':data.date,
                    'memberId':data.member_id.id,
                    'memberName':data.member_id.name,
                    'amount':data.amount,
                    'paymentMode':data.payment_mode,
                    'remarks':data.remarks,
                    'createdBy':data.createdBy.name,
                })
            return JsonResponse(result, safe=False, status=200)
        except Exception as e:
                return JsonResponse({'message' : str(e),'status': False},status=200)

class GroupDataView(views.APIView):
    def get(self, request, id=0):
        try:
            group = Group.objects.filter(id=id).get()

            auction = []
            auctionData = GroupAuction.objects.filter(group_id=id)
            for data in auctionData:
                auction.append({
                    'id':data.id,
                    'date':data.date,
                    'auctionAmount':data.auction_amount,
                    'payable':data.payable,
                    'month':data.month,
                    'memberId':data.member_id.id,
                    'memberName':data.member_id.name,
                    'remarks':data.remarks
                })    

            # members = []
            # groupMem = GroupMembers.objects.filter(group_id=id)
            # for member in groupMem:
            #     members.append({
            #         'id':member.id,
            #         'memberId':member.member_id.id,
            #         'name':member.member_id.name,
            #         'phoneNo':member.member_id.phone_number
            #     })

            payableData = PayableAuction.objects.values('member_id').annotate(paidAmount=Sum('paid_amount'),totalPayable=Sum('total_payable')).filter(group_id=Group.objects.filter(id=id).get())
            due = []
            
            # return JsonResponse('result', safe=False, status=200)
            
            for data in payableData:
                due.append({
                    'memberId':data['member_id'],
                    'memberName':Members.objects.filter(id=data['member_id']).get().name,
                    'totalPayable':data['totalPayable'],
                    'paidAmount':data['paidAmount'],
                    'outstanding':data['totalPayable'] - data['paidAmount'],
                })

            result = {
                'id':group.id,
                'name':group.name,
                'startDate':group.start_date,
                'remarks':group.remarks,
                'chitId':group.chit_id.id,
                'chitName':group.chit_id.amount,
                'typeId':group.type_id.id,
                'typeName':group.type_id.name,
                'auction':auction,
                # 'members':members,
                'due':due
            }

            return JsonResponse(result, safe=False, status=200)
        
        except Exception as e:
            return JsonResponse({'message' : str(e),'status': False},status=200)

class TestAPI(views.APIView):
    def get(self,request):
        return JsonResponse({'code': request.GET['code']}, status=200)

class MemberDetailView(views.APIView):
    def get(self,request, id=0):
        try:
            member = GroupMembers.objects.filter(member_id=id)
            due = PayableAuction.objects.filter(member_id=id).aggregate(due=(Sum('total_payable')-Sum('paid_amount')))
            details = []
            for detail in member:
                paycount = GroupAuction.objects.filter(group_id=detail.group_id).count()
                details.append({
                    'group':detail.group_id.name,
                    'type':detail.group_id.type_id.name,
                    'color':detail.group_id.type_id.color,
                    'amount':detail.group_id.chit_id.amount,
                    'date':detail.group_id.start_date,
                    'months':paycount,
                })
            result = {
                'name':member[0].member_id.name,
                'groups':member.count(),
                'due':due['due'],
                'details':details,
            }
            return JsonResponse(result, safe=False, status=200)
        except Exception as e:
            return JsonResponse({'message' : str(e),'status': False},status=200)

class MemberTransactionView(views.APIView):
    def get(self,request, id=0):
        try:
            transactions = Transaction.objects.filter(member_id=id)
            transaction = []
            for detail in transactions:
                transaction.append({
                    'id':detail.id,
                    'date':detail.date,
                    'amount':detail.amount,
                    'payment_mode':detail.payment_mode,
                    'remarks':detail.remarks,
                })
            result = {
                'id':transactions[0].member_id.id,
                'name':transactions[0].member_id.name,
                'transactions':transaction,
            }
            return JsonResponse(result, safe=False, status=200)
        except Exception as e:
            return JsonResponse({'message' : str(e),'status': False},status=200)

class DailyIncomeView(views.APIView):
    def post(self, request):
        try:
            date = request.data['date']
            data = Transaction.objects.filter(date=date).aggregate(income=Sum('amount'))
            return JsonResponse(income['amount'], safe=False, status=200)

        except Exception as e:
            return JsonResponse({'message' : str(e),'status': False},status=200)