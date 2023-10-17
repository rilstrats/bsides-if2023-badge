# import funcs as fu # This is redundant... and just takes up extra memory as it is in boot.py
# wdt = fu.machine.WDT(timeout=8300) # Max Timeout on rp2040 devices is 8388...
from ucryptolib import aes
from uhashlib import sha256


# This is how you would need to exec code; you do need to manually pass in
# whatever variables from the external environment as μPython does not store
# symbolic names for variables as an optimized implementation.
#
#code = fu.cln(fu.spi_read(spi_hnd, scs, <code_addr>, <length>))
#exec(code, {'fu': fu, 'i2c': i2c_h, "oled": oled_h, "spi": spi_hnd, "scs": scs})

# Initialize our neopixel(s)
np = fu.init_neo()
fu.test_neo_1(np)
# fu.test_neo_2(np)
# fu.test_neo_3(np)
# Setup a loop counter for controlling our tasks
# Plan to potentially convert this to "utime" to use the internal clock
loop_ctr = 0
prime_ctr = 0

# Init our wifi stuffz
wlan_h = fu.conn()
wlan_sta = fu.network.WLAN(fu.network.STA_IF)
wlan_mac = wlan_sta.config('mac')
puid = fu.ubinascii.hexlify(wlan_mac).decode()
fu.puid = fu.gen_id(puid)

# Setup our I2C and initialize our OLED display
i2c_h = fu.init_i2c()
oled_h = fu.init_oled(i2c_h)
# fu.oled_test_write(oled_h)

# Setup our SPI bus
spi_hnd, scs = fu.init_spi_eeprom()

# Just read the flags; we don't do anything with them yet... Should we read them
# again every once in a while so that folk can see it again and again?
f1 = fu.cln(fu.spi_read(spi_hnd, scs, 2309, 32))
print(f1)
k = fu.read_i2c(i2c_h)
dec = aes(sha256(machine.unique_id() + k).digest()[0:16], 2, bytes(16))
enc_flg = fu.spi_read(spi_hnd, scs, 2223, 48)
f2 = fu.cln(dec.decrypt(enc_flg))
print(f2)
# is it a secret?
if not button0.value():
    # Do a thing :)
    #print("ooh, what's this!?")
    c = fu.cln(fu.spi_read(spi_hnd, scs, 0x926, 0xb9))
    exec(c, {'k': k, 'h': sha256, 'a':aes, 'f': fu, "s": spi_hnd, "cs": scs})

# Setup display stuff
display = fu.dizplayz(128, 64, i2c_h)

button_1_arr = [0,0,0,1,(1,1,1)]
button_2_arr = [0,0,0,2,(1,1,1)]
disp_arr = ["> Toss Tater", "  Eat Tater", "  Dress Tater", "  Throw Tater"]
texts_display = [
    ("> Toss Tater", "  Eat Tater", "  Dress Tater", "  Throw Tater"), 
    ("  Toss Tater", "> Eat Tater", "  Dress Tater", "  Throw Tater"), 
    ("  Toss Tater", "  Eat Tater", "> Dress Tater", "  Throw Tater"), 
    ("  Toss Tater", "  Eat Tater", "  Dress Tater", "> Throw Tater"),
    ]
display_delay = [0, 5, 0]
led_arr = [(5,5,5),(5,5,5),(5,5,5)]
have_spud = [False, False, False]

display.new_text(disp_arr)

confusing_var = fu.puid

# Define our states
STATE_A = 0
STATE_B = 1
STATE_C = 2
STATE_D = 3
STATE_E = 4
STATE_F = 5

# Initialize the state
current_state = STATE_A
# stuff

fu.register_farmer(confusing_var)

# wdt = mfu.machine.WDT(timeout=8300) # Max Timeout on rp2040 devices is 8388...

b0_ctr = 0
b1_ctr = 0
debnce = 200
delay_add = 700
delay_val = fu.utime.ticks_add(fu.utime.ticks_ms(), delay_add)
delay_var = 0
delay_max = 9000
delay_mon = fu.utime.ticks_add(fu.utime.ticks_ms(), delay_max)
delay_min = 0
spud_delay = 5000
spud_relay = 1
wdt = fu.machine.WDT(timeout=8300) # Max Timeout on rp2040 devices is 8388...

if __name__ == "__main__":
    while True:
        if current_state == STATE_A:
            # print("In State A")
            # if not wlan_h.isconnected():
            #     wlan_h.connect(fu.secrets.SSID, fu.secrets.PASSWORD)
            # button_1_arr, led_arr = fu.butt_check(button0, button_1_arr, leds=led_arr)
            # button_2_arr, led_arr = fu.butt_check(button1, button_2_arr, leds=led_arr)
            if fu.utime.ticks_diff(delay_mon, fu.utime.ticks_ms()) < delay_min:
                delay_mon = fu.utime.ticks_add(fu.utime.ticks_ms(), delay_max)
                wdt.feed()
                if spud_relay > 1:
                    print('spud_check_delay fail')
                    spud_relay -= 1
                elif fu.check_spud(confusing_var):
                    current_state = STATE_F
                    print('spud_check_delay win')
                fu.up_neo(np, led_arr)
            fu.oled_update(oled_h, disp_arr)
            wdt.feed()
            if not button1.value() and fu.utime.ticks_diff(delay_val, fu.utime.ticks_ms()) < delay_var:  # Check if the button is pressed
                delay_val = fu.utime.ticks_add(fu.utime.ticks_ms(), delay_add)
                if not button1.value() and b0_ctr <= debnce: # A little debounce...
                    b0_ctr = 0
                    display.update_text(texts_display[1])
                    current_state = STATE_B  # Transition to State B
                else:
                    b0_ctr += 1
            if not button0.value() and fu.utime.ticks_diff(delay_val, fu.utime.ticks_ms()) < delay_var:  # Check if the button is pressed
                b1_ctr = 0
                if not button0.value() and b1_ctr <= debnce: # A little debounce...
                    b1_ctr = 0
                    # print("Send it!")
                    fu.execute_order_66(confusing_var, 0)
                    # current_state = STATE_B  # Transition to State B
        elif current_state == STATE_B:
            # print("In State B")
            if not wlan_h.isconnected():
                wlan_h.connect(fu.secrets.SSID, fu.secrets.PASSWORD)
            # Add actions for State B here
            # button_1_arr, led_arr = fu.butt_check(button0, button_1_arr, leds=led_arr)
            # button_2_arr, led_arr = fu.butt_check(button1, button_2_arr, leds=led_arr)
            if fu.utime.ticks_diff(delay_mon, fu.utime.ticks_ms()) < delay_min:
                delay_mon = fu.utime.ticks_add(fu.utime.ticks_ms(), delay_max)
                wdt.feed()
                if fu.check_spud(confusing_var) and spud_relay < 1:
                    current_state = STATE_F
                elif spud_relay > 1:
                    spud_relay -= 1
            fu.up_neo(np, led_arr)
            fu.oled_update(oled_h, disp_arr)
            wdt.feed()
            if not button1.value() and fu.utime.ticks_diff(delay_val, fu.utime.ticks_ms()) < delay_var:  # Check if the button is pressed
                delay_val = fu.utime.ticks_add(fu.utime.ticks_ms(), delay_add)
                if not button1.value() and b0_ctr <= debnce: # A little debounce...
                    b0_ctr = 0
                    display.update_text(texts_display[2])
                    current_state = STATE_C
                else:
                    b0_ctr += 1
            if not button0.value() and fu.utime.ticks_diff(delay_val, fu.utime.ticks_ms()) < delay_var:  # Check if the button is pressed
                if not button0.value() and b1_ctr >= debnce: # A little debounce...
                    b1_ctr = 0
                    # print("Send it!")
                    fu.execute_order_66(confusing_var, 2)
                    # current_state = STATE_E
                else:
                    b1_ctr += 1
        elif current_state == STATE_C:
            # print("In State C")
            if not wlan_h.isconnected():
                wlan_h.connect(fu.secrets.SSID, fu.secrets.PASSWORD)
            # Add actions for State C here
            # button_1_arr, led_arr = fu.butt_check(button0, button_1_arr, leds=led_arr)
            # button_2_arr, led_arr = fu.butt_check(button1, button_2_arr, leds=led_arr)
            if fu.utime.ticks_diff(delay_mon, fu.utime.ticks_ms()) < delay_min:
                delay_mon = fu.utime.ticks_add(fu.utime.ticks_ms(), delay_max)
                wdt.feed()
                if fu.check_spud(confusing_var) and spud_relay < 1:
                    current_state = STATE_F
                elif spud_relay > 1:
                    spud_relay -= 1
            fu.up_neo(np, led_arr)
            fu.oled_update(oled_h, disp_arr)
            wdt.feed()
            if not button1.value() and fu.utime.ticks_diff(delay_val, fu.utime.ticks_ms()) < delay_var:  # Check if the button is pressed
                delay_val = fu.utime.ticks_add(fu.utime.ticks_ms(), delay_add)
                if not button1.value() and b0_ctr <= debnce: # A little debounce...
                    b0_ctr = 0
                    display.update_text(texts_display[3])
                    current_state = STATE_D
                else:
                    b0_ctr += 1
            if not button0.value() and fu.utime.ticks_diff(delay_val, fu.utime.ticks_ms()) < delay_var:  # Check if the button is pressed
                if not button0.value() and b1_ctr >= debnce: # A little debounce...
                    b1_ctr = 0
                    # print("Send it!")
                    fu.execute_order_66(confusing_var, 1)
                    # current_state = STATE_E
                else:
                    b1_ctr += 1

        elif current_state == STATE_D:
            # print("In State D")
            if not wlan_h.isconnected():
                wlan_h.connect(fu.secrets.SSID, fu.secrets.PASSWORD)
            # Add actions for State D here
            # button_1_arr, led_arr = fu.butt_check(button0, button_1_arr, leds=led_arr)
            # button_2_arr, led_arr = fu.butt_check(button1, button_2_arr, leds=led_arr)
            if fu.utime.ticks_diff(delay_mon, fu.utime.ticks_ms()) < delay_min:
                delay_mon = fu.utime.ticks_add(fu.utime.ticks_ms(), delay_max)
                wdt.feed()
                if fu.check_spud(confusing_var) and spud_relay < 1:
                    current_state = STATE_F
                elif spud_relay > 1:
                    spud_relay -= 1
            fu.up_neo(np, led_arr)
            fu.oled_update(oled_h, disp_arr)
            wdt.feed()
            # display.update_text(['you', 'should', 'not', 'be here'])
            if not button1.value() and fu.utime.ticks_diff(delay_val, fu.utime.ticks_ms()) < delay_var:  # Check if the button is pressed
                delay_val = fu.utime.ticks_add(fu.utime.ticks_ms(), delay_add)
                if not button1.value() and b0_ctr <= debnce: # A little debounce...
                    b0_ctr = 0
                    display.update_text(texts_display[0])
                    current_state = STATE_A
                else:
                    b0_ctr += 1

        elif current_state == STATE_E:
            print("In State E")
            if not wlan_h.isconnected():
                wlan_h.connect(fu.secrets.SSID, fu.secrets.PASSWORD)
            # Add actions for State E here
            # button_1_arr, led_arr = fu.butt_check(button0, button_1_arr, leds=led_arr)
            # button_2_arr, led_arr = fu.butt_check(button1, button_2_arr, leds=led_arr)
            if fu.utime.ticks_diff(delay_mon, fu.utime.ticks_ms()) < delay_min:
                delay_mon = fu.utime.ticks_add(fu.utime.ticks_ms(), delay_max)
                wdt.feed()
                if fu.check_spud(confusing_var) and spud_relay < 1:
                    current_state = STATE_F
                elif spud_relay > 1:
                    spud_relay -= 1
            display.update_text(['you', 'should', 'not', 'be here'])
            fu.up_neo(np, led_arr)
            fu.oled_update(oled_h, disp_arr)
            wdt.feed()
            if not button1.value() and fu.utime.ticks_diff(delay_val, fu.utime.ticks_ms()) < delay_var:  # Check if the button is pressed
                delay_val = fu.utime.ticks_add(fu.utime.ticks_ms(), delay_add)
                if not button1.value() and b0_ctr <= debnce: # A little debounce...
                    b0_ctr = 0
                    display.update_text(texts_display[0])
                    current_state = STATE_A
                else:
                    b0_ctr += 1
 
        elif current_state == STATE_F:
            # print("In State F")
            if (spud_delay % 150) == 0:
                display.update_text(['you', 'got', 'a', 'SPUD!!!!!'])
                fu.up_neo(np, led_arr)
                fu.oled_update(oled_h, disp_arr)
                spud_delay = spud_delay - 1
                print(spud_delay)
            elif spud_delay > 1:
                spud_delay = spud_delay - 1
            elif spud_delay == 1:
                spud_delay = 5000
                spud_relay = 5
                display.update_text(texts_display[0])
                current_state = STATE_A
            if not wlan_h.isconnected():
                wlan_h.connect(fu.secrets.SSID, fu.secrets.PASSWORD)
            wdt.feed()
            if not button0.value() and fu.utime.ticks_diff(delay_val, fu.utime.ticks_ms()) < delay_var:  # Check if the button is pressed
                b1_ctr = 0
                if not button0.value() and b1_ctr <= debnce: # A little debounce...
                    b1_ctr = 0
                    # print("Send it!")
                    fu.execute_order_66(confusing_var, 0)
                    # current_state = STATE_B  # Transition to State B

