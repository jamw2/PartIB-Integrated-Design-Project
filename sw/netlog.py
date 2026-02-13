# sw/netlog.py
import network, socket, time


def wlan_connect(ssid, password, timeout_s=10):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        wlan.connect(ssid, password)
        t0 = time.ticks_ms()
        while not wlan.isconnected():
            if time.ticks_diff(time.ticks_ms(), t0) > timeout_s * 1000:
                # raise RuntimeError("Wi-Fi connect timeout")
                return
            time.sleep(0.1)
    return wlan


class UDPLogger:
    def __init__(self, host, port=9000):
        self.addr = (host, port)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def log(self, msg):
        try:
            self.sock.sendto((msg + "\n").encode(), self.addr)
        except Exception:
            pass


wlan_connect("Eduroam Never Works", "iNeedWifi")
log = UDPLogger("10.11.160.253", 9000)
log.log("HI")
print("HI")
