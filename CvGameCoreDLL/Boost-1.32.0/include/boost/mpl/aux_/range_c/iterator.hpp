
#ifndef BOOST_MPL_AUX_RANGE_C_ITERATOR_HPP_INCLUDED
#define BOOST_MPL_AUX_RANGE_C_ITERATOR_HPP_INCLUDED

// Copyright Aleksey Gurtovoy 2000-2004
//
// Distributed under the Boost Software License, Version 1.0.
// (See accompanying file LICENSE_1_0.txt or copy at
// http://www.boost.org/LICENSE_1_0.txt)
//
// See http://www.boost.org/libs/mpl for documentation.

// $Source: /cvsroot/boost/boost/boost/mpl/aux_/range_c/iterator.hpp,v $
// $Date: 2004/11/10 23:38:09 $
// $Revision: 1.6.2.1 $

#include <boost/mpl/iterator_tags.hpp>
#include <boost/mpl/advance_fwd.hpp>
#include <boost/mpl/distance_fwd.hpp>
#include <boost/mpl/next_prior.hpp>
#include <boost/mpl/deref.hpp>
#include <boost/mpl/plus.hpp>
#include <boost/mpl/minus.hpp>
#include <boost/mpl/aux_/value_wknd.hpp>
#include <boost/mpl/aux_/config/ctps.hpp>

namespace boost { namespace mpl {

// theoretically will work on any discrete numeric type
template< typename N > struct r_iter
{
    typedef aux::r_iter_tag tag;
    typedef random_access_iterator_tag category;
    typedef N type;

#if defined(BOOST_NO_TEMPLATE_PARTIAL_SPECIALIZATION)
    typedef r_iter< typename mpl::next<N>::type > next;
    typedef r_iter< typename mpl::prior<N>::type > prior;
#endif
};

#if !defined(BOOST_NO_TEMPLATE_PARTIAL_SPECIALIZATION)

template<
      typename N
    >
struct next< r_iter<N> >
{
    typedef r_iter< typename mpl::next<N>::type > type;
};

template<
      typename N
    >
struct prior< r_iter<N> >
{
    typedef r_iter< typename mpl::prior<N>::type > type;
};

#endif


template<> struct advance_impl<aux::r_iter_tag>
{
    template< typename Iter, typename Dist > struct apply
    {
        typedef typename Iter::type n_;
        typedef typename plus<n_,Dist>::type m_;

        // agurt, 10/nov/04: to be generic, the code have to do something along
        // the lines below...
        //
        // typedef typename apply_wrap1<
        //       numeric_cast< typename m_::tag, typename n_::tag >
        //     , m_
        //     >::type result_;
        //
        // ... meanwhile:

        typedef integral_c<
              typename n_::value_type
            , BOOST_MPL_AUX_VALUE_WKND(m_)::value
            > result_;

        typedef r_iter<result_> type;
    };
};

template<> struct distance_impl<aux::r_iter_tag>
{
    template< typename Iter1, typename Iter2 > struct apply
        : minus<
              typename Iter2::type
            , typename Iter1::type
            >
    {
    };
};

}}

#endif // BOOST_MPL_AUX_RANGE_C_ITERATOR_HPP_INCLUDED
