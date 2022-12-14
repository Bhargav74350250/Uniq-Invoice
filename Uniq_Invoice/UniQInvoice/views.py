from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from UniQInvoice.models import Company_Master, Dealer_Master, Login_Master
from django.contrib.auth import authenticate, login, logout
import datetime  
from django.contrib import messages
from django.conf import settings
from Uniq_Invoice.settings import EMAIL_HOST_USER
from django.core.mail import BadHeaderError, send_mail
from django.http import HttpResponse, HttpResponseRedirect
from django.core.mail import send_mass_mail   
import re 
import random
import string

# Create your views here.

def AdminCanWatch(request):
    
    allcompany = Company_Master.objects.all()
    
    print(type(allcompany[0].IsActive))
    
    return render(request,'admin.html',{'allcompany':allcompany})

def companyaccept(request, id):
    
    company = Company_Master.objects.get(id=id)
    
    loginPassword = ''.join((random.choice(string.ascii_letters + string.digits)) for x in range(8))
    
    text = f'your registration is accepted...\nthis is your credential\n\nUsername : {company.Email_Address}\nPassword : {loginPassword}'
    message1 = ('Uniq Invoice - Credential', text, EMAIL_HOST_USER, [company.Email_Address])
    
    
    
    
    message2 = ('UniqInvoice - Company Acceptance', f'you accepted registration of {company.Company_Name}', EMAIL_HOST_USER, ['hulkmarvadi@gmail.com'])

    send_mass_mail((message1, message2), fail_silently=False)
  
    loginmaster = Login_Master(Company_id_id=company.id,User_Name = company.Email_Address, Password=loginPassword)
    loginmaster.save()
    
    company.IsActive = '1'
    company.save()
    
    
    
    
    
    allcompany = Company_Master.objects.all()
    return render(request,'admin.html',{'allcompany':allcompany})
    
    

def companyreject(request,id): 
    
    deletecompany = Company_Master.objects.get(id=id)
    deletecompany.delete()
    
    allcompany = Company_Master.objects.all()
    return render(request,'admin.html',{'allcompany':allcompany})



def Company_register(request):
    if request.method == "POST":
        Company_Name=request.POST.get('Company_Name')
        Owner_Name=request.POST.get('Owner_Name')
        GST_Number=request.POST.get('GST_Number')
        Address=request.POST.get('Address')
        Email_Address=request.POST.get('Email_Address')
        Phone_Number = request.POST.get('Phone_Number')
        Office_Number=request.POST.get('Office_Number')
        Company_website=request.POST.get('Company_website')
        CreatedDate=datetime.date.today()
        ModifiedDate=datetime.date.today()
        
        if len(Company_website) == 0:
            Company_website = None
        
        
        if len(GST_Number)== 15:
            print("valid")
            pass
        else:
            print("invalid gst number")
            g_msg = "YOU HAVE TO ENTER 15 DIGIT"
            return render(request,"Company-signup.html",{'g_msg':g_msg})
        
        regex = r'\b[A-Za-z0-9._%+-]+@gmail.com\b'
    
        if(re.fullmatch(regex, Email_Address)):
            pass   
        else:
            print("invalid email")
            e_msg = "PLEASE ENTER VALID EMAIL"
            return render(request,"Company-signup.html",{'e_msg':e_msg})
    
    
       
    
        
        
        if Phone_Number.isdigit():
            if len(Phone_Number)== 10:
                print("valid")
                pass
        else:
            print("invalid")
            m_msg = "YOU SHOULD ENTER 10 DIGIT"
            return render(request,"Company-signup.html",{'m_msg':m_msg})
        CompanyMaster = Company_Master(Company_website=Company_website, Company_Name = Company_Name, Owner_name = Owner_Name,GST_Number = GST_Number,Address = Address,Email_Address=Email_Address,Phone_Number=Phone_Number,Office_Number =Office_Number,IsDeleted= '0',IsActive='0',CreatedBy='raj',CreatedDate=ModifiedDate,ModifiedBy='raj',ModifiedDate=ModifiedDate)
        CompanyMaster.save()
       
        # subject = 'Uniq Invoice'
        # message1 = 'Thank you for registration,We will provide you your credential in your registered mail, once admin approve your registration'
        # message2 = 'one more company avilable please accept or reject'
        # from_email = 'q5630025@gmail.com'
       
        # print("emailn sending")
        # send_mail(subject, message1, EMAIL_HOST_USER, [Email_Address])
        
        message1 = ('Uniq Invoice', 'Thank you for registration,We will provide you your credential in your registered mail, once admin approve your registration', EMAIL_HOST_USER, [Email_Address])
        message2 = ('Uniq Invoice', 'one more company avilable please accept or reject', EMAIL_HOST_USER, ['hulkmarvadi@gmail.com'])

        send_mass_mail((message1, message2), fail_silently=False)
        
        
        
        







        print("email sent")
    
        return render(request,'Company-signup.html',{'success_msg':"You're Successfully registered"})
        
    else: 
        return render(request,'Company-signup.html')
  



    
    
  
    
def Dashboard(request):
    try:
        user = request.session['email']
        uid = Login_Master.objects.get(User_Name=user)
        if uid is not None:
            lid = Login_Master.objects.get(id = request.session['id'])
            companyname = Company_Master.objects.get(id = lid.Company_id_id)
            return render(request, 'index.html',{'companyname':companyname,'user':user,'uid':uid})
        else:
            return redirect('/companylogin/')
    except:
        messages.error(request,'you have to login first')
        return redirect('/companylogin/')
        
def companylogin(request):
    if request.method == "POST":
        email = request.POST.get('email')
        passw = request.POST.get('password')
        try:
            uid = Login_Master.objects.get(User_Name=email)
            if email == uid.User_Name:
                if passw == uid.Password:
                    request.session['id'] = uid.id
                    request.session['email'] = uid.User_Name
                    return redirect('/dashboard/')
                else:
                    messages.error(request,'Invalid Password', extra_tags='loginpass')
                    return render(request,'Login.html')
            else:
                messages.error(request,'Invalid Email', extra_tags='logemail')
                return render(request, 'Login.html')
        except:
            messages.error(request,'invalid cradencial', extra_tags = 'log')
    else:
        messages.error(request, 'hiiiiiiiiiiiii')
    return render(request,"Login.html")




def company_logout(request):
    if 'id'  in request.session:

        logout(request)
        return render(request, 'Login.html')
    else:
        return render(request, 'Login.html')



    
    
def dealercanwatch(request):
    if 'id'  in request.session:
        lid = Login_Master.objects.get(id = request.session['id'])
        companyname = Company_Master.objects.get(id = lid.Company_id_id)
    
        alldealer = Dealer_Master.objects.filter(IsDeleted='0',IsDealer='1')
        
        # print(type(allcompany[0].IsActive))
        
        return render(request,'dealer_View.html',{'alldealer':alldealer,'companyname':companyname})
    else:
        return render(request, 'Login.html')



def add_Dealer_Master(request):
    

    if request.method == "POST":
        dealer_company_name=request.POST.get('dealer_company_name')
        dealre_name=request.POST.get('dealre_name')
        dealer_address=request.POST.get('dealer_address')
        gst_number=request.POST.get('gst_number')
        dealer_email_address=request.POST.get('dealer_email_address')
        dealer_phone_number=request.POST.get('dealer_phone_number')
        dealer_office_number=request.POST.get('dealer_office_number')
        CreatedDate=datetime.date.today()
        ModifiedDate=datetime.date.today()

        print(request.session['id'])
        L_id = Login_Master.objects.get(id=request.session['id'])
        
        cid = Company_Master.objects.get(id=L_id.Company_id_id)
        
        
        # if len(gst_number)== 15:
        #     print("valid")
        #     pass
        # else:
           
        #     # print("invalid",sel_dealer)
        #     g_msg = "YOU HAVE TO ENTER 15 DIGIT"
        #     return render(request, "Dealermaster.html", {'g_msg':g_msg})
        
        regex = r'\b[A-Za-z0-9._%+-]+@gmail.com\b'
    
        if(re.fullmatch(regex, dealer_email_address)):
            pass   
        else:
            sel_dealer= Dealer_Master.objects.get(id = id)
            print("invalid email")
            e_msg = "PLEASE ENTER VALID EMAIL"

            return render(request,"Dealermaster.html",{'e_msg':e_msg})
    
    
        # print("PLEASE ENTER UNIQ EMAIL")
        # e_msg = "PLEASE ENTER VALID EMAIL"
        # return redirect(request,"Dealermaster.html", {'e_msg':e_msg})
        # return render(request,"select_dealer.html",{'e_msg':e_msg})
    
        
        
        if dealer_phone_number.isdigit():
            if len(dealer_phone_number)== 10:
                print("valid")
                pass
        else:
            sel_dealer= Dealer_Master.objects.get(id = id)
            print("invalid")
            m_msg = "YOU SHOULD ENTER 10 DIGIT"
            # return redirect('/select_Dealer_Master/{{sel_dealer}}', {'m_msg':m_msg})
            return render(request,"Dealermaster.html",{'m_msg':m_msg})



        
        DealerMaster = Dealer_Master.objects.create(Company_id_id = cid.id, dealer_company_name = dealer_company_name,dealre_name = dealre_name,dealer_address = dealer_address,gst_number=gst_number,dealer_email_address=dealer_email_address,dealer_phone_number =dealer_phone_number,dealer_office_number=dealer_office_number,IsActive='1',IsDeleted='0',CreatedBy='raj',CreatedDate=ModifiedDate,ModifiedBy='raj',ModifiedDate=ModifiedDate ,IsDealer='True')
        alldealer = Dealer_Master.objects.filter(IsDeleted='0',IsDealer='1')
       
        return render(request,"dealer_view.html",{'alldealer':alldealer})
    else:
        return render(request,"Dealermaster.html")
        # pass
        
    return render(request,'company_dash.html')   

def customer_all(request):
    if 'id'  in request.session:
        lid = Login_Master.objects.get(id = request.session['id'])
        companyname = Company_Master.objects.get(id = lid.Company_id_id)
        customer = Dealer_Master.objects.filter(IsDeleted='0',IsDealer='0')
        return render(request,'customer_view.html',{'customer':customer,'companyname':companyname})
    else:
        return render(request, 'Login.html')


    
def Customer_Master(request):
    if request.method == "POST":
        customer_company_name=request.POST.get('company_name')
        customer_name=request.POST.get('dealre_name')
        customer_address=request.POST.get('address')
        customer_gst_number=request.POST.get('gst_number')
        customer_email_address=request.POST.get('email_address')
        customer_phone_number=request.POST.get('phone_number')
        customer_office_number=request.POST.get('office_number')
        CreatedDate=datetime.date.today()
        ModifiedDate=datetime.date.today()
        # print("customer_company_name",customer_company_name)
        print(request.session['id'])
        L_id = Login_Master.objects.get(id=request.session['id'])
        
        cid = Company_Master.objects.get(id=L_id.Company_id_id)
        
        
        # if len(customer_gst_number)== 15:
        #     print("valid")
        #     pass
        # else:
           
        #     # print("invalid",sel_dealer)
        #     g_msg = "YOU HAVE TO ENTER 15 DIGIT"
        #     return render(request, "customer.html", {'g_msg':g_msg})
        
        regex = r'\b[A-Za-z0-9._%+-]+@gmail.com\b'
    
        if(re.fullmatch(regex, customer_email_address)):
            pass   
        else:
            sel_dealer= Dealer_Master.objects.get(id = id)
            print("invalid email")
            e_msg = "PLEASE ENTER VALID EMAIL"

            return render(request,"customer.html",{'e_msg':e_msg})
    
    
        # print("PLEASE ENTER UNIQ EMAIL")
        # e_msg = "PLEASE ENTER VALID EMAIL"
        # return redirect(request,"Dealermaster.html", {'e_msg':e_msg})
        # return render(request,"select_dealer.html",{'e_msg':e_msg})
    
        
        
        if customer_phone_number.isdigit():
            if len(customer_phone_number)== 10:
                print("valid")
                pass
        else:
            sel_dealer= Dealer_Master.objects.get(id = id)
            print("invalid")
            m_msg = "YOU SHOULD ENTER 10 DIGIT"
            # return redirect('/select_Dealer_Master/{{sel_dealer}}', {'m_msg':m_msg})
            return render(request,"customer.html",{'m_msg':m_msg})



        
        DealerMaster = Dealer_Master.objects.create(Company_id_id = cid.id, dealer_company_name = customer_company_name,dealre_name = customer_name,dealer_address = customer_address,gst_number=customer_gst_number,dealer_email_address=customer_email_address,dealer_phone_number =customer_phone_number,dealer_office_number=customer_office_number,IsActive='1',IsDeleted='0',CreatedBy='raj',CreatedDate=ModifiedDate,ModifiedBy='raj',ModifiedDate=ModifiedDate ,IsDealer='False' )
        customer = Dealer_Master.objects.filter(IsDeleted='0',IsDealer='0')
       
        return render(request,"customer_view.html",{'customer':customer})
    else:
        lid = Login_Master.objects.get(id = request.session['id'])
        companyname = Company_Master.objects.get(id = lid.Company_id_id)
        return render(request,"customer.html",{'companyname':companyname})


def select_Customer_Master(request,pk):
    if request.method=="GET":
        sel_customer= Dealer_Master.objects.get(id = pk)

        
        return render (request,"customer_edit.html",{"sel_customer":sel_customer})
    elif request.method=="POST":
        
        customer_company_name=request.POST['company_name']
        customer_name=request.POST['customer_name']
        customer_address=request.POST['address']
        gst_number=request.POST['gst_number']
        customer_email_address=request.POST['email_address']
        customer_phone_number=request.POST['phone_number']
        customer_office_number=request.POST['office_number']
        sel_customer= Dealer_Master.objects.get(id = pk)


        # if len(gst_number)== 15:
        #     print("valid")
        #     pass
        # else:
        #     sel_dealer= Dealer_Master.objects.get(id = id)
        #     # print("invalid",sel_dealer)
        #     g_msg = "YOU HAVE TO ENTER 15 DIGIT"
        #     return render(request, "customer_edit.html", {'sel_dealer':sel_dealer,'g_msg':g_msg})
        
        regex = r'\b[A-Za-z0-9._%+-]+@gmail.com\b'
    
        if(re.fullmatch(regex, customer_email_address)):
            pass   
        else:
            sel_customer= Dealer_Master.objects.get(id = pk)
            print("invalid email")
            e_msg = "PLEASE ENTER VALID EMAIL"

            return render(request,"customer_edit.html",{'sel_customer':sel_customer,'e_msg':e_msg})
    
    
        # print("PLEASE ENTER UNIQ EMAIL")
        # e_msg = "PLEASE ENTER VALID EMAIL"
        # return redirect(request,"customer_edit.html", {'sel_dealer':sel_dealer,'e_msg':e_msg})
        # return render(request,"customer_edit.html",{'e_msg':e_msg})
    
        
        
        if customer_phone_number.isdigit():
            if len(customer_phone_number)== 10:
                print("valid")
                pass
        else:
            sel_customer= Dealer_Master.objects.get(id = pk)
            print("invalid")
            m_msg = "YOU SHOULD ENTER 10 DIGIT"
            # return redirect('/customer_edit_Master/{{sel_dealer}}', {'m_msg':m_msg})
            return render(request,"customer_edit.html",{'sel_customer':sel_customer,'m_msg':m_msg})

        sel_customer.dealer_company_name = customer_company_name
        sel_customer.dealre_name = customer_name
        sel_customer.dealer_address=customer_address
        sel_customer.gst_number=gst_number
        sel_customer.dealer_email_address=customer_email_address
        sel_customer.dealer_phone_number=customer_phone_number
        sel_customer.dealer_office_number=customer_office_number

        sel_customer.save()
        return redirect('/customer_all/')


def delete_Customer_Master(request,pk):
    del_dealer = Dealer_Master.objects.get(id=pk)
    del_dealer.IsDeleted=1
    del_dealer.save()
    customer = Dealer_Master.objects.filter(IsDeleted='0',IsDealer='0')
   
    return  redirect("/customer_all/",{'customer':customer})
    
    
def delete_Dealer_Master(request,id):
    del_dealer = Dealer_Master.objects.get(id=id)
    del_dealer.IsDeleted=1
    del_dealer.save()
    alldealer = Dealer_Master.objects.filter(IsDeleted='0',IsDealer='1')
    return  redirect("/dealercanwatch/",{'alldealer':alldealer})



def select_Dealer_Master(request,pk):
    if request.method=="GET":
        sel_dealer= Dealer_Master.objects.get(id = pk)

        
        return render (request,"select_dealer.html",{"sel_dealer":sel_dealer})
    elif request.method=="POST":
        
        dealer_company_name=request.POST['dealer_company_name']
        dealre_name=request.POST['dealre_name']
        dealer_address=request.POST['dealer_address']
        gst_number=request.POST['gst_number']
        dealer_email_address=request.POST['dealer_email_address']
        dealer_phone_number=request.POST['dealer_phone_number']
        dealer_office_number=request.POST['dealer_office_number']
        sel_dealer= Dealer_Master.objects.get(id = pk)


        # if len(gst_number)== 15:
        #     print("valid")
        #     pass
        # else:
        #     sel_dealer= Dealer_Master.objects.get(id = id)
        #     # print("invalid",sel_dealer)
        #     g_msg = "YOU HAVE TO ENTER 15 DIGIT"
        #     return render(request, "select_dealer.html", {'sel_dealer':sel_dealer,'g_msg':g_msg})
        
        regex = r'\b[A-Za-z0-9._%+-]+@gmail.com\b'
    
        if(re.fullmatch(regex, dealer_email_address)):
            pass   
        else:
            sel_dealer= Dealer_Master.objects.get(id = pk)
            print("invalid email")
            e_msg = "PLEASE ENTER VALID EMAIL"

            return render(request,"select_dealer.html",{'sel_dealer':sel_dealer,'e_msg':e_msg})
    
    
        # print("PLEASE ENTER UNIQ EMAIL")
        # e_msg = "PLEASE ENTER VALID EMAIL"
        # return redirect(request,"select_dealer.html", {'sel_dealer':sel_dealer,'e_msg':e_msg})
        # return render(request,"select_dealer.html",{'e_msg':e_msg})
    
        
        
        if dealer_phone_number.isdigit():
            if len(dealer_phone_number)== 10:
                print("valid")
                pass
        else:
            sel_dealer= Dealer_Master.objects.get(id = pk)
            print("invalid")
            m_msg = "YOU SHOULD ENTER 10 DIGIT"
            # return redirect('/select_Dealer_Master/{{sel_dealer}}', {'m_msg':m_msg})
            return render(request,"select_dealer.html",{'sel_dealer':sel_dealer,'m_msg':m_msg})





        
        sel_dealer.dealer_company_name = dealer_company_name
        sel_dealer.dealre_name = dealre_name
        sel_dealer.dealer_address=dealer_address
        sel_dealer.gst_number=gst_number
        sel_dealer.dealer_email_address=dealer_email_address
        sel_dealer.dealer_phone_number=dealer_phone_number
        sel_dealer.dealer_office_number=dealer_office_number

        sel_dealer.save()
        return redirect('/dealercanwatch/')


def view_profile(request):
    lid = Login_Master.objects.get(id = request.session['id'])
    # print('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&',lid)
    c_id = Company_Master.objects.get(id = lid.Company_id_id)
    # print("************************************************************************",c_id)
    
    return render (request,"company_profile.html",{"c_id":c_id})   
    

    



def select_profile(request):
    if request.method=="GET":
        lid = Login_Master.objects.get(id = request.session['id'])
        # print('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&',lid)
        c_id = Company_Master.objects.get(id = lid.Company_id_id)
        # print("************************************************************************",c_id)
        
        return render (request,"select_profile.html",{"c_id":c_id})
    elif request.method=="POST":
        Company_Name=request.POST['Company_Name']
        GST_Number=request.POST['GST_Number']
        Address=request.POST['Address']
        Email_Address=request.POST['Email_Address']
        Phone_Number=request.POST['Phone_Number']
        Office_Number=request.POST['Office_Number']
        Owner_name=request.POST['Owner_name']
        Company_website=request.POST['Company_website']
        
        
        
        if len(Company_website) == 0:
            Company_website = None
        
        
        if len(GST_Number)== 15:
            print("valid")
            pass
        else:
            print("invalid gst number")
            g_msg = "YOU HAVE TO ENTER 15 DIGIT"
            return redirect('/select_profile/',{'g_msg':g_msg})
        
        regex = r'\b[A-Za-z0-9._%+-]+@gmail.com\b'
    
        if(re.fullmatch(regex, Email_Address)):
            pass   
        else:
            print("invalid email")
            e_msg = "PLEASE ENTER VALID EMAIL"
            return redirect("/select_profile/",{'e_msg':e_msg})
    
    
       
    
        
        
        if Phone_Number.isdigit():
            if len(Phone_Number)== 10:
                print("valid")
                pass
        else:
            print("invalid")
            m_msg = "YOU SHOULD ENTER 10 DIGIT"
            return redirect("/select_profile/",{'m_msg':m_msg})
        
        
        lid = Login_Master.objects.get(id = request.session['id'])
        c_id = Company_Master.objects.get(id = lid.Company_id_id)
        
        c_id.Company_Name = Company_Name
        c_id.GST_Number = GST_Number
        c_id.Address=Address
        c_id.Email_Address=Email_Address
        c_id.Phone_Number=Phone_Number
        c_id.Office_Number=Office_Number
        c_id.Owner_name=Owner_name
        c_id.Company_website=Company_website
        

        c_id.save()
        
        return redirect('/view_profile/')
    

def base( request):
    return render (request,"base.html")
    