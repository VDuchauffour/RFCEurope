//
//  Copyright (c) 2000-2002
//  Joerg Walter, Mathias Koch
//
//  Permission to use, copy, modify, distribute and sell this software
//  and its documentation for any purpose is hereby granted without fee,
//  provided that the above copyright notice appear in all copies and
//  that both that copyright notice and this permission notice appear
//  in supporting documentation.  The authors make no representations
//  about the suitability of this software for any purpose.
//  It is provided "as is" without express or implied warranty.
//
//  The authors gratefully acknowledge the support of
//  GeNeSys mbH & Co. KG in producing this work.
//

#ifndef BOOST_UBLAS_FUNCTIONAL_H
#define BOOST_UBLAS_FUNCTIONAL_H

#include <functional>

#include <boost/numeric/ublas/config.hpp>
#include <boost/numeric/ublas/exception.hpp>
#include <boost/numeric/ublas/traits.hpp>
#ifdef BOOST_UBLAS_USE_DUFF_DEVICE
#include <boost/numeric/ublas/duff.hpp>
#endif
#ifdef BOOST_UBLAS_USE_SIMD
#include <boost/numeric/ublas/raw.hpp>
#else
namespace boost { namespace numeric { namespace ublas { namespace raw {
}}}}
#endif
#ifdef BOOST_UBLAS_HAVE_BINDINGS
#include <boost/numeric/bindings/traits/std_vector.hpp>
#include <boost/numeric/bindings/traits/ublas_vector.hpp>
#include <boost/numeric/bindings/traits/ublas_matrix.hpp>
#include <boost/numeric/bindings/atlas/cblas.hpp>
#endif



namespace boost { namespace numeric { namespace ublas {

    // Scalar functors

    // Unary
    template<class T>
    struct scalar_unary_functor {
        typedef T value_type;
        typedef typename type_traits<T>::const_reference argument_type;
        typedef typename type_traits<T>::value_type result_type;
    };

    template<class T>
    struct scalar_identity:
        public scalar_unary_functor<T> {
        typedef typename scalar_unary_functor<T>::argument_type argument_type;
        typedef typename scalar_unary_functor<T>::result_type result_type;

        static BOOST_UBLAS_INLINE
        result_type apply (argument_type t) {
            return t;
        }
    };
    template<class T>
    struct scalar_negate:
        public scalar_unary_functor<T> {
        typedef typename scalar_unary_functor<T>::argument_type argument_type;
        typedef typename scalar_unary_functor<T>::result_type result_type;

        static BOOST_UBLAS_INLINE
        result_type apply (argument_type t) {
            return - t;
        }
    };
    template<class T>
    struct scalar_conj:
        public scalar_unary_functor<T> {
        typedef typename scalar_unary_functor<T>::value_type value_type;
        typedef typename scalar_unary_functor<T>::argument_type argument_type;
        typedef typename scalar_unary_functor<T>::result_type result_type;

        static BOOST_UBLAS_INLINE
        result_type apply (argument_type t) {
            return type_traits<value_type>::conj (t);
        }
    };

    // Unary returning real
    template<class T>
    struct scalar_real_unary_functor {
        typedef T value_type;
        typedef typename type_traits<T>::const_reference argument_type;
        typedef typename type_traits<T>::real_type result_type;
    };

    template<class T>
    struct scalar_real:
        public scalar_real_unary_functor<T> {
        typedef typename scalar_real_unary_functor<T>::value_type value_type;
        typedef typename scalar_real_unary_functor<T>::argument_type argument_type;
        typedef typename scalar_real_unary_functor<T>::result_type result_type;

        static BOOST_UBLAS_INLINE
        result_type apply (argument_type t) {
            return type_traits<value_type>::real (t);
        }
    };
    template<class T>
    struct scalar_imag:
        public scalar_real_unary_functor<T> {
        typedef typename scalar_real_unary_functor<T>::value_type value_type;
        typedef typename scalar_real_unary_functor<T>::argument_type argument_type;
        typedef typename scalar_real_unary_functor<T>::result_type result_type;

        static BOOST_UBLAS_INLINE
        result_type apply (argument_type t) {
            return type_traits<value_type>::imag (t);
        }
    };

    // Binary
    template<class T1, class T2>
    struct scalar_binary_functor {
        typedef typename type_traits<T1>::const_reference argument1_type;
        typedef typename type_traits<T2>::const_reference argument2_type;
        typedef typename promote_traits<T1, T2>::promote_type result_type;
    };

    template<class T1, class T2>
    struct scalar_plus:
        public scalar_binary_functor<T1, T2> {
        typedef typename scalar_binary_functor<T1, T2>::argument1_type argument1_type;
        typedef typename scalar_binary_functor<T1, T2>::argument2_type argument2_type;
        typedef typename scalar_binary_functor<T1, T2>::result_type result_type;

        static BOOST_UBLAS_INLINE
        result_type apply (argument1_type t1, argument2_type t2) {
            return t1 + t2;
        }
    };
    template<class T1, class T2>
    struct scalar_minus:
        public scalar_binary_functor<T1, T2> {
        typedef typename scalar_binary_functor<T1, T2>::argument1_type argument1_type;
        typedef typename scalar_binary_functor<T1, T2>::argument2_type argument2_type;
        typedef typename scalar_binary_functor<T1, T2>::result_type result_type;

        static BOOST_UBLAS_INLINE
        result_type apply (argument1_type t1, argument2_type t2) {
            return t1 - t2;
        }
    };
    template<class T1, class T2>
    struct scalar_multiplies:
        public scalar_binary_functor<T1, T2> {
        typedef typename scalar_binary_functor<T1, T2>::argument1_type argument1_type;
        typedef typename scalar_binary_functor<T1, T2>::argument2_type argument2_type;
        typedef typename scalar_binary_functor<T1, T2>::result_type result_type;

        static BOOST_UBLAS_INLINE
        result_type apply (argument1_type t1, argument2_type t2) {
            return t1 * t2;
        }
    };
    template<class T1, class T2>
    struct scalar_divides:
        public scalar_binary_functor<T1, T2> {
        typedef typename scalar_binary_functor<T1, T2>::argument1_type argument1_type;
        typedef typename scalar_binary_functor<T1, T2>::argument2_type argument2_type;
        typedef typename scalar_binary_functor<T1, T2>::result_type result_type;

        static BOOST_UBLAS_INLINE
        result_type apply (argument1_type t1, argument2_type t2) {
            return t1 / t2;
        }
    };

    template<class T1, class T2>
    struct scalar_binary_assign_functor {
        // ISSUE Remove reference to avoid reference to reference problems
        typedef typename type_traits<typename boost::remove_reference<T1>::type>::reference argument1_type;
        typedef typename type_traits<T2>::const_reference argument2_type;
    };

    struct assign_tag {};
    struct computed_assign_tag {};

    template<class T1, class T2>
    struct scalar_assign:
        public scalar_binary_assign_functor<T1, T2> {
        typedef typename scalar_binary_assign_functor<T1, T2>::argument1_type argument1_type;
        typedef typename scalar_binary_assign_functor<T1, T2>::argument2_type argument2_type;
        typedef assign_tag assign_category;

        static BOOST_UBLAS_INLINE
        void apply (argument1_type t1, argument2_type t2) {
            t1 = t2;
        }

        template<class U1, class U2>
        static BOOST_UBLAS_INLINE
        scalar_assign<U1, U2> make_debug_functor () {
            return scalar_assign<U1, U2> ();
        }

    };
    template<class T1, class T2>
    struct scalar_plus_assign:
        public scalar_binary_assign_functor<T1, T2> {
        typedef typename scalar_binary_assign_functor<T1, T2>::argument1_type argument1_type;
        typedef typename scalar_binary_assign_functor<T1, T2>::argument2_type argument2_type;
        typedef computed_assign_tag assign_category;

        static BOOST_UBLAS_INLINE
        void apply (argument1_type t1, argument2_type t2) {
            t1 += t2;
        }

        template<class U1, class U2>
        static BOOST_UBLAS_INLINE
        scalar_plus_assign<U1, U2> make_debug_functor () {
            return scalar_plus_assign<U1, U2> ();
        }
    };
    template<class T1, class T2>
    struct scalar_minus_assign:
        public scalar_binary_assign_functor<T1, T2> {
        typedef typename scalar_binary_assign_functor<T1, T2>::argument1_type argument1_type;
        typedef typename scalar_binary_assign_functor<T1, T2>::argument2_type argument2_type;
        typedef computed_assign_tag assign_category;

        static BOOST_UBLAS_INLINE
        void apply (argument1_type t1, argument2_type t2) {
            t1 -= t2;
        }

        template<class U1, class U2>
        static BOOST_UBLAS_INLINE
        scalar_minus_assign<U1, U2> make_debug_functor () {
            return scalar_minus_assign<U1, U2> ();
        }
    };
    template<class T1, class T2>
    struct scalar_multiplies_assign:
        public scalar_binary_assign_functor<T1, T2> {
        typedef typename scalar_binary_assign_functor<T1, T2>::argument1_type argument1_type;
        typedef typename scalar_binary_assign_functor<T1, T2>::argument2_type argument2_type;
        typedef computed_assign_tag assign_category;

        static BOOST_UBLAS_INLINE
        void apply (argument1_type t1, argument2_type t2) {
            t1 *= t2;
        }

        template<class U1, class U2>
        static BOOST_UBLAS_INLINE
        scalar_multiplies_assign<U1, U2> make_debug_functor () {
            return scalar_multiplies_assign<U1, U2> ();
        }
    };
    template<class T1, class T2>
    struct scalar_divides_assign:
        public scalar_binary_assign_functor<T1, T2> {
        typedef typename scalar_binary_assign_functor<T1, T2>::argument1_type argument1_type;
        typedef typename scalar_binary_assign_functor<T1, T2>::argument2_type argument2_type;
        typedef computed_assign_tag assign_category;

        static BOOST_UBLAS_INLINE
        void apply (argument1_type t1, argument2_type t2) {
            t1 /= t2;
        }

        template<class U1, class U2>
        static BOOST_UBLAS_INLINE
        scalar_divides_assign<U1, U2> make_debug_functor () {
            return scalar_divides_assign<U1, U2> ();
        }
    };

    template<class T1, class T2>
    struct scalar_binary_swap_functor {
        typedef typename type_traits<typename boost::remove_reference<T1>::type>::reference argument1_type;
        typedef typename type_traits<typename boost::remove_reference<T2>::type>::reference argument2_type;
    };

    template<class T1, class T2>
    struct scalar_swap:
        public scalar_binary_swap_functor<T1, T2> {
        typedef typename scalar_binary_swap_functor<T1, T2>::argument1_type argument1_type;
        typedef typename scalar_binary_swap_functor<T1, T2>::argument2_type argument2_type;

        static BOOST_UBLAS_INLINE
        void apply (argument1_type t1, argument2_type t2) {
            std::swap (t1, t2);
        }

        template<class U1, class U2>
        static BOOST_UBLAS_INLINE
        scalar_swap<U1, U2> make_debug_functor () {
            return scalar_swap<U1, U2> ();
        }
    };

    // Vector functors

    // Unary returning scalar
    template<class T>
    struct vector_scalar_unary_functor {
        typedef std::size_t size_type;
        typedef std::ptrdiff_t difference_type;
        typedef T value_type;
        typedef T result_type;
    };

    template<class T>
    struct vector_sum:
        public vector_scalar_unary_functor<T> {
        typedef typename vector_scalar_unary_functor<T>::size_type size_type;
        typedef typename vector_scalar_unary_functor<T>::difference_type difference_type;
        typedef typename vector_scalar_unary_functor<T>::value_type value_type;
        typedef typename vector_scalar_unary_functor<T>::result_type result_type;

        template<class E>
        static BOOST_UBLAS_INLINE
        result_type apply (const vector_expression<E> &e) {
            result_type t = result_type (0);
            size_type size (e ().size ());
            for (size_type i = 0; i < size; ++ i)
                t += e () (i);
            return t;
        }
        // Dense case
        template<class I>
        static BOOST_UBLAS_INLINE
        result_type apply (difference_type size, I it) {
            result_type t = result_type (0);
            while (-- size >= 0)
                t += *it, ++ it;
            return t;
        }
        // Sparse case
        template<class I>
        static BOOST_UBLAS_INLINE
        result_type apply (I it, const I &it_end) {
            result_type t = result_type (0);
            while (it != it_end)
                t += *it, ++ it;
            return t;
        }
    };

    // Unary returning real scalar
    template<class T>
    struct vector_scalar_real_unary_functor {
        typedef std::size_t size_type;
        typedef std::ptrdiff_t difference_type;
        typedef T value_type;
        typedef typename type_traits<T>::real_type real_type;
        typedef real_type result_type;
    };

    template<class T>
    struct vector_norm_1:
        public vector_scalar_real_unary_functor<T> {
        typedef typename vector_scalar_real_unary_functor<T>::size_type size_type;
        typedef typename vector_scalar_real_unary_functor<T>::difference_type difference_type;
        typedef typename vector_scalar_real_unary_functor<T>::value_type value_type;
        typedef typename vector_scalar_real_unary_functor<T>::real_type real_type;
        typedef typename vector_scalar_real_unary_functor<T>::result_type result_type;

        template<class E>
        static BOOST_UBLAS_INLINE
        result_type apply (const vector_expression<E> &e) {
            real_type t = real_type ();
            size_type size (e ().size ());
            for (size_type i = 0; i < size; ++ i) {
                real_type u (type_traits<value_type>::norm_1 (e () (i)));
                t += u;
            }
            return t;
        }
        // Dense case
        template<class I>
        static BOOST_UBLAS_INLINE
        result_type apply (difference_type size, I it) {
            real_type t = real_type ();
            while (-- size >= 0) {
                real_type u (type_traits<value_type>::norm_1 (*it));
                t += u;
                ++ it;
            }
            return t;
        }
        // Sparse case
        template<class I>
        static BOOST_UBLAS_INLINE
        result_type apply (I it, const I &it_end) {
            real_type t = real_type ();
            while (it != it_end) {
                real_type u (type_traits<value_type>::norm_1 (*it));
                t += u;
                ++ it;
            }
            return t;
        }
    };
    template<class T>
    struct vector_norm_2:
        public vector_scalar_real_unary_functor<T> {
        typedef typename vector_scalar_real_unary_functor<T>::size_type size_type;
        typedef typename vector_scalar_real_unary_functor<T>::difference_type difference_type;
        typedef typename vector_scalar_real_unary_functor<T>::value_type value_type;
        typedef typename vector_scalar_real_unary_functor<T>::real_type real_type;
        typedef typename vector_scalar_real_unary_functor<T>::result_type result_type;

        template<class E>
        static BOOST_UBLAS_INLINE
        result_type apply (const vector_expression<E> &e) {
#ifndef BOOST_UBLAS_SCALED_NORM
            real_type t = real_type ();
            size_type size (e ().size ());
            for (size_type i = 0; i < size; ++ i) {
                real_type u (type_traits<value_type>::norm_2 (e () (i)));
                t +=  u * u;
            }
            return type_traits<real_type>::sqrt (t);
#else
            real_type scale = real_type ();
            real_type sum_squares (1);
            size_type size (e ().size ());
            for (size_type i = 0; i < size; ++ i) {
                real_type u (type_traits<value_type>::norm_2 (e () (i)));
                if (scale < u) {
                    real_type v (scale / u);
                    sum_squares = sum_squares * v * v + real_type (1);
                    scale = u;
                } else {
                    real_type v (u / scale);
                    sum_squares += v * v;
                }
            }
            return scale * type_traits<real_type>::sqrt (sum_squares);
#endif
        }
        // Dense case
        template<class I>
        static BOOST_UBLAS_INLINE
        result_type apply (difference_type size, I it) {
#ifndef BOOST_UBLAS_SCALED_NORM
            real_type t = real_type ();
            while (-- size >= 0) {
                real_type u (type_traits<value_type>::norm_2 (*it));
                t +=  u * u;
                ++ it;
            }
            return type_traits<real_type>::sqrt (t);
#else
            real_type scale = real_type ();
            real_type sum_squares (1);
            while (-- size >= 0) {
                real_type u (type_traits<value_type>::norm_2 (*it));
                if (scale < u) {
                    real_type v (scale / u);
                    sum_squares = sum_squares * v * v + real_type (1);
                    scale = u;
                } else {
                    real_type v (u / scale);
                    sum_squares += v * v;
                }
                ++ it;
            }
            return scale * type_traits<real_type>::sqrt (sum_squares);
#endif
        }
        // Sparse case
        template<class I>
        static BOOST_UBLAS_INLINE
        result_type apply (I it, const I &it_end) {
#ifndef BOOST_UBLAS_SCALED_NORM
            real_type t = real_type ();
            while (it != it_end) {
                real_type u (type_traits<value_type>::norm_2 (*it));
                t +=  u * u;
                ++ it;
            }
            return type_traits<real_type>::sqrt (t);
#else
            real_type scale = real_type ();
            real_type sum_squares (1);
            while (it != it_end) {
                real_type u (type_traits<value_type>::norm_2 (*it));
                if (scale < u) {
                    real_type v (scale / u);
                    sum_squares = sum_squares * v * v + real_type (1);
                    scale = u;
                } else {
                    real_type v (u / scale);
                    sum_squares += v * v;
                }
                ++ it;
            }
            return scale * type_traits<real_type>::sqrt (sum_squares);
#endif
        }
    };
    template<class T>
    struct vector_norm_inf:
        public vector_scalar_real_unary_functor<T> {
        typedef typename vector_scalar_real_unary_functor<T>::size_type size_type;
        typedef typename vector_scalar_real_unary_functor<T>::difference_type difference_type;
        typedef typename vector_scalar_real_unary_functor<T>::value_type value_type;
        typedef typename vector_scalar_real_unary_functor<T>::real_type real_type;
        typedef typename vector_scalar_real_unary_functor<T>::result_type result_type;

        template<class E>
        static BOOST_UBLAS_INLINE
        result_type apply (const vector_expression<E> &e) {
            real_type t = real_type ();
            size_type size (e ().size ());
            for (size_type i = 0; i < size; ++ i) {
                real_type u (type_traits<value_type>::norm_inf (e () (i)));
                if (u > t)
                    t = u;
            }
            return t;
        }
        // Dense case
        template<class I>
        static BOOST_UBLAS_INLINE
        result_type apply (difference_type size, I it) {
            real_type t = real_type ();
            while (-- size >= 0) {
                real_type u (type_traits<value_type>::norm_inf (*it));
                if (u > t)
                    t = u;
                ++ it;
            }
            return t;
        }
        // Sparse case
        template<class I>
        static BOOST_UBLAS_INLINE
        result_type apply (I it, const I &it_end) {
            real_type t = real_type ();
            while (it != it_end) {
                real_type u (type_traits<value_type>::norm_inf (*it));
                if (u > t)
                    t = u;
                ++ it;
            }
            return t;
        }
    };

    // Unary returning index
    template<class T>
    struct vector_scalar_index_unary_functor {
        typedef std::size_t size_type;
        typedef std::ptrdiff_t difference_type;
        typedef T value_type;
        typedef typename type_traits<T>::real_type real_type;
        typedef size_type result_type;
    };

    template<class T>
    struct vector_index_norm_inf:
        public vector_scalar_index_unary_functor<T> {
        typedef typename vector_scalar_index_unary_functor<T>::size_type size_type;
        typedef typename vector_scalar_index_unary_functor<T>::difference_type difference_type;
        typedef typename vector_scalar_index_unary_functor<T>::value_type value_type;
        typedef typename vector_scalar_index_unary_functor<T>::real_type real_type;
        typedef typename vector_scalar_index_unary_functor<T>::result_type result_type;

        template<class E>
        static BOOST_UBLAS_INLINE
        result_type apply (const vector_expression<E> &e) {
            // ISSUE For CBLAS compatibility return 0 index in empty case
            result_type i_norm_inf (0);
            real_type t = real_type ();
            size_type size (e ().size ());
            for (size_type i = 0; i < size; ++ i) {
                real_type u (type_traits<value_type>::norm_inf (e () (i)));
                if (u > t) {
                    i_norm_inf = i;
                    t = u;
                }
            }
            return i_norm_inf;
        }
        // Dense case
        template<class I>
        static BOOST_UBLAS_INLINE
        result_type apply (difference_type size, I it) {
            // ISSUE For CBLAS compatibility return 0 index in empty case
            result_type i_norm_inf (0);
            real_type t = real_type ();
            while (-- size >= 0) {
                real_type u (type_traits<value_type>::norm_inf (*it));
                if (u > t) {
                    i_norm_inf = it.index ();
                    t = u;
                }
                ++ it;
            }
            return i_norm_inf;
        }
        // Sparse case
        template<class I>
        static BOOST_UBLAS_INLINE
        result_type apply (I it, const I &it_end) {
            // ISSUE For CBLAS compatibility return 0 index in empty case
            result_type i_norm_inf (0);
            real_type t = real_type ();
            while (it != it_end) {
                real_type u (type_traits<value_type>::norm_inf (*it));
                if (u > t) {
                    i_norm_inf = it.index ();
                    t = u;
                }
                ++ it;
            }
            return i_norm_inf;
        }
    };

    // Binary returning scalar
    template<class T1, class T2, class TR>
    struct vector_scalar_binary_functor {
        typedef std::size_t size_type;
        typedef std::ptrdiff_t difference_type;
        typedef TR value_type;
        typedef TR result_type;
    };

    template<class T1, class T2, class TR>
    struct vector_inner_prod:
        public vector_scalar_binary_functor<T1, T2, TR> {
        typedef typename vector_scalar_binary_functor<T1, T2, TR>::size_type size_type ;
        typedef typename vector_scalar_binary_functor<T1, T2, TR>::difference_type difference_type;
        typedef typename vector_scalar_binary_functor<T1, T2, TR>::value_type value_type;
        typedef typename vector_scalar_binary_functor<T1, T2, TR>::result_type result_type;

        template<class E1, class E2>
        static BOOST_UBLAS_INLINE
        result_type apply (const vector_expression<E1> &e1,
                                 const vector_expression<E2> &e2,
                                 concrete_tag) {
#ifndef BOOST_UBLAS_HAVE_BINDINGS
            using namespace raw;
            size_type size (BOOST_UBLAS_SAME (e1 ().size (), e2 ().size ()));
            const T1 *data1 = data_const (e1 ());
            const T2 *data2 = data_const (e2 ());
            size_type s1 = stride (e1 ());
            size_type s2 = stride (e2 ());
            result_type t = result_type (0);
            if (s1 == 1 && s2 == 1) {
                for (size_type i = 0; i < size; ++ i)
                    t += data1 [i] * data2 [i];
            } else if (s2 == 1) {
                for (size_type i = 0, i1 = 0; i < size; ++ i, i1 += s1)
                    t += data1 [i1] * data2 [i];
            } else if (s1 == 1) {
                for (size_type i = 0, i2 = 0; i < size; ++ i, i2 += s2)
                    t += data1 [i] * data2 [i2];
            } else {
                for (size_type i = 0, i1 = 0, i2 = 0; i < size; ++ i, i1 += s1, i2 += s2)
                    t += data1 [i1] * data2 [i2];
            }
            return t;
#else
            return boost::numeric::bindings::atlas::dot (e1 (), e2 ());
#endif
        }
        template<class E1, class E2>
        static BOOST_UBLAS_INLINE
        result_type apply (const vector_expression<E1> &e1,
                                 const vector_expression<E2> &e2,
                                 abstract_tag) {
            size_type size (BOOST_UBLAS_SAME (e1 ().size (), e2 ().size ()));
            result_type t = result_type (0);
#ifndef BOOST_UBLAS_USE_DUFF_DEVICE
            for (size_type i = 0; i < size; ++ i)
                t += e1 () (i) * e2 () (i);
#else
            size_type i (0);
            DD (size, 4, r, (t += e1 () (i) * e2 () (i), ++ i));
#endif
            return t;
        }
        template<class E1, class E2>
        static BOOST_UBLAS_INLINE
        result_type apply (const vector_expression<E1> &e1,
                                 const vector_expression<E2> &e2) {
#ifdef BOOST_UBLAS_USE_SIMD
            typedef typename boost::mpl::if_<
                boost::mpl::and_<boost::is_same<typename E1::simd_category, concrete_tag>,
                                 boost::is_same<typename E2::simd_category, concrete_tag> >,
                    concrete_tag,
                    abstract_tag>::type simd_category;
#else
            typedef abstract_tag simd_category;
#endif
            return apply (e1, e2, simd_category ());
        }
        // Dense case
        template<class I1, class I2>
        static BOOST_UBLAS_INLINE
        result_type apply (difference_type size, I1 it1, I2 it2) {
            result_type t = result_type (0);
#ifndef BOOST_UBLAS_USE_DUFF_DEVICE
            while (-- size >= 0)
                t += *it1 * *it2, ++ it1, ++ it2;
#else
            DD (size, 4, r, (t += *it1 * *it2, ++ it1, ++ it2));
#endif
            return t;
        }
        // Packed case
        template<class I1, class I2>
        static BOOST_UBLAS_INLINE
        result_type apply (I1 it1, const I1 &it1_end, I2 it2, const I2 &it2_end) {
            result_type t = result_type (0);
            difference_type it1_size (it1_end - it1);
            difference_type it2_size (it2_end - it2);
            difference_type diff (0);
            if (it1_size > 0 && it2_size > 0)
                diff = it2.index () - it1.index ();
            if (diff != 0) {
                difference_type size = (std::min) (diff, it1_size);
                if (size > 0) {
                    it1 += size;
                    it1_size -= size;
                    diff -= size;
                }
                size = (std::min) (- diff, it2_size);
                if (size > 0) {
                    it2 += size;
                    it2_size -= size;
                    diff += size;
                }
            }
            difference_type size ((std::min) (it1_size, it2_size));
            while (-- size >= 0)
                t += *it1 * *it2, ++ it1, ++ it2;
            return t;
        }
        // Sparse case
        template<class I1, class I2>
        static BOOST_UBLAS_INLINE
        result_type apply (I1 it1, const I1 &it1_end, I2 it2, const I2 &it2_end, sparse_bidirectional_iterator_tag) {
            result_type t = result_type (0);
            if (it1 != it1_end && it2 != it2_end) {
                size_type it1_index = it1.index (), it2_index = it2.index ();
                while (true) {
                    difference_type compare = it1_index - it2_index;
                    if (compare == 0) {
                        t += *it1 * *it2, ++ it1, ++ it2;
                        if (it1 != it1_end && it2 != it2_end) {
                            it1_index = it1.index ();
                            it2_index = it2.index ();
                        } else
                            break;
                    } else if (compare < 0) {
                        increment (it1, it1_end, - compare);
                        if (it1 != it1_end)
                            it1_index = it1.index ();
                        else
                            break;
                    } else if (compare > 0) {
                        increment (it2, it2_end, compare);
                        if (it2 != it2_end)
                            it2_index = it2.index ();
                        else
                            break;
                    }
                }
            }
            return t;
        }
    };

    // Matrix functors

    // Binary returning vector
    template<class T1, class T2, class TR>
    struct matrix_vector_binary_functor {
        typedef std::size_t size_type;
        typedef std::ptrdiff_t difference_type;
        typedef TR value_type;
        typedef TR result_type;
    };

    template<class T1, class T2, class TR>
    struct matrix_vector_prod1:
        public matrix_vector_binary_functor<T1, T2, TR> {
        typedef typename matrix_vector_binary_functor<T1, T2, TR>::size_type size_type;
        typedef typename matrix_vector_binary_functor<T1, T2, TR>::difference_type difference_type;
        typedef typename matrix_vector_binary_functor<T1, T2, TR>::value_type value_type;
        typedef typename matrix_vector_binary_functor<T1, T2, TR>::result_type result_type;

        template<class E1, class E2>
        static BOOST_UBLAS_INLINE
        result_type apply (const matrix_expression<E1> &e1,
                                 const vector_expression<E2> &e2,
                                 size_type i, concrete_tag) {
#ifndef BOOST_UBLAS_HAVE_BINDINGS
            using namespace raw;
            size_type size = BOOST_UBLAS_SAME (e1 ().size2 (), e2 ().size ());
            const T1 *data1 = data_const (e1 ()) + i * stride1 (e1 ());
            const T2 *data2 = data_const (e2 ());
            size_type s1 = stride2 (e1 ());
            size_type s2 = stride (e2 ());
            result_type t = result_type (0);
            if (s1 == 1 && s2 == 1) {
                for (size_type j = 0; j < size; ++ j)
                    t += data1 [j] * data2 [j];
            } else if (s2 == 1) {
                for (size_type j = 0, j1 = 0; j < size; ++ j, j1 += s1)
                    t += data1 [j1] * data2 [j];
            } else if (s1 == 1) {
                for (size_type j = 0, j2 = 0; j < size; ++ j, j2 += s2)
                    t += data1 [j] * data2 [j2];
            } else {
                for (size_type j = 0, j1 = 0, j2 = 0; j < size; ++ j, j1 += s1, j2 += s2)
                    t += data1 [j1] * data2 [j2];
            }
            return t;
#else
            return boost::numeric::bindings::atlas::dot (e1 ().row (i), e2 ());
#endif
        }
        template<class E1, class E2>
        static BOOST_UBLAS_INLINE
        result_type apply (const matrix_expression<E1> &e1,
                                 const vector_expression<E2> &e2,
                                 size_type i, abstract_tag) {
            size_type size = BOOST_UBLAS_SAME (e1 ().size2 (), e2 ().size ());
            result_type t = result_type (0);
#ifndef BOOST_UBLAS_USE_DUFF_DEVICE
            for (size_type j = 0; j < size; ++ j)
                t += e1 () (i, j) * e2 () (j);
#else
            size_type j (0);
            DD (size, 4, r, (t += e1 () (i, j) * e2 () (j), ++ j));
#endif
            return t;
        }
        template<class E1, class E2>
        static BOOST_UBLAS_INLINE
        result_type apply (const matrix_expression<E1> &e1,
                                 const vector_expression<E2> &e2,
                                 size_type i) {
#ifdef BOOST_UBLAS_USE_SIMD
            typedef typename boost::mpl::if_<
                boost::mpl::and_<boost::is_same<typename E1::simd_category, concrete_tag>,
                                 boost::is_same<typename E2::simd_category, concrete_tag> >,
                    concrete_tag,
                    abstract_tag>::type simd_category;
#else
            typedef abstract_tag simd_category;
#endif
            return apply (e1, e2, i, simd_category ());
        }
        // Dense case
        template<class I1, class I2>
        static BOOST_UBLAS_INLINE
        result_type apply (difference_type size, I1 it1, I2 it2) {
            result_type t = result_type (0);
#ifndef BOOST_UBLAS_USE_DUFF_DEVICE
            while (-- size >= 0)
                t += *it1 * *it2, ++ it1, ++ it2;
#else
            DD (size, 4, r, (t += *it1 * *it2, ++ it1, ++ it2));
#endif
            return t;
        }
        // Packed case
        template<class I1, class I2>
        static BOOST_UBLAS_INLINE
        result_type apply (I1 it1, const I1 &it1_end, I2 it2, const I2 &it2_end) {
            result_type t = result_type (0);
            difference_type it1_size (it1_end - it1);
            difference_type it2_size (it2_end - it2);
            difference_type diff (0);
            if (it1_size > 0 && it2_size > 0)
                diff = it2.index () - it1.index2 ();
            if (diff != 0) {
                difference_type size = (std::min) (diff, it1_size);
                if (size > 0) {
                    it1 += size;
                    it1_size -= size;
                    diff -= size;
                }
                size = (std::min) (- diff, it2_size);
                if (size > 0) {
                    it2 += size;
                    it2_size -= size;
                    diff += size;
                }
            }
            difference_type size ((std::min) (it1_size, it2_size));
            while (-- size >= 0)
                t += *it1 * *it2, ++ it1, ++ it2;
            return t;
        }
        // Sparse case
        template<class I1, class I2>
        static BOOST_UBLAS_INLINE
        result_type apply (I1 it1, const I1 &it1_end, I2 it2, const I2 &it2_end,
                                 sparse_bidirectional_iterator_tag, sparse_bidirectional_iterator_tag) {
            result_type t = result_type (0);
            if (it1 != it1_end && it2 != it2_end) {
                size_type it1_index = it1.index2 (), it2_index = it2.index ();
                while (true) {
                    difference_type compare = it1_index - it2_index;
                    if (compare == 0) {
                        t += *it1 * *it2, ++ it1, ++ it2;
                        if (it1 != it1_end && it2 != it2_end) {
                            it1_index = it1.index2 ();
                            it2_index = it2.index ();
                        } else
                            break;
                    } else if (compare < 0) {
                        increment (it1, it1_end, - compare);
                        if (it1 != it1_end)
                            it1_index = it1.index2 ();
                        else
                            break;
                    } else if (compare > 0) {
                        increment (it2, it2_end, compare);
                        if (it2 != it2_end)
                            it2_index = it2.index ();
                        else
                            break;
                    }
                }
            }
            return t;
        }
        // Sparse packed case
        template<class I1, class I2>
        static BOOST_UBLAS_INLINE
        result_type apply (I1 it1, const I1 &it1_end, I2 it2, const I2 &/* it2_end */,
                                 sparse_bidirectional_iterator_tag, packed_random_access_iterator_tag) {
            result_type t = result_type (0);
            while (it1 != it1_end) {
                t += *it1 * it2 () (it1.index2 ());
                ++ it1;
            }
            return t;
        }
        // Packed sparse case
        template<class I1, class I2>
        static BOOST_UBLAS_INLINE
        result_type apply (I1 it1, const I1 &/* it1_end */, I2 it2, const I2 &it2_end,
                                 packed_random_access_iterator_tag, sparse_bidirectional_iterator_tag) {
            result_type t = result_type (0);
            while (it2 != it2_end) {
                t += it1 () (it1.index1 (), it2.index ()) * *it2;
                ++ it2;
            }
            return t;
        }
        // Another dispatcher
        template<class I1, class I2>
        static BOOST_UBLAS_INLINE
        result_type apply (I1 it1, const I1 &it1_end, I2 it2, const I2 &it2_end,
                                 sparse_bidirectional_iterator_tag) {
            typedef typename I1::iterator_category iterator1_category;
            typedef typename I2::iterator_category iterator2_category;
            return apply (it1, it1_end, it2, it2_end, iterator1_category (), iterator2_category ());
        }
    };

    template<class T1, class T2, class TR>
    struct matrix_vector_prod2:
        public matrix_vector_binary_functor<T1, T2, TR> {
        typedef typename matrix_vector_binary_functor<T1, T2, TR>::size_type size_type;
        typedef typename matrix_vector_binary_functor<T1, T2, TR>::difference_type difference_type;
        typedef typename matrix_vector_binary_functor<T1, T2, TR>::value_type value_type;
        typedef typename matrix_vector_binary_functor<T1, T2, TR>::result_type result_type;

        template<class E1, class E2>
        static BOOST_UBLAS_INLINE
        result_type apply (const vector_expression<E1> &e1,
                                 const matrix_expression<E2> &e2,
                                 size_type i, concrete_tag) {
#ifndef BOOST_UBLAS_HAVE_BINDINGS
            using namespace raw;
            size_type size = BOOST_UBLAS_SAME (e1 ().size (), e2 ().size1 ());
            const T1 *data1 = data_const (e1 ());
            const T2 *data2 = data_const (e2 ()) + i * stride2 (e2 ());
            size_type s1 = stride (e1 ());
            size_type s2 = stride1 (e2 ());
            result_type t = result_type (0);
            if (s1 == 1 && s2 == 1) {
                for (size_type j = 0; j < size; ++ j)
                    t += data1 [j] * data2 [j];
            } else if (s2 == 1) {
                for (size_type j = 0, j1 = 0; j < size; ++ j, j1 += s1)
                    t += data1 [j1] * data2 [j];
            } else if (s1 == 1) {
                for (size_type j = 0, j2 = 0; j < size; ++ j, j2 += s2)
                    t += data1 [j] * data2 [j2];
            } else {
                for (size_type j = 0, j1 = 0, j2 = 0; j < size; ++ j, j1 += s1, j2 += s2)
                    t += data1 [j1] * data2 [j2];
            }
            return t;
#else
            return boost::numeric::bindings::atlas::dot (e1 (), e2 ().column (i));
#endif
        }
        template<class E1, class E2>
        static BOOST_UBLAS_INLINE
        result_type apply (const vector_expression<E1> &e1,
                                 const matrix_expression<E2> &e2,
                                 size_type i, abstract_tag) {
            size_type size = BOOST_UBLAS_SAME (e1 ().size (), e2 ().size1 ());
            result_type t = result_type (0);
#ifndef BOOST_UBLAS_USE_DUFF_DEVICE
            for (size_type j = 0; j < size; ++ j)
                t += e1 () (j) * e2 () (j, i);
#else
            size_type j (0);
            DD (size, 4, r, (t += e1 () (j) * e2 () (j, i), ++ j));
#endif
            return t;
        }
        template<class E1, class E2>
        static BOOST_UBLAS_INLINE
        result_type apply (const vector_expression<E1> &e1,
                                 const matrix_expression<E2> &e2,
                                 size_type i) {
#ifdef BOOST_UBLAS_USE_SIMD
            typedef typename boost::mpl::if_<
                boost::mpl::and_<boost::is_same<typename E1::simd_category, concrete_tag>,
                                 boost::is_same<typename E2::simd_category, concrete_tag> >,
                    concrete_tag,
                    abstract_tag>::type simd_category;
#else
            typedef abstract_tag simd_category;
#endif
            return apply (e1, e2, i, simd_category ());
        }
        // Dense case
        template<class I1, class I2>
        static BOOST_UBLAS_INLINE
        result_type apply (difference_type size, I1 it1, I2 it2) {
            result_type t = result_type (0);
#ifndef BOOST_UBLAS_USE_DUFF_DEVICE
            while (-- size >= 0)
                t += *it1 * *it2, ++ it1, ++ it2;
#else
            DD (size, 4, r, (t += *it1 * *it2, ++ it1, ++ it2));
#endif
            return t;
        }
        // Packed case
        template<class I1, class I2>
        static BOOST_UBLAS_INLINE
        result_type apply (I1 it1, const I1 &it1_end, I2 it2, const I2 &it2_end) {
            result_type t = result_type (0);
            difference_type it1_size (it1_end - it1);
            difference_type it2_size (it2_end - it2);
            difference_type diff (0);
            if (it1_size > 0 && it2_size > 0)
                diff = it2.index1 () - it1.index ();
            if (diff != 0) {
                difference_type size = (std::min) (diff, it1_size);
                if (size > 0) {
                    it1 += size;
                    it1_size -= size;
                    diff -= size;
                }
                size = (std::min) (- diff, it2_size);
                if (size > 0) {
                    it2 += size;
                    it2_size -= size;
                    diff += size;
                }
            }
            difference_type size ((std::min) (it1_size, it2_size));
            while (-- size >= 0)
                t += *it1 * *it2, ++ it1, ++ it2;
            return t;
        }
        // Sparse case
        template<class I1, class I2>
        static BOOST_UBLAS_INLINE
        result_type apply (I1 it1, const I1 &it1_end, I2 it2, const I2 &it2_end,
                                 sparse_bidirectional_iterator_tag, sparse_bidirectional_iterator_tag) {
            result_type t = result_type (0);
            if (it1 != it1_end && it2 != it2_end) {
                size_type it1_index = it1.index (), it2_index = it2.index1 ();
                while (true) {
                    difference_type compare = it1_index - it2_index;
                    if (compare == 0) {
                        t += *it1 * *it2, ++ it1, ++ it2;
                        if (it1 != it1_end && it2 != it2_end) {
                            it1_index = it1.index ();
                            it2_index = it2.index1 ();
                        } else
                            break;
                    } else if (compare < 0) {
                        increment (it1, it1_end, - compare);
                        if (it1 != it1_end)
                            it1_index = it1.index ();
                        else
                            break;
                    } else if (compare > 0) {
                        increment (it2, it2_end, compare);
                        if (it2 != it2_end)
                            it2_index = it2.index1 ();
                        else
                            break;
                    }
                }
            }
            return t;
        }
        // Packed sparse case
        template<class I1, class I2>
        static BOOST_UBLAS_INLINE
        result_type apply (I1 it1, const I1 &/* it1_end */, I2 it2, const I2 &it2_end,
                                 packed_random_access_iterator_tag, sparse_bidirectional_iterator_tag) {
            result_type t = result_type (0);
            while (it2 != it2_end) {
                t += it1 () (it2.index1 ()) * *it2;
                ++ it2;
            }
            return t;
        }
        // Sparse packed case
        template<class I1, class I2>
        static BOOST_UBLAS_INLINE
        result_type apply (I1 it1, const I1 &it1_end, I2 it2, const I2 &/* it2_end */,
                                 sparse_bidirectional_iterator_tag, packed_random_access_iterator_tag) {
            result_type t = result_type (0);
            while (it1 != it1_end) {
                t += *it1 * it2 () (it1.index (), it2.index2 ());
                ++ it1;
            }
            return t;
        }
        // Another dispatcher
        template<class I1, class I2>
        static BOOST_UBLAS_INLINE
        result_type apply (I1 it1, const I1 &it1_end, I2 it2, const I2 &it2_end,
                                 sparse_bidirectional_iterator_tag) {
            typedef typename I1::iterator_category iterator1_category;
            typedef typename I2::iterator_category iterator2_category;
            return apply (it1, it1_end, it2, it2_end, iterator1_category (), iterator2_category ());
        }
    };

    // Binary returning matrix
    template<class T1, class T2, class TR>
    struct matrix_matrix_binary_functor {
        typedef std::size_t size_type;
        typedef std::ptrdiff_t difference_type;
        typedef TR value_type;
        typedef TR result_type;
    };

    template<class T1, class T2, class TR>
    struct matrix_matrix_prod:
        public matrix_matrix_binary_functor<T1, T2, TR> {
        typedef typename matrix_matrix_binary_functor<T1, T2, TR>::size_type size_type;
        typedef typename matrix_matrix_binary_functor<T1, T2, TR>::difference_type difference_type;
        typedef typename matrix_matrix_binary_functor<T1, T2, TR>::value_type value_type;
        typedef typename matrix_matrix_binary_functor<T1, T2, TR>::result_type result_type;

        template<class E1, class E2>
        static BOOST_UBLAS_INLINE
        result_type apply (const matrix_expression<E1> &e1,
                                 const matrix_expression<E2> &e2,
                                 size_type i, size_type j, concrete_tag) {
#ifndef BOOST_UBLAS_HAVE_BINDINGS
            using namespace raw;
            size_type size = BOOST_UBLAS_SAME (e1 ().size2 (), e2 ().size1 ());
            const T1 *data1 = data_const (e1 ()) + i * stride1 (e1 ());
            const T2 *data2 = data_const (e2 ()) + j * stride2 (e2 ());
            size_type s1 = stride2 (e1 ());
            size_type s2 = stride1 (e2 ());
            result_type t = result_type (0);
            if (s1 == 1 && s2 == 1) {
                for (size_type k = 0; k < size; ++ k)
                    t += data1 [k] * data2 [k];
            } else if (s2 == 1) {
                for (size_type k = 0, k1 = 0; k < size; ++ k, k1 += s1)
                    t += data1 [k1] * data2 [k];
            } else if (s1 == 1) {
                for (size_type k = 0, k2 = 0; k < size; ++ k, k2 += s2)
                    t += data1 [k] * data2 [k2];
            } else {
                for (size_type k = 0, k1 = 0, k2 = 0; k < size; ++ k, k1 += s1, k2 += s2)
                    t += data1 [k1] * data2 [k2];
            }
            return t;
#else
            return boost::numeric::bindings::atlas::dot (e1 ().row (i), e2 ().column (j));
#endif
        }
        template<class E1, class E2>
        static BOOST_UBLAS_INLINE
        result_type apply (const matrix_expression<E1> &e1,
                                 const matrix_expression<E2> &e2,
                                 size_type i, size_type j, abstract_tag) {
            size_type size = BOOST_UBLAS_SAME (e1 ().size2 (), e2 ().size1 ());
            result_type t = result_type (0);
#ifndef BOOST_UBLAS_USE_DUFF_DEVICE
            for (size_type k = 0; k < size; ++ k)
                t += e1 () (i, k) * e2 () (k, j);
#else
            size_type k (0);
            DD (size, 4, r, (t += e1 () (i, k) * e2 () (k, j), ++ k));
#endif
            return t;
        }
        template<class E1, class E2>
        static BOOST_UBLAS_INLINE
        result_type apply (const matrix_expression<E1> &e1,
                                 const matrix_expression<E2> &e2,
                                 size_type i, size_type j) {
#ifdef BOOST_UBLAS_USE_SIMD
            typedef typename boost::mpl::if_<
                boost::mpl::and_<boost::is_same<typename E1::simd_category, concrete_tag>,
                                 boost::is_same<typename E2::simd_category, concrete_tag> >,
                    concrete_tag,
                    abstract_tag>::type simd_category;
#else
            typedef abstract_tag simd_category;
#endif
            return apply (e1, e2, i, j, simd_category ());
        }
        // Dense case
        template<class I1, class I2>
        static BOOST_UBLAS_INLINE
        result_type apply (difference_type size, I1 it1, I2 it2) {
            result_type t = result_type (0);
#ifndef BOOST_UBLAS_USE_DUFF_DEVICE
            while (-- size >= 0)
                t += *it1 * *it2, ++ it1, ++ it2;
#else
            DD (size, 4, r, (t += *it1 * *it2, ++ it1, ++ it2));
#endif
            return t;
        }
        // Packed case
        template<class I1, class I2>
        static BOOST_UBLAS_INLINE
        result_type apply (I1 it1, const I1 &it1_end, I2 it2, const I2 &it2_end, packed_random_access_iterator_tag) {
            result_type t = result_type (0);
            difference_type it1_size (it1_end - it1);
            difference_type it2_size (it2_end - it2);
            difference_type diff (0);
            if (it1_size > 0 && it2_size > 0)
                diff = it2.index1 () - it1.index2 ();
            if (diff != 0) {
                difference_type size = (std::min) (diff, it1_size);
                if (size > 0) {
                    it1 += size;
                    it1_size -= size;
                    diff -= size;
                }
                size = (std::min) (- diff, it2_size);
                if (size > 0) {
                    it2 += size;
                    it2_size -= size;
                    diff += size;
                }
            }
            difference_type size ((std::min) (it1_size, it2_size));
            while (-- size >= 0)
                t += *it1 * *it2, ++ it1, ++ it2;
            return t;
        }
        // Sparse case
        template<class I1, class I2>
        static BOOST_UBLAS_INLINE
        result_type apply (I1 it1, const I1 &it1_end, I2 it2, const I2 &it2_end, sparse_bidirectional_iterator_tag) {
            result_type t = result_type (0);
            if (it1 != it1_end && it2 != it2_end) {
                size_type it1_index = it1.index2 (), it2_index = it2.index1 ();
                while (true) {
                    difference_type compare = it1_index - it2_index;
                    if (compare == 0) {
                        t += *it1 * *it2, ++ it1, ++ it2;
                        if (it1 != it1_end && it2 != it2_end) {
                            it1_index = it1.index2 ();
                            it2_index = it2.index1 ();
                        } else
                            break;
                    } else if (compare < 0) {
                        increment (it1, it1_end, - compare);
                        if (it1 != it1_end)
                            it1_index = it1.index2 ();
                        else
                            break;
                    } else if (compare > 0) {
                        increment (it2, it2_end, compare);
                        if (it2 != it2_end)
                            it2_index = it2.index1 ();
                        else
                            break;
                    }
                }
            }
            return t;
        }
    };

    // Unary returning scalar norm
    template<class T>
    struct matrix_scalar_real_unary_functor {
        typedef std::size_t size_type;
        typedef std::ptrdiff_t difference_type;
        typedef T value_type;
        typedef typename type_traits<T>::real_type real_type;
        typedef real_type result_type;
    };

    template<class T>
    struct matrix_norm_1:
        public matrix_scalar_real_unary_functor<T> {
        typedef typename matrix_scalar_real_unary_functor<T>::size_type size_type;
        typedef typename matrix_scalar_real_unary_functor<T>::difference_type difference_type;
        typedef typename matrix_scalar_real_unary_functor<T>::value_type value_type;
        typedef typename matrix_scalar_real_unary_functor<T>::real_type real_type;
        typedef typename matrix_scalar_real_unary_functor<T>::result_type result_type;

        template<class E>
        static BOOST_UBLAS_INLINE
        result_type apply (const matrix_expression<E> &e) {
            real_type t = real_type ();
            size_type size2 (e ().size2 ());
            for (size_type j = 0; j < size2; ++ j) {
                real_type u = real_type ();
                size_type size1 (e ().size1 ());
                for (size_type i = 0; i < size1; ++ i) {
                    real_type v (type_traits<value_type>::norm_1 (e () (i, j)));
                    u += v;
                }
                if (u > t)
                    t = u;
            }
            return t;
        }
    };
    template<class T>
    struct matrix_norm_frobenius:
        public matrix_scalar_real_unary_functor<T> {
        typedef typename matrix_scalar_real_unary_functor<T>::size_type size_type;
        typedef typename matrix_scalar_real_unary_functor<T>::difference_type difference_type;
        typedef typename matrix_scalar_real_unary_functor<T>::value_type value_type;
        typedef typename matrix_scalar_real_unary_functor<T>::real_type real_type;
        typedef typename matrix_scalar_real_unary_functor<T>::result_type result_type;

        template<class E>
        static BOOST_UBLAS_INLINE
        result_type apply (const matrix_expression<E> &e) {
            real_type t = real_type ();
            size_type size1 (e ().size1 ());
            for (size_type i = 0; i < size1; ++ i) {
                size_type size2 (e ().size2 ());
                for (size_type j = 0; j < size2; ++ j) {
                    real_type u (type_traits<value_type>::norm_2 (e () (i, j)));
                    t +=  u * u;
                }
            }
            return type_traits<real_type>::sqrt (t);
        }
    };
    template<class T>
    struct matrix_norm_inf:
        public matrix_scalar_real_unary_functor<T> {
        typedef typename matrix_scalar_real_unary_functor<T>::size_type size_type;
        typedef typename matrix_scalar_real_unary_functor<T>::difference_type difference_type;
        typedef typename matrix_scalar_real_unary_functor<T>::value_type value_type;
        typedef typename matrix_scalar_real_unary_functor<T>::real_type real_type;
        typedef typename matrix_scalar_real_unary_functor<T>::result_type result_type;

        template<class E>
        static BOOST_UBLAS_INLINE
        result_type apply (const matrix_expression<E> &e) {
            real_type t = real_type ();
            size_type size1 (e ().size1 ());
            for (size_type i = 0; i < size1; ++ i) {
                real_type u = real_type ();
                size_type size2 (e ().size2 ());
                for (size_type j = 0; j < size2; ++ j) {
                    real_type v (type_traits<value_type>::norm_inf (e () (i, j)));
                    u += v;
                }
                if (u > t)
                    t = u;
            }
            return t;
        }
    };

    // This functor computes the address translation
    // matrix [i] [j] -> storage [i * size2 + j]
    struct row_major {
        typedef std::size_t size_type;
        typedef std::ptrdiff_t difference_type;
        typedef row_major_tag orientation_category;

        static
        BOOST_UBLAS_INLINE
        size_type storage_size (size_type size1, size_type size2) {
            return size1 * size2;
        }

        // Indexing
        static
        BOOST_UBLAS_INLINE
        size_type element (size_type i, size_type size1, size_type j, size_type size2) {
            // Guarding against overflow.
            BOOST_UBLAS_CHECK ((size1 * size2) / size1 == size2, bad_size ());
            BOOST_UBLAS_CHECK (i < size1, bad_index ());
            BOOST_UBLAS_CHECK (j < size2, bad_index ());
            return i * size2 + j;
        }
        static
        BOOST_UBLAS_INLINE
        size_type address (size_type i, size_type size1, size_type j, size_type size2) {
            // Guarding against overflow.
            BOOST_UBLAS_CHECK (size1 == 0 || (size1 * size2) / size1 == size2, bad_size ());
            BOOST_UBLAS_CHECK (i <= size1, bad_index ());
            BOOST_UBLAS_CHECK (j <= size2, bad_index ());
            return i * size2 + j;
        }
        static
        BOOST_UBLAS_INLINE
        difference_type distance1 (difference_type k, size_type /* size1 */, size_type size2) {
            return size2 != 0 ? k / size2 : 0;
        }
        static
        BOOST_UBLAS_INLINE
        difference_type distance2 (difference_type k, size_type /* size1 */, size_type /* size2 */) {
            return k;
        }
        static
        BOOST_UBLAS_INLINE
        size_type index1 (difference_type k, size_type /* size1 */, size_type size2) {
            return size2 != 0 ? k / size2 : 0;
        }
        static
        BOOST_UBLAS_INLINE
        size_type index2 (difference_type k, size_type /* size1 */, size_type size2) {
            return size2 != 0 ? k % size2 : 0;
        }
        static
        BOOST_UBLAS_INLINE
        bool fast1 () {
            return false;
        }
        static
        BOOST_UBLAS_INLINE
        size_type one1 (size_type /* size1 */, size_type size2) {
            return size2;
        }
        static
        BOOST_UBLAS_INLINE
        bool fast2 () {
            return true;
        }
        static
        BOOST_UBLAS_INLINE
        size_type one2 (size_type /* size1 */, size_type /* size2 */) {
            return 1;
        }

        static
        BOOST_UBLAS_INLINE
        size_type lower_element (size_type i, size_type size1, size_type j, size_type size2) {
            BOOST_UBLAS_CHECK (i < size1, bad_index ());
            BOOST_UBLAS_CHECK (j < size2, bad_index ());
            BOOST_UBLAS_CHECK (i >= j, bad_index ());
            // sigma_i (i + 1) = (i + 1) * i / 2
            // i = 0 1 2 3, sigma = 0 1 3 6
            return ((i + 1) * i) / 2 + j;
        }
        static
        BOOST_UBLAS_INLINE
        size_type upper_element (size_type i, size_type size1, size_type j, size_type size2) {
            BOOST_UBLAS_CHECK (i < size1, bad_index ());
            BOOST_UBLAS_CHECK (j < size2, bad_index ());
            BOOST_UBLAS_CHECK (i <= j, bad_index ());
            // sigma_i (size - i) = size * i - i * (i - 1) / 2
            // i = 0 1 2 3, sigma = 0 4 7 9
            return (i * (2 * (std::max) (size1, size2) - i + 1)) / 2 + j - i;
        }

        static
        BOOST_UBLAS_INLINE
        size_type element1 (size_type i, size_type size1, size_type /* j */, size_type /* size2 */) {
            BOOST_UBLAS_CHECK (i < size1, bad_index ());
            return i;
        }
        static
        BOOST_UBLAS_INLINE
        size_type element2 (size_type /* i */, size_type /* size1 */, size_type j, size_type size2) {
            BOOST_UBLAS_CHECK (j < size2, bad_index ());
            return j;
        }
        static
        BOOST_UBLAS_INLINE
        size_type address1 (size_type i, size_type size1, size_type /* j */, size_type /* size2 */) {
            BOOST_UBLAS_CHECK (i <= size1, bad_index ());
            return i;
        }
        static
        BOOST_UBLAS_INLINE
        size_type address2 (size_type /* i */, size_type /* size1 */, size_type j, size_type size2) {
            BOOST_UBLAS_CHECK (j <= size2, bad_index ());
            return j;
        }
        static
        BOOST_UBLAS_INLINE
        size_type index1 (size_type index1, size_type /* index2 */) {
            return index1;
        }
        static
        BOOST_UBLAS_INLINE
        size_type index2 (size_type /* index1 */, size_type index2) {
            return index2;
        }
        static
        BOOST_UBLAS_INLINE
        size_type size1 (size_type size1, size_type /* size2 */) {
            return size1;
        }
        static
        BOOST_UBLAS_INLINE
        size_type size2 (size_type /* size1 */, size_type size2) {
            return size2;
        }

        // Iterating
        template<class I>
        static
        BOOST_UBLAS_INLINE
        void increment1 (I &it, size_type /* size1 */, size_type size2) {
            it += size2;
        }
        template<class I>
        static
        BOOST_UBLAS_INLINE
        void decrement1 (I &it, size_type /* size1 */, size_type size2) {
            it -= size2;
        }
        template<class I>
        static
        BOOST_UBLAS_INLINE
        void increment2 (I &it, size_type /* size1 */, size_type /* size2 */) {
            ++ it;
        }
        template<class I>
        static
        BOOST_UBLAS_INLINE
        void decrement2 (I &it, size_type /* size1 */, size_type /* size2 */) {
            -- it;
        }
    };

    // This functor computes the address translation
    // matrix [i] [j] -> storage [i + j * size1]
    struct column_major {
        typedef std::size_t size_type;
        typedef std::ptrdiff_t difference_type;
        typedef column_major_tag orientation_category;

        static
        BOOST_UBLAS_INLINE
        size_type storage_size (size_type size1, size_type size2) {
            return size1 * size2;
        }

        // Indexing
        static
        BOOST_UBLAS_INLINE
        size_type element (size_type i, size_type size1, size_type j, size_type size2) {
            // Guarding against overflow.
            BOOST_UBLAS_CHECK ((size1 * size2) / size1 == size2, bad_size ());
            BOOST_UBLAS_CHECK (i < size1, bad_index ());
            BOOST_UBLAS_CHECK (j < size2, bad_index ());
            return i + j * size1;
        }
        static
        BOOST_UBLAS_INLINE
        size_type address (size_type i, size_type size1, size_type j, size_type size2) {
            // Guarding against overflow.
            BOOST_UBLAS_CHECK (size1 == 0 || (size1 * size2) / size1 == size2, bad_size ());
            BOOST_UBLAS_CHECK (i <= size1, bad_index ());
            BOOST_UBLAS_CHECK (j <= size2, bad_index ());
            return i + j * size1;
        }
        static
        BOOST_UBLAS_INLINE
        difference_type distance1 (difference_type k, size_type /* size1 */, size_type /* size2 */) {
            return k;
        }
        static
        BOOST_UBLAS_INLINE
        difference_type distance2 (difference_type k, size_type size1, size_type /* size2 */) {
            return size1 != 0 ? k / size1 : 0;
        }
        static
        BOOST_UBLAS_INLINE
        size_type index1 (difference_type k, size_type size1, size_type /* size2 */) {
            return size1 != 0 ? k % size1 : 0;
        }
        static
        BOOST_UBLAS_INLINE
        size_type index2 (difference_type k, size_type size1, size_type /* size2 */) {
            return size1 != 0 ? k / size1 : 0;
        }
        static
        BOOST_UBLAS_INLINE
        bool fast1 () {
            return true;
        }
        static
        BOOST_UBLAS_INLINE
        size_type one1 (size_type /* size1 */, size_type /* size2 */) {
            return 1;
        }
        static
        BOOST_UBLAS_INLINE
        bool fast2 () {
            return false;
        }
        static
        BOOST_UBLAS_INLINE
        size_type one2 (size_type size1, size_type /* size2 */) {
            return size1;
        }

        static
        BOOST_UBLAS_INLINE
        size_type lower_element (size_type i, size_type size1, size_type j, size_type size2) {
            BOOST_UBLAS_CHECK (i < size1, bad_index ());
            BOOST_UBLAS_CHECK (j < size2, bad_index ());
            BOOST_UBLAS_CHECK (i >= j, bad_index ());
            // sigma_j (size - j) = size * j - j * (j - 1) / 2
            // j = 0 1 2 3, sigma = 0 4 7 9
            return i - j + (j * (2 * (std::max) (size1, size2) - j + 1)) / 2;
        }
        static
        BOOST_UBLAS_INLINE
        size_type upper_element (size_type i, size_type size1, size_type j, size_type size2) {
            BOOST_UBLAS_CHECK (i < size1, bad_index ());
            BOOST_UBLAS_CHECK (j < size2, bad_index ());
            BOOST_UBLAS_CHECK (i <= j, bad_index ());
            // sigma_j (j + 1) = (j + 1) * j / 2
            // j = 0 1 2 3, sigma = 0 1 3 6
            return i + ((j + 1) * j) / 2;
        }

        static
        BOOST_UBLAS_INLINE
        size_type element1 (size_type /* i */, size_type /* size1 */, size_type j, size_type size2) {
            BOOST_UBLAS_CHECK (j < size2, bad_index ());
            return j;
        }
        static
        BOOST_UBLAS_INLINE
        size_type element2 (size_type i, size_type size1, size_type /* j */, size_type /* size2 */) {
            BOOST_UBLAS_CHECK (i < size1, bad_index ());
            return i;
        }
        static
        BOOST_UBLAS_INLINE
        size_type address1 (size_type /* i */, size_type /* size1 */, size_type j, size_type size2) {
            BOOST_UBLAS_CHECK (j <= size2, bad_index ());
            return j;
        }
        static
        BOOST_UBLAS_INLINE
        size_type address2 (size_type i, size_type size1, size_type /* j */, size_type /* size2 */) {
            BOOST_UBLAS_CHECK (i <= size1, bad_index ());
            return i;
        }
        static
        BOOST_UBLAS_INLINE
        size_type index1 (size_type /* index1 */, size_type index2) {
            return index2;
        }
        static
        BOOST_UBLAS_INLINE
        size_type index2 (size_type index1, size_type /* index2 */) {
            return index1;
        }
        static
        BOOST_UBLAS_INLINE
        size_type size1 (size_type /* size1 */, size_type size2) {
            return size2;
        }
        static
        BOOST_UBLAS_INLINE
        size_type size2 (size_type size1, size_type /* size2 */) {
            return size1;
        }

        // Iterating
        template<class I>
        static
        BOOST_UBLAS_INLINE
        void increment1 (I &it, size_type /* size1 */, size_type /* size2 */) {
            ++ it;
        }
        template<class I>
        static
        BOOST_UBLAS_INLINE
        void decrement1 (I &it, size_type /* size1 */, size_type /* size2 */) {
            -- it;
        }
        template<class I>
        static
        BOOST_UBLAS_INLINE
        void increment2 (I &it, size_type size1, size_type /* size2 */) {
            it += size1;
        }
        template<class I>
        static
        BOOST_UBLAS_INLINE
        void decrement2 (I &it, size_type size1, size_type /* size2 */) {
            it -= size1;
        }
    };

    struct full {
        typedef std::size_t size_type;

        static
        BOOST_UBLAS_INLINE
        size_type packed_size (size_type size1, size_type size2) {
            return size1 * size2;
        }

        static
        BOOST_UBLAS_INLINE
        bool zero (size_type /* i */, size_type /* j */) {
            return false;
        }
        static
        BOOST_UBLAS_INLINE
        bool one (size_type /* i */, size_type /* j */) {
            return false;
        }
        static
        BOOST_UBLAS_INLINE
        bool other (size_type /* i */, size_type /* j */) {
            return true;
        }
    };

    struct lower {
        typedef std::size_t size_type;
        typedef lower_tag packed_category;

        static
        BOOST_UBLAS_INLINE
        size_type packed_size (size_type size1, size_type size2) {
            size_type size = (std::max) (size1, size2);
            return ((size + 1) * size) / 2;
        }

        static
        BOOST_UBLAS_INLINE
        bool zero (size_type i, size_type j) {
            return j > i;
        }
        static
        BOOST_UBLAS_INLINE
        bool one (size_type /* i */, size_type /* j */) {
            return false;
        }
        static
        BOOST_UBLAS_INLINE
        bool other (size_type i, size_type j) {
            return j <= i;
        }
        template<class F>
        static
        BOOST_UBLAS_INLINE
        size_type element (F, size_type i, size_type size1, size_type j, size_type size2) {
            return F::lower_element (i, size1, j, size2);
        }

        static
        BOOST_UBLAS_INLINE
        size_type restrict1 (size_type i, size_type j) {
            return (std::max) (i, j);
        }
        static
        BOOST_UBLAS_INLINE
        size_type restrict2 (size_type i, size_type j) {
            return (std::min) (i + 1, j);
        }
        static
        BOOST_UBLAS_INLINE
        size_type mutable_restrict1 (size_type i, size_type j) {
            return (std::max) (i, j);
        }
        static
        BOOST_UBLAS_INLINE
        size_type mutable_restrict2 (size_type i, size_type j) {
            return (std::min) (i + 1, j);
        }
    };
    struct upper {
        typedef std::size_t size_type;
        typedef upper_tag packed_category;

        static
        BOOST_UBLAS_INLINE
        size_type packed_size (size_type size1, size_type size2) {
            size_type size = (std::max) (size1, size2);
            return ((size + 1) * size) / 2;
        }

        static
        BOOST_UBLAS_INLINE
        bool zero (size_type i, size_type j) {
            return j < i;
        }
        static
        BOOST_UBLAS_INLINE
        bool one (size_type /* i */, size_type /* j */) {
            return false;
        }
        static
        BOOST_UBLAS_INLINE
        bool other (size_type i, size_type j) {
            return j >= i;
        }
        template<class F>
        static
        BOOST_UBLAS_INLINE
        size_type element (F, size_type i, size_type size1, size_type j, size_type size2) {
            return F::upper_element (i, size1, j, size2);
        }

        static
        BOOST_UBLAS_INLINE
        size_type restrict1 (size_type i, size_type j) {
            return (std::min) (i, j + 1);
        }
        static
        BOOST_UBLAS_INLINE
        size_type restrict2 (size_type i, size_type j) {
            return (std::max) (i, j);
        }
        static
        BOOST_UBLAS_INLINE
        size_type mutable_restrict1 (size_type i, size_type j) {
            return (std::min) (i, j + 1);
        }
        static
        BOOST_UBLAS_INLINE
        size_type mutable_restrict2 (size_type i, size_type j) {
            return (std::max) (i, j);
        }
    };
    struct unit_lower {
        typedef std::size_t size_type;
        typedef unit_lower_tag packed_category;

        static
        BOOST_UBLAS_INLINE
        size_type packed_size (size_type size1, size_type size2) {
            size_type size = (std::max) (size1, size2);
            return ((size + 1) * size) / 2;
        }

        static
        BOOST_UBLAS_INLINE
        bool zero (size_type i, size_type j) {
            return j > i;
        }
        static
        BOOST_UBLAS_INLINE
        bool one (size_type i, size_type j) {
            return j == i;
        }
        static
        BOOST_UBLAS_INLINE
        bool other (size_type i, size_type j) {
            return j < i;
        }
        template<class F>
        static
        BOOST_UBLAS_INLINE
        size_type element (F, size_type i, size_type size1, size_type j, size_type size2) {
            return F::lower_element (i, size1, j, size2);
        }

        static
        BOOST_UBLAS_INLINE
        size_type restrict1 (size_type i, size_type j) {
            return (std::max) (i, j);
        }
        static
        BOOST_UBLAS_INLINE
        size_type restrict2 (size_type i, size_type j) {
            return (std::min) (i + 1, j);
        }
        static
        BOOST_UBLAS_INLINE
        size_type mutable_restrict1 (size_type i, size_type j) {
            return (std::max) (i, j);
        }
        static
        BOOST_UBLAS_INLINE
        size_type mutable_restrict2 (size_type i, size_type j) {
            return (std::min) (i, j);
        }
    };
    struct unit_upper {
        typedef std::size_t size_type;
        typedef unit_upper_tag packed_category;

        static
        BOOST_UBLAS_INLINE
        size_type packed_size (size_type size1, size_type size2) {
            size_type size = (std::max) (size1, size2);
            return ((size + 1) * size) / 2;
        }

        static
        BOOST_UBLAS_INLINE
        bool zero (size_type i, size_type j) {
            return j < i;
        }
        static
        BOOST_UBLAS_INLINE
        bool one (size_type i, size_type j) {
            return j == i;
        }
        static
        BOOST_UBLAS_INLINE
        bool other (size_type i, size_type j) {
            return j > i;
        }
        template<class F>
        static
        BOOST_UBLAS_INLINE
        size_type element (F, size_type i, size_type size1, size_type j, size_type size2) {
            return F::upper_element (i, size1, j, size2);
        }

        static
        BOOST_UBLAS_INLINE
        size_type restrict1 (size_type i, size_type j) {
            return (std::min) (i, j + 1);
        }
        static
        BOOST_UBLAS_INLINE
        size_type restrict2 (size_type i, size_type j) {
            return (std::max) (i, j);
        }
        static
        BOOST_UBLAS_INLINE
        size_type mutable_restrict1 (size_type i, size_type j) {
            return (std::min) (i, j);
        }
        static
        BOOST_UBLAS_INLINE
        size_type mutable_restrict2 (size_type i, size_type j) {
            return (std::max) (i, j);
        }
    };
    struct strict_lower {
        typedef std::size_t size_type;
        typedef unit_lower_tag packed_category;

        static
        BOOST_UBLAS_INLINE
        size_type packed_size (size_type size1, size_type size2) {
            size_type size = (std::max) (size1, size2);
            return ((size + 1) * size) / 2;
        }

        static
        BOOST_UBLAS_INLINE
        bool zero (size_type i, size_type j) {
            return j >= i;
        }
        static
        BOOST_UBLAS_INLINE
        bool one (size_type /*i*/, size_type /*j*/) {
            return false;
        }
        static
        BOOST_UBLAS_INLINE
        bool other (size_type i, size_type j) {
            return j < i;
        }
        template<class F>
        static
        BOOST_UBLAS_INLINE
        size_type element (F, size_type i, size_type size1, size_type j, size_type size2) {
            return F::lower_element (i, size1, j, size2);
        }

        static
        BOOST_UBLAS_INLINE
        size_type restrict1 (size_type i, size_type j) {
            return (std::max) (i, j);
        }
        static
        BOOST_UBLAS_INLINE
        size_type restrict2 (size_type i, size_type j) {
            return (std::min) (i, j);
        }
        static
        BOOST_UBLAS_INLINE
        size_type mutable_restrict1 (size_type i, size_type j) {
            return (std::max) (i, j);
        }
        static
        BOOST_UBLAS_INLINE
        size_type mutable_restrict2 (size_type i, size_type j) {
            return (std::min) (i, j);
        }
    };
    struct strict_upper {
        typedef std::size_t size_type;
        typedef unit_upper_tag packed_category;

        static
        BOOST_UBLAS_INLINE
        size_type packed_size (size_type size1, size_type size2) {
            size_type size = (std::max) (size1, size2);
            return ((size + 1) * size) / 2;
        }

        static
        BOOST_UBLAS_INLINE
        bool zero (size_type i, size_type j) {
            return j <= i;
        }
        static
        BOOST_UBLAS_INLINE
        bool one (size_type /*i*/, size_type /*j*/) {
            return false;
        }
        static
        BOOST_UBLAS_INLINE
        bool other (size_type i, size_type j) {
            return j > i;
        }
        template<class F>
        static
        BOOST_UBLAS_INLINE
        size_type element (F, size_type i, size_type size1, size_type j, size_type size2) {
            return F::upper_element (i, size1, j, size2);
        }

        static
        BOOST_UBLAS_INLINE
        size_type restrict1 (size_type i, size_type j) {
            return (std::min) (i, j);
        }
        static
        BOOST_UBLAS_INLINE
        size_type restrict2 (size_type i, size_type j) {
            return (std::max) (i, j);
        }
        static
        BOOST_UBLAS_INLINE
        size_type mutable_restrict1 (size_type i, size_type j) {
            return (std::min) (i, j);
        }
        static
        BOOST_UBLAS_INLINE
        size_type mutable_restrict2 (size_type i, size_type j) {
            return (std::max) (i, j);
        }
    };

}}}

#endif
