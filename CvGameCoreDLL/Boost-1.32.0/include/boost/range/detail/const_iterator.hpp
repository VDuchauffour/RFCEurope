// Boost.Range library
//
//  Copyright Thorsten Ottosen 2003-2004. Use, modification and
//  distribution is subject to the Boost Software License, Version
//  1.0. (See accompanying file LICENSE_1_0.txt or copy at
//  http://www.boost.org/LICENSE_1_0.txt)
//
// For more information, see http://www.boost.org/libs/range/
//

#ifndef BOOST_RANGE_DETAIL_CONST_ITERATOR_HPP
#define BOOST_RANGE_DETAIL_CONST_ITERATOR_HPP

#include <boost/range/detail/common.hpp>
#include <boost/type_traits/remove_bounds.hpp>

//////////////////////////////////////////////////////////////////////////////
// missing partial specialization  workaround.
//////////////////////////////////////////////////////////////////////////////

namespace boost
{
    namespace range_detail
    {
        template< typename T >
        struct range_const_iterator_;

        template<>
        struct range_const_iterator_<std_container_>
        {
            template< typename C >
            struct pts
            {
                typedef BOOST_DEDUCED_TYPENAME C::const_iterator type;
            };
        };

        template<>
        struct range_const_iterator_<std_pair_>
        {
            template< typename P >
            struct pts
            {
                typedef BOOST_DEDUCED_TYPENAME P::first_type type;
            };
        };


        template<>
        struct range_const_iterator_<array_>
        {
            template< typename T >
            struct pts
            {
                typedef const BOOST_RANGE_DEDUCED_TYPENAME
                    remove_bounds<T>::type* type;
            };
        };

        template<>
        struct range_const_iterator_<char_array_>
        {
            template< typename T >
            struct pts
            {
                typedef const BOOST_RANGE_DEDUCED_TYPENAME
                    remove_bounds<T>::type* type;
            };
        };

        template<>
        struct range_const_iterator_<char_ptr_>
        {
            template< typename S >
            struct pts
            {
                typedef const char* type;
            };
        };

        template<>
        struct range_const_iterator_<const_char_ptr_>
        {
            template< typename S >
            struct pts
            {
                typedef const char* type;
            };
        };

        template<>
        struct range_const_iterator_<wchar_t_ptr_>
        {
            template< typename S >
            struct pts
            {
                typedef const wchar_t* type;
            };
        };

        template<>
        struct range_const_iterator_<const_wchar_t_ptr_>
        {
             template< typename S >
             struct pts
             {
                 typedef const wchar_t* type;
             };
         };

    }

    template< typename C >
    class range_const_iterator
    {
        typedef BOOST_DEDUCED_TYPENAME range_detail::range<C>::type c_type;
    public:
        typedef BOOST_DEDUCED_TYPENAME range_detail::range_const_iterator_<c_type>::BOOST_NESTED_TEMPLATE pts<C>::type type;
    };

}

#endif
