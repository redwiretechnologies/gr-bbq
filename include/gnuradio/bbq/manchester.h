/* -*- c++ -*- */
/*
 * Copyright 2024 Red Wire Technologies.
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 */

#ifndef INCLUDED_BBQ_MANCHESTER_H
#define INCLUDED_BBQ_MANCHESTER_H

#include <gnuradio/bbq/api.h>
#include <gnuradio/block.h>

namespace gr {
  namespace bbq {

    /*!
     * \brief <+description of block+>
     * \ingroup bbq
     *
     */
    class BBQ_API manchester : virtual public gr::block
    {
     public:
      typedef std::shared_ptr<manchester> sptr;

      /*!
       * \brief Return a shared_ptr to a new instance of bbq::manchester.
       *
       * To avoid accidental use of raw pointers, bbq::manchester's
       * constructor is in a private implementation
       * class. bbq::manchester::make is the public interface for
       * creating new instances.
       */
      static sptr make(uint16_t sps, const std::vector<float>& preamble, bool verbose, int coding_scheme);
    };

  } // namespace bbq
} // namespace gr

#endif /* INCLUDED_BBQ_MANCHESTER_H */
