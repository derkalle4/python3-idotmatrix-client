# python imports
from fastapi import FastAPI, BackgroundTasks, UploadFile, File, status, Request
from fastapi.exceptions import HTTPException
import os
import signal
import shutil
import uvicorn
from bleak import BleakClient

# idotmatrix imports
from core.idotmatrix.common import Common
from core.idotmatrix.gif import Gif
from core.idotmatrix.const import UUID_WRITE_DATA

PORT = 9191

app = FastAPI()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")

ble = None
currentPixels = 0
currentAdress = ""

def checkBLEconnected():
    if ble is None or not ble.is_connected:
        return False
    return True

async def bleconnect():
    global ble
    ble = BleakClient(currentAdress)
    try:
        await ble.connect()
    except Exception as e:
        print("ble device not found")
    
async def bledisconnect():
    global ble
    await ble.disconnect()
    
async def send(message):
    global ble
    # check if connected
    print(message)
    if not checkBLEconnected():
        return False
    await ble.write_gatt_char(
        UUID_WRITE_DATA,
        message,
    )
    return True
    
async def bleSetBrightness(brightness: int):
    if not checkBLEconnected() :
        return
    await send(Common().set_screen_brightness(brightness))
    
async def bleTurnoff():
    if not checkBLEconnected() :
        return
    await send(Common().turn_screen_off())
    
async def bleTurnon():
    if not checkBLEconnected() :
        return
    await send(Common().turn_screen_on())
    
async def blesendgif(file):
    global currentPixels
    if not checkBLEconnected() :
        return
    #await asyncio.sleep(2)
    await send(Gif().upload_processed(file,currentPixels))
    

@app.get("/BLEconnect/{address}/{pixels}")
async def BLEconnect(address: str, pixels: int, BackgroundTasks: BackgroundTasks):
    global currentAdress, currentPixels
    address = (':'.join(address[i:i+2] for i in range(0,12,2))).upper()
    print(address)
    if currentAdress != address:
        if checkBLEconnected():
            BackgroundTasks.add_task(bledisconnect)
        currentAdress = address
        currentPixels = pixels
    
    if not checkBLEconnected() :
        BackgroundTasks.add_task(bleconnect)
        return "Success"
    return "Already connected"

@app.get("/BLEdisconnect")
async def BLEdisconnect(BackgroundTasks: BackgroundTasks):
    if checkBLEconnected():
        BackgroundTasks.add_task(bledisconnect)
        return "Success"
    return "Not connected"
    
@app.get("/BLEstatus")
def BLEstatus():
    if not checkBLEconnected():
        return {"connected": False }
    return {"connected": True }

@app.get("/brightness/{brightness}")
async def set_brightness(brightness: int, BackgroundTasks: BackgroundTasks):
    if brightness >= 5 and brightness <= 100:
        BackgroundTasks.add_task(bleSetBrightness, brightness)
        return "Success"
    return "Out of range 5 to 100"

@app.get("/turnoff")
async def turn_off(BackgroundTasks: BackgroundTasks):
    BackgroundTasks.add_task(bleTurnoff)
    return "Success"

@app.get("/turnon")
async def turn_on(BackgroundTasks: BackgroundTasks):
    BackgroundTasks.add_task(bleTurnon)
    return "Success"

@app.get("/getFileNames")
def get_file_names():
    mylist = os.listdir(UPLOAD_DIR)
    return {"count": len(mylist),"filenames": mylist}

@app.get("/shutdown")
async def shutdown_server(BackgroundTasks: BackgroundTasks):
    if checkBLEconnected():
        BackgroundTasks.add_task(bledisconnect)
    os.kill(os.getpid(), signal.SIGTERM)
    return "Shutting down server"

@app.post('/upload')
async def upload_file(request: Request, BackgroundTasks: BackgroundTasks, file: UploadFile = File(...)):
    print(file.filename)
    if file.content_type  != 'image/gif' and file.content_type  != 'image/png':
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Wow, That's not allowed")
        return
    
    print("uploaded {} successful".format(file.filename))
    
    SAVE_F = os.path.join(UPLOAD_DIR, file.filename)
    
    with open(SAVE_F, 'w+b') as diskfile:
        shutil.copyfileobj(file.file, diskfile)
        
    print(SAVE_F)
    
    BackgroundTasks.add_task(blesendgif, SAVE_F)
    
    return "Success"

@app.get('/uselocal/{filename}')
async def use_local_file(BackgroundTasks: BackgroundTasks, filename: str):
    SAVE_F = os.path.join(UPLOAD_DIR, filename)
    if os.path.isfile(SAVE_F):
        BackgroundTasks.add_task(blesendgif, SAVE_F)
        return "Success"
    else:

        return "File not found"

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=PORT)
