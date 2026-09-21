import hashlib, datetime
correct_hash = "23d042d2c4fcc4b76e2d77558b7101f1581493cb33848aa2a60de13dbb562b25"
pwd = input("دخل كلمة المرور: ")
h = hashlib.sha256(pwd.encode()).hexdigest()
time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
if h == correct_hash:
    print("دخول ناجح")
    open("hack_log.txt","a",encoding="utf-8").write(f"[{time}] دخول ناجح\n")
else:
    print("فشل - تم تسجيل المحاولة!")
    open("hack_log.txt","a",encoding="utf-8").write(f"[{time}] فاشلة: {pwd}\n")
print("--- السجل ---")
print(open("hack_log.txt","r",encoding="utf-8").read())
