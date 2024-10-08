# Copyright 2020 Free Software Foundation, Inc.
#
# This file is part of GNU Radio
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

########################################################################
# Check if there is C++ code at all
########################################################################
if(NOT bbq_sources)
    MESSAGE(STATUS "No C++ sources... skipping python bindings")
    return()
endif(NOT bbq_sources)

########################################################################
# Check for pygccxml
########################################################################
GR_PYTHON_CHECK_MODULE_RAW(
    "pygccxml"
    "import pygccxml"
    PYGCCXML_FOUND
    )

include(GrPybind)

########################################################################
# Python Bindings
########################################################################

list(APPEND bbq_python_files
    manchester_python.cc
    packet_parser_python.cc python_bindings.cc)

GR_PYBIND_MAKE_OOT(bbq
   ../../..
   gr::bbq
   "${bbq_python_files}")

# copy bindings extension for use in QA test module
add_custom_command(TARGET bbq_python POST_BUILD
    COMMAND ${CMAKE_COMMAND} -E copy $<TARGET_FILE:bbq_python>
    ${PROJECT_BINARY_DIR}/test_modules/gnuradio/bbq/
)

install(TARGETS bbq_python DESTINATION ${GR_PYTHON_DIR}/gnuradio/bbq COMPONENT pythonapi)
