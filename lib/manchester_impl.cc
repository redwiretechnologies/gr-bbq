/* -*- c++ -*- */
/*
 * Copyright 2024 Red Wire Technologies.
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 */

#include <gnuradio/io_signature.h>
#include "manchester_impl.h"
#include <gnuradio/filter/firdes.h>
#include <volk/volk.h>
#include <stdio.h>

namespace gr {
  namespace bbq {

    manchester::sptr
    manchester::make(uint16_t sps, const std::vector<float>& preamble, bool verbose, int coding_scheme)
    {
      return gnuradio::make_block_sptr<manchester_impl>(
        sps, preamble, verbose, coding_scheme);
    }

    /*
     * The private constructor
     */
    manchester_impl::manchester_impl(uint16_t sps, const std::vector<float>& preamble, bool verbose, int coding_scheme)
      : gr::block("manchester",
              gr::io_signature::make(0, 0, 0),
              gr::io_signature::make(0, 0, 0)),
              d_sps(sps),
              d_preamble(preamble),
              d_verbose(verbose),
              d_coding_scheme(coding_scheme)
    {
      message_port_register_in(pmt::mp("symbols_in"));
      set_msg_handler(pmt::mp("symbols_in"), [this](pmt::pmt_t msg){ this->message_handler(msg); });
      message_port_register_out(pmt::mp("data_out"));
      message_port_register_out(pmt::mp("corr_out"));

      //  Build the full sps sof code        
      for(int k=0; k < 32; k++){
        for(unsigned long m=0; m < sps; m++){
          d_sps_sof.push_back(d_preamble[k]);
        }
      }
        
      //  Set up the correlation filters for the preamble
      std::reverse(d_sps_sof.begin(), d_sps_sof.end());
      d_sof_filter = new kernel::fir_filter_fff(d_sps_sof);
    }

    /*
     * Our virtual destructor.
     */
    manchester_impl::~manchester_impl()
    {
      delete d_sof_filter;
    }

    void
    manchester_impl::message_handler(pmt::pmt_t msg)
    {
      pmt::pmt_t out_vector;
      pmt::pmt_t corr_vector;
      pmt::pmt_t meta = pmt::car(msg);
      pmt::pmt_t in_vector = pmt::cdr(msg);
      uint32_t v_len = pmt::length(in_vector);
         
      std::vector<float> data_in = pmt::f32vector_elements(in_vector);

      std::vector<float> d_sof_corr, in_data;
      d_sof_corr.resize(v_len);
      in_data.clear();

      //  Pad the data vector with zeroes to flush the filter after completion
      in_data.insert(in_data.end(), data_in.begin(), data_in.end());
      for(unsigned long p=0; p<d_sps_sof.size()*d_sps; p++){
        in_data.push_back(0);
      }

      d_sof_filter->filterN(d_sof_corr.data(), in_data.data(), v_len);  
      
      std::vector<float>::iterator sof_result;
      uint16_t sof_loc = 0;
      uint8_t n_packets = 4;
      float threshold = d_sps_sof.size()*0.8;
      uint16_t packet_size = d_sps*420;

      //  Decoding the signal         
      for(uint8_t k=0; k<n_packets; k++){
        // printf("[Manchester Decoder] sof_loc = %d\n", sof_loc);
        // TODO: These needs to be a better algorithm to find the first packet in the burst.
        if(k>0){
          sof_result = std::max_element(d_sof_corr.begin() + sof_loc + d_sps*10, d_sof_corr.begin() + sof_loc + packet_size);
        }
        else{
          sof_result = std::max_element(d_sof_corr.begin(), d_sof_corr.begin() + sof_loc + packet_size);
        }
        // sof_result = std::max_element(d_sof_corr.begin() + sof_loc, d_sof_corr.end());
        // sof_result = std::upper_bound(d_sof_corr.begin(), d_sof_corr.end(), threshold);
        sof_loc = std::distance(d_sof_corr.begin(), sof_result);
        if(d_verbose){
          printf("[Manchester Decoder] sof_loc = %d\n", sof_loc);
          printf("[Manchester Decoder] d_sof_corr[sof_loc] = %f\n", d_sof_corr[sof_loc]);
          printf("[Manchester Decoder] threshold = %f\n", threshold);
        }
        
        if((d_sof_corr[sof_loc] > threshold) & (sof_loc < d_sof_corr.size())){
          std::vector<uint8_t> packet_data;
          packet_data.clear();
        
          bool edge_found;
          float temp_bit_1;
          float temp_bit_2;
          uint16_t n = sof_loc + d_preamble.size()*d_sps;
        
          while(n < in_data.size()){
            edge_found = false;
            temp_bit_1 = in_data[n];
            n++;
            while(edge_found == false){
              if(temp_bit_1 == in_data[n]){
                n++;
              }
              else{
                if(temp_bit_1 > in_data[n]){
                  //  This is a falling edge
                  packet_data.push_back(code[d_coding_scheme][0]);
                }
                else if(temp_bit_1 < in_data[n]){
                  //  This is a rising edge
                  packet_data.push_back(code[d_coding_scheme][1]);
                }
                else{
                  std::cout << "Error: invalid values" << std::endl;
                  break;
                }
                edge_found = true;
                n = n + d_sps*1.5;
              }
            }
          }

          out_vector = pmt::make_blob(&packet_data[0], 96);
          message_port_pub(pmt::mp("data_out"), pmt::cons(meta, out_vector));
        }
        else{
          if(d_verbose){printf("[Manchester Decoder] Insufficient Data");}
        }
      }
      corr_vector = pmt::init_f32vector(d_sof_corr.size(), (const float *)&d_sof_corr[0]);
      message_port_pub(pmt::mp("corr_out"), pmt::cons(meta, corr_vector));
    }

  } /* namespace bbq */
} /* namespace gr */
