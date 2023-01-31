import struct
import time

from prometheus_client import Counter, Gauge, start_http_server
from pymodbus.client import ModbusTcpClient

UA = Gauge('ua', 'Voltage Phase A [V]')
UB = Gauge('ub', 'Voltage Phase B [V]')
UC = Gauge('uc', 'Voltage Phase C [V]')
IA = Gauge('ia', 'Current Phase A [A]')
IB = Gauge('ib', 'Current Phase B [A]')
IC = Gauge('ic', 'Current Phase C [A]')
PT = Gauge('pt', 'Total Power [W]')
F = Gauge('f', 'Frequency [Hz]')
IMP = Gauge('impep', 'Imported Power [kWh]')
EXP = Gauge('expep', 'Exported Power [kWh]')
ERR = Counter('errors', 'Python Exceptions')
QRS = Counter('queries', 'Queries performed')

client = ModbusTcpClient('waveshare-58a4', 8899)


def get_smart_meter_value(address):
    result = client.read_holding_registers(address, count=2, slave=1)
    hex_value = result.registers[0] * 0x10000 + result.registers[1]
    if hex_value != 0:
        return (struct.unpack('!f', bytes.fromhex(f'{hex_value:x}'))[0])
    else:
        return 0


if __name__ == "__main__":
    start_http_server(8080)
    client.connect()

    print("Started polling loop")

    try:
        while True:
            try:
                UA.set(get_smart_meter_value(0x2006) * 0.1)
                UB.set(get_smart_meter_value(0x2008) * 0.1)
                UC.set(get_smart_meter_value(0x200A) * 0.1)
                IA.set(get_smart_meter_value(0x200C) * 0.001)
                IB.set(get_smart_meter_value(0x200E) * 0.001)
                IC.set(get_smart_meter_value(0x2010) * 0.001)
                PT.set(get_smart_meter_value(0x2012) * 0.1)
                F.set(get_smart_meter_value(0x2044) * 0.01)
                IMP.set(get_smart_meter_value(0x101E))
                EXP.set(get_smart_meter_value(0x1028))
                QRS.inc()

                time.sleep(15)
            except Exception as e:
                ERR.inc()
                print(e)

    except KeyboardInterrupt as ex:
        client.close()
        print('exited.')
