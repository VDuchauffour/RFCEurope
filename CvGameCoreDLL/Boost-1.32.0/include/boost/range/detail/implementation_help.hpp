// Boost.Range library
//
//  Copyright Thorsten Ottosen 2003-2004. Use, modification and
//  distribution is subject to the Boost Software License, Version
//  1.0. (See accompanying file LICENSE_1_0.txt or copy at
//  http://www.boost.org/LICENSE_1_0.txt)
//
// For more information, see http://www.boost.org/libs/range/
//

#ifndef BOOST_RANGE_DETAIL_IMPLEMENTATION_HELP_HPP
#define BOOST_RANGE_DETAIL_IMPLEMENTATION_HELP_HPP

#include <boost/range/config.hpp>
#include <boost/range/detail/common.hpp>
#include <boost/type_traits/is_same.hpp>
#include <cstddef>
#include <string.h>

#ifndef BOOST_NO_CWCHAR
#include <wchar.h>
#endif

namespace boost
{
    namespace range_detail
    {

        /////////////////////////////////////////////////////////////////////
        // end() help
        /////////////////////////////////////////////////////////////////////

        inline const char* str_end( const char* s, const char* )
        {
            return s + strlen( s );
        }

#ifndef BOOST_NO_CWCHAR
        inline const wchar_t* str_end( const wchar_t* s, const wchar_t* )
        {
            return s + wcslen( s );
        }
#else
        inline const wchar_t* str_end( const wchar_t* s, const wchar_t* )
        {
            if( s == 0 && s[0] == 0 )
                return s;
            while( *++s != 0 )
                ;
            return s;
        }
#endif

        template< class Char >
        inline Char* str_end( Char* s )
        {
            return (Char*)str_end( s, s );
        }

        template< class T, std::size_t sz >
        inline T* array_end( T BOOST_RANGE_ARRAY_REF()[sz], int )
        {
            return array + sz;
        }

        template< class T, std::size_t sz >
        inline const T* array_end( const T BOOST_RANGE_ARRAY_REF()[sz], int )
        {
            return array + sz;
        }

        template< class T, std::size_t sz >
        inline T* array_end( T BOOST_RANGE_ARRAY_REF()[sz], char_or_wchar_t_array_tag )
        {
            return array + sz - 1;
        }

        template< class T, std::size_t sz >
        inline const T* array_end( const T BOOST_RANGE_ARRAY_REF()[sz], char_or_wchar_t_array_tag )
        {
            return array + sz - 1;
        }

        template< class T, std::size_t sz >
        inline T* array_end( T BOOST_RANGE_ARRAY_REF()[sz] )
        {
            typedef BOOST_RANGE_DEDUCED_TYPENAME boost::mpl::if_c< is_same<char,T>::value || is_same<wchar_t,T>::value,
                                                                char_or_wchar_t_array_tag,
                                                                int >::type tag;

            return array_end<T,sz>( array, tag() );
        }

        template< class T, std::size_t sz >
        inline const T* array_end( const T BOOST_RANGE_ARRAY_REF()[sz] )
        {
            typedef BOOST_RANGE_DEDUCED_TYPENAME boost::mpl::if_c< is_same<char,T>::value || is_same<wchar_t,T>::value,
                                                                char_or_wchar_t_array_tag,
                                                                int >::type tag;

            return array_end<T,sz>( array, tag() );
        }

        /////////////////////////////////////////////////////////////////////
        // size() help
        /////////////////////////////////////////////////////////////////////

        template< class Char >
        inline std::size_t str_size( const Char* const& s )
        {
            return str_end( s ) - s;
        }

        template< class T, std::size_t sz >
        inline std::size_t array_size( T BOOST_RANGE_ARRAY_REF()[sz], int )
        {
            return sz;
        }

        template< class T, std::size_t sz >
        inline std::size_t array_size( const T BOOST_RANGE_ARRAY_REF()[sz], int )
        {
            return sz;
        }

        template< class T, std::size_t sz >
        inline std::size_t array_size( T BOOST_RANGE_ARRAY_REF()[sz], char_or_wchar_t_array_tag )
        {
            return sz - 1;
        }

        template< class T, std::size_t sz >
        inline std::size_t array_size( const T BOOST_RANGE_ARRAY_REF()[sz], char_or_wchar_t_array_tag )
        {
            return sz - 1;
        }

        template< class T, std::size_t sz >
        inline std::size_t array_size( T BOOST_RANGE_ARRAY_REF()[sz] )
        {
            typedef BOOST_RANGE_DEDUCED_TYPENAME boost::mpl::if_c< is_same<const char,T>::value || is_same<const wchar_t,T>::value ||
                                                                   is_same<char,T>::value       || is_same<wchar_t,T>::value,
                                                                char_or_wchar_t_array_tag,
                                                                int >::type tag;
            return array_size<T,sz>( array, tag() );
        }

        template< class T, std::size_t sz >
        inline std::size_t array_size( const T BOOST_RANGE_ARRAY_REF()[sz] )
        {
            typedef BOOST_RANGE_DEDUCED_TYPENAME boost::mpl::if_c< is_same<char,T>::value || is_same<wchar_t,T>::value,
                                                                char_or_wchar_t_array_tag,
                                                                int >::type tag;
            return array_size<T,sz>( array, tag() );
        }

    } // namespace 'range_detail'

} // namespace 'boost'


#endif
