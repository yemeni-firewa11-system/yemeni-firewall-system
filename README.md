<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>نظام الحماية اليمني</title>
<style>body{background:#0f172a;color:#fff;font-family:system-ui;display:flex;justify-content:center;padding:15px} .box{background:#1e293b;padding:20px;border-radius:16px;width:100%;max-width:380px;margin-top:30px;border:1px solid #334155} input{width:100%;padding:11px;margin:5px 0;border-radius:10px;border:1px solid #334155;background:#0f172a;color:#fff} button{width:100%;padding:12px;margin-top:8px;background:#22c55e;border:0;border-radius:10px;font-weight:800;cursor:pointer} .item{background:#0f172a;padding:10px;border-radius:10px;margin-top:8px;display:flex;justify-content:space-between;font-size:13px;border:1px solid #1e293b}</style>
</head>
<body>
<div class="box">
<h3>🛡️ نظام الحماية اليمني</h3>
<p style="color:#94a3b8;font-size:12px;margin:8px 0">يحفظ في الجهاز فقط</p>
<input id="user" placeholder="اسم المستخدم">
<input id="pass" type="password" placeholder="كلمة السر">
<button onclick="save()">حفظ البيانات 💾</button>
<button onclick="clearAll()" style="background:#ef4444">حذف الكل</button>
<div id="list" style="margin-top:15px"></div>
</div>
<script>
function load(){
 let data = JSON.parse(localStorage.getItem('yemeni_accounts') || '[]');
 let html = data.length ? '<p style="font-size:12px;color:#22c55e">المحفوظات: '+data.length+'</p>' : '';
 data.forEach((a,i)=>{
   html+=`<div class="item"><span>👤 ${a.u} <br>🔑 ${a.p}</span><span onclick="del(${i})" style="color:#ef4444;cursor:pointer">حذف</span></div>`;
 });
 document.getElementById('list').innerHTML=html;
}
function save(){
 let u=document.getElementById('user').value, p=document.getElementById('pass').value;
 if(!u || !p){ alert('اكتب الاسم وكلمة السر'); return; }
 let data = JSON.parse(localStorage.getItem('yemeni_accounts') || '[]');
 data.push({u:u,p:p});
 localStorage.setItem('yemeni_accounts', JSON.stringify(data));
 document.getElementById('user').value=''; document.getElementById('pass').value='';
 load();
}
function del(i){
 let data = JSON.parse(localStorage.getItem('yemeni_accounts') || '[]');
 data.splice(i,1);
 localStorage.setItem('yemeni_accounts', JSON.stringify(data));
 load();
}
function clearAll(){ localStorage.removeItem('yemeni_accounts'); load(); }
load();
</script>
</body>
</html>
