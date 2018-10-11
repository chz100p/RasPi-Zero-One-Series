#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from dashing import *

import signal
import time
import GYRO

if __name__ == "__main__":
	signal.signal(signal.SIGINT,signal.SIG_DFL)
	gyro = GYRO.GYRO()
	time.sleep(0.1)
	gyro.sensor_calib()
	ui = VSplit(
		Log(title='logs', border_color=5, color=3),
		HSplit(
			VGauge(title="accel.x", val=0, border_color=2),
			VGauge(title="accel.y", val=0, border_color=2),
			VGauge(title="accel.z", val=0, border_color=2),
			VGauge(title="gyro.x",val=0, border_color=2),
			VGauge(title="gyro.y",val=0, border_color=2),
			VGauge(title="gyro.z",val=0, border_color=2),
			VGauge(title="mag.x",val=0, border_color=2),
			VGauge(title="mag.y",val=0, border_color=2),
			VGauge(title="mag.z",val=0, border_color=2),
		),
		title='ADRSZGY',
	)
	log = ui.items[0]
	log.append("0 -----")
	log.append("1 Hello")
	log.append("2 -----")
	min = [0] * 3
	max = [0] * 3
	prev = time.time()
	while True:
		now = time.time()
		vals = gyro.get_sense_value()
		for i, j in ((0,0),(0,1),(0,2),(1,3),(1,4),(1,5),(2,6),(2,7),(2,8)):
			n = vals[j]
			if min[i] > n:
				min[i] = n
			if max[i] < n:
				max[i] = n
			if min[i] < max[i]:
				n = ( n - min[i] ) * 100 / ( max[i] - min[i] )
			else:
				n = 0
			ui.items[-1].items[j].value = n
		ui.display()
		prev = now
		time.sleep(0.05)
