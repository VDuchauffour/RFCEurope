
#ifndef BOOST_MPL_MAP_AUX_ITERATOR_HPP_INCLUDED
#define BOOST_MPL_MAP_AUX_ITERATOR_HPP_INCLUDED

// Copyright Aleksey Gurtovoy 2003-2004
// Copyright David Abrahams 2003-2004
//
// Distributed under the Boost Software License, Version 1.0.
// (See accompanying file LICENSE_1_0.txt or copy at
// http://www.boost.org/LICENSE_1_0.txt)
//
// See http://www.boost.org/libs/mpl for documentation.

// $Source: /cvsroot/boost/boost/boost/mpl/map/aux_/iterator.hpp,v $
// $Date: 2004/09/02 15:41:00 $
// $Revision: 1.2 $

#include <boost/mpl/map/aux_/map0.hpp>
#include <boost/mpl/map/aux_/at_impl.hpp>
#include <boost/mpl/map/aux_/tag.hpp>
#include <boost/mpl/iterator_tags.hpp>
#include <boost/mpl/if.hpp>
#include <boost/mpl/next.hpp>
#include <boost/mpl/deref.hpp>
#include <boost/mpl/long.hpp>
#include <boost/mpl/void.hpp>
#include <boost/mpl/aux_/config/ctps.hpp>


namespace boost { namespace mpl {

template<
      typename Map
    , long order
    , long max_order
    >
struct next_order
    : if_<
          is_void_< typename item_by_order<Map,order>::type >
        , next_order<Map,(order+1),max_order>
        , long_<order>
        >::type
{
};

template<
      typename Map
    , long max_order
    >
struct next_order<Map,max_order,max_order>
    : long_<max_order>
{
};


template< typename Map, long order, long max_order >
struct m_iter
{
    typedef forward_iterator_tag category;
    typedef typename item_by_order<Map,order>::type type;
};

template< typename Map, long max_order >
struct m_iter<Map,max_order,max_order>
{
    typedef forward_iterator_tag category;
};


template< typename Map, long order, long max_order >
struct next< m_iter<Map,order,max_order> >
{
    typedef m_iter<
          Map
        , next_order<Map,order+1,max_order>::value
        , max_order
        > type;
};

template< typename Map, long max_order >
struct next< m_iter<Map,max_order,max_order> >
{
};

}}

#endif // BOOST_MPL_MAP_AUX_ITERATOR_HPP_INCLUDED
