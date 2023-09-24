import funcs as fu


button1 = fu.machine.Pin(1, fu.machine.Pin.IN, fu.machine.Pin.PULL_UP)
button0 = fu.machine.Pin(0, fu.machine.Pin.IN, fu.machine.Pin.PULL_UP)

# Shhhhhhhhhhh
dbg = (fu.machine.Pin(12, fu.machine.Pin.IN, fu.machine.Pin.PULL_UP),
       fu.machine.Pin(13, fu.machine.Pin.IN, fu.machine.Pin.PULL_UP),
       fu.machine.Pin(15, fu.machine.Pin.IN, fu.machine.Pin.PULL_UP),
       fu.machine.Pin(15, fu.machine.Pin.IN, fu.machine.Pin.PULL_UP))

