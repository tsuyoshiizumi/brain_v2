# -*- coding: utf-8 -*-

import serial.tools.list_ports


def port_p(location):
    ports = list(serial.tools.list_ports.comports())
    res = ''
    for p in ports:
        if location == p.location:
            print('kk')
            print(p)
            print(p.device)
            print(p.name)
            print(p.description)
            print(p.hwid)
            print(p.vid)
            print(p.pid)
            print(p.serial_number)
            print(p.location)
            print(p.manufacturer)
            print(p.product)
            print(p.interface)
            res = p.name
    return res
