from fastapi import APIRouter, Request, HTTPException, Response, Depends, Form
from database.config import get_settings
from fastapi.responses import RedirectResponse
from sqlalchemy.exc import SQLAlchemyError
from services.auth.auth import AuthService
from services.crud.measurementcrud import MeasurementsCRUD
from services.crud.devicecrud import DevicesCRUD
from schemas.user import SUserInfo
from schemas.measurement import SMeasurementAdd, SMeasurement, SRectangle, SDevice

router = APIRouter(prefix='/measure', tags=['Функции для обработки измерений'])

@router.put('/add', summary='Добавить измерение в таблицу measurements')
def addMeasurement(measurement: SMeasurement,device: SDevice = Depends(AuthService.get_current_device)) -> dict:
    item = SMeasurementAdd(device_id = device, 
                         lat = measurement.lat,
                         lon = measurement.lon,
                         bs_num = measurement.bs_num,
                         cell_num = measurement.cell_num,
                         operator = measurement.operator,
                         upload = measurement.upload,
                         download = measurement.download,
                         rsrp = measurement.rsrp,
                         rssi = measurement.rssi
                         )
    result = {"message": "success"}
    try:
        MeasurementsCRUD.add(item)
    except SQLAlchemyError:
        result = {"message": "failure"}

    
    return result

@router.post('/view', summary='Вернуть список указанных точек по координатам углов пряямоугольника')
def viewMeasurement(data: SRectangle, user: SUserInfo = Depends(AuthService.get_current_user)) -> list:
    items = MeasurementsCRUD.find_rectangle_measurements(data)
    result = [{"id": itm.id, 
               "device_id": itm.device_id, 
               "lat": itm.lat,
               "lon": itm.lon,
               "bs_num": itm.bs_num,
               "cell_num": itm.cell_num,
               "operator": itm.operator,
               "upload": itm.upload,
               "download": itm.download,
               "rsrp": itm.rsrp,
               "rssi": itm.rssi,
               "event_datetime": itm.event_datetime
               } for itm in items]
    
    return result