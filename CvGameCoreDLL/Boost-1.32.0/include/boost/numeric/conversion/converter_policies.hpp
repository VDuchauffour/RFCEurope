//  � Copyright Fernando Luis Cacciola Carballal 2000-2004
//  Use, modification, and distribution is subject to the Boost Software
//  License, Version 1.0. (See accompanying file LICENSE_1_0.txt or copy at
//  http://www.boost.org/LICENSE_1_0.txt)

//  See library home page at http://www.boost.org/libs/numeric/conversion
//
// Contact the author at: fernando_cacciola@hotmail.com
//
#ifndef BOOST_NUMERIC_CONVERSION_CONVERTER_POLICIES_FLC_12NOV2002_HPP
#define BOOST_NUMERIC_CONVERSION_CONVERTER_POLICIES_FLC_12NOV2002_HPP

#include <typeinfo> // for std::bad_cast

#include <cmath> // for std::floor and std::ceil

#include "boost/type_traits/is_arithmetic.hpp"

#include "boost/mpl/if.hpp"
#include "boost/mpl/integral_c.hpp"

namespace boost { namespace numeric
{

template<class S>
struct Trunc
{
  typedef S source_type ;

  typedef typename mpl::if_< is_arithmetic<S>,S,S const&>::type argument_type ;

  static source_type nearbyint ( argument_type s )
  {
#if !defined(BOOST_NO_STDC_NAMESPACE)
    using std::floor ;
    using std::ceil  ;
#endif

    return s < static_cast<S>(0) ? ceil(s) : floor(s) ;
  }

  typedef mpl::integral_c< std::float_round_style, std::round_toward_zero> round_style ;
} ;

template<class S>
struct RoundEven
{
  typedef S source_type ;

  typedef typename mpl::if_< is_arithmetic<S>,S,S const&>::type argument_type ;

  static source_type nearbyint ( argument_type s )
  {
    // Algorithm contributed by Guillaume Melquiond

#if !defined(BOOST_NO_STDC_NAMESPACE)
    using std::floor ;
    using std::ceil  ;
#endif

    // only works inside the range not at the boundaries
    S a = floor(s);
    S b = ceil(s);

    S c = (s - a) - (b - s); // the "good" subtraction

    if ( c < static_cast<S>(0.0) )
      return a;
    else if ( c >  static_cast<S>(0.0) )
      return b;
    else
      return 2 * floor(b / static_cast<S>(2.0)); // needs to behave sanely
  }

  typedef mpl::integral_c< std::float_round_style, std::round_to_nearest> round_style ;
} ;

template<class S>
struct Ceil
{
  typedef S source_type ;

  typedef typename mpl::if_< is_arithmetic<S>,S,S const&>::type argument_type ;

  static source_type nearbyint ( argument_type s )
  {
#if !defined(BOOST_NO_STDC_NAMESPACE)
    using std::ceil ;
#endif

    return ceil(s) ;
  }

  typedef mpl::integral_c< std::float_round_style, std::round_toward_infinity> round_style ;
} ;

template<class S>
struct Floor
{
  typedef S source_type ;

  typedef typename mpl::if_< is_arithmetic<S>,S,S const&>::type argument_type ;

  static source_type nearbyint ( argument_type s )
  {
#if !defined(BOOST_NO_STDC_NAMESPACE)
    using std::floor ;
#endif

    return floor(s) ;
  }

  typedef mpl::integral_c< std::float_round_style, std::round_toward_neg_infinity> round_style ;
} ;







enum range_check_result
{
  cInRange     = 0 ,
  cNegOverflow = 1 ,
  cPosOverflow = 2
} ;

class bad_numeric_conversion : public std::bad_cast
{
  public:

    virtual const char * what() const throw()
      {  return "bad numeric conversion: overflow"; }
};

class negative_overflow : public bad_numeric_conversion
{
  public:

    virtual const char * what() const throw()
      {  return "bad numeric conversion: negative overflow"; }
};
class positive_overflow : public bad_numeric_conversion
{
  public:

    virtual const char * what() const throw()
      { return "bad numeric conversion: positive overflow"; }
};

struct def_overflow_handler
{
  void operator() ( range_check_result r ) // throw(negative_overflow,positive_overflow)
  {
    if ( r == cNegOverflow )
      throw negative_overflow() ;
    else if ( r == cPosOverflow )
           throw positive_overflow() ;
  }
} ;

struct silent_overflow_handler
{
  void operator() ( range_check_result ) {} // throw()
} ;






template<class Traits>
struct raw_converter
{
  typedef typename Traits::result_type   result_type   ;
  typedef typename Traits::argument_type argument_type ;

  static result_type low_level_convert ( argument_type s ) { return static_cast<result_type>(s) ; }
} ;

struct UseInternalRangeChecker {} ;

} } // namespace boost::numeric

#endif
