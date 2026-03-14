from fastapi import APIRouter, Request, HTTPException, Response, Depends, Form
from fastapi.templating import Jinja2Templates
from database.config import get_settings
from fastapi.responses import RedirectResponse
from fastapi.responses import StreamingResponse
from schemas.user import SUserAuth, SUserRegister, SUser, SUserID, SUserInfo
from services.crud.usercrud import UsersCRUD
from services.auth.auth import AuthService
import os


router = APIRouter(tags=['Личный кабинет'])

templates = Jinja2Templates(directory='templates')

settings = get_settings()

def get_panel(token, additional):
    user = AuthService.get_user_from_token(token)
    panel = {}
    if user.is_access:
        panel['Предсказания скорости'] = ['Forecast', 'fa-eye']
        panel['Измерения'] = ['Measure', 'fa-signal']
        if user.is_admin:
            panel['Админ панель'] = ['Admin', 'fa-user-shield']
        panel.update(additional)
    panel['Документация к проекту'] = ['Doc', 'fa-file-alt']
    panel['Выход'] = ['Out', 'fa-sign-out-alt']
    return panel

def create_page(request: Request, mode = "unknown"):
    token = request.cookies.get(settings.COOKIE_NAME)
    if token:
        try:
            panel = get_panel(token, {})
            return templates.TemplateResponse(name='index.html',
                                            context={'request': request,
                                                     'mode': mode,
                                                     'panel': panel}
                                            )
        except HTTPException:
            raise 
    
    raise HTTPException(status_code=404, detail="User not found")

@router.get("/", summary='Страница приглашения в сервис!')
def home_page(request: Request):
    try:
        return create_page(request, "measure")
    except HTTPException:
        None
    return RedirectResponse("/login")

@router.get("/measurements", summary='Страница измерений!')
def measurement_page(request: Request):
    try:
        return create_page(request, "measure")
    except HTTPException:
        None
    return RedirectResponse("/login")

@router.get("/forecasts", summary='Страница прогнозирования!')
def forecast_page(request: Request):
    try:
        return create_page(request, "forecast")
    except HTTPException:
        None
    return RedirectResponse("/login")


@router.get("/admin", summary='Кабинет админа')
def adminpanel(request: Request):
    token = request.cookies.get(settings.COOKIE_NAME)
    if token: 
        try:
            user = AuthService.get_user_from_token(token)
            if not user.is_admin:
                return RedirectResponse("/")
            panel = get_panel(token, {})
            table = list()
            for user_item in UsersCRUD.find_all_users():
                table.append({'id': user_item.id,
                               'email': user_item.email,
                               'admin': user_item.is_admin,
                               'access': user_item.is_access})
            return templates.TemplateResponse(name='admin.html', context={'request': request,'panel': panel, 'table': table})
        except HTTPException:
            raise 
   
    raise HTTPException(status_code=404, detail="User not found")


@router.get("/login", summary='Вход в личный кабинет!')
def login(request: Request):
    panel = {'Документация к проекту': ['Doc', 'fa-file-alt']}
    return templates.TemplateResponse(name='auth.html', context={'request': request, 'panel': panel})


@router.get("/logout", summary='Покиинуть личный кабинет!')
def logout(response: Response, request: Request):
    response.delete_cookie(key=settings.COOKIE_NAME)
    return templates.TemplateResponse(name='auth.html', context={'request': request})

@router.get("/info", summary='Пояснительная записка к дипломной работе')
def diplom(response: Response, request: Request):
    token = request.cookies.get(settings.COOKIE_NAME)
    if token:
        try:
            panel = get_panel(token, {})
            return templates.TemplateResponse(name='info.html',
                                            context={'request': request,
                                                     'panel': panel}
                                            )
        except HTTPException:
            None
    
    panel = {'Вход': ['In', 'fa-sign-in-alt']}
    return templates.TemplateResponse(name='info.html', context={'request': request, 'panel': panel})
    
def generate():
    chunk = os.urandom(64 * 1024)
    while True:
        yield chunk    

@router.get("/b0e349b6-aaa3-4341-b7f7-39102f6243a1", summary='Страница измерения скорости')
def temp():
    return StreamingResponse(generate(), media_type="application/octet-stream")


@router.post("/c8686ff0-ae42-4883-9216-b56a1a70d555", summary='Страница измерения скорости')
async def upload(request: Request):

    async for chunk in request.stream():
        pass

    return {"status": "ok"}

@router.get(
    "/image/{file}",
    responses = {
        200: {
            "content": {"image/png": {}}
        }
    },
    response_class=Response
)
def get_image(file: str, user: SUserInfo = Depends(AuthService.get_current_user)):
    with open(f'./files/{file}', 'rb') as f:
        image_bytes: bytes = f.read()
    return Response(content=image_bytes, media_type="image/png")
