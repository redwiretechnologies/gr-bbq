find_package(PkgConfig)

PKG_CHECK_MODULES(PC_GR_BBQ gnuradio-bbq)

FIND_PATH(
    GR_BBQ_INCLUDE_DIRS
    NAMES gnuradio/bbq/api.h
    HINTS $ENV{BBQ_DIR}/include
        ${PC_BBQ_INCLUDEDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/include
          /usr/local/include
          /usr/include
)

FIND_LIBRARY(
    GR_BBQ_LIBRARIES
    NAMES gnuradio-bbq
    HINTS $ENV{BBQ_DIR}/lib
        ${PC_BBQ_LIBDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/lib
          ${CMAKE_INSTALL_PREFIX}/lib64
          /usr/local/lib
          /usr/local/lib64
          /usr/lib
          /usr/lib64
          )

include("${CMAKE_CURRENT_LIST_DIR}/gnuradio-bbqTarget.cmake")

INCLUDE(FindPackageHandleStandardArgs)
FIND_PACKAGE_HANDLE_STANDARD_ARGS(GR_BBQ DEFAULT_MSG GR_BBQ_LIBRARIES GR_BBQ_INCLUDE_DIRS)
MARK_AS_ADVANCED(GR_BBQ_LIBRARIES GR_BBQ_INCLUDE_DIRS)
