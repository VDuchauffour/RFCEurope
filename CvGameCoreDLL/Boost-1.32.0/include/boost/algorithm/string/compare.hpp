//  Boost string_algo library compare.hpp header file  -------------------------//

//  Copyright Pavol Droba 2002-2003. Use, modification and
//  distribution is subject to the Boost Software License, Version
//  1.0. (See accompanying file LICENSE_1_0.txt or copy at
//  http://www.boost.org/LICENSE_1_0.txt)

//  See http://www.boost.org for updates, documentation, and revision history.

#ifndef BOOST_STRING_COMPARE_HPP
#define BOOST_STRING_COMPARE_HPP

#include <boost/algorithm/string/config.hpp>
#include <locale>

/*! \file
    Defines element comparison predicates. Many algorithms in this library can
    take an additional argument with a predicate used to compare elements.
    This makes it possible, for instance, to have case insensitive versions
    of the algorithms.
*/

namespace boost {
    namespace algorithm {

        //  is_equal functor  -----------------------------------------------//

        //! is_equal functor
        /*!
            Standard STL equal_to only handle comparison between arguments
            of the same type. This is a less restrictive version which wraps operator ==.
        */
        struct is_equal
        {
            //! Function operator
            /*!
                Compare two operands for equality
            */
            template< typename T1, typename T2 >
                bool operator ()( const T1& Arg1, const T2& Arg2 ) const
            {
                return Arg1==Arg2;
            }
        };

        //! case insensitive version of is_equal
        /*!
            Case insensitive comparison predicate. Comparison is done using
            specified locales.
        */
        struct is_iequal
        {
            //! Constructor
            /*!
                \param Loc locales used for comparison
            */
            is_iequal( const std::locale& Loc=std::locale() ) :
                m_Loc( Loc ) {}

            //! Function operator
            /*!
                Compare two operands. Case is ignored.
            */
            template< typename T1, typename T2 >
                bool operator ()( const T1& Arg1, const T2& Arg2 ) const
            {
                return std::toupper(Arg1,m_Loc)==std::toupper(Arg2,m_Loc);
            }

        private:
            std::locale m_Loc;
        };

    } // namespace algorithm

    // pull names to the boost namespace
    using algorithm::is_equal;
    using algorithm::is_iequal;

} // namespace boost


#endif  // BOOST_STRING_COMPARE_HPP
