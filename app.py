from fastapi import FastAPI, Request ,Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from starlette.responses import HTMLResponse,RedirectResponse
from starlette.middleware.sessions import SessionMiddleware
import mysql.connector

# 創建 MySQL 連接
con = mysql.connector.connect(
    host="localhost",
    user="root",
    password="abc31415",
    database="website"
)

app = FastAPI()

app.add_middleware(SessionMiddleware, secret_key="mySignIn") ##提供一個秘密鍵來簽名 cookie

# 設置 Jinja2 模板
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    if "username" not in request.session:
        return templates.TemplateResponse("myindex.html", {"request": request})
    else:
        return RedirectResponse(url="/member")

#Member Page:
@app.get("/member", response_class=HTMLResponse)
async def login_success(request: Request):
    if "username" in request.session:
        cursor=con.cursor()
        cursor.execute("SELECT * FROM member")
        users = cursor.fetchall()
        username=request.session["username"][0]
        
        cursor.execute("SELECT member.yourname, message.content,member.username \
                       FROM message \
                       JOIN member ON message.member_id = member.id \
                       ORDER BY message.time DESC;")
        
        usersandcontents = cursor.fetchall()
        cursor.execute("SELECT yourname FROM member WHERE username=%s",(username,))
        yourname=cursor.fetchone()[0]
        cursor.close()
        return templates.TemplateResponse("member.html", {"request": request,"users":users,\
                                                          "yourname":yourname,"username":username,"usersandcontents":usersandcontents})
    else:
        return RedirectResponse(url="/")
    
#/error?msg=錯誤訊息
@app.get("/error",response_class=HTMLResponse)
async def error(request: Request,msg: str="發生錯誤"):
    if "username" in request.session:
        return RedirectResponse(url="/member")
    return templates.TemplateResponse("error.html", {"request": request,"msg":msg})

#避免瀏覽器直接打入url="/signup"登入@app.post("/signup")，如果已登入讓其導向/member，沒登入讓其導向首頁url="/"
@app.get("/signup")
async def signupfromInternet(request: Request):
    if "username" in request.session:
        return RedirectResponse(url="/member")
    else:
        return RedirectResponse(url="/")

#Signup Endpoint
@app.post("/signup")
async def signup(request: Request, yourname: str = Form(None), username: str = Form(None), password: str = Form(None)):
    with con.cursor() as cursor:
        cursor.execute("SELECT * FROM member WHERE username = %s", (username,))
        user = cursor.fetchone()
        if user:
            # 如果找到使用者，返回帳號已被註冊的訊息
            return RedirectResponse(url="/error?msg=帳號已被註冊",status_code=303)
        # 如果沒有找到使用者，則新增使用者資料
        cursor.execute("INSERT INTO member (yourname, username, password) VALUES (%s, %s, %s)", (yourname, username, password))
        con.commit()
    # 新增成功後重新導向到首頁
    return RedirectResponse(url="/", status_code=303)

#避免瀏覽器直接打入url="/signin"登入@app.post("/signup")，如果已登入讓其導向/member，沒登入讓其導向首頁url="/"    
@app.get("/signin")
async def signfromInternet(request: Request):
    if "username" in request.session:
        return RedirectResponse(url="/member")
    else:
        return RedirectResponse(url="/")
    
#Signin Endpoint:
@app.post("/signin")
async def signin(request: Request, username: str = Form(None), password: str = Form(None)):
    
    cursor=con.cursor()
    cursor.execute("SELECT * FROM member WHERE username = %s and password=%s", (username,password))
    user = cursor.fetchone()
    if user==None:
        return RedirectResponse("/error?msg=帳號或密碼輸入錯誤",status_code=303)
    request.session["username"] = [user[2], user[3]] #將帳號與密碼放入sessionMiddleware
    return RedirectResponse("/member",status_code=303)

#Signout Endpoint:    
@app.get("/signout")
async def signout(request: Request):
    
    if "username" in request.session:
        del request.session["username"]
    return RedirectResponse("/")

#CreateMessage Endpoint:
@app.post("/createMessage")
async def createMessage(request: Request, mycontent: str = Form(...)):
    if "username" not in request.session:
        return RedirectResponse("/")
    username=request.session["username"][0] #抓取sessionMiddleware中的使用者username
    
    with con.cursor() as cursor:
        cursor.execute("SELECT id FROM member WHERE username = %s", (username,))
        user_id = cursor.fetchone()[0]
    with con.cursor() as cursor:
        cursor.execute("INSERT INTO message (member_id, content) VALUES (%s, %s)", (user_id, mycontent))
        con.commit()
    return RedirectResponse(url="/member", status_code=303)


#DeleteMessage Endpoint:
@app.post("/DeleteMessage")
async def DeleteMessage(request: Request, myDelcontent: str = Form(...)):
    if "username" not in request.session:
        return RedirectResponse("/")
    username=request.session["username"][0]
    with con.cursor() as cursor:
        cursor.execute("DELETE FROM message WHERE content =%s", (myDelcontent,))
    return RedirectResponse(url="/member", status_code=303)

    

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)