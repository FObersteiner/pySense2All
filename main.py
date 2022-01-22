#!/usr/bin/env python
#
# Copyright (c) 2020, Pycom Limited.
#
# This software is licensed under the GNU GPL version 3 or any
# later version, with permitted additional terms. For more information
# see the Pycom Licence v1.0 document supplied with this file, or
# available at https://www.pycom.io/opensource/licensing
#

# See https://docs.pycom.io for more information regarding library specifics

import utime

import pycom
from pysense import Pysense
# import machine

from LIS2HH12 import LIS2HH12
from SI7006A20 import SI7006A20
from LTR329ALS01 import LTR329ALS01
from MPL3115A2 import MPL3115A2, PRESSURE

pycom.heartbeat(False)
pycom.rgbled(0x7F0000)

py = Pysense()

li = LIS2HH12(py)
lt = LTR329ALS01(py)
mp = MPL3115A2(py, mode=PRESSURE)
si = SI7006A20(py)

duration_ms = 3000
colors = (0x002C00, 0x00002C)
counter = 0
LogSep = "\t"

while True:
    t0 = utime.ticks_ms()

    # LIS2HH12
    acc, rol, pit = li.acceleration(), li.roll(), li.pitch()

    # LTR329ALS01
    lux = lt.light()
    lux_blue, lux_red = lux[0], lux[1]

    # SI7006A20
    si_T, si_RH = si.temperature(), si.humidity()

    # MPL3115A2
    mp_T, mp_p = mp.temperature(), mp.pressure()/100

    # format to output string:
    # p
    s = "[[ {:.1f}{}{:.1f}{}".format(mp_T, LogSep, mp_p, LogSep)
    # T
    s += "{:.1f}{}{:.1f}{}".format(si_T, LogSep, si_RH, LogSep)
    # acc
    s += "{:.2f}{}{:.2f}{}{:.2f}".format(acc[0],
                                         LogSep, acc[1], LogSep, acc[2])
    # orient
    s += "{}{:.1f}{}{:.1f}{}".format(LogSep, pit, LogSep, rol, LogSep)
    # light
    s += "{:d}{}{:d} ]]".format(lux_blue, LogSep, lux_red)

    pycom.rgbled(colors[counter % 2])
    print(s)

    dt = utime.ticks_ms()-t0
    if dt < duration_ms:
        utime.sleep_ms(duration_ms-dt)

    counter += 1

pycom.rgbled(0x7F0000)
