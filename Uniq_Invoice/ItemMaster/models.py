from django.db import models
from UniQInvoice.models import Company_Master ,Dealer_Master


# Create your models here.



class Warehouse_Master(models.Model):
    company_id = models.ForeignKey(Company_Master,on_delete=models.CASCADE,null=False)
    warehouse_name=models.CharField(max_length=250,null=False)
    warehouse_address=models.CharField(max_length=250,null=False)
    IsDeleted = models.IntegerField(null = False)
    IsActive = models.IntegerField(null = False)
    CreatedBy = models.CharField(max_length=250,null = False)
    CreatedDate = models.DateField(auto_now=False, auto_now_add=False,null = False)
    ModifiedBy = models.CharField(max_length=250,null = False)
    ModifiedDate = models.DateField(auto_now=False, auto_now_add=False,null = False)

   


class Item_Master(models.Model):
    company_id = models.ForeignKey(Company_Master,on_delete=models.CASCADE,null=False)
    warehouse_id = models.ForeignKey(Warehouse_Master,on_delete=models.CASCADE,null=False)
    item_name=models.CharField(max_length=250,null=False)
    vehicle_type=models.CharField(max_length=250,null=False)
    item_description=models.CharField(max_length=250,null=False)
    model_name=models.CharField(max_length=250,null=False)
    manufecture_date=models.DateField(auto_now=False, auto_now_add=False, null=False)
    receiving_data=models.DateField(auto_now=False, auto_now_add=False, null=False)
    DP_price=models.IntegerField(null=False)
    MRP=models.IntegerField(null=False)
    Battery_type=models.CharField(max_length=250)
    Ampear=models.CharField(max_length=250)
    Quantity=models.IntegerField(default=0)
    IsDeleted = models.IntegerField(null = False)
    IsActive = models.IntegerField(null = False)
    CreatedBy = models.CharField(max_length=250,null = False)
    CreatedDate = models.DateField(auto_now=False, auto_now_add=False,null = False)
    ModifiedBy = models.CharField(max_length=250,null = False)
    ModifiedDate = models.DateField(auto_now=False, auto_now_add=False,null = False)

   
   



class User_Master(models.Model):
    company_id = models.ForeignKey(Company_Master,on_delete=models.CASCADE,null=False) 
    First_name =models.CharField(max_length=250,null=False)
    Last_name =models.CharField(max_length=250,null=False)
    phone_number = models.CharField(max_length=250,null=False)
    email_address = models.CharField(unique=True,max_length=250,null=False)
    password = models.CharField(max_length=20,null=False)
    IsDeleted = models.IntegerField(null = False)
    IsActive = models.IntegerField(null = False)
    CreatedBy = models.CharField(max_length=250,null = False)
    CreatedDate = models.DateField(auto_now=False, auto_now_add=False,null = False)
    ModifiedBy = models.CharField(max_length=250,null = False)
    ModifiedDate = models.DateField(auto_now=False, auto_now_add=False,null = False)
   

   


class Stock(models.Model):
    Warehouse_id = models.ForeignKey(Warehouse_Master,on_delete=models.CASCADE,null=False)
    Item_id = models.ForeignKey(Item_Master,on_delete=models.CASCADE,null=False)
    Quantity=models.IntegerField(default=0)
    Arrving_Date=models.DateField(auto_now=False, auto_now_add=False, null=False)

   


class INVOICE_MASTER(models.Model):
    InvoiceNo =models.CharField(max_length=250, null = False)
    InvoiceDate = models.DateField(auto_now=False, auto_now_add=False, null = False)
    InvoiceDueDate = models.DateField(auto_now=False, auto_now_add=False, null = False)
    DealerId = models.ForeignKey(Dealer_Master, on_delete=models.CASCADE, null = False)
    TotalAmount = models.IntegerField(null = False)
    DueAmount=models.IntegerField(null = False,default=TotalAmount)
    TotalTax = models.CharField(max_length=50, null = False)
    CreatedBy = models.CharField(max_length=50, null = False)
    CreatedDate = models.DateField(auto_now=False, auto_now_add=False, null = False)
    ModifiedBy = models.CharField(max_length=50, null = False)
    ModifiedDate = models.DateField(auto_now=False, auto_now_add=False, null = False)
    
   
    
class INVOICE_DETAILS(models.Model):
    Invoiceid = models.ForeignKey(INVOICE_MASTER, on_delete=models.CASCADE, null = False)
    ItemId = models.ForeignKey(Item_Master, on_delete=models.CASCADE, null = False)
    Quantity = models.IntegerField(null = True)
    Rate = models.IntegerField(null=True)
    ItemServiceNo = models.IntegerField(null = True)

   


class PAYMENT_MASTER(models.Model):
    Invoice_Id=models.ForeignKey(INVOICE_MASTER, on_delete=models.CASCADE, null = False)
    Dealer_Id= models.ForeignKey(Dealer_Master, on_delete=models.CASCADE, null = False)
    Payment_Id=models.CharField(max_length=50, null = False)
    Amount=models.IntegerField(null = False)
    Payment_Date=models.DateField(auto_now=False, auto_now_add=False, null = False)
    


class PAYMENT_STATUS_MASTER(models.Model):
    Invoice_Id=models.ForeignKey(INVOICE_MASTER, on_delete=models.CASCADE, null = False)
    Status = models.CharField( max_length=200 ,default="PENDING")
    Total_Amount=models.IntegerField(null = False)
    Received_Amount=models.IntegerField(null = False)
    Full_Payment_Received_Date=models.DateField(auto_now=False, auto_now_add=False, null = False)

    
