// Boost.Range library
//
//  Copyright Thorsten Ottosen 2003-2004. Use, modification and
//  distribution is subject to the Boost Software License, Version
//  1.0. (See accompanying file LICENSE_1_0.txt or copy at
//  http://www.boost.org/LICENSE_1_0.txt)
//
// For more information, see http://www.boost.org/libs/range/
//

#ifndef BOOST_RANGE_DETAIL_VALUE_TYPE_HPP
#define BOOST_RANGE_DETAIL_VALUE_TYPE_HPP

#include <boost/range/detail/common.hpp>
#include <boost/type_traits/remove_bounds.hpp>
#include <boost/iterator/iterator_traits.hpp>

//////////////////////////////////////////////////////////////////////////////
// missing partial specialization  workaround.
//////////////////////////////////////////////////////////////////////////////

namespace boost
{
    namespace range_detail
    {
        template< typename T >
        struct range_value_type_;

        template<>
        struct range_value_type_<std_container_>
        {
            template< typename C >
            struct pts
            {
                typedef BOOST_DEDUCED_TYPENAME C::value_type type;
            };
        };

        template<>
        struct range_value_type_<std_pair_>
        {
            template< typename P >
            struct pts
            {
                typedef BOOST_DEDUCED_TYPENAME boost::iterator_value< BOOST_RANGE_DEDUCED_TYPENAME P::first_type >::type type;
            };
        };

        template<>
        struct range_value_type_<array_>
        {
            template< typename T >
            struct pts
            {
                typedef BOOST_DEDUCED_TYPENAME boost::remove_bounds<T>::type type;
            };
        };

        template<>
        struct range_value_type_<char_array_>
        {
            template< typename T >
            struct pts
            {
                typedef char type;
            };
        };

        template<>
        struct range_value_type_<char_ptr_>
        {
            template< typename S >
            struct pts
            {
                typedef char type;
            };
        };

        template<>
        struct range_value_type_<const_char_ptr_>
        {
            template< typename S >
            struct pts
            {
                typedef const char type;
            };
        };

        template<>
        struct range_value_type_<wchar_t_ptr_>
        {
            template< typename S >
            struct pts
            {
                typedef wchar_t type;
            };
        };

        template<>
        struct range_value_type_<const_wchar_t_ptr_>
        {
             template< typename S >
             struct pts
             {
                 typedef const wchar_t type;
             };
         };

    }

    template< typename C >
    class range_value
    {
        typedef BOOST_DEDUCED_TYPENAME range_detail::range<C>::type c_type;
    public:
        typedef BOOST_DEDUCED_TYPENAME range_detail::range_value_type_<c_type>::BOOST_NESTED_TEMPLATE pts<C>::type type;
    };

}

#endif
