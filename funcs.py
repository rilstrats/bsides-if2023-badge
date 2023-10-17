# This is where most the main functions will reside
import machine
import utime
import network
import secrets
import neopixel
import ssd1306
import gc
import micropython as mp
import urequests
import ujson
import ubinascii
import hashlib


from i2c_eeprom import i2c_eeprom_init, read_i2c, write_i2c


puid = ''
net_sta = ''

def jeckle(tamerz):
    timer = tamerz
    return timer

def conn():
    # net_sta = network.STA_IF
    # wlan = network.WLAN(net_sta)
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    # print(secrets.SSID, secrets.PASSWORD)
    # while not wlan.isconnected():
        # wlan.connect(secrets.SSID, secrets.PASSWORD)
    for network_pair in secrets.NETWORKS:
        wlan.connect(network_pair[0], network_pair[1])
        if wlan.isconnected(): break
    return wlan

def test_p1n(num):
    pin_num = machine.Pin(num, machine.Pin.OUT)
    for each in range(10):
        pin_num.off()
        utime.sleep.ms(25)
        pin_num.on()
        utime.sleep.ms(25)

def test_pin(pin):
    for each in range(5):
        pin.low()
        utime.sleep_ms(100)
        pin.high()
        utime.sleep_ms(100)

def set_cols(col_arr):
    request = urequests.put("http://game.ifhacker.org/update")

def butt_check(butt_hndl, butt_arr, leds):
    delay_val = 50
    # Array struct { button_status, butt_pressed, button_utimer, button_num, button_led_old_values}
    if butt_hndl.value() == 1:
        butt_arr[0] = 0
        butt_arr[1] = 0
        butt_arr[2] = 0
        butt_num = butt_arr[3]
        leds[butt_num] = butt_arr[4]
    else:
        butt_arr[0] = 1
        butt_num = butt_arr[3]
    if butt_arr[0]:
        if butt_arr[2] == 0:
            print(f'butt_num is {butt_num} and leds is {leds}')
            butt_arr[2] += 1
            butt_arr[4] = leds[butt_num]
        elif butt_arr[2] <= delay_val:
            butt_arr[2] += 1
        elif butt_arr[2] > delay_val:
            butt_arr[2] += 1
            butt_arr[1] = 1
            leds[butt_num] = (5,0,5)
        else:
            print("Something wrong with button!")
    return butt_arr, leds

def butt_done():
    if True:
        print('button_1_pressed')
    if b2_arr[0]:
        print('button_2_pressed')

# class buttonz(button_map):
#     def __init__(self):
#         status = 0
#         utimer = 0
#         button_map = button_map
#     def button_check(self, button_hndl):
#         if button_hndl

class dizplayz:
    def __init__(self, width, height, i2c_h, addr=0x3c):
        self.width = width
        self.height = height
        # self.i2c = machine.I2C(scl=machine.Pin(5), sda=machine.Pin(4))
        self.i2c = i2c_h
        self.addr = addr
        # Initialize the display
        self.display = ssd1306.SSD1306_I2C(width, height, self.i2c, addr)

    def clear(self):
        self.display.fill(0)
        self.display.show()

    def update_text(self, oled_arr):
        self.clear()
        self.display.text(oled_arr[0], 0, 0)
        self.display.text(oled_arr[1], 0, 15)
        self.display.text(oled_arr[2], 0, 30)
        self.display.text(oled_arr[3], 0, 45)
        self.display.show()

    def new_text(self, oled_arr):
        self.clear()
        self.display.text(oled_arr[0], 0, 0)
        self.display.text(oled_arr[1], 0, 15)
        self.display.text(oled_arr[2], 0, 30)
        self.display.text(oled_arr[3], 0, 45)
        self.display.show()

    def old_text(self, oled_arr):
        self.clear()
        self.display.text(oled_arr[0], 0, 0)
        self.display.text(oled_arr[1], 0, 15)
        self.display.text(oled_arr[2], 0, 30)
        self.display.text(oled_arr[3], 0, 45)
        self.display.show()

def mangle(gluid):
    tmp = hashlib.sha1(gluid)
    my_val = tmp.digest()
    bluid = ubinascii.hexlify(my_val).decode()
    return bluid[3:15]

def get_po_stat(uidz):
    domz = '.badgernet.xyz'
    stuff = 'my-points'
    # Define the API URL
    payload = {"uid": uidz}
    url = f"http://{stuff}{domz}:8080/"
    # Define the JSON payload with the "bad" parameter
    # Convert the payload to JSON format
    payload_json = ujson.dumps(payload)
    # Define headers (if needed)
    headers = {
        "Content-Type": "application/json",
    }

    try:
        # Make the POST request with the payload
        # response = urequests.post(url, data=payload_json, headers=headers)
        response = urequests.get(url, json=payload)

        # Check if the request was successful (HTTP status code 200)
        if response.status_code == 200:
            # Parse and print the response JSON data
            response_data = response.json()
            print("Response JSON:", response_data)
        else:
            print("Request failed with status code:", response.status_code)

    finally:
        # Close the HTTP connection
        response.close()
    
def get_stat(stat, uidz):
    domz = '.badgernet.xyz:8080'
    # Define the API URL
    url = f"http://{stat}{domz}/"
    # Define the JSON payload with the "bad" parameter
    payload = { "uid": uidz }
    # Convert the payload to JSON format
    payload_json = ujson.dumps(payload)
    # Define headers (if needed)
    headers = {
        "Content-Type": "application/json",
    }
    try:
        # Make the POST request with the payload
        response = urequests.get(url, json=payload)
        # Check if the request was successful (HTTP status code 200)
        if response.status_code == 200:
            # Parse and print the response JSON data
            response_data = response.json()
            print("Response JSON:", response_data)
            response.close()
        else:
            print("Request failed with status code:", response.status_code)
        # Close the HTTP connection
    except:
        pass

def init_i2c():
    # I2C Setup Section
    scl_pin = machine.Pin(5)
    sda_pin = machine.Pin(4)
    i2c_zero = machine.I2C(0, scl=scl_pin, sda=sda_pin, freq=400000)
    return i2c_zero

def init_spi_eeprom():
    # SPI Setup Section
    miso = machine.Pin(16, machine.Pin.IN)
    mosi = machine.Pin(19)
    sck = machine.Pin(18)
    scs = machine.Pin(17, machine.Pin.OUT)
    # spi_page = 256
    swp = machine.Pin(20, machine.Pin.OUT)
    swp.high()
    spi_zero = machine.SPI(0, 1_000_000, sck=sck, mosi=mosi, miso=miso, polarity=0, phase=0)
    return spi_zero, scs

def init_oled(i2c_handle):
    oled_WIDTH = 128
    oled_HEIGHT= 64
    oled_addr=0x5c
    oled = []
    # oled = ssd1306.SSD1306_I2C(oled_WIDTH, oled_HEIGHT,i2c_handle, oled_addr)
    # oled = ssd1306.SSD1306_I2C(width, height, self.i2c, oled_addr)
    return oled

def init_neo():
    npin = machine.Pin(6, machine.Pin.OUT)
    neopix = neopixel.NeoPixel(npin, 3)
    return neopix

def dev_scan(i2c_handle):
    devices = i2c_handle.scan()
    if len(devices) != 0:
        print('Number of I2C devices found=',len(devices))
        for device in devices:
            print("Device Hexadecimel Address= ",hex(device))
    else:
        print("No device found")

def oled_update(oled_h, oled_arr):
    # oled_h.fill(0)
    # oled_h.text(oled_arr[0], 0, 0)
    # oled_h.text(oled_arr[1], 0, 15)
    # oled_h.text(oled_arr[2], 0, 30)
    # oled_h.text(oled_arr[3], 0, 45)
    # oled_h.show()
    return oled_arr

def gen_id(gluid):
    salt = 'some_rando_val'
    tmp = mangle( f"{gluid}{salt}")
    tmp = mangle( f"{salt}{tmp}")
    tmp = mangle( f"{tmp}{salt}")
    tmp = mangle( f"{salt}{tmp}")
    tmp = mangle( f"{tmp}{salt}")
    return tmp

def oled_test_write(oled_h):
    oled_h.fill(0)
    oled_h.text("Electrocredible", 0, 0)
    oled_h.text("OLED interfacing", 0, 20)
    oled_h.text("Tutorial", 0, 40)
    oled_h.show()


def register_farmer(uid: str):
    execute_order_66(uid, 0, "register-farmer")


def execute_order_66(uid: str, state: int, subdom: str = None):
    domz = 'badgernet.xyz:8080'
    mapping = [
        "pass-potato", # A
        "dress-potato",  # B
        "eat-potato", # C
        "asdf", # D
        "asdf", # E
        "throw-potato" # F
    ]
    if not subdom:
        subdom = mapping[state]
    url = f"http://{subdom}.{domz}"
    payload: dict = {
        "uid": uid
    }
    try:
        # Make the POST request with the payload
        response = urequests.get(url, json=payload)
        # Check if the request was successful (HTTP status code 200)
        if response.status_code == 200:
            # Parse and print the response JSON data
            response_data = response.json()
            # print("Response JSON:", response_data)
            return response_data
        else:
            print("Request failed with status code:", response.status_code)
        response.close()
    except Exception:
        pass

def check_stat(stat, uidz):
    domz = '.badgernet.xyz:8080'
    # Define the API URL
    url = f"http://{stuff}{domz}/"
    # Define the JSON payload with the "bad" parameter
    payload = { "uid": uidz }
    # Convert the payload to JSON format
    payload_json = ujson.dumps(payload)
    # Define headers (if needed)
    headers = {
        "Content-Type": "application/json",
    }
    try:
        # Make the POST request with the payload
        response = urequests.get(url, json=payload)
        # Check if the request was successful (HTTP status code 200)
        if response.status_code == 200:
            # Parse and print the response JSON data
            response_data = response.json()
            print("Response JSON:", response_data)
        else:
            print("Request failed with status code:", response.status_code)
    finally:
        # Close the HTTP connection
        response.close()


def test_i2c(i2c_hndle):
    mem_addr = 0
    # write_data_to_i2c_eeprom(b'this is a eeprom', i2c_hndle, 0x50)
    utime.sleep(.1)
    data = i2c_hndle.readfrom_mem(80, 0, 32)
    # print("Read before : ", data )
    # i2c_hndle.writeto_mem(80, 0, 0x50)
    print("Read after : ", i2c_hndle.readfrom_mem(80, mem_addr, 4 ) )

def test_spi(spi_handle, scs):
    spi_write(spi_handle, scs, 32, 'this is some data to write')
    utime.sleep(.1)
    tmp = spi_read(spi_handle, scs, 0, 128)
    print("Data read from SPI: ", tmp)

def test_neo_1(np):
    np[0] = (0, 24, 0)
    np[1] = (2, 2, 2)
    np[2] = (20, 4, 0)
    np.write()

# def test_neo_2(np):
#     np[0] = (0, 5, 5)
#     np[1] = (5, 5, 5)
#     np[2] = (5, 0, 0)
#     np.write()

# def test_neo_3(np):
#     np[0] = (10, 5, 15)
#     np[1] = (5, 15, 5)
#     np[2] = (5, 10, 10)
#     np.write()

def neo_in(np_curr):
    if np_curr == (5,5,5):
        led_val = (0,4,4)
        return led_val
    elif np_curr == (0,4,4):
        led_val = (5,5,5)
        return led_val
    elif np_curr == (1,1,1):
        led_val = (5,5,5)
        return led_val
    else:
        return np_curr
        # print("something is wrong with led_arr")


def up_neo(np, npvals):
    np[0] = npvals[0]
    np[1] = npvals[1]
    np[2] = npvals[2]
    np.write()


def spi_wren(spi, scs):
    scs.low()
    # utime.sleep_us(5)
    spi.write(b'\x06')
    scs.high()

def check_spud(nuid):
    tmp = execute_order_66(nuid, 0, "do-i-have-a-potato")
    # print(tmp['maybe'])
    if tmp is None and tmp['maybe']:
        return True


def spi_read(spi, scs, addr, bytenum):
    buf = bytearray(bytenum)
    buf = bytearray(b'\x03' + addr.to_bytes(2, 'big') + buf)
    # print(f'read buf: {buf}')
    scs.low()
    # utime.sleep_us(5)
    spi.write_readinto(buf, buf)
    scs.high()
    # print(f'got back from read: {buf}')
    utime.sleep_ms(10)
    return buf[3:]

def spi_write(spi, scs, addr, data):
    spi_page = 64

    num_b = len(data)

    if ua_len := addr % spi_page:
        # Unaligned
        l = min(num_b, spi_page - ua_len)
        #print(f"{len(data)} and {l}")
        buf = bytearray(b'\x02' + addr.to_bytes(2, 'big') + data[0: l])
        spi_wren(spi, scs)

        scs.low()
        utime.sleep_ms(10)
        spi.write_readinto(buf, buf)
        scs.high()
        utime.sleep_ms(10)

        num_b -= l
        addr += l
        data = data[l:]

    for page_ctr in range(0, num_b, spi_page):
        # aligned
        address = (addr + page_ctr)
        l = min(len(data[page_ctr:]), spi_page)
        # print(f'address: {address}')
        buf = bytearray(b'\x02' + address.to_bytes(2, 'big') + data[page_ctr:page_ctr + l])
        # print(f'writing @{address}: "{buf}"')
        spi_wren(spi, scs)
        scs.low()
        utime.sleep_ms(10)
        spi.write_readinto(buf, buf)
        scs.high()
        # print(f'got back from write: {buf}')
        utime.sleep_ms(10)
    return 0

def cln(s):
    return s.rstrip(b'\x00\xff').decode('utf8', 'backslashreplace')


