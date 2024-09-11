#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2024 Red Wire Technologies.
#
# SPDX-License-Identifier: GPL-3.0-or-later
#


import numpy
from gnuradio import gr
import pmt
import zmq
import json
from datetime import datetime

class packet_to_zmq(gr.sync_block):
    """
    docstring for block packet_to_zmq
    """
    def __init__(self, address):
        gr.sync_block.__init__(self,
            name="packet_to_zmq",
            in_sig=None,
            out_sig=None)
        
        self.message_port_register_in(pmt.intern("packet_in"))
        self.set_msg_handler(pmt.intern("packet_in"), self.packet_handler)

        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.PUB)
        self.socket.bind(address)


    def packet_handler(self, packet):
        meta = pmt.car(packet)
        data = pmt.to_python(pmt.cdr(packet))

        now = datetime.utcnow()
        rx_time = now.strftime("%H:%M:%S.%f")

        packet_type = pmt.to_python(pmt.dict_ref(meta, pmt.intern("Packet Type"), pmt.from_uint64(0)))
        food_temp = pmt.to_python(pmt.dict_ref(meta, pmt.intern("Food Probe"), pmt.from_uint64(0)))
        bbq_temp = pmt.to_python(pmt.dict_ref(meta, pmt.intern("BBQ Probe"), pmt.from_uint64(0)))

        data = {'packetType': packet_type, 'foodTemp': food_temp, 'bbqTemp': bbq_temp, 'timeData': rx_time}

        data_json = json.dumps(data)
        self.socket.send_string(data_json)