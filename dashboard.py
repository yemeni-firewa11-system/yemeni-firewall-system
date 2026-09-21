import http.server, hashlib, datetime, urllib.parse

correct_hash = "23d042d2c4fcc4b76e2d77558b7101f1581493cb33848aa2a60de13dbb562b25"
fails = {}

HTML_LOGIN = """
<!DOCTYPE html><html dir="rtl"><head><meta charset="utf-8"><title>دخول</title>
<style>body{text-align:center;font-family:sans-serif;margin-top:50px;background:#f5f5f5}
.box{background:white;padding:30px;border-radius:15px;width:300px;margin:auto;box-shadow:0 0 10px #ccc}
input{padding:10px;width:90%;margin:10px}button{padding:10px 20px;background:#2196F3;color:white;border:none;border-radius:5px}</style>
</head><body><div class="box"><h2>🔐 نظام الحماية اليمني</h2>
<form method="POST"><input type="password" name="password" placeholder="كلمة المرور"><br>
<button type="submit">دخول</button></form><p style="font-size:12px;color:gray">جرب: 123456</p>
<a href="/logs">📊 سجل الهجمات</a></div></body></html>
"""

def logs_page():
    try:
        logs = open("hack_log.txt","r",encoding="utf-8").read().splitlines()
    except:
        logs = ["لا يوجد سجلات بعد"]
    rows=""
    for line in reversed(logs[-50:]): # اخر 50
        color = "#e8f5e9" if "ناجح" in line else "#ffebee"
        icon = "✅" if "ناجح" in line else "❌"
        rows+=f"<tr style='background:{color}'><td>{icon}</td><td>{line}</td></tr>"
    return f"""
    <html dir="rtl"><head><meta charset="utf-8"><title>سجل الهجمات</title>
    <style>body{{font-family:sans-serif;background:#f5f5f5;text-align:center}}
    table{{width:90%;margin:20px auto;background:white;border-collapse:collapse;box-shadow:0 0 10px #ccc}}
    td{{padding:10px;border:1px solid #ddd;text-align:right}}th{{background:#333;color:white;padding:10px}}</style>
    </head><body><h1>📊 لوحة مراقبة الهجمات</h1>
    <a href="/">رجوع للدخول</a> | <a href="/hack_log.txt">الملف الخام</a>
    <table><tr><th>حالة</th><th>التفاصيل</th></tr>{rows}</table></body></html>
    """

class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/logs" or self.path == "/hack_log.txt":
            if self.path == "/hack_log.txt":
                self.send_response(200); self.send_header('Content-type','text/plain; charset=utf-8'); self.end_headers()
                try: self.wfile.write(open("hack_log.txt","rb").read())
                except: self.wfile.write("لا يوجد سجل".encode('utf-8'))
                return
            self.send_response(200); self.send_header('Content-type','text/html; charset=utf-8'); self.end_headers()
            self.wfile.write(logs_page().encode('utf-8'))
        else:
            self.send_response(200); self.send_header('Content-type','text/html; charset=utf-8'); self.end_headers()
            self.wfile.write(HTML_LOGIN.encode('utf-8'))

    def do_POST(self):
        length = int(self.headers.get('content-length',0))
        pwd = urllib.parse.parse_qs(self.rfile.read(length).decode()).get('password',[''])[0]
        h = hashlib.sha256(pwd.encode()).hexdigest()
        time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ip = self.client_address[0]

        if h == correct_hash:
            msg = "✅ دخول ناجح! أهلا بالخبير!"
            fails[ip]=0
            open("hack_log.txt","a",encoding="utf-8").write(f"[{time}] {ip} ناجح\n")
        else:
            fails[ip]=fails.get(ip,0)+1
            if fails[ip] >= 3:
                msg = f"🚫 تم حظرك! الجدار الناري اشتغل"
            else:
                msg = f"❌ فاشلة! محاولة {fails[ip]}/3"
            open("hack_log.txt","a",encoding="utf-8").write(f"[{time}] {ip} فاشلة: {pwd} ({fails[ip]}/3)\n")

        self.send_response(200); self.send_header('Content-type','text/html; charset=utf-8'); self.end_headers()
        self.wfile.write(f"<html dir='rtl'><body style='text-align:center;font-family:sans-serif;margin-top:50px'><h1>{msg}</h1><a href='/'>رجوع</a> | <a href='/logs'>شوف اللوحة</a></body></html>".encode('utf-8'))

print("🚀 السيرفر الاحترافي شغال: http://localhost:8000")
print("📊 اللوحة: http://localhost:8000/logs")
http.server.HTTPServer(("",8000), Handler).serve_forever()
