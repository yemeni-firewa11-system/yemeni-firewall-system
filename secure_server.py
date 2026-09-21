import http.server, hashlib, datetime, urllib.parse, os

correct_hash = "23d042d2c4fcc4b76e2d77558b7101f1581493cb33848aa2a60de13dbb562b25"
fails = {}

class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/" or self.path == "/login.html":
            self.path = "/login.html"
        try:
            f = open("."+self.path, "rb")
            self.send_response(200)
            if self.path.endswith(".html"):
                self.send_header('Content-type','text/html; charset=utf-8')
            else:
                self.send_header('Content-type','text/plain; charset=utf-8')
            self.end_headers()
            self.wfile.write(f.read())
            f.close()
        except:
            self.send_response(404)
            self.end_headers()
            self.wfile.write("الصفحة غير موجودة".encode('utf-8'))

    def do_POST(self):
        length = int(self.headers.get('content-length',0))
        data = self.rfile.read(length).decode()
        pwd = urllib.parse.parse_qs(data).get('password',[''])[0]
        h = hashlib.sha256(pwd.encode()).hexdigest()
        time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ip = self.client_address[0]

        if h == correct_hash:
            msg = "✅ دخول ناجح! أهلا بالخبير اليمني!"
            fails[ip]=0
            open("hack_log.txt","a",encoding="utf-8").write(f"[{time}] {ip} ناجح\n")
        else:
            fails[ip]=fails.get(ip,0)+1
            if fails[ip] >= 3:
                msg = f"🚫 تم حظرك يا {ip}! الجدار الناري اشتغل بعد 3 محاولات!"
            else:
                msg = f"❌ فاشلة! محاولة {fails[ip]}/3"
            open("hack_log.txt","a",encoding="utf-8").write(f"[{time}] {ip} فاشلة: {pwd} ({fails[ip]}/3)\n")

        self.send_response(200)
        self.send_header('Content-type','text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(f"<html><body style='text-align:center;font-family:sans-serif'><h1>{msg}</h1><a href='/login.html'>رجوع</a> | <a href='/hack_log.txt'>شوف سجل الهجمات</a></body></html>".encode('utf-8'))

print("السيرفر شغال على http://localhost:8000/login.html")
http.server.HTTPServer(("",8000), Handler).serve_forever()
