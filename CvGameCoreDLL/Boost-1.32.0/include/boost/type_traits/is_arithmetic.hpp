
//  (C) Copyright Steve Cleary, Beman Dawes, Howard Hinnant & John Maddock 2000.
//  Use, modification and distribution are subject to the Boost Software License,
//  Version 1.0. (See accompanying file LICENSE_1_0.txt or copy at
//  http://www.boost.org/LICENSE_1_0.txt).
//
//  See http://www.boost.org/libs/type_traits for most recent version including documentation.

#ifndef BOOST_TT_IS_ARITHMETIC_HPP_INCLUDED
#define BOOST_TT_IS_ARITHMETIC_HPP_INCLUDED

#include "boost/type_traits/is_integral.hpp"
#include "boost/type_traits/is_float.hpp"
#include "boost/type_traits/detail/ice_or.hpp"
#include "boost/config.hpp"

// should be the last #include
#include "boost/type_traits/detail/bool_trait_def.hpp"

namespace boost {

namespace detail {

template< typename T >
struct is_arithmetic_impl
{
    BOOST_STATIC_CONSTANT(bool, value =
        (::boost::type_traits::ice_or<
            ::boost::is_integral<T>::value,
            ::boost::is_float<T>::value
        >::value));
};

} // namespace detail

//* is a type T an arithmetic type described in the standard (3.9.1p8)
BOOST_TT_AUX_BOOL_TRAIT_DEF1(is_arithmetic,T,::boost::detail::is_arithmetic_impl<T>::value)

} // namespace boost

#include "boost/type_traits/detail/bool_trait_undef.hpp"

#endif // BOOST_TT_IS_ARITHMETIC_HPP_INCLUDED
