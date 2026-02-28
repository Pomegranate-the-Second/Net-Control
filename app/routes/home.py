from fastapi import APIRouter, Request, HTTPException, Response, Depends, Form
from fastapi.templating import Jinja2Templates
from database.config import get_settings
from fastapi.responses import RedirectResponse
from schemas.user import SUserAuth, SUserRegister, SUser, SUserID, SUserInfo
from services.crud.usercrud import UsersCRUD
from services.auth.auth import AuthService


router = APIRouter(tags=['Личный кабинет'])

templates = Jinja2Templates(directory='templates')

settings = get_settings()


@router.get("/", summary='Страница приглашения в сервис!')
def home_page(request: Request):
    token = request.cookies.get(settings.COOKIE_NAME)
    if token:
        try:
            user = AuthService.get_user_from_token(token)
            panel = {'Предсказания скорости': ['Forecast', 'fa-circle-nodes'],
                     'Измерения': ['Measure', 'fa-chart-line'],
                     'Админ панель': ['Admin', 'fa-tasks'],
                     'Документация к проекту': ['Doc', 'fa-file-alt'],
                     'Выход': ['Out', 'fa-sign-out-alt']
                    }
            return templates.TemplateResponse(name='index.html',
                                            context={'request': request,
                                                     'panel': panel}
                                            )
        except HTTPException:
            user = None
    
    return RedirectResponse("/login")


@router.get("/registration", summary='Регистрация личного кабинета!')
def registration(request: Request):
    panel = {'Вход': ['In', 'fa-sign-in-alt']}
    return templates.TemplateResponse(name='registration.html', context={'request': request, 'panel': panel})


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
            panel = {'Предсказания скорости': ['Forecast', 'fa-circle-nodes'],
                     'Измерения': ['Measure', 'fa-chart-line'],
                     'Админ панель': ['Admin', 'fa-tasks'],
                     'Выход': ['Out', 'fa-sign-out-alt']
                    }
            return templates.TemplateResponse(name='info.html',
                                            context={'request': request,
                                                     'panel': panel}
                                            )
        except HTTPException:
            None
    
    panel = {'Вход': ['In', 'fa-sign-in-alt']}
    return templates.TemplateResponse(name='info.html', context={'request': request, 'panel': panel})
    


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
