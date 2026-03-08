from fastapi import APIRouter, Request, HTTPException, Response, Depends, Form
from database.config import get_settings
from fastapi.responses import RedirectResponse
from sqlalchemy.exc import SQLAlchemyError
from services.auth.auth import AuthService
from services.crud.forecastcrud import ForecastsCRUD
from services.crud.devicecrud import DevicesCRUD
from schemas.user import SUserInfo
from schemas.forecast import SForecast, SForecastAdd, SRectangle, SComplete
from services.rm.rm import RabbitMQSender
import json

router = APIRouter(prefix='/forecast', tags=['Функции для прогнозирования'])

@router.put('/add', summary='Добавить измерение в таблицу forecasts')
def addForecast(forecast: SForecast, user: SUserInfo = Depends(AuthService.get_current_user)) -> dict:
    item = SForecastAdd(user_id = user.id, 
                         lat = forecast.lat,
                         lon = forecast.lon,
                         operator = forecast.operator
                         )
    result = {"message": "success"}
    try:
        new_item = ForecastsCRUD.add(item)

    except SQLAlchemyError:
        result = {"message": "failure"}

    th_item = {'id': new_item.id,
            'lat': new_item.lat,
            'lon': new_item.lon,
            'operator': new_item.operator
            }
    with RabbitMQSender("ml_task_queue") as sender:
        sender.send_task(json.dumps(th_item))
    return result

@router.post('/view', summary='Вернуть список указанных точек по координатам углов пряямоугольника')
def viewForecast(data: SRectangle, user: SUserInfo = Depends(AuthService.get_current_user)) -> list:
    items = ForecastsCRUD.find_rectangle_measurements(data)
    result = [{"id": itm.id, 
               "user_id": itm.user_id, 
               "lat": itm.lat,
               "lon": itm.lon,
               "operator": itm.operator,
               "upload": itm.upload,
               "download": itm.download,
               "status": itm.status,
               "event_datetime": itm.event_datetime
               } for itm in items]
    
    return result

@router.patch('/complete', summary='Обновить данные предсказания в таблице', include_in_schema=False)
def completeForecast(item: SComplete) -> dict:
    result = {"message": "success"}
    try:
        ForecastsCRUD.update_forecast_by_id(item.id,
                                            item.upload,
                                            item.download,
                                            item.state)
    except SQLAlchemyError:
        result = {"message": "failure"}

    return result