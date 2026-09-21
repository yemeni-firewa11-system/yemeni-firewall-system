import hashlib

# كلمة المرور الصحيحة مشفرة
correct_hash = "23d042d2c4fcc4b76e2d77558b7101f1581493cb33848aa2a60de13dbb562b25"
attempts = 0

while attempts < 3:
    pwd = input("دخل كلمة المرور: ")
    h = hashlib.sha256(pwd.encode()).hexdigest()
    if h == correct_hash:
        print("تم الدخول بنجاح! مرحبا بك يا خبير الحماية!")
        break
    else:
        attempts += 1
        print(f"غلط! باقي لك {3-attempts} محاولات")
        
if attempts == 3:
    print("تم قفل النظام! محاولات كثيرة - هذا هو الجدار الناري!")
