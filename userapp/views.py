from django.shortcuts import render, redirect
from userapp.models import *
from django.contrib import messages
import urllib.request
import urllib.parse
import random 
import time
from adminapp.models import *
import pickle
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.svm  import SVC
from sklearn.metrics import accuracy_score,f1_score, recall_score, precision_score, auc, roc_auc_score, roc_curve
import ssl
from django.core.mail import send_mail
from django.conf import settings




#Create your views here.

# SMS send
def sendSMS(user, otp, mobile):
    data = urllib.parse.urlencode({
        'username': 'Codebook',
        'apikey': '56dbbdc9cea86b276f6c',
        'mobile': mobile,
        'message': f'Hello {user}, your OTP for account activation is {otp}. This message is generated from https://www.codebook.in server. Thank you',
        'senderid': 'CODEBK'
    })
    data = data.encode('utf-8')
    # Disable SSL certificate verification
    context = ssl._create_unverified_context()
    request = urllib.request.Request("https://smslogin.co/v3/api.php?")
    f = urllib.request.urlopen(request, data,context=context)
    return f.read()



# User Register details
def register(req):
    if req.method == 'POST' :
        name = req.POST.get('myName')
        age = req.POST.get('myAge')
        password = req.POST.get('myPwd')
        phone = req.POST.get('myPhone')
        email = req.POST.get('myEmail')
        address = req.POST.get("address")
        image = req.FILES['image']
        number = random.randint(1000,9999)
        
        print(number)
        try:
            user_data = User_details.objects.get(Email = email)
            messages.warning(req, 'Email was already registered, choose another email..!')
            return redirect("register")
        except:
            sendSMS(name,number,phone)
            User_details.objects.create(Full_name = name, Image = image, Age = age, Password = password, Address = address, Email = email, Phone_Number = phone, Otp_Num = number)
            mail_message = f'Registration Successfully\n Your 4 digit Pin is below\n {number}'
            print(mail_message)
            send_mail("Student Password", mail_message , settings.EMAIL_HOST_USER, [email])
            req.session['Email'] = email
            messages.success(req, 'Your account was created..')
            return redirect('otpverify')
    return render(req, 'user/user-register.html')

# User Login 
def login(req):
    if req.method == 'POST':
        user_email = req.POST.get('uemail')
        user_password = req.POST.get('upwd')
        print( user_email,user_password)
        
        # try:
        user_data = User_details.objects.get(Email = user_email)
        print(user_data)
        if user_data.Password == user_password:
            if user_data.Otp_Status == 'verified' and user_data.User_Status=='accepted':
                req.session['User_id'] = user_data.User_id
                messages.success(req, 'You are logged in..')
                user_data.No_Of_Times_Login += 1
                user_data.save()
                return redirect('userdashboard')
            elif user_data.Otp_Status == 'verified' and user_data.User_Status=='pending':
                messages.info(req, 'Your Status is in pending')
                return redirect('login')
            else:
                messages.warning(req, 'verifyOTP...!')
                req.session['Email'] = user_data.Email
                return redirect('otpverify')
        else:
            messages.error(req, 'incorrect credentials...!')
            return redirect('login')
    return render(req, 'main/main-user.html')



# OTP Verification 
def otpverify(req):
    user_id = req.session['Email']
    user_o = User_details.objects.get(Email = user_id)
    print(user_o.Otp_Num,'data otp')
    if req.method == 'POST':
        user_otp = req.POST.get('otp')
        u_otp = int(user_otp)
        if u_otp == user_o.Otp_Num:
            user_o.Otp_Status = 'verified'
            user_o.save()
            messages.success(req, 'OTP verification was Success. Now you can continue to login..!')
            return redirect('home')
        else:
            messages.error(req, 'OTP verification was Faild. You entered invalid OTP..!')
            return redirect('otpverify')
    return render(req, 'user/user-otpverify.html')

# user-dashboard Function
def userdashboard(req):
    prediction_count =  User_details.objects.all().count()
    user_id = req.session["User_id"]
    user = User_details.objects.get(User_id = user_id)
    return render(req, 'user/user-dashboard.html', {'predictions' : prediction_count, 'la' : user})


# user-profile Function
def profile(req):
    user_id = req.session["User_id"]
    user = User_details.objects.get(User_id = user_id)
    if req.method == 'POST':
        user_name = req.POST.get('userName')
        user_age = req.POST.get('userAge')
        user_phone = req.POST.get('userPhNum')
        user_email = req.POST.get('userEmail')
        user_address = req.POST.get("userAddress")
        # user_img = request.POST.get("userimg")

        user.Full_name = user_name
        user.Age = user_age
        user.Address = user_address
        user.Phone_Number = user_phone
        user.Email=user_email
       

        if len(req.FILES) != 0:
            image = req.FILES['profilepic']
            user.Image = image
            user.Full_name = user_name
            user.Age = user_age
            user.Address = user_address
            user.Phone_Number = user_phone
            user.Email=user_email
            user.Address=user_address
            
            user.save()
            messages.success(req, 'Updated SUccessfully...!')
        else:
            user.Full_name = user_name
            user.Age = user_age
            user.save()
            messages.success(req, 'Updated SUccessfully...!')
            
    context = {"i":user}
    return render(req, 'user/user-profile.html',context)

from sklearn.ensemble import RandomForestClassifier
# predictdiabetes form Function
def predict(req):
    if req.method == 'POST':
        age = req.POST.get('field1')
        sex = req.POST.get('sex')
        plasma_CA19_9 = req.POST.get('field2')
        creatinine = req.POST.get('field7')
        lyve1 = req.POST.get('field3')
        regb1 = req.POST.get('field8')
        tff1 = req.POST.get('field4')
        age = int(age)
        if sex == 0:
            gender = "male"
        else:
            gender = "female"
        context = {'gender': gender}
        
        plasma_CA19_9 = float(plasma_CA19_9)
        creatinine = float(creatinine)
        lyve1 = float(lyve1)
        tff1=float(tff1)
            
        # print(type(age),x)
        # DATASET.objects.create(Age = age, Glucose = sex, BloodPressure = plasma_CA19_9, SkinThickness = creatinine, Insulin = lyve1, BMI = regb1, DiabetesPedigreeFunction = tff1)
        import pickle
        file_path = 'rfc_pancrease.pkl'  # Path to the saved model file

        with open(file_path, 'rb') as file:
            loaded_model = pickle.load(file)
            res =loaded_model.predict([[age,sex,plasma_CA19_9,creatinine,lyve1,regb1,tff1]])
            # res=loaded_model.predict([[25,1,50.125,12.0255,0.15,99.255,45.325]])

            dataset = Upload_dataset_model.objects.last()
            # print(dataset.Dataset)
            df=pd.read_csv(dataset.Dataset.path)
            # df['diagnosis']= df.diagnosis == 3

            # df.sex = df.sex.map({'M': 1, 'F': 0})

            # df.drop(['sample_id', 'patient_cohort', 'sample_origin',"REG1A","benign_sample_diagnosis",'stage'],axis=1,inplace=True)
            # df['plasma_CA19_9']=df['plasma_CA19_9'].fillna(df['plasma_CA19_9'].mean())

            X = df.drop('diagnosis', axis = 1)
            y = df['diagnosis']
            import imblearn
            from imblearn.over_sampling import SMOTE
            ros = SMOTE()  # You need to add parentheses to create an instance
            X_oversample, y_oversample = ros.fit_resample(X, y)
            print(X_oversample.shape)
            print(y_oversample.shape)

            from sklearn.model_selection import train_test_split
            X_train,X_test,y_train,y_test = train_test_split(X_oversample,y_oversample,random_state=1,test_size=0.2)


            from sklearn.ensemble import RandomForestClassifier
            XGB = RandomForestClassifier()
            XGB.fit(X_train, y_train)

            # prediction
            train_prediction= XGB.predict(X_train)
            test_prediction= XGB.predict(X_test)
            print('*'*20)

            # evaluation
            from sklearn.metrics import accuracy_score
            accuracy = round(accuracy_score(y_test,test_prediction)*100, 2)
            precession = round(precision_score(test_prediction,y_test,average = 'macro')*100, 2)
            recall = round(recall_score(test_prediction,y_test,average = 'macro')*100, 2)
            f1_score = round(recall_score(test_prediction,y_test,average = 'macro')*100, 2)
            print(precession, accuracy,recall, f1_score,'uuuuuuuuuuuuuuuuuuuuuuuuuuu')
            x=0
            if res == 0:
                x = 0
                messages.success(req,"Cancer Is Not Detected")
            else:
                x=1
                messages.warning(req,"Cancer Is Detected")
            print(x)
            context = {'accc': accuracy,'pre': precession,'f1':f1_score,'call':recall,'res':x}
            print(type(res), 'ttttttttttttttttttttttttt')
            print(res)
            
            return render(req, 'user/user-result.html',context)
    return render(req, 'user/user-predict.html')


# Result function
def result(req):
    return render(req, 'user/user-result.html')

# User Logout
def userlogout(req):
    user_id = req.session["User_id"]
    user = User_details.objects.get(User_id = user_id) 
    t = time.localtime()
    user.Last_Login_Time = t
    current_time = time.strftime('%H:%M:%S', t)
    user.Last_Login_Time = current_time
    current_date = time.strftime('%Y-%m-%d')
    user.Last_Login_Date = current_date
    user.save()
    messages.info(req, 'You are logged out..')
    # print(user.Last_Login_Time)
    # print(user.Last_Login_Date)
    return redirect('login')
