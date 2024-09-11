/* -*- c++ -*- */
/*
 * Copyright 2024 Red Wire Technologies.
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 */

#ifndef INCLUDED_BBQ_PACKET_PARSER_IMPL_H
#define INCLUDED_BBQ_PACKET_PARSER_IMPL_H

#include <gnuradio/bbq/packet_parser.h>

namespace gr {
  namespace bbq {

    class packet_parser_impl : public packet_parser
    {
     private:
      bool d_verbose = true;

     public:
      packet_parser_impl();
      ~packet_parser_impl();

      // Where all the action really happens
      void message_handler(pmt::pmt_t msg);
    };

  } // namespace bbq
} // namespace gr

#endif /* INCLUDED_BBQ_PACKET_PARSER_IMPL_H */
