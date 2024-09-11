/* -*- c++ -*- */
/*
 * Copyright 2024 Red Wire Technologies.
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 */

#ifndef INCLUDED_BBQ_MANCHESTER_IMPL_H
#define INCLUDED_BBQ_MANCHESTER_IMPL_H

#include <gnuradio/bbq/manchester.h>
#include <gnuradio/filter/fir_filter.h>
#include <vector>

using namespace gr::filter;

namespace gr {
  namespace bbq {

    class manchester_impl : public manchester
    {
     private:
      uint16_t d_sps;
      int d_coding_scheme;
      std::vector<float> d_preamble;
      std::vector<float> d_sps_sof;
      bool d_verbose;
      uint8_t code[2][2] = {{0, 1}, {1, 0}};

      kernel::fir_filter_fff* d_sof_filter;

     public:
      manchester_impl(uint16_t sps, const std::vector<float>& preamble, bool verbose, int coding_scheme);
      ~manchester_impl();

      // Where all the action really happens
      void message_handler(
              pmt::pmt_t message
      );
    };

  } // namespace bbq
} // namespace gr

#endif /* INCLUDED_BBQ_MANCHESTER_IMPL_H */
