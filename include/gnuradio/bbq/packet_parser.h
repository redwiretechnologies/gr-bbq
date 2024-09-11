/* -*- c++ -*- */
/*
 * Copyright 2024 Red Wire Technologies.
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 */

#ifndef INCLUDED_BBQ_PACKET_PARSER_H
#define INCLUDED_BBQ_PACKET_PARSER_H

#include <gnuradio/bbq/api.h>
#include <gnuradio/block.h>

namespace gr {
  namespace bbq {

    /*!
     * \brief <+description of block+>
     * \ingroup bbq
     *
     */
    class BBQ_API packet_parser : virtual public gr::block
    {
     public:
      typedef std::shared_ptr<packet_parser> sptr;

      /*!
       * \brief Return a shared_ptr to a new instance of bbq::packet_parser.
       *
       * To avoid accidental use of raw pointers, bbq::packet_parser's
       * constructor is in a private implementation
       * class. bbq::packet_parser::make is the public interface for
       * creating new instances.
       */
      static sptr make();
    };

  } // namespace bbq
} // namespace gr

#endif /* INCLUDED_BBQ_PACKET_PARSER_H */
