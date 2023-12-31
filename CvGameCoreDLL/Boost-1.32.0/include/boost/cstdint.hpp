//  boost cstdint.hpp header file  ------------------------------------------//

//  (C) Copyright Beman Dawes 1999.
//  (C) Copyright Jens Mauer 2001
//  (C) Copyright John Maddock 2001
//  Distributed under the Boost
//  Software License, Version 1.0. (See accompanying file
//  LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)

//  See http://www.boost.org/libs/integer for documentation.

//  Revision History
//   31 Oct 01  use BOOST_HAS_LONG_LONG to check for "long long" (Jens M.)
//   16 Apr 01  check LONGLONG_MAX when looking for "long long" (Jens Maurer)
//   23 Jan 01  prefer "long" over "int" for int32_t and intmax_t (Jens Maurer)
//   12 Nov 00  Merged <boost/stdint.h> (Jens Maurer)
//   23 Sep 00  Added INTXX_C macro support (John Maddock).
//   22 Sep 00  Better 64-bit support (John Maddock)
//   29 Jun 00  Reimplement to avoid including stdint.h within namespace boost
//    8 Aug 99  Initial version (Beman Dawes)


#ifndef BOOST_CSTDINT_HPP
#define BOOST_CSTDINT_HPP

#include <boost/config.hpp>


#ifdef BOOST_HAS_STDINT_H

// The following #include is an implementation artifact; not part of interface.
# ifdef __hpux
// HP-UX has a vaguely nice <stdint.h> in a non-standard location
#   include <inttypes.h>
#   ifdef __STDC_32_MODE__
      // this is triggered with GCC, because it defines __cplusplus < 199707L
#     define BOOST_NO_INT64_T
#   endif
# elif defined(__FreeBSD__) || defined(__IBMCPP__)
#   include <inttypes.h>
# else
#   include <stdint.h>
# endif

namespace boost
{

  using ::int8_t;
  using ::int_least8_t;
  using ::int_fast8_t;
  using ::uint8_t;
  using ::uint_least8_t;
  using ::uint_fast8_t;

  using ::int16_t;
  using ::int_least16_t;
  using ::int_fast16_t;
  using ::uint16_t;
  using ::uint_least16_t;
  using ::uint_fast16_t;

  using ::int32_t;
  using ::int_least32_t;
  using ::int_fast32_t;
  using ::uint32_t;
  using ::uint_least32_t;
  using ::uint_fast32_t;

# ifndef BOOST_NO_INT64_T

  using ::int64_t;
  using ::int_least64_t;
  using ::int_fast64_t;
  using ::uint64_t;
  using ::uint_least64_t;
  using ::uint_fast64_t;

# endif

  using ::intmax_t;
  using ::uintmax_t;

} // namespace boost

#elif defined(__FreeBSD__) && (__FreeBSD__ <= 4) || defined(__osf__)
// FreeBSD and Tru64 have an <inttypes.h> that contains much of what we need.
# include <inttypes.h>

namespace boost {

  using ::int8_t;
  typedef int8_t int_least8_t;
  typedef int8_t int_fast8_t;
  using ::uint8_t;
  typedef uint8_t uint_least8_t;
  typedef uint8_t uint_fast8_t;

  using ::int16_t;
  typedef int16_t int_least16_t;
  typedef int16_t int_fast16_t;
  using ::uint16_t;
  typedef uint16_t uint_least16_t;
  typedef uint16_t uint_fast16_t;

  using ::int32_t;
  typedef int32_t int_least32_t;
  typedef int32_t int_fast32_t;
  using ::uint32_t;
  typedef uint32_t uint_least32_t;
  typedef uint32_t uint_fast32_t;

# ifndef BOOST_NO_INT64_T

  using ::int64_t;
  typedef int64_t int_least64_t;
  typedef int64_t int_fast64_t;
  using ::uint64_t;
  typedef uint64_t uint_least64_t;
  typedef uint64_t uint_fast64_t;

  typedef int64_t intmax_t;
  typedef uint64_t uintmax_t;

# else

  typedef int32_t intmax_t;
  typedef uint32_t uintmax_t;

# endif

} // namespace boost

#else  // BOOST_HAS_STDINT_H

# include <boost/limits.hpp> // implementation artifact; not part of interface


namespace boost
{

//  These are fairly safe guesses for some 16-bit, and most 32-bit and 64-bit
//  platforms.  For other systems, they will have to be hand tailored.
//
//  Because the fast types are assumed to be the same as the undecorated types,
//  it may be possible to hand tailor a more efficient implementation.  Such
//  an optimization may be illusionary; on the Intel x86-family 386 on, for
//  example, byte arithmetic and load/stores are as fast as "int" sized ones.

//  8-bit types  ------------------------------------------------------------//

# if UCHAR_MAX == 0xff
     typedef signed char     int8_t;
     typedef signed char     int_least8_t;
     typedef signed char     int_fast8_t;
     typedef unsigned char   uint8_t;
     typedef unsigned char   uint_least8_t;
     typedef unsigned char   uint_fast8_t;
# else
#    error defaults not correct; you must hand modify boost/cstdint.hpp
# endif

//  16-bit types  -----------------------------------------------------------//

# if USHRT_MAX == 0xffff
#  if defined(__crayx1)
     // The Cray X1 has a 16-bit short, however it is not recommend
     // for use in performance critical code.
     typedef short           int16_t;
     typedef short           int_least16_t;
     typedef int             int_fast16_t;
     typedef unsigned short  uint16_t;
     typedef unsigned short  uint_least16_t;
     typedef unsigned int    uint_fast16_t;
#  else
     typedef short           int16_t;
     typedef short           int_least16_t;
     typedef short           int_fast16_t;
     typedef unsigned short  uint16_t;
     typedef unsigned short  uint_least16_t;
     typedef unsigned short  uint_fast16_t;
#  endif
# elif (USHRT_MAX == 0xffffffff) && defined(CRAY)
     // no 16-bit types on Cray:
     typedef short           int_least16_t;
     typedef short           int_fast16_t;
     typedef unsigned short  uint_least16_t;
     typedef unsigned short  uint_fast16_t;
# else
#    error defaults not correct; you must hand modify boost/cstdint.hpp
# endif

//  32-bit types  -----------------------------------------------------------//

# if ULONG_MAX == 0xffffffff
     typedef long            int32_t;
     typedef long            int_least32_t;
     typedef long            int_fast32_t;
     typedef unsigned long   uint32_t;
     typedef unsigned long   uint_least32_t;
     typedef unsigned long   uint_fast32_t;
# elif UINT_MAX == 0xffffffff
     typedef int             int32_t;
     typedef int             int_least32_t;
     typedef int             int_fast32_t;
     typedef unsigned int    uint32_t;
     typedef unsigned int    uint_least32_t;
     typedef unsigned int    uint_fast32_t;
# else
#    error defaults not correct; you must hand modify boost/cstdint.hpp
# endif

//  64-bit types + intmax_t and uintmax_t  ----------------------------------//

# if defined(BOOST_HAS_LONG_LONG) && \
   !defined(BOOST_MSVC) && !defined(__BORLANDC__) && \
   (!defined(__GLIBCPP__) || defined(_GLIBCPP_USE_LONG_LONG)) && \
   (defined(ULLONG_MAX) || defined(ULONG_LONG_MAX) || defined(ULONGLONG_MAX))
#    if defined(__hpux)
     // HP-UX's value of ULONG_LONG_MAX is unusable in preprocessor expressions
#    elif (defined(ULLONG_MAX) && ULLONG_MAX == 18446744073709551615ULL) || (defined(ULONG_LONG_MAX) && ULONG_LONG_MAX == 18446744073709551615ULL) || (defined(ULONGLONG_MAX) && ULONGLONG_MAX == 18446744073709551615ULL)
                                                                 // 2**64 - 1
#    else
#       error defaults not correct; you must hand modify boost/cstdint.hpp
#    endif

     typedef  ::boost::long_long_type            intmax_t;
     typedef  ::boost::ulong_long_type   uintmax_t;
     typedef  ::boost::long_long_type            int64_t;
     typedef  ::boost::long_long_type            int_least64_t;
     typedef  ::boost::long_long_type            int_fast64_t;
     typedef  ::boost::ulong_long_type   uint64_t;
     typedef  ::boost::ulong_long_type   uint_least64_t;
     typedef  ::boost::ulong_long_type   uint_fast64_t;

# elif ULONG_MAX != 0xffffffff

#    if ULONG_MAX == 18446744073709551615 // 2**64 - 1
     typedef long                 intmax_t;
     typedef unsigned long        uintmax_t;
     typedef long                 int64_t;
     typedef long                 int_least64_t;
     typedef long                 int_fast64_t;
     typedef unsigned long        uint64_t;
     typedef unsigned long        uint_least64_t;
     typedef unsigned long        uint_fast64_t;
#    else
#       error defaults not correct; you must hand modify boost/cstdint.hpp
#    endif
# elif defined(__GNUC__) && defined(BOOST_HAS_LONG_LONG)
     __extension__ typedef long long            intmax_t;
     __extension__ typedef unsigned long long   uintmax_t;
     __extension__ typedef long long            int64_t;
     __extension__ typedef long long            int_least64_t;
     __extension__ typedef long long            int_fast64_t;
     __extension__ typedef unsigned long long   uint64_t;
     __extension__ typedef unsigned long long   uint_least64_t;
     __extension__ typedef unsigned long long   uint_fast64_t;
# elif defined(BOOST_HAS_MS_INT64)
     //
     // we have Borland/Intel/Microsoft __int64:
     //
     typedef __int64             intmax_t;
     typedef unsigned __int64    uintmax_t;
     typedef __int64             int64_t;
     typedef __int64             int_least64_t;
     typedef __int64             int_fast64_t;
     typedef unsigned __int64    uint64_t;
     typedef unsigned __int64    uint_least64_t;
     typedef unsigned __int64    uint_fast64_t;
# else // assume no 64-bit integers
#  define BOOST_NO_INT64_T
     typedef int32_t              intmax_t;
     typedef uint32_t             uintmax_t;
# endif

} // namespace boost


#endif // BOOST_HAS_STDINT_H

#endif // BOOST_CSTDINT_HPP


/****************************************************

Macro definition section:

Define various INTXX_C macros only if
__STDC_CONSTANT_MACROS is defined.

Undefine the macros if __STDC_CONSTANT_MACROS is
not defined and the macros are (cf <cassert>).

Added 23rd September 2000 (John Maddock).
Modified 11th September 2001 to be excluded when
BOOST_HAS_STDINT_H is defined (John Maddock).

******************************************************/

#if defined(__STDC_CONSTANT_MACROS) && !defined(BOOST__STDC_CONSTANT_MACROS_DEFINED) && !defined(BOOST_HAS_STDINT_H)
# define BOOST__STDC_CONSTANT_MACROS_DEFINED
# if defined(BOOST_HAS_MS_INT64)
//
// Borland/Intel/Microsoft compilers have width specific suffixes:
//
#  define INT8_C(value)     value##i8
#  define INT16_C(value)    value##i16
#  define INT32_C(value)    value##i32
#  define INT64_C(value)    value##i64
#  ifdef __BORLANDC__
    // Borland bug: appending ui8 makes the type a signed char
#   define UINT8_C(value)    static_cast<unsigned char>(value##u)
#  else
#   define UINT8_C(value)    value##ui8
#  endif
#  define UINT16_C(value)   value##ui16
#  define UINT32_C(value)   value##ui32
#  define UINT64_C(value)   value##ui64
#  define INTMAX_C(value)   value##i64
#  define UINTMAX_C(value)  value##ui64

# else
//  do it the old fashioned way:

//  8-bit types  ------------------------------------------------------------//

#  if UCHAR_MAX == 0xff
#   define INT8_C(value) static_cast<boost::int8_t>(value)
#   define UINT8_C(value) static_cast<boost::uint8_t>(value##u)
#  endif

//  16-bit types  -----------------------------------------------------------//

#  if USHRT_MAX == 0xffff
#   define INT16_C(value) static_cast<boost::int16_t>(value)
#   define UINT16_C(value) static_cast<boost::uint16_t>(value##u)
#  endif

//  32-bit types  -----------------------------------------------------------//

#  if UINT_MAX == 0xffffffff
#   define INT32_C(value) value
#   define UINT32_C(value) value##u
#  elif ULONG_MAX == 0xffffffff
#   define INT32_C(value) value##L
#   define UINT32_C(value) value##uL
#  endif

//  64-bit types + intmax_t and uintmax_t  ----------------------------------//

#  if defined(BOOST_HAS_LONG_LONG) && \
    (defined(ULLONG_MAX) || defined(ULONG_LONG_MAX) || defined(ULONGLONG_MAX))

#    if defined(__hpux)
     // HP-UX's value of ULONG_LONG_MAX is unusable in preprocessor expressions
#    elif (defined(ULLONG_MAX) && ULLONG_MAX == 18446744073709551615U) ||  \
        (defined(ULONG_LONG_MAX) && ULONG_LONG_MAX == 18446744073709551615U) ||  \
        (defined(ULONGLONG_MAX) && ULONGLONG_MAX == 18446744073709551615U)

#    else
#       error defaults not correct; you must hand modify boost/cstdint.hpp
#    endif
#    define INT64_C(value) value##LL
#    define UINT64_C(value) value##uLL
#  elif ULONG_MAX != 0xffffffff

#    if ULONG_MAX == 18446744073709551615 // 2**64 - 1
#       define INT64_C(value) value##L
#       define UINT64_C(value) value##uL
#    else
#       error defaults not correct; you must hand modify boost/cstdint.hpp
#    endif
#  endif

#  ifdef BOOST_NO_INT64_T
#   define INTMAX_C(value) INT32_C(value)
#   define UINTMAX_C(value) UINT32_C(value)
#  else
#   define INTMAX_C(value) INT64_C(value)
#   define UINTMAX_C(value) UINT64_C(value)
#  endif

# endif // Borland/Microsoft specific width suffixes


#elif defined(BOOST__STDC_CONSTANT_MACROS_DEFINED) && !defined(__STDC_CONSTANT_MACROS) && !defined(BOOST_HAS_STDINT_H)
//
// undef all the macros:
//
# undef INT8_C
# undef INT16_C
# undef INT32_C
# undef INT64_C
# undef UINT8_C
# undef UINT16_C
# undef UINT32_C
# undef UINT64_C
# undef INTMAX_C
# undef UINTMAX_C

#endif // __STDC_CONSTANT_MACROS_DEFINED etc.
