from fastapi import FastAPI, Request ,Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from starlette.responses import HTMLResponse,RedirectResponse
from starlette.middleware.sessions import SessionMiddleware
import mysql.connector

# 创建 MySQL 连接
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

# 設置靜態文件目錄
# app.mount("/staticFile", StaticFiles(directory="staticFile"), name="static")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    if "username" not in request.session:
        return templates.TemplateResponse("myindex.html", {"request": request})
    else:
        return RedirectResponse(url="/member")

@app.get("/member", response_class=HTMLResponse)
async def login_success(request: Request):
    if "username" in request.session:
        cursor=con.cursor()
        cursor.execute("SELECT * FROM memberData")
        users = cursor.fetchall()
        username=request.session["username"][0]
        # username=request.session["username"][1]
        # print(username)
        cursor.execute("SELECT memberData.yourname, memberContent.content,memberData.username \
                       FROM memberContent \
                       JOIN memberData ON memberContent.member_id = memberData.id \
                       ORDER BY memberContent.time DESC;")
        
        usersandcontents = cursor.fetchall()
        cursor.execute("SELECT yourname FROM memberData WHERE username=%s",(username,))
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

@app.get("/signup")
async def signupfromInternet(request: Request):
    if "username" in request.session:
        return RedirectResponse(url="/member")
    else:
        return RedirectResponse(url="/")

@app.post("/signup")
async def signup(request: Request, yourname: str = Form(None), username: str = Form(None), password: str = Form(None)):
    with con.cursor() as cursor:
        cursor.execute("SELECT * FROM memberData WHERE username = %s", (username,))
        user = cursor.fetchone()
        if user:
            # 如果找到使用者，返回帳號已被註冊的訊息
            return RedirectResponse(url="/error?msg=帳號已被註冊",status_code=303)
        # 如果沒有找到使用者，則新增使用者資料
        cursor.execute("INSERT INTO memberData (yourname, username, password) VALUES (%s, %s, %s)", (yourname, username, password))
        con.commit()
    # 新增成功後重新導向到首頁
    return RedirectResponse(url="/", status_code=303)

    
@app.get("/signin")
async def signfromInternet(request: Request):
    if "username" in request.session:
        return RedirectResponse(url="/member")
    else:
        return RedirectResponse(url="/")
@app.post("/signin")
async def signin(request: Request, username: str = Form(None), password: str = Form(None)):
    # if "username" in request.session:
    #     return "ok"
    cursor=con.cursor()
    cursor.execute("SELECT * FROM memberData WHERE username = %s and password=%s", (username,password))
    user = cursor.fetchone()
    if user==None:
        return RedirectResponse("/error?msg=帳號或密碼輸入錯誤",status_code=303)
    request.session["username"] = [user[2], user[3]]
    return RedirectResponse("/member",status_code=303)
    
@app.get("/signout")
async def signout(request: Request):
    # if "username" in request.session:
    #     return RedirectResponse(url="/member")
    if "username" in request.session:
        del request.session["username"]
    return RedirectResponse("/")

@app.post("/createMessage")
async def createMessage(request: Request, mycontent: str = Form(...)):
    if "username" not in request.session:
        return RedirectResponse("/")
    username=request.session["username"][0]
    # print(username)
    with con.cursor() as cursor:
        cursor.execute("SELECT id FROM memberData WHERE username = %s", (username,))
        user_id = cursor.fetchone()[0]
    with con.cursor() as cursor:
        cursor.execute("INSERT INTO memberContent (member_id, content) VALUES (%s, %s)", (user_id, mycontent))
        con.commit()
    return RedirectResponse(url="/member", status_code=303)

@app.post("/DeleteMessage")
async def DeleteMessage(request: Request, myDelcontent: str = Form(...)):
    if "username" not in request.session:
        return RedirectResponse("/")
    username=request.session["username"][0]
    with con.cursor() as cursor:
        cursor.execute("DELETE FROM memberContent WHERE content =%s", (myDelcontent,))
    return RedirectResponse(url="/member", status_code=303)

    

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)