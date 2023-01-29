from pymodbus.client.sync import ModbusTcpClient
import struct

registers = [ (0x2006, "Ua", 0.1, "V"),
              (0x2008, "Ub", 0.1, "V"),
              (0x200A, "Uc", 0.1, "V"),
              (0x200C, "Ia", 0.001, "A"),
              (0x200E, "Ib", 0.001, "A"),
              (0x2010, "Ic", 0.001, "A"),
              (0x2012, "Pt", 0.1, "W"),
              (0x2044, "Freq", 0.01, "Hz"),
              (0x101E, "ImpEp", 1, "kWh"),
              (0x1028, "ExpEp", 1, "kWh")]

def get_smart_meter_value(client, address):
    result = client.read_holding_registers(address,count=2,unit=1)
    hex_value = result.registers[0] * 0x10000 + result.registers[1]
    if hex_value != 0:
        return(struct.unpack('!f', bytes.fromhex(f'{hex_value:x}'))[0])
    else:
        return 0

def main():
    global registers
    client = ModbusTcpClient('waveshare-58a4', 8899)
    client.connect()
    
    for (address, name, factor, unit) in registers:
        value = get_smart_meter_value(client, address)
        print(f"{name} {value * factor}{unit}")
     
    client.close()

if __name__ == "__main__":
    main()





