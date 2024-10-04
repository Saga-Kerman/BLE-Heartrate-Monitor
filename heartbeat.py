import tkinter as tk
import threading
import asyncio
from bleak import BleakClient, BleakScanner
from bleak.backends.characteristic import BleakGATTCharacteristic

#  of your device
par_notification_characteristic="00002a37-0000-1000-8000-00805f9b34fb"
# MAC address of your device
par_device_addr="D4:0A:C7:E0:B2:46"

# callback listener function, to print heartbeat
def notification_handler(characteristic: BleakGATTCharacteristic, data: bytearray):
    hb=int(str(data.hex())[2:],16)
    # print("rev data:",data)
    # print(int(str(data.hex())[2:],16))
    label.config(text='♥ '+str(hb))

async def main():
    print("starting scan...")

    # look for the device by MAC
    device = await BleakScanner.find_device_by_address(
        par_device_addr, cb=dict(use_bdaddr=False) 
    )
    if device is None:
        print("could not find device with address: "+par_device_addr)
        return
    else:
        print("connecting to: "+str(device.name))
        async with BleakClient(device) as client:
            print("successfully connected to: "+str(device.name))
            await client.start_notify(par_notification_characteristic, notification_handler)
            print('receving heartbeat')  
            await asyncio.sleep(999999)   #程序监听的时间，此处为持续监听
            await client.stop_notify(par_notification_characteristic)      

def run_bt():
    asyncio.run(main())
    
def start_bt_listener():
    bt_thread = threading.Thread(target=run_bt)
    bt_thread.daemon = True
    bt_thread.start()

if __name__=='__main__':

    root = tk.Tk()

    root.attributes('-alpha', 1)
    root.overrideredirect(True)
    root.wm_attributes('-topmost', True)
    root.attributes('-transparentcolor','limegreen')# set transparent color, it should be same as 'bg' in tk.Label()

    label = tk.Label(root, text="♥ 73", font=('Times',12), fg="lightgreen", bg="limegreen")
    label.pack()
    root.geometry("+2515+-3") # xy coord of the window's topleft conor
    # root.geometry("+897+1324")

    start_bt_listener()

    root.mainloop()