//  (C) Copyright John Maddock 2001 - 2002.
//  (C) Copyright Darin Adler 2001.
//  (C) Copyright Jens Maurer 2001.
//  Use, modification and distribution are subject to the
//  Boost Software License, Version 1.0. (See accompanying file
//  LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)

//  See http://www.boost.org for most recent version.

//  STLPort standard library config:

#if !defined(__SGI_STL_PORT) && !defined(_STLPORT_VERSION)
#  include <utility>
#  if !defined(__SGI_STL_PORT) && !defined(_STLPORT_VERSION)
#      error "This is not STLPort!"
#  endif
#endif

//
// __STL_STATIC_CONST_INIT_BUG implies BOOST_NO_LIMITS_COMPILE_TIME_CONSTANTS
// for versions prior to 4.1(beta)
//
#if (defined(__STL_STATIC_CONST_INIT_BUG) || defined(_STLP_STATIC_CONST_INIT_BUG)) && (__SGI_STL_PORT <= 0x400)
#  define BOOST_NO_LIMITS_COMPILE_TIME_CONSTANTS
#endif

//
// If STLport thinks that there is no partial specialisation, then there is no
// std::iterator traits:
//
#if !(defined(_STLP_CLASS_PARTIAL_SPECIALIZATION) || defined(__STL_CLASS_PARTIAL_SPECIALIZATION))
#  define BOOST_NO_STD_ITERATOR_TRAITS
#endif

//
// No new style iostreams on GCC without STLport's iostreams enabled:
//
#if (defined(__GNUC__) && (__GNUC__ < 3)) && !(defined(__SGI_STL_OWN_IOSTREAMS) || defined(_STLP_OWN_IOSTREAMS))
#  define BOOST_NO_STRINGSTREAM
#endif

//
// No new iostreams implies no std::locale, and no std::stringstream:
//
#if defined(__STL_NO_IOSTREAMS) || defined(__STL_NO_NEW_IOSTREAMS) || defined(_STLP_NO_IOSTREAMS) || defined(_STLP_NO_NEW_IOSTREAMS)
#  define BOOST_NO_STD_LOCALE
#  define BOOST_NO_STRINGSTREAM
#endif

//
// If the streams are not native, and we have a "using ::x" compiler bug
// then the io stream facets are not available in namespace std::
//
#ifdef _STLPORT_VERSION
#  if !defined(_STLP_OWN_IOSTREAMS) && defined(_STLP_USE_NAMESPACES) && defined(BOOST_NO_USING_TEMPLATE) && !defined(__BORLANDC__)
#     define BOOST_NO_STD_LOCALE
#  endif
#else
#  if !defined(__SGI_STL_OWN_IOSTREAMS) && defined(__STL_USE_NAMESPACES) && defined(BOOST_NO_USING_TEMPLATE) && !defined(__BORLANDC__)
#     define BOOST_NO_STD_LOCALE
#  endif
#endif

//
// Without member template support enabled, their are no template
// iterate constructors, and no std::allocator:
//
#if !(defined(__STL_MEMBER_TEMPLATES) || defined(_STLP_MEMBER_TEMPLATES))
#  define BOOST_NO_TEMPLATED_ITERATOR_CONSTRUCTORS
#  define BOOST_NO_STD_ALLOCATOR
#endif
//
// however we always have at least a partial allocator:
//
#define BOOST_HAS_PARTIAL_STD_ALLOCATOR

#if !defined(_STLP_MEMBER_TEMPLATE_CLASSES)
#  define BOOST_NO_STD_ALLOCATOR
#endif

#if defined(_STLP_NO_MEMBER_TEMPLATE_KEYWORD) && defined(BOOST_MSVC) && (BOOST_MSVC <= 1300)
#  define BOOST_NO_STD_ALLOCATOR
#endif

//
// If STLport thinks there is no wchar_t at all, then we have to disable
// the support for the relevant specilazations of std:: templates.
//
#if !defined(_STLP_HAS_WCHAR_T) && !defined(_STLP_WCHAR_T_IS_USHORT)
#  ifndef  BOOST_NO_STD_WSTRING
#     define BOOST_NO_STD_WSTRING
#  endif
#  ifndef  BOOST_NO_STD_WSTREAMBUF
#     define BOOST_NO_STD_WSTREAMBUF
#  endif
#endif

//
// We always have SGI style hash_set, hash_map, and slist:
//
#define BOOST_HAS_HASH
#define BOOST_HAS_SLIST

//
// STLport does a good job of importing names into namespace std::,
// but doesn't always get them all, define BOOST_NO_STDC_NAMESPACE, since our
// workaround does not conflict with STLports:
//
//
// Harold Howe says:
// Borland switched to STLport in BCB6. Defining BOOST_NO_STDC_NAMESPACE with
// BCB6 does cause problems. If we detect C++ Builder, then don't define
// BOOST_NO_STDC_NAMESPACE
//
#if !defined(__BORLANDC__) && !defined(__DMC__)
//
// If STLport is using it's own namespace, and the real names are in
// the global namespace, then we duplicate STLport's using declarations
// (by defining BOOST_NO_STDC_NAMESPACE), we do this because STLport doesn't
// necessarily import all the names we need into namespace std::
//
#  if (defined(__STL_IMPORT_VENDOR_CSTD) \
         || defined(__STL_USE_OWN_NAMESPACE) \
         || defined(_STLP_IMPORT_VENDOR_CSTD) \
         || defined(_STLP_USE_OWN_NAMESPACE)) \
      && (defined(__STL_VENDOR_GLOBAL_CSTD) || defined (_STLP_VENDOR_GLOBAL_CSTD))
#     define BOOST_NO_STDC_NAMESPACE
#     define BOOST_NO_EXCEPTION_STD_NAMESPACE
#  endif
#elif defined(__BORLANDC__) && __BORLANDC__ < 0x560
// STLport doesn't import std::abs correctly:
#include <stdlib.h>
namespace std { using ::abs; }
// and strcmp/strcpy don't get imported either ('cos they are macros)
#include <string.h>
#ifdef strcpy
#  undef strcpy
#endif
#ifdef strcmp
#  undef strcmp
#endif
#ifdef _STLP_VENDOR_CSTD
namespace std{ using _STLP_VENDOR_CSTD::strcmp; using _STLP_VENDOR_CSTD::strcpy; }
#endif
#endif

//
// std::use_facet may be non-standard, uses a class instead:
//
#if defined(__STL_NO_EXPLICIT_FUNCTION_TMPL_ARGS) || defined(_STLP_NO_EXPLICIT_FUNCTION_TMPL_ARGS)
#  define BOOST_NO_STD_USE_FACET
#  define BOOST_HAS_STLP_USE_FACET
#endif

//
// If STLport thinks there are no wide functions, <cwchar> etc. is not working; but
// only if BOOST_NO_STDC_NAMESPACE is not defined (if it is then we do the import
// into std:: ourselves).
//
#if defined(_STLP_NO_NATIVE_WIDE_FUNCTIONS) && !defined(BOOST_NO_STDC_NAMESPACE)
#  define BOOST_NO_CWCHAR
#  define BOOST_NO_CWCTYPE
#endif

//
// If STLport for some reason was configured so that it thinks that wchar_t
// is not an intrinsic type, then we have to disable the support for it as
// well (we would be missing required specializations otherwise).
//
#if !defined( _STLP_HAS_WCHAR_T) || defined(_STLP_WCHAR_T_IS_USHORT)
#  undef  BOOST_NO_INTRINSIC_WCHAR_T
#  define BOOST_NO_INTRINSIC_WCHAR_T
#endif

//
// Borland ships a version of STLport with C++ Builder 6 that lacks
// hashtables and the like:
//
#if defined(__BORLANDC__) && (__BORLANDC__ == 0x560)
#  undef BOOST_HAS_HASH
#endif

//
// gcc-2.95.3/STLPort does not like the using declarations we use to get ADL with std::min/max
//
#if defined(__GNUC__) && (__GNUC__ < 3)
#  include <algorithm> // for std::min and std::max
#  define BOOST_USING_STD_MIN() ((void)0)
#  define BOOST_USING_STD_MAX() ((void)0)
namespace boost { using std::min; using std::max; }
#endif

#define BOOST_STDLIB "STLPort standard library version " BOOST_STRINGIZE(__SGI_STL_PORT)
