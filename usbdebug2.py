# -*- coding: utf-8 -*-

import serial.tools.list_ports


def port_p(location):
    ports = list(serial.tools.list_ports.comports())
    res = ''
    for p in ports:
        if p.location in location :
            print(p.device)
            print(p.location)
            res = p.device
    return res
