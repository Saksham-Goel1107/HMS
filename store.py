import mysql.connector as stor
import datetime
connect=stor.connect(user="root",host="localhost",passwd="123456",database="HospitalManagement")
mycur=connect.cursor()
print("\t\t\t\t\t\t\t\t****Welcone To HMS****\n\n")
uid=0
money=0

def info():                                                                                         #INFO
    global uid
    print("\t\t\t\t\t\t\t\t****Login Details****\n\n")
    a=0
    ch=input("Do you already have an account(yes/no)?:")
    if ch.lower()=="yes":
        ch=int(input("\nEnter your id:"))
        mycur.execute("SELECT pid FROM pinfo")
        data=mycur.fetchall()
        for i in data:
            if ch == i[0]:
                print(f"\nyou have successfully accessed your account id:{ch}\n")
                uid=ch
                a=1
        if a==0:
            print("\nEnter correct id\n")
            info()
        
    elif ch.lower()=="no":                                                                                     
        print("\t\t\t\t\t\t\t\t****Welcome to Personal Details section****\n\n")
        uid=int(input("enter your id:"))                                                                                                      #userinfo
        name=input("enter your name:")
        dob=input("enter your dob(yyyy-mm-dd):")
        gender=input("enter your gender:")
        phno=int(input("enter your Phone number:"))
        address=input("enter your address:")
        email=input("enter your email:")
        pincode=int(input("enter your Pin Code:"))
        mycur.execute("insert into pinfo values({},'{}','{}','{}',{},'{}',{},'{}')".format(uid,name,dob,gender,phno,address,pincode,email))
        connect.commit()
        print("\nYour account has been successfully added!\n")
    else:
        print("Enter correct choice:\n")
        info()

hour=int(datetime.datetime.now().hour)
if hour>=0 and hour<=12:
    time="Morning"
elif hour>12 and hour<18:
    time="evening"
else:
    time="night"
now = datetime.datetime.now()
day_name = now.strftime("%A")

def doctor():                                                                                                # CONSULTING
    result=0
    global money    
    
    print("\t\t\t\t\t\t\t\t****Welcome to Doctor Consultancy****\n\n")
    if time=="night":
        print("Sorry,currently no doctors are available!\n")
        main()
    print("1. online consulting\n2. offline consulting\n3. Exit\n")
    ch=int(input("Enter your choice(1/2/3):"))
    if ch==1:
        print("\ncurrently available doctors are:\n\n(doctorid, name, specialization, shift, fees)\n")
        query = "SELECT * FROM onlinedoc WHERE shift = %s"
        mycur.execute(query, (time,))
        data=mycur.fetchall()
        for i in data:
            print("\n")
            print(i)
        ch= int(input("\nEnter the doctor_id you want to consult:"))
        query = "SELECT doctor_id FROM onlinedoc WHERE shift = %s"
        mycur.execute(query, (time,))
        data=mycur.fetchall()
        for i in data:
            if ch == i[0]:
                query = "SELECT fees FROM onlinedoc WHERE doctor_id = %s"
                mycur.execute(query, (ch,))
                result = mycur.fetchone()
                
            
        if result:
            print(f"The consultation fees for doctor {ch} is ₹{result[0]}")
            money=result[0]
            result=1
        else:
            print(f"Doctor with ID {ch} not found.\n")
            doctor()

    elif ch==2:
        print("\ncurrently available doctors are:\n\n(doctor_id, name, specialization, shift, fees)\n")
        query = "SELECT * FROM offlinedoc WHERE shift = %s"
        mycur.execute(query, (time,))
        data=mycur.fetchall()
        for i in data:
            print("\n")
            print(i)
        ch= int(input("\nEnter the doctor_id you want to consult:"))
        query = "SELECT doctor_id FROM offlinedoc WHERE shift = %s"
        mycur.execute(query, (time,))
        data=mycur.fetchall()
        for i in data:
            if ch == i[0]:
                query = "SELECT fees FROM offlinedoc WHERE doctor_id = %s"
                mycur.execute(query, (ch,))
                result = mycur.fetchone()
        if result:
            print(f"The consultation fees for doctor {ch} is ₹{result[0]}")
            money=result[0]
            result=1
        else:
            print(f"Doctor with ID {ch} not found.")
            doctor()
    elif ch==3:
        print("\nExiting Doctor Consultancy\n")
        main()
    else:
        print("Please choose one out of above two options!")
        doctor()
    if result==1:
        ch=input("\nDo you want to Book an appointment(yes/no)?:")
        if ch.lower()=="yes":
            print("Select the payment mode:\n1. Credit card\n2. Debit Card\n3. Net banking")
            py= int(input("Select one option(1/2/3):"))
            print("\nPayment Done!")
            print("Your booking is done!\n")
            mycur.execute("INSERT INTO history VALUES (%s,'Doctor consultation', %s,%s)",(uid,day_name,money))
            connect.commit()
        
        else:
            print("Thank You for contacting!\n")
            main()

def services():                                                                                         #SERVICES
    result=0
    global money
    print("\t\t\t\t\t\t\t\t****Welcome to Tests section****\n\n")
    print("Services Provided:\n1. Home service\n2. Self visit at centre\n3. Exit\n")
    ch= int(input("Select the service you want to avail(1/2/3):"))
    if ch==1:
        print("\ncurrently available tests are:\n\n(service_id, test name, fees)\n")
        mycur.execute("select * from hs")
        data=mycur.fetchall()
        for i in data:
            print("\n")
            print(i)
        ch= int(input("\nEnter the test_id you want:"))
        query = "SELECT test_fees FROM hs WHERE service_id = %s"
        mycur.execute(query, (ch,))
        ifresult = mycur.fetchone()

        if ifresult:
            print(f"The test fees for service {ch} is ₹{ifresult[0]}")
            money=ifresult[0]
            result=1
        else:
            print(f"\nTest with ID {ch} not found.\n")
            services()
        
    elif ch==2:
        if time=="night":
            print("\nSorry,currently no Self service Test are available!\n")
            main()
        print("\ncurrently available tests are:\n\n(service_id, test name, shift, fees)\n")
        query = "SELECT * FROM ss WHERE shift = %s"
        mycur.execute(query, (time,))
        data=mycur.fetchall()
        for i in data:
            print("\n")
            print(i)
        ch= int(input("\nEnter the test_id you want:"))
        query = "SELECT service_id FROM ss WHERE shift = %s"
        mycur.execute(query, (time,))
        data=mycur.fetchall()
        for i in data:
            if ch== i[0]:
                query = "SELECT test_fees FROM ss WHERE service_id = %s"
                mycur.execute(query, (ch,))
                result = mycur.fetchone()
            
        if result:
            print(f"The test fees for service {ch} is ₹{result[0]}")
            money=result[0]
            result=1
        else:
            print(f"Test with ID {ch} not found.")
            services()
    elif ch==3:
        print("Exiting services!\n")
        main()
    else:
        print("Please choose one out of above three options!")
        doctor()
    if result==1:
        ch=input("\nDo you want to Book an Test(yes/no)?:")
        if ch.lower()=="yes":
            print("Select the payment mode:\n1. Credit card\n2. Debit Card\n3. Net banking")
            py= int(input("Select one option(1/2/3):"))
            print("\nPayment Done!")
            print("Your booking is done!\n")
            mycur.execute("INSERT INTO history VALUES (%s,'Test booking', %s,%s)",(uid,day_name,money))
            connect.commit()
        
        else:
            print("Thank You for contacting!\n")
            main()

def blood():                                                                                                  #blood related
    a=0
    print("\t\t\t\t\t\t\t\t****Welcome to Blood Bank****\n\n")
    print("Select one of the following:\n1. Donate blood\n2. Blood Bank\n3. Blood group info with contact details\n4. Exit")
    ch=int(input("\nEnter your choice(1/2/3/4):"))
    if ch==1:
        na = input("Enter your name:")
        ph = int(input("Enter your phone number:"))
        bl = input("Enter your Blood Group:")
        av = input("When are you available to donate?(Morning/Afternoon/Evening):")
        mycur.execute("INSERT INTO blood (name, phone_number, blood_group, availability) VALUES (%s, %s, %s, %s)",(na, ph, bl, av))
        connect.commit()
        print("\nThank you for donating!\n")
    elif ch==2:
        ch=input("Enter the blood group requirement(A+/AB+...):")
        mycur.execute("SELECT blood_group FROM bb")
        data=mycur.fetchall()
        for i in data:
            
            if ch == i[0]:
                query = "SELECT units FROM bb WHERE blood_group= %s"
                mycur.execute(query, (ch,))
                result = mycur.fetchone()
                resulti=int(result[0])
                print(f"\navailable:\n{resulti} units\n")
                a=1
        if a==0:
            print(f"\nsorry {ch} is not available\n")
    elif ch==3:
        ch=input("Enter the blood group requirement(A+/AB+...):")
        mycur.execute("SELECT blood_group FROM blood")
        data=mycur.fetchall()
        for i in data:
            
            if ch == i[0]:
                
                query = "SELECT * FROM blood WHERE blood_group= %s"
                mycur.execute(query, (ch,))
                result = mycur.fetchall()
        print(" blood_id, name, phone_number, blood_group, availability")
        print("\n",result,"\n")
    elif ch==4:
        print("\nExiting Blood related services\n ")
        main()
    else:
        print("\nEnter the correct choice!\n")
        blood()

def uinfo():                                                                                        #User info
    query = "SELECT * FROM pinfo WHERE pid = %s"
    mycur.execute(query, (uid,))
    data=mycur.fetchall()
    print("\n",data,"\n")

def history():                                                                                      #User history
    print("\t\t\t\t\t\t\t\t****Welcome to History Section****\n\n")
    query = "SELECT * FROM history WHERE pid = %s"
    mycur.execute(query, (uid,))
    data=mycur.fetchall()
    print("pid, service_availed, day, fees")
    print(data,"\n")
    
def main():                                                                                              # STARTING
    while True:                                                                                             
        print("Please select the service you want to avail:\n1. Doctor Consultation\n2. Tests\n3. Blood related\n4. Your profile\n5. History\n6. To Exit")
        ch=int(input("Enter your choice(1/2/3/4/5/6):"))
        
            
        if ch==1:
            print()
            doctor()
            
        elif ch==2:
            print()
            services()
        
        elif ch==3:
            print()
            blood()

        elif ch==4:
            uinfo()
        
        elif ch==5:
            history()
            
        elif ch==6:
            print("Thank You For contacting us!")
            exit()
        else:
            print("Enter correct choice!")

info()
main()




