
//  (C) Copyright Dave Abrahams, Steve Cleary, Beman Dawes,
//  Aleksey Gurtovoy, Howard Hinnant & John Maddock 2000.
//  Use, modification and distribution are subject to the Boost Software License,
//  Version 1.0. (See accompanying file LICENSE_1_0.txt or copy at
//  http://www.boost.org/LICENSE_1_0.txt).
//
//  See http://www.boost.org/libs/type_traits for most recent version including documentation.

#if !defined(BOOST_PP_IS_ITERATING)

///// header body

#ifndef BOOST_TT_DETAIL_IS_MEM_FUN_POINTER_TESTER_HPP_INCLUDED
#define BOOST_TT_DETAIL_IS_MEM_FUN_POINTER_TESTER_HPP_INCLUDED

#include "boost/type_traits/detail/yes_no_type.hpp"
#include "boost/type_traits/config.hpp"

#if defined(BOOST_TT_PREPROCESSING_MODE)
#   include "boost/preprocessor/iterate.hpp"
#   include "boost/preprocessor/enum_params.hpp"
#   include "boost/preprocessor/comma_if.hpp"
#endif

namespace boost {
namespace type_traits {

no_type BOOST_TT_DECL is_mem_fun_pointer_tester(...);

#if !defined(BOOST_TT_PREPROCESSING_MODE)
// preprocessor-generated part, don't edit by hand!

template <class R,class T>
yes_type is_mem_fun_pointer_tester(R (T::*)());
template <class R,class T>
yes_type is_mem_fun_pointer_tester(R (T::*)() const);
template <class R,class T>
yes_type is_mem_fun_pointer_tester(R (T::*)() volatile);
template <class R,class T>
yes_type is_mem_fun_pointer_tester(R (T::*)() const volatile);

template <class R,class T,class T0 >
yes_type is_mem_fun_pointer_tester(R (T::*)(T0));
template <class R,class T,class T0 >
yes_type is_mem_fun_pointer_tester(R (T::*)(T0) const);
template <class R,class T,class T0 >
yes_type is_mem_fun_pointer_tester(R (T::*)(T0) volatile);
template <class R,class T,class T0 >
yes_type is_mem_fun_pointer_tester(R (T::*)(T0) const volatile);

template <class R,class T,class T0,class T1 >
yes_type is_mem_fun_pointer_tester(R (T::*)(T0,T1));
template <class R,class T,class T0,class T1 >
yes_type is_mem_fun_pointer_tester(R (T::*)(T0,T1) const);
template <class R,class T,class T0,class T1 >
yes_type is_mem_fun_pointer_tester(R (T::*)(T0,T1) volatile);
template <class R,class T,class T0,class T1 >
yes_type is_mem_fun_pointer_tester(R (T::*)(T0,T1) const volatile);

template <class R,class T,class T0,class T1,class T2 >
yes_type is_mem_fun_pointer_tester(R (T::*)(T0,T1,T2));
template <class R,class T,class T0,class T1,class T2 >
yes_type is_mem_fun_pointer_tester(R (T::*)(T0,T1,T2) const);
template <class R,class T,class T0,class T1,class T2 >
yes_type is_mem_fun_pointer_tester(R (T::*)(T0,T1,T2) volatile);
template <class R,class T,class T0,class T1,class T2 >
yes_type is_mem_fun_pointer_tester(R (T::*)(T0,T1,T2) const volatile);

template <class R,class T,class T0,class T1,class T2,class T3 >
yes_type is_mem_fun_pointer_tester(R (T::*)(T0,T1,T2,T3));
template <class R,class T,class T0,class T1,class T2,class T3 >
yes_type is_mem_fun_pointer_tester(R (T::*)(T0,T1,T2,T3) const);
template <class R,class T,class T0,class T1,class T2,class T3 >
yes_type is_mem_fun_pointer_tester(R (T::*)(T0,T1,T2,T3) volatile);
template <class R,class T,class T0,class T1,class T2,class T3 >
yes_type is_mem_fun_pointer_tester(R (T::*)(T0,T1,T2,T3) const volatile);

template <class R,class T,class T0,class T1,class T2,class T3,class T4 >
yes_type is_mem_fun_pointer_tester(R (T::*)(T0,T1,T2,T3,T4));
template <class R,class T,class T0,class T1,class T2,class T3,class T4 >
yes_type is_mem_fun_pointer_tester(R (T::*)(T0,T1,T2,T3,T4) const);
template <class R,class T,class T0,class T1,class T2,class T3,class T4 >
yes_type is_mem_fun_pointer_tester(R (T::*)(T0,T1,T2,T3,T4) volatile);
template <class R,class T,class T0,class T1,class T2,class T3,class T4 >
yes_type is_mem_fun_pointer_tester(R (T::*)(T0,T1,T2,T3,T4) const volatile);

template <class R,class T,class T0,class T1,class T2,class T3,class T4,class T5 >
yes_type is_mem_fun_pointer_tester(R (T::*)(T0,T1,T2,T3,T4,T5));
template <class R,class T,class T0,class T1,class T2,class T3,class T4,class T5 >
yes_type is_mem_fun_pointer_tester(R (T::*)(T0,T1,T2,T3,T4,T5) const);
template <class R,class T,class T0,class T1,class T2,class T3,class T4,class T5 >
yes_type is_mem_fun_pointer_tester(R (T::*)(T0,T1,T2,T3,T4,T5) volatile);
template <class R,class T,class T0,class T1,class T2,class T3,class T4,class T5 >
yes_type is_mem_fun_pointer_tester(R (T::*)(T0,T1,T2,T3,T4,T5) const volatile);

template <class R,class T,class T0,class T1,class T2,class T3,class T4,class T5,class T6 >
yes_type is_mem_fun_pointer_tester(R (T::*)(T0,T1,T2,T3,T4,T5,T6));
template <class R,class T,class T0,class T1,class T2,class T3,class T4,class T5,class T6 >
yes_type is_mem_fun_pointer_tester(R (T::*)(T0,T1,T2,T3,T4,T5,T6) const);
template <class R,class T,class T0,class T1,class T2,class T3,class T4,class T5,class T6 >
yes_type is_mem_fun_pointer_tester(R (T::*)(T0,T1,T2,T3,T4,T5,T6) volatile);
template <class R,class T,class T0,class T1,class T2,class T3,class T4,class T5,class T6 >
yes_type is_mem_fun_pointer_tester(R (T::*)(T0,T1,T2,T3,T4,T5,T6) const volatile);

template <class R,class T,class T0,class T1,class T2,class T3,class T4,class T5,class T6,class T7 >
yes_type is_mem_fun_pointer_tester(R (T::*)(T0,T1,T2,T3,T4,T5,T6,T7));
template <class R,class T,class T0,class T1,class T2,class T3,class T4,class T5,class T6,class T7 >
yes_type is_mem_fun_pointer_tester(R (T::*)(T0,T1,T2,T3,T4,T5,T6,T7) const);
template <class R,class T,class T0,class T1,class T2,class T3,class T4,class T5,class T6,class T7 >
yes_type is_mem_fun_pointer_tester(R (T::*)(T0,T1,T2,T3,T4,T5,T6,T7) volatile);
template <class R,class T,class T0,class T1,class T2,class T3,class T4,class T5,class T6,class T7 >
yes_type is_mem_fun_pointer_tester(R (T::*)(T0,T1,T2,T3,T4,T5,T6,T7) const volatile);

template <class R,class T,class T0,class T1,class T2,class T3,class T4,class T5,class T6,class T7,class T8 >
yes_type is_mem_fun_pointer_tester(R (T::*)(T0,T1,T2,T3,T4,T5,T6,T7,T8));
template <class R,class T,class T0,class T1,class T2,class T3,class T4,class T5,class T6,class T7,class T8 >
yes_type is_mem_fun_pointer_tester(R (T::*)(T0,T1,T2,T3,T4,T5,T6,T7,T8) const);
template <class R,class T,class T0,class T1,class T2,class T3,class T4,class T5,class T6,class T7,class T8 >
yes_type is_mem_fun_pointer_tester(R (T::*)(T0,T1,T2,T3,T4,T5,T6,T7,T8) volatile);
template <class R,class T,class T0,class T1,class T2,class T3,class T4,class T5,class T6,class T7,class T8 >
yes_type is_mem_fun_pointer_tester(R (T::*)(T0,T1,T2,T3,T4,T5,T6,T7,T8) const volatile);

template <class R,class T,class T0,class T1,class T2,class T3,class T4,class T5,class T6,class T7,class T8,class T9 >
yes_type is_mem_fun_pointer_tester(R (T::*)(T0,T1,T2,T3,T4,T5,T6,T7,T8,T9));
template <class R,class T,class T0,class T1,class T2,class T3,class T4,class T5,class T6,class T7,class T8,class T9 >
yes_type is_mem_fun_pointer_tester(R (T::*)(T0,T1,T2,T3,T4,T5,T6,T7,T8,T9) const);
template <class R,class T,class T0,class T1,class T2,class T3,class T4,class T5,class T6,class T7,class T8,class T9 >
yes_type is_mem_fun_pointer_tester(R (T::*)(T0,T1,T2,T3,T4,T5,T6,T7,T8,T9) volatile);
template <class R,class T,class T0,class T1,class T2,class T3,class T4,class T5,class T6,class T7,class T8,class T9 >
yes_type is_mem_fun_pointer_tester(R (T::*)(T0,T1,T2,T3,T4,T5,T6,T7,T8,T9) const volatile);

template <class R,class T,class T0,class T1,class T2,class T3,class T4,class T5,class T6,class T7,class T8,class T9,class T10 >
yes_type is_mem_fun_pointer_tester(R (T::*)(T0,T1,T2,T3,T4,T5,T6,T7,T8,T9,T10));
template <class R,class T,class T0,class T1,class T2,class T3,class T4,class T5,class T6,class T7,class T8,class T9,class T10 >
yes_type is_mem_fun_pointer_tester(R (T::*)(T0,T1,T2,T3,T4,T5,T6,T7,T8,T9,T10) const);
template <class R,class T,class T0,class T1,class T2,class T3,class T4,class T5,class T6,class T7,class T8,class T9,class T10 >
yes_type is_mem_fun_pointer_tester(R (T::*)(T0,T1,T2,T3,T4,T5,T6,T7,T8,T9,T10) volatile);
template <class R,class T,class T0,class T1,class T2,class T3,class T4,class T5,class T6,class T7,class T8,class T9,class T10 >
yes_type is_mem_fun_pointer_tester(R (T::*)(T0,T1,T2,T3,T4,T5,T6,T7,T8,T9,T10) const volatile);

template <class R,class T,class T0,class T1,class T2,class T3,class T4,class T5,class T6,class T7,class T8,class T9,class T10,class T11 >
yes_type is_mem_fun_pointer_tester(R (T::*)(T0,T1,T2,T3,T4,T5,T6,T7,T8,T9,T10,T11));
template <class R,class T,class T0,class T1,class T2,class T3,class T4,class T5,class T6,class T7,class T8,class T9,class T10,class T11 >
yes_type is_mem_fun_pointer_tester(R (T::*)(T0,T1,T2,T3,T4,T5,T6,T7,T8,T9,T10,T11) const);
template <class R,class T,class T0,class T1,class T2,class T3,class T4,class T5,class T6,class T7,class T8,class T9,class T10,class T11 >
yes_type is_mem_fun_pointer_tester(R (T::*)(T0,T1,T2,T3,T4,T5,T6,T7,T8,T9,T10,T11) volatile);
template <class R,class T,class T0,class T1,class T2,class T3,class T4,class T5,class T6,class T7,class T8,class T9,class T10,class T11 >
yes_type is_mem_fun_pointer_tester(R (T::*)(T0,T1,T2,T3,T4,T5,T6,T7,T8,T9,T10,T11) const volatile);

template <class R,class T,class T0,class T1,class T2,class T3,class T4,class T5,class T6,class T7,class T8,class T9,class T10,class T11,class T12 >
yes_type is_mem_fun_pointer_tester(R (T::*)(T0,T1,T2,T3,T4,T5,T6,T7,T8,T9,T10,T11,T12));
template <class R,class T,class T0,class T1,class T2,class T3,class T4,class T5,class T6,class T7,class T8,class T9,class T10,class T11,class T12 >
yes_type is_mem_fun_pointer_tester(R (T::*)(T0,T1,T2,T3,T4,T5,T6,T7,T8,T9,T10,T11,T12) const);
template <class R,class T,class T0,class T1,class T2,class T3,class T4,class T5,class T6,class T7,class T8,class T9,class T10,class T11,class T12 >
yes_type is_mem_fun_pointer_tester(R (T::*)(T0,T1,T2,T3,T4,T5,T6,T7,T8,T9,T10,T11,T12) volatile);
template <class R,class T,class T0,class T1,class T2,class T3,class T4,class T5,class T6,class T7,class T8,class T9,class T10,class T11,class T12 >
yes_type is_mem_fun_pointer_tester(R (T::*)(T0,T1,T2,T3,T4,T5,T6,T7,T8,T9,T10,T11,T12) const volatile);

template <class R,class T,class T0,class T1,class T2,class T3,class T4,class T5,class T6,class T7,class T8,class T9,class T10,class T11,class T12,class T13 >
yes_type is_mem_fun_pointer_tester(R (T::*)(T0,T1,T2,T3,T4,T5,T6,T7,T8,T9,T10,T11,T12,T13));
template <class R,class T,class T0,class T1,class T2,class T3,class T4,class T5,class T6,class T7,class T8,class T9,class T10,class T11,class T12,class T13 >
yes_type is_mem_fun_pointer_tester(R (T::*)(T0,T1,T2,T3,T4,T5,T6,T7,T8,T9,T10,T11,T12,T13) const);
template <class R,class T,class T0,class T1,class T2,class T3,class T4,class T5,class T6,class T7,class T8,class T9,class T10,class T11,class T12,class T13 >
yes_type is_mem_fun_pointer_tester(R (T::*)(T0,T1,T2,T3,T4,T5,T6,T7,T8,T9,T10,T11,T12,T13) volatile);
template <class R,class T,class T0,class T1,class T2,class T3,class T4,class T5,class T6,class T7,class T8,class T9,class T10,class T11,class T12,class T13 >
yes_type is_mem_fun_pointer_tester(R (T::*)(T0,T1,T2,T3,T4,T5,T6,T7,T8,T9,T10,T11,T12,T13) const volatile);

template <class R,class T,class T0,class T1,class T2,class T3,class T4,class T5,class T6,class T7,class T8,class T9,class T10,class T11,class T12,class T13,class T14 >
yes_type is_mem_fun_pointer_tester(R (T::*)(T0,T1,T2,T3,T4,T5,T6,T7,T8,T9,T10,T11,T12,T13,T14));
template <class R,class T,class T0,class T1,class T2,class T3,class T4,class T5,class T6,class T7,class T8,class T9,class T10,class T11,class T12,class T13,class T14 >
yes_type is_mem_fun_pointer_tester(R (T::*)(T0,T1,T2,T3,T4,T5,T6,T7,T8,T9,T10,T11,T12,T13,T14) const);
template <class R,class T,class T0,class T1,class T2,class T3,class T4,class T5,class T6,class T7,class T8,class T9,class T10,class T11,class T12,class T13,class T14 >
yes_type is_mem_fun_pointer_tester(R (T::*)(T0,T1,T2,T3,T4,T5,T6,T7,T8,T9,T10,T11,T12,T13,T14) volatile);
template <class R,class T,class T0,class T1,class T2,class T3,class T4,class T5,class T6,class T7,class T8,class T9,class T10,class T11,class T12,class T13,class T14 >
yes_type is_mem_fun_pointer_tester(R (T::*)(T0,T1,T2,T3,T4,T5,T6,T7,T8,T9,T10,T11,T12,T13,T14) const volatile);

template <class R,class T,class T0,class T1,class T2,class T3,class T4,class T5,class T6,class T7,class T8,class T9,class T10,class T11,class T12,class T13,class T14,class T15 >
yes_type is_mem_fun_pointer_tester(R (T::*)(T0,T1,T2,T3,T4,T5,T6,T7,T8,T9,T10,T11,T12,T13,T14,T15));
template <class R,class T,class T0,class T1,class T2,class T3,class T4,class T5,class T6,class T7,class T8,class T9,class T10,class T11,class T12,class T13,class T14,class T15 >
yes_type is_mem_fun_pointer_tester(R (T::*)(T0,T1,T2,T3,T4,T5,T6,T7,T8,T9,T10,T11,T12,T13,T14,T15) const);
template <class R,class T,class T0,class T1,class T2,class T3,class T4,class T5,class T6,class T7,class T8,class T9,class T10,class T11,class T12,class T13,class T14,class T15 >
yes_type is_mem_fun_pointer_tester(R (T::*)(T0,T1,T2,T3,T4,T5,T6,T7,T8,T9,T10,T11,T12,T13,T14,T15) volatile);
template <class R,class T,class T0,class T1,class T2,class T3,class T4,class T5,class T6,class T7,class T8,class T9,class T10,class T11,class T12,class T13,class T14,class T15 >
yes_type is_mem_fun_pointer_tester(R (T::*)(T0,T1,T2,T3,T4,T5,T6,T7,T8,T9,T10,T11,T12,T13,T14,T15) const volatile);

template <class R,class T,class T0,class T1,class T2,class T3,class T4,class T5,class T6,class T7,class T8,class T9,class T10,class T11,class T12,class T13,class T14,class T15,class T16 >
yes_type is_mem_fun_pointer_tester(R (T::*)(T0,T1,T2,T3,T4,T5,T6,T7,T8,T9,T10,T11,T12,T13,T14,T15,T16));
template <class R,class T,class T0,class T1,class T2,class T3,class T4,class T5,class T6,class T7,class T8,class T9,class T10,class T11,class T12,class T13,class T14,class T15,class T16 >
yes_type is_mem_fun_pointer_tester(R (T::*)(T0,T1,T2,T3,T4,T5,T6,T7,T8,T9,T10,T11,T12,T13,T14,T15,T16) const);
template <class R,class T,class T0,class T1,class T2,class T3,class T4,class T5,class T6,class T7,class T8,class T9,class T10,class T11,class T12,class T13,class T14,class T15,class T16 >
yes_type is_mem_fun_pointer_tester(R (T::*)(T0,T1,T2,T3,T4,T5,T6,T7,T8,T9,T10,T11,T12,T13,T14,T15,T16) volatile);
template <class R,class T,class T0,class T1,class T2,class T3,class T4,class T5,class T6,class T7,class T8,class T9,class T10,class T11,class T12,class T13,class T14,class T15,class T16 >
yes_type is_mem_fun_pointer_tester(R (T::*)(T0,T1,T2,T3,T4,T5,T6,T7,T8,T9,T10,T11,T12,T13,T14,T15,T16) const volatile);

template <class R,class T,class T0,class T1,class T2,class T3,class T4,class T5,class T6,class T7,class T8,class T9,class T10,class T11,class T12,class T13,class T14,class T15,class T16,class T17 >
yes_type is_mem_fun_pointer_tester(R (T::*)(T0,T1,T2,T3,T4,T5,T6,T7,T8,T9,T10,T11,T12,T13,T14,T15,T16,T17));
template <class R,class T,class T0,class T1,class T2,class T3,class T4,class T5,class T6,class T7,class T8,class T9,class T10,class T11,class T12,class T13,class T14,class T15,class T16,class T17 >
yes_type is_mem_fun_pointer_tester(R (T::*)(T0,T1,T2,T3,T4,T5,T6,T7,T8,T9,T10,T11,T12,T13,T14,T15,T16,T17) const);
template <class R,class T,class T0,class T1,class T2,class T3,class T4,class T5,class T6,class T7,class T8,class T9,class T10,class T11,class T12,class T13,class T14,class T15,class T16,class T17 >
yes_type is_mem_fun_pointer_tester(R (T::*)(T0,T1,T2,T3,T4,T5,T6,T7,T8,T9,T10,T11,T12,T13,T14,T15,T16,T17) volatile);
template <class R,class T,class T0,class T1,class T2,class T3,class T4,class T5,class T6,class T7,class T8,class T9,class T10,class T11,class T12,class T13,class T14,class T15,class T16,class T17 >
yes_type is_mem_fun_pointer_tester(R (T::*)(T0,T1,T2,T3,T4,T5,T6,T7,T8,T9,T10,T11,T12,T13,T14,T15,T16,T17) const volatile);

template <class R,class T,class T0,class T1,class T2,class T3,class T4,class T5,class T6,class T7,class T8,class T9,class T10,class T11,class T12,class T13,class T14,class T15,class T16,class T17,class T18 >
yes_type is_mem_fun_pointer_tester(R (T::*)(T0,T1,T2,T3,T4,T5,T6,T7,T8,T9,T10,T11,T12,T13,T14,T15,T16,T17,T18));
template <class R,class T,class T0,class T1,class T2,class T3,class T4,class T5,class T6,class T7,class T8,class T9,class T10,class T11,class T12,class T13,class T14,class T15,class T16,class T17,class T18 >
yes_type is_mem_fun_pointer_tester(R (T::*)(T0,T1,T2,T3,T4,T5,T6,T7,T8,T9,T10,T11,T12,T13,T14,T15,T16,T17,T18) const);
template <class R,class T,class T0,class T1,class T2,class T3,class T4,class T5,class T6,class T7,class T8,class T9,class T10,class T11,class T12,class T13,class T14,class T15,class T16,class T17,class T18 >
yes_type is_mem_fun_pointer_tester(R (T::*)(T0,T1,T2,T3,T4,T5,T6,T7,T8,T9,T10,T11,T12,T13,T14,T15,T16,T17,T18) volatile);
template <class R,class T,class T0,class T1,class T2,class T3,class T4,class T5,class T6,class T7,class T8,class T9,class T10,class T11,class T12,class T13,class T14,class T15,class T16,class T17,class T18 >
yes_type is_mem_fun_pointer_tester(R (T::*)(T0,T1,T2,T3,T4,T5,T6,T7,T8,T9,T10,T11,T12,T13,T14,T15,T16,T17,T18) const volatile);

template <class R,class T,class T0,class T1,class T2,class T3,class T4,class T5,class T6,class T7,class T8,class T9,class T10,class T11,class T12,class T13,class T14,class T15,class T16,class T17,class T18,class T19 >
yes_type is_mem_fun_pointer_tester(R (T::*)(T0,T1,T2,T3,T4,T5,T6,T7,T8,T9,T10,T11,T12,T13,T14,T15,T16,T17,T18,T19));
template <class R,class T,class T0,class T1,class T2,class T3,class T4,class T5,class T6,class T7,class T8,class T9,class T10,class T11,class T12,class T13,class T14,class T15,class T16,class T17,class T18,class T19 >
yes_type is_mem_fun_pointer_tester(R (T::*)(T0,T1,T2,T3,T4,T5,T6,T7,T8,T9,T10,T11,T12,T13,T14,T15,T16,T17,T18,T19) const);
template <class R,class T,class T0,class T1,class T2,class T3,class T4,class T5,class T6,class T7,class T8,class T9,class T10,class T11,class T12,class T13,class T14,class T15,class T16,class T17,class T18,class T19 >
yes_type is_mem_fun_pointer_tester(R (T::*)(T0,T1,T2,T3,T4,T5,T6,T7,T8,T9,T10,T11,T12,T13,T14,T15,T16,T17,T18,T19) volatile);
template <class R,class T,class T0,class T1,class T2,class T3,class T4,class T5,class T6,class T7,class T8,class T9,class T10,class T11,class T12,class T13,class T14,class T15,class T16,class T17,class T18,class T19 >
yes_type is_mem_fun_pointer_tester(R (T::*)(T0,T1,T2,T3,T4,T5,T6,T7,T8,T9,T10,T11,T12,T13,T14,T15,T16,T17,T18,T19) const volatile);

template <class R,class T,class T0,class T1,class T2,class T3,class T4,class T5,class T6,class T7,class T8,class T9,class T10,class T11,class T12,class T13,class T14,class T15,class T16,class T17,class T18,class T19,class T20 >
yes_type is_mem_fun_pointer_tester(R (T::*)(T0,T1,T2,T3,T4,T5,T6,T7,T8,T9,T10,T11,T12,T13,T14,T15,T16,T17,T18,T19,T20));
template <class R,class T,class T0,class T1,class T2,class T3,class T4,class T5,class T6,class T7,class T8,class T9,class T10,class T11,class T12,class T13,class T14,class T15,class T16,class T17,class T18,class T19,class T20 >
yes_type is_mem_fun_pointer_tester(R (T::*)(T0,T1,T2,T3,T4,T5,T6,T7,T8,T9,T10,T11,T12,T13,T14,T15,T16,T17,T18,T19,T20) const);
template <class R,class T,class T0,class T1,class T2,class T3,class T4,class T5,class T6,class T7,class T8,class T9,class T10,class T11,class T12,class T13,class T14,class T15,class T16,class T17,class T18,class T19,class T20 >
yes_type is_mem_fun_pointer_tester(R (T::*)(T0,T1,T2,T3,T4,T5,T6,T7,T8,T9,T10,T11,T12,T13,T14,T15,T16,T17,T18,T19,T20) volatile);
template <class R,class T,class T0,class T1,class T2,class T3,class T4,class T5,class T6,class T7,class T8,class T9,class T10,class T11,class T12,class T13,class T14,class T15,class T16,class T17,class T18,class T19,class T20 >
yes_type is_mem_fun_pointer_tester(R (T::*)(T0,T1,T2,T3,T4,T5,T6,T7,T8,T9,T10,T11,T12,T13,T14,T15,T16,T17,T18,T19,T20) const volatile);

template <class R,class T,class T0,class T1,class T2,class T3,class T4,class T5,class T6,class T7,class T8,class T9,class T10,class T11,class T12,class T13,class T14,class T15,class T16,class T17,class T18,class T19,class T20,class T21 >
yes_type is_mem_fun_pointer_tester(R (T::*)(T0,T1,T2,T3,T4,T5,T6,T7,T8,T9,T10,T11,T12,T13,T14,T15,T16,T17,T18,T19,T20,T21));
template <class R,class T,class T0,class T1,class T2,class T3,class T4,class T5,class T6,class T7,class T8,class T9,class T10,class T11,class T12,class T13,class T14,class T15,class T16,class T17,class T18,class T19,class T20,class T21 >
yes_type is_mem_fun_pointer_tester(R (T::*)(T0,T1,T2,T3,T4,T5,T6,T7,T8,T9,T10,T11,T12,T13,T14,T15,T16,T17,T18,T19,T20,T21) const);
template <class R,class T,class T0,class T1,class T2,class T3,class T4,class T5,class T6,class T7,class T8,class T9,class T10,class T11,class T12,class T13,class T14,class T15,class T16,class T17,class T18,class T19,class T20,class T21 >
yes_type is_mem_fun_pointer_tester(R (T::*)(T0,T1,T2,T3,T4,T5,T6,T7,T8,T9,T10,T11,T12,T13,T14,T15,T16,T17,T18,T19,T20,T21) volatile);
template <class R,class T,class T0,class T1,class T2,class T3,class T4,class T5,class T6,class T7,class T8,class T9,class T10,class T11,class T12,class T13,class T14,class T15,class T16,class T17,class T18,class T19,class T20,class T21 >
yes_type is_mem_fun_pointer_tester(R (T::*)(T0,T1,T2,T3,T4,T5,T6,T7,T8,T9,T10,T11,T12,T13,T14,T15,T16,T17,T18,T19,T20,T21) const volatile);

template <class R,class T,class T0,class T1,class T2,class T3,class T4,class T5,class T6,class T7,class T8,class T9,class T10,class T11,class T12,class T13,class T14,class T15,class T16,class T17,class T18,class T19,class T20,class T21,class T22 >
yes_type is_mem_fun_pointer_tester(R (T::*)(T0,T1,T2,T3,T4,T5,T6,T7,T8,T9,T10,T11,T12,T13,T14,T15,T16,T17,T18,T19,T20,T21,T22));
template <class R,class T,class T0,class T1,class T2,class T3,class T4,class T5,class T6,class T7,class T8,class T9,class T10,class T11,class T12,class T13,class T14,class T15,class T16,class T17,class T18,class T19,class T20,class T21,class T22 >
yes_type is_mem_fun_pointer_tester(R (T::*)(T0,T1,T2,T3,T4,T5,T6,T7,T8,T9,T10,T11,T12,T13,T14,T15,T16,T17,T18,T19,T20,T21,T22) const);
template <class R,class T,class T0,class T1,class T2,class T3,class T4,class T5,class T6,class T7,class T8,class T9,class T10,class T11,class T12,class T13,class T14,class T15,class T16,class T17,class T18,class T19,class T20,class T21,class T22 >
yes_type is_mem_fun_pointer_tester(R (T::*)(T0,T1,T2,T3,T4,T5,T6,T7,T8,T9,T10,T11,T12,T13,T14,T15,T16,T17,T18,T19,T20,T21,T22) volatile);
template <class R,class T,class T0,class T1,class T2,class T3,class T4,class T5,class T6,class T7,class T8,class T9,class T10,class T11,class T12,class T13,class T14,class T15,class T16,class T17,class T18,class T19,class T20,class T21,class T22 >
yes_type is_mem_fun_pointer_tester(R (T::*)(T0,T1,T2,T3,T4,T5,T6,T7,T8,T9,T10,T11,T12,T13,T14,T15,T16,T17,T18,T19,T20,T21,T22) const volatile);

template <class R,class T,class T0,class T1,class T2,class T3,class T4,class T5,class T6,class T7,class T8,class T9,class T10,class T11,class T12,class T13,class T14,class T15,class T16,class T17,class T18,class T19,class T20,class T21,class T22,class T23 >
yes_type is_mem_fun_pointer_tester(R (T::*)(T0,T1,T2,T3,T4,T5,T6,T7,T8,T9,T10,T11,T12,T13,T14,T15,T16,T17,T18,T19,T20,T21,T22,T23));
template <class R,class T,class T0,class T1,class T2,class T3,class T4,class T5,class T6,class T7,class T8,class T9,class T10,class T11,class T12,class T13,class T14,class T15,class T16,class T17,class T18,class T19,class T20,class T21,class T22,class T23 >
yes_type is_mem_fun_pointer_tester(R (T::*)(T0,T1,T2,T3,T4,T5,T6,T7,T8,T9,T10,T11,T12,T13,T14,T15,T16,T17,T18,T19,T20,T21,T22,T23) const);
template <class R,class T,class T0,class T1,class T2,class T3,class T4,class T5,class T6,class T7,class T8,class T9,class T10,class T11,class T12,class T13,class T14,class T15,class T16,class T17,class T18,class T19,class T20,class T21,class T22,class T23 >
yes_type is_mem_fun_pointer_tester(R (T::*)(T0,T1,T2,T3,T4,T5,T6,T7,T8,T9,T10,T11,T12,T13,T14,T15,T16,T17,T18,T19,T20,T21,T22,T23) volatile);
template <class R,class T,class T0,class T1,class T2,class T3,class T4,class T5,class T6,class T7,class T8,class T9,class T10,class T11,class T12,class T13,class T14,class T15,class T16,class T17,class T18,class T19,class T20,class T21,class T22,class T23 >
yes_type is_mem_fun_pointer_tester(R (T::*)(T0,T1,T2,T3,T4,T5,T6,T7,T8,T9,T10,T11,T12,T13,T14,T15,T16,T17,T18,T19,T20,T21,T22,T23) const volatile);

template <class R,class T,class T0,class T1,class T2,class T3,class T4,class T5,class T6,class T7,class T8,class T9,class T10,class T11,class T12,class T13,class T14,class T15,class T16,class T17,class T18,class T19,class T20,class T21,class T22,class T23,class T24 >
yes_type is_mem_fun_pointer_tester(R (T::*)(T0,T1,T2,T3,T4,T5,T6,T7,T8,T9,T10,T11,T12,T13,T14,T15,T16,T17,T18,T19,T20,T21,T22,T23,T24));
template <class R,class T,class T0,class T1,class T2,class T3,class T4,class T5,class T6,class T7,class T8,class T9,class T10,class T11,class T12,class T13,class T14,class T15,class T16,class T17,class T18,class T19,class T20,class T21,class T22,class T23,class T24 >
yes_type is_mem_fun_pointer_tester(R (T::*)(T0,T1,T2,T3,T4,T5,T6,T7,T8,T9,T10,T11,T12,T13,T14,T15,T16,T17,T18,T19,T20,T21,T22,T23,T24) const);
template <class R,class T,class T0,class T1,class T2,class T3,class T4,class T5,class T6,class T7,class T8,class T9,class T10,class T11,class T12,class T13,class T14,class T15,class T16,class T17,class T18,class T19,class T20,class T21,class T22,class T23,class T24 >
yes_type is_mem_fun_pointer_tester(R (T::*)(T0,T1,T2,T3,T4,T5,T6,T7,T8,T9,T10,T11,T12,T13,T14,T15,T16,T17,T18,T19,T20,T21,T22,T23,T24) volatile);
template <class R,class T,class T0,class T1,class T2,class T3,class T4,class T5,class T6,class T7,class T8,class T9,class T10,class T11,class T12,class T13,class T14,class T15,class T16,class T17,class T18,class T19,class T20,class T21,class T22,class T23,class T24 >
yes_type is_mem_fun_pointer_tester(R (T::*)(T0,T1,T2,T3,T4,T5,T6,T7,T8,T9,T10,T11,T12,T13,T14,T15,T16,T17,T18,T19,T20,T21,T22,T23,T24) const volatile);

#else

#define BOOST_PP_ITERATION_PARAMS_1 \
    (3, (0, 25, "boost/type_traits/detail/is_mem_fun_pointer_tester.hpp"))
#include BOOST_PP_ITERATE()

#endif // BOOST_TT_PREPROCESSING_MODE

} // namespace type_traits
} // namespace boost

#endif // BOOST_TT_DETAIL_IS_MEM_FUN_POINTER_TESTER_HPP_INCLUDED

///// iteration

#else
#define i BOOST_PP_FRAME_ITERATION(1)

template <class R, class T BOOST_PP_COMMA_IF(i) BOOST_PP_ENUM_PARAMS(i,class T) >
yes_type is_mem_fun_pointer_tester(R (T::*)(BOOST_PP_ENUM_PARAMS(i,T)));

template <class R, class T BOOST_PP_COMMA_IF(i) BOOST_PP_ENUM_PARAMS(i,class T) >
yes_type is_mem_fun_pointer_tester(R (T::*)(BOOST_PP_ENUM_PARAMS(i,T)) const);

template <class R, class T BOOST_PP_COMMA_IF(i) BOOST_PP_ENUM_PARAMS(i,class T) >
yes_type is_mem_fun_pointer_tester(R (T::*)(BOOST_PP_ENUM_PARAMS(i,T)) volatile);

template <class R, class T BOOST_PP_COMMA_IF(i) BOOST_PP_ENUM_PARAMS(i,class T) >
yes_type is_mem_fun_pointer_tester(R (T::*)(BOOST_PP_ENUM_PARAMS(i,T)) const volatile);

#undef i
#endif // BOOST_PP_IS_ITERATING
