#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Not titled yet
# Author: jbonior
# GNU Radio version: v3.11.0.0git-802-g61ba4c66

from PyQt5 import Qt
from gnuradio import qtgui
from gnuradio import bbq
from gnuradio import blocks
from gnuradio import gr
from gnuradio.filter import firdes
from gnuradio.fft import window
import sys
import signal
from PyQt5 import Qt
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import rwt_tools
import numpy as np
import rwt
import pmt
import sip
import threading



class redi_check_rx(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Not titled yet", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Not titled yet")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except BaseException as exc:
            print(f"Qt GUI: Could not set Icon: {str(exc)}", file=sys.stderr)
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("gnuradio/flowgraphs", "redi_check_rx")

        try:
            geometry = self.settings.value("geometry")
            if geometry:
                self.restoreGeometry(geometry)
        except BaseException as exc:
            print(f"Qt GUI: Could not restore geometry: {str(exc)}", file=sys.stderr)
        self.flowgraph_started = threading.Event()

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 2e6
        self.preamble = preamble = [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0]
        self.center_freq = center_freq = 433.94e6

        ##################################################
        # Blocks
        ##################################################

        self.rwt_tools_stream_to_message_0 = rwt_tools.stream_to_message(2, 0, 1024, 10000, 10000)
        self.rwt_tools_ook_preamble_correlator_0 = rwt_tools.ook_preamble_correlator(2000000, 4000, preamble, len(preamble)*500*0.5)
        self.rwt_source_0 = None
        rwt_cfg = {
          "rx_freq": str(int(center_freq)),
          "rx_bw": str(int(int(samp_rate))),
          "samplerate": str(int(int(samp_rate))),
          "rx_rfport1": "A_BALANCED",
          "rx_rfport2": "A_BALANCED",
          "escape": str(0xAAAAAAAAAAAAAAAA),
          "rx_gain1": str(50.0),
          "rx_gain1_mode": "manual",
          "rx_gain2": str(50.0),
          "rx_gain2_mode": "manual",
          "quadrature": str(int(True)),
          "rfdc": str(int(True)),
          "bbdc": str(int(True)),
          "decimation_arbitrary": str(int(0)),
          "correction_enable": str(int(True)),
          "bypass_enable": str(int(False)),
        }
        rwt_extra = {} if '' == "" else dict(x.split('=') for x in ''.split(','))
        rwt_cfg.update(rwt_extra)
        self.rwt_source_0 = rwt.rwt_source(
          pmt.to_pmt(rwt_cfg), True, False,
          0x9D000000, '', True, True,
          "default", False, 32000,
          "ad9361-phy", "cf-ad9361-lpc", "cf-ad9361-dds-core-lpc")
        self.qtgui_freq_sink_x_0 = qtgui.freq_sink_c(
            16384, #size
            window.WIN_BLACKMAN_hARRIS, #wintype
            center_freq, #fc
            samp_rate, #bw
            "", #name
            1,
            None # parent
        )
        self.qtgui_freq_sink_x_0.set_update_time(0.10)
        self.qtgui_freq_sink_x_0.set_y_axis((-140), 10)
        self.qtgui_freq_sink_x_0.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_AUTO, 0.2, 0, "")
        self.qtgui_freq_sink_x_0.enable_autoscale(False)
        self.qtgui_freq_sink_x_0.enable_grid(False)
        self.qtgui_freq_sink_x_0.set_fft_average(1.0)
        self.qtgui_freq_sink_x_0.enable_axis_labels(True)
        self.qtgui_freq_sink_x_0.enable_control_panel(True)
        self.qtgui_freq_sink_x_0.set_fft_window_normalized(False)



        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_0_win = sip.wrapinstance(self.qtgui_freq_sink_x_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_freq_sink_x_0_win)
        self.blocks_threshold_ff_0_0 = blocks.threshold_ff(0.05, 0.15, 0)
        self.blocks_null_sink_0 = blocks.null_sink(gr.sizeof_float*1)
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_ff(2)
        self.blocks_keep_one_in_n_0 = blocks.keep_one_in_n(gr.sizeof_float*1, 100)
        self.blocks_complex_to_mag_0_0_0 = blocks.complex_to_mag(1)
        self.blocks_add_const_vxx_0 = blocks.add_const_ff((-1))
        self.bbq_packet_to_zmq_0 = bbq.packet_to_zmq('tcp://*:4001')
        self.bbq_packet_parser_0 = bbq.packet_parser()
        self.bbq_manchester_1 = bbq.manchester(5, [1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 1, 1, -1, -1, 1, 1, -1, -1, 1, 1, -1, -1, 1, 1, -1], False, 1)


        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.bbq_manchester_1, 'data_out'), (self.bbq_packet_parser_0, 'bits_in'))
        self.msg_connect((self.bbq_packet_parser_0, 'data_out'), (self.bbq_packet_to_zmq_0, 'packet_in'))
        self.msg_connect((self.rwt_tools_stream_to_message_0, 'message_out'), (self.bbq_manchester_1, 'symbols_in'))
        self.connect((self.blocks_add_const_vxx_0, 0), (self.rwt_tools_ook_preamble_correlator_0, 0))
        self.connect((self.blocks_complex_to_mag_0_0_0, 0), (self.blocks_threshold_ff_0_0, 0))
        self.connect((self.blocks_keep_one_in_n_0, 0), (self.rwt_tools_stream_to_message_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.blocks_add_const_vxx_0, 0))
        self.connect((self.blocks_threshold_ff_0_0, 0), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.rwt_source_0, 0), (self.blocks_complex_to_mag_0_0_0, 0))
        self.connect((self.rwt_source_0, 0), (self.qtgui_freq_sink_x_0, 0))
        self.connect((self.rwt_tools_ook_preamble_correlator_0, 0), (self.blocks_keep_one_in_n_0, 0))
        self.connect((self.rwt_tools_ook_preamble_correlator_0, 1), (self.blocks_null_sink_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("gnuradio/flowgraphs", "redi_check_rx")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.qtgui_freq_sink_x_0.set_frequency_range(self.center_freq, self.samp_rate)
        self.rwt_source_0.set_config("rx_bw", str(int(int(self.samp_rate))))
        self.rwt_source_0.set_config("samplerate", str(int(int(self.samp_rate))))

    def get_preamble(self):
        return self.preamble

    def set_preamble(self, preamble):
        self.preamble = preamble
        self.rwt_tools_ook_preamble_correlator_0.set_preamble(self.preamble)
        self.rwt_tools_ook_preamble_correlator_0.set_threshold(len(self.preamble)*500*0.5)

    def get_center_freq(self):
        return self.center_freq

    def set_center_freq(self, center_freq):
        self.center_freq = center_freq
        self.qtgui_freq_sink_x_0.set_frequency_range(self.center_freq, self.samp_rate)
        self.rwt_source_0.set_config("rx_freq", str(int(self.center_freq)))




def main(top_block_cls=redi_check_rx, options=None):

    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

    tb.start()
    tb.flowgraph_started.set()

    tb.show()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    qapp.exec_()

if __name__ == '__main__':
    main()
