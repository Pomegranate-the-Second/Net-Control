from fastapi import FastAPI
from routes.home import router as home_router
from routes.auth import router as auth_router
from routes.measurement import router as measure_router
#from routes.user import router as user_router
#from routes.ml import router as ml_router
#from routes.admin import router as admin_router
#from routes.health import router as health_router
from database.database import init_db
from services.crud.usercrud import UsersCRUD
from services.crud.devicecrud import DevicesCRUD
from services.crud.measurementcrud import MeasurementsCRUD
from schemas.user import SUser, SUserEmail
from schemas.device import SDeviceAdd
from schemas.measurement import SMeasurementAdd
from services.auth.auth import AuthService
from models.user import User
from models.devices import Devices
import uvicorn

def lifespan(app: FastAPI):
    init_db()
    user = SUser(first_name='User', 
            last_name='Test', 
            email='User@Test.ru', 
            password=AuthService.get_password_hash('testpwd')
            )
    if UsersCRUD.find_one_or_none_by_email(SUserEmail(email=user.email)) is None: UsersCRUD.add(user)
    device = SDeviceAdd(id = 121, imeisv = "121")
    if DevicesCRUD.find_one_or_none(device) is None: DevicesCRUD.add(device)
    mlist = [
        [121, 47.209497, 38.935356, 615806, 2, "02", 33, 33, -102, -103], 
        [121, 47.206931, 38.943433, 615806, 2, "02", 23, 11, -116, -103],
        [121, 47.206378, 38.940356, 615806, 2, "02", 36, 98, -130, -104],
        [121, 47.205000, 38.940400, 615806, 2, "02", 73, 57, -116, -103],
        [121, 47.205200, 38.940700, 615806, 2, "02", 30, 14, -119, -102],
        [121, 47.209549, 38.903899, 615806, 2, "02", 53, 85, -106, -103],
        [121, 47.209233, 38.901014, 615806, 2, "02", 37, 10, -112, -106],
        [121, 47.252374, 38.906111, 615806, 2, "02", 43, 11, -116, -103],
        [121, 47.252973, 38.911321, 615806, 2, "02", 44, 42, -127, -109],
    ]
    keys = ["device_id", "lat", "lon", "bs_num", "cell_num", "operator", "upload", "download", "rsrp", "rssi"]
    for itm in mlist:
        measurement = SMeasurementAdd(**dict(zip(keys, itm)))
        MeasurementsCRUD.add(measurement)
    yield

app = FastAPI(lifespan=lifespan)

#app.include_router(health_router)
app.include_router(home_router)
app.include_router(auth_router)
app.include_router(measure_router)
#app.include_router(user_router)
#app.include_router(ml_router)
#app.include_router(admin_router)


if __name__=='__main__':
    uvicorn.run('api:app', host='0.0.0.0', port=8000, reload=True)