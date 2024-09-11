/* -*- c++ -*- */
/*
 * Copyright 2024 Red Wire Technologies.
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 */

#include <gnuradio/io_signature.h>
#include "packet_parser_impl.h"

namespace gr {
  namespace bbq {

    packet_parser::sptr
    packet_parser::make()
    {
      return gnuradio::make_block_sptr<packet_parser_impl>(
        );
    }

    /*
     * The private constructor
     */
    packet_parser_impl::packet_parser_impl()
      : gr::block("packet_parser",
              gr::io_signature::make(0, 0, 0),
              gr::io_signature::make(0, 0, 0))
    {
      message_port_register_in(pmt::mp("bits_in"));
      set_msg_handler(pmt::mp("bits_in"), [this](pmt::pmt_t msg){ this->message_handler(msg); });
      message_port_register_out(pmt::mp("data_out"));
    }

    /*
     * Our virtual destructor.
     */
    packet_parser_impl::~packet_parser_impl()
    {
    }

    void
    packet_parser_impl::message_handler(pmt::pmt_t msg)
    {
      pmt::pmt_t out_meta;
      pmt::pmt_t out_vector;
      pmt::pmt_t meta = pmt::car(msg);
      pmt::pmt_t in_vector = pmt::cdr(msg);

      uint8_t packet_type = 0;
      int temp_1 = 0;
      int temp_2 = 0;
      uint16_t crc_packet = 0;
      uint64_t packet = 0;
         
      std::vector<uint8_t> data_in = pmt::u8vector_elements(in_vector);
      std::vector<uint8_t> packet_vector;

      // Packet
      for(uint8_t k=0; k<40; k++){
        packet += ((uint64_t) data_in[k*2 + 17] << (39-k));
      }

      packet_vector.push_back((packet >> 32) & 0x00000000000000ff);
      packet_vector.push_back((packet >> 24) & 0x00000000000000ff);
      packet_vector.push_back((packet >> 16) & 0x00000000000000ff);
      packet_vector.push_back((packet >> 8) & 0x00000000000000ff);
      packet_vector.push_back(packet & 0x00000000000000ff);

      // Parse Packet
      packet_type = (packet >> 36) & 0x000000000000000f;
      temp_1 = (packet >> 26) & 0x00000000000003ff;
      temp_2 = (packet >> 16) & 0x00000000000003ff;
      crc_packet = packet & 0x000000000000ffff;

      if(d_verbose){
        printf("[Redi Chek Parser] Packet Type: %u\n", packet_type);
        if(temp_1 == 0){
          printf("[Redi Chek Parser] Food Probe Disconnected\n");        
        }
        else{
          printf("[Redi Chek Parser] Food Temp: %d C\n", temp_1-532);
        }
        
        if(temp_2 == 0){
          printf("[Redi Chek Parser] BBQ Probe Disconnected\n");        
        }
        else{
          printf("[Redi Chek Parser] BBQ Temp: %d C\n", temp_2-532);
        }

        printf("[Redi Chek Parser] Packet: %lx\n", packet);
        printf("[Redi Chek Parser] Checksum: %04x\n\n", crc_packet);
      }

      out_meta = pmt::make_dict();
      out_meta = dict_add(out_meta, pmt::intern("Packet Type"), pmt::from_uint64(packet_type));
      out_meta = dict_add(out_meta, pmt::intern("Food Probe"), pmt::from_long(temp_1-532));
      out_meta = dict_add(out_meta, pmt::intern("BBQ Probe"), pmt::from_long(temp_2-532));

      out_vector = pmt::make_blob(&packet_vector[0], 5);

      message_port_pub(pmt::mp("data_out"), pmt::cons(out_meta, out_vector));
    }

  } /* namespace bbq */
} /* namespace gr */
