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

#ifndef BOOST_UBLAS_MATRIX_H
#define BOOST_UBLAS_MATRIX_H

#include <boost/numeric/ublas/config.hpp>
#include <boost/numeric/ublas/storage.hpp>
#include <boost/numeric/ublas/vector.hpp>
#include <boost/numeric/ublas/matrix_expression.hpp>
#include <boost/numeric/ublas/matrix_assign.hpp>
#include <boost/numeric/ublas/matrix_proxy.hpp>

// Iterators based on ideas of Jeremy Siek

namespace boost { namespace numeric { namespace ublas {

    namespace detail {
        using namespace boost::numeric::ublas;

        // Matrix resizing algorithm
        template <class F, class M>
        BOOST_UBLAS_INLINE
        void matrix_resize_preserve (M& m, M& temporary, BOOST_UBLAS_TYPENAME M::size_type size1, BOOST_UBLAS_TYPENAME M::size_type size2) {
            typedef F functor_type;
            typedef typename M::size_type size_type;
            // Common elements to preserve
            const size_type size1_min = (std::min) (size1, m.size1_);
            const size_type size2_min = (std::min) (size2, m.size2_);
            // Order loop for i-major and j-minor sizes
            const size_type i_size = functor_type::size1 (size1_min, size2_min);
            const size_type j_size = functor_type::size2 (size1_min, size2_min);
            for (size_type i = 0; i != i_size; ++i) {    // indexing copy over major
                for (size_type j = 0; j != j_size; ++j) {
                    temporary.data () [functor_type::element (functor_type::element1(i,i_size, j,j_size), size1, functor_type::element2(i,i_size, j,j_size), size2)] =
                        m.data() [functor_type::element (functor_type::element1(i,i_size, j,j_size), m.size1_, functor_type::element2(i,i_size, j,j_size), m.size2_)];
                }
            }
            assign_temporary (temporary);
        }
    }


    // Array based matrix class
    template<class T, class F, class A>
    class matrix:
        public matrix_expression<matrix<T, F, A> > {
    public:
#ifndef BOOST_UBLAS_NO_PROXY_SHORTCUTS
        BOOST_UBLAS_USING matrix_expression<matrix<T, F, A> >::operator ();
#endif
        typedef typename A::size_type size_type;
        typedef typename A::difference_type difference_type;
        typedef T value_type;
        typedef const T &const_reference;
        typedef T &reference;
        typedef A array_type;
    private:
        typedef T *pointer;
        typedef F functor_type;
        typedef matrix<T, F, A> self_type;
    public:
#ifndef BOOST_UBLAS_CT_REFERENCE_BASE_TYPEDEFS
        typedef const matrix_const_reference<const self_type> const_closure_type;
#else
        typedef const matrix_reference<const self_type> const_closure_type;
#endif
        typedef matrix_reference<self_type> closure_type;
        typedef vector<T, A> vector_temporary_type;
        typedef self_type matrix_temporary_type;
        typedef dense_tag storage_category;
        // This could be better for performance,
        // typedef typename unknown_orientation_tag orientation_category;
        // but others depend on the orientation information...
        typedef typename functor_type::orientation_category orientation_category;
        typedef concrete_tag simd_category;

        // Construction and destruction
        BOOST_UBLAS_INLINE
        matrix ():
            matrix_expression<self_type> (),
            size1_ (0), size2_ (0), data_ () {}
        BOOST_UBLAS_INLINE
        matrix (size_type size1, size_type size2):
            matrix_expression<self_type> (),
            size1_ (size1), size2_ (size2), data_ (functor_type::storage_size (size1, size2)) {
        }
        BOOST_UBLAS_INLINE
        matrix (size_type size1, size_type size2, const array_type &data):
            matrix_expression<self_type> (),
            size1_ (size1), size2_ (size2), data_ (data) {}
        BOOST_UBLAS_INLINE
        matrix (const matrix &m):
            matrix_expression<self_type> (),
            size1_ (m.size1_), size2_ (m.size2_), data_ (m.data_) {}
        template<class AE>
        BOOST_UBLAS_INLINE
        matrix (const matrix_expression<AE> &ae):
            matrix_expression<self_type> (),
            size1_ (ae ().size1 ()), size2_ (ae ().size2 ()), data_ (functor_type::storage_size (size1_, size2_)) {
            matrix_assign (scalar_assign<reference, BOOST_UBLAS_TYPENAME AE::value_type> (), *this, ae);
        }

        // Accessors
        BOOST_UBLAS_INLINE
        size_type size1 () const {
            return size1_;
        }
        BOOST_UBLAS_INLINE
        size_type size2 () const {
            return size2_;
        }
        BOOST_UBLAS_INLINE
        const array_type &data () const {
            return data_;
        }
        BOOST_UBLAS_INLINE
        array_type &data () {
            return data_;
        }

        // Resizing
        BOOST_UBLAS_INLINE
        void resize (size_type size1, size_type size2, bool preserve = true) {
            if (preserve) {
                self_type temporary (size1, size2);
                // FIXME use matrix_resize_preserve on conformant compilers
                // detail::matrix_resize_reserve<functor_type> (*this, temporary, size1, size2);
                // Common elements to preserve
                const size_type size1_min = (std::min) (size1, size1_);
                const size_type size2_min = (std::min) (size2, size2_);
                // Order loop for i-major and j-minor sizes
                const size_type i_size = functor_type::size1 (size1_min, size2_min);
                const size_type j_size = functor_type::size2 (size1_min, size2_min);
                for (size_type i = 0; i != i_size; ++i) {    // indexing copy over major
                    for (size_type j = 0; j != j_size; ++j) {
                        temporary.data () [functor_type::element (functor_type::element1(i,i_size, j,j_size), size1, functor_type::element2(i,i_size, j,j_size), size2)] =
                            data() [functor_type::element (functor_type::element1(i,i_size, j,j_size), size1_, functor_type::element2(i,i_size, j,j_size), size2_)];
                    }
                }
                assign_temporary (temporary);
            }
            else {
                data ().resize (functor_type::storage_size (size1, size2));
                size1_ = size1;
                size2_ = size2;
            }
        }

        // Element access
        BOOST_UBLAS_INLINE
        const_reference operator () (size_type i, size_type j) const {
            return data () [functor_type::element (i, size1_, j, size2_)];
        }
        BOOST_UBLAS_INLINE
        reference operator () (size_type i, size_type j) {
            return data () [functor_type::element (i, size1_, j, size2_)];
        }

        // Assignment
        BOOST_UBLAS_INLINE
        matrix &operator = (const matrix &m) {
            size1_ = m.size1_;
            size2_ = m.size2_;
            data () = m.data ();
            return *this;
        }
#ifndef BOOST_NO_TEMPLATE_PARTIAL_SPECIALIZATION
        template<class A2, class F2>          // Generic matrix assignment without temporary
        BOOST_UBLAS_INLINE
        matrix &operator = (const matrix<T, A2, F2> &m) {
            resize (m.size1 (), m.size2 ());
            assign (m);
            return *this;
        }
#endif
        BOOST_UBLAS_INLINE
        matrix &assign_temporary (matrix &m) {
            swap (m);
            return *this;
        }
        template<class AE>
        BOOST_UBLAS_INLINE
        matrix &operator = (const matrix_expression<AE> &ae) {
            // return assign (self_type (ae));
            self_type temporary (ae);
            return assign_temporary (temporary);
        }
        template<class AE>
        BOOST_UBLAS_INLINE
        matrix &assign (const matrix_expression<AE> &ae) {
            matrix_assign (scalar_assign<reference, BOOST_UBLAS_TYPENAME AE::value_type> (), *this, ae);
            return *this;
        }
        template<class AE>
        BOOST_UBLAS_INLINE
        matrix& operator += (const matrix_expression<AE> &ae) {
            // return assign (self_type (*this + ae));
            self_type temporary (*this + ae);
            return assign_temporary (temporary);
        }
        template<class AE>
        BOOST_UBLAS_INLINE
        matrix &plus_assign (const matrix_expression<AE> &ae) {
            matrix_assign (scalar_plus_assign<reference, BOOST_UBLAS_TYPENAME AE::value_type> (), *this, ae);
            return *this;
        }
        template<class AE>
        BOOST_UBLAS_INLINE
        matrix& operator -= (const matrix_expression<AE> &ae) {
            // return assign (self_type (*this - ae));
            self_type temporary (*this - ae);
            return assign_temporary (temporary);
        }
        template<class AE>
        BOOST_UBLAS_INLINE
        matrix &minus_assign (const matrix_expression<AE> &ae) {
            matrix_assign (scalar_minus_assign<reference, BOOST_UBLAS_TYPENAME AE::value_type> (), *this, ae);
            return *this;
        }
        template<class AT>
        BOOST_UBLAS_INLINE
        matrix& operator *= (const AT &at) {
            matrix_assign_scalar (scalar_multiplies_assign<reference, AT> (), *this, at);
            return *this;
        }
        template<class AT>
        BOOST_UBLAS_INLINE
        matrix& operator /= (const AT &at) {
            matrix_assign_scalar (scalar_divides_assign<reference, AT> (), *this, at);
            return *this;
        }

        // Swapping
        BOOST_UBLAS_INLINE
        void swap (matrix &m) {
            if (this != &m) {
                std::swap (size1_, m.size1_);
                std::swap (size2_, m.size2_);
                data ().swap (m.data ());
            }
        }
#ifndef BOOST_UBLAS_NO_MEMBER_FRIENDS
        BOOST_UBLAS_INLINE
        friend void swap (matrix &m1, matrix &m2) {
            m1.swap (m2);
        }
#endif

        // Element insertion and erasure
        // These functions should work with std::vector.
        // Thanks to Kresimir Fresl for spotting this.
        BOOST_UBLAS_INLINE
        void insert (size_type i, size_type j, const_reference t) {
            BOOST_UBLAS_CHECK (data () [functor_type::element (i, size1_, j, size2_)] == value_type (0), bad_index ());
            // data ().insert (data ().begin () + functor_type::element (i, size1_, j, size2_), t);
            data () [functor_type::element (i, size1_, j, size2_)] = t;
        }
        BOOST_UBLAS_INLINE
        void erase (size_type i, size_type j) {
            // data ().erase (data ().begin () + functor_type::element (i, size1_, j, size2_));
            data () [functor_type::element (i, size1_, j, size2_)] = value_type (0);
        }
        BOOST_UBLAS_INLINE
        void clear () {
            // data ().clear ();
            std::fill (data ().begin (), data ().end (), value_type (0));
        }

        // Iterator types
    private:
        // Use the storage array iterator
        typedef typename A::const_iterator const_iterator_type;
        typedef typename A::iterator iterator_type;

    public:
#ifdef BOOST_UBLAS_USE_INDEXED_ITERATOR
        typedef indexed_iterator1<self_type, dense_random_access_iterator_tag> iterator1;
        typedef indexed_iterator2<self_type, dense_random_access_iterator_tag> iterator2;
        typedef indexed_const_iterator1<self_type, dense_random_access_iterator_tag> const_iterator1;
        typedef indexed_const_iterator2<self_type, dense_random_access_iterator_tag> const_iterator2;
#else
        class const_iterator1;
        class iterator1;
        class const_iterator2;
        class iterator2;
#endif
#ifdef BOOST_MSVC_STD_ITERATOR
        typedef reverse_iterator_base1<const_iterator1, value_type, const_reference> const_reverse_iterator1;
        typedef reverse_iterator_base1<iterator1, value_type, reference> reverse_iterator1;
        typedef reverse_iterator_base2<const_iterator2, value_type, const_reference> const_reverse_iterator2;
        typedef reverse_iterator_base2<iterator2, value_type, reference> reverse_iterator2;
#else
        typedef reverse_iterator_base1<const_iterator1> const_reverse_iterator1;
        typedef reverse_iterator_base1<iterator1> reverse_iterator1;
        typedef reverse_iterator_base2<const_iterator2> const_reverse_iterator2;
        typedef reverse_iterator_base2<iterator2> reverse_iterator2;
#endif

        // Element lookup
        BOOST_UBLAS_INLINE
        const_iterator1 find1 (int /* rank */, size_type i, size_type j) const {
#ifdef BOOST_UBLAS_USE_INDEXED_ITERATOR
            return const_iterator1 (*this, i, j);
#else
            return const_iterator1 (*this, data ().begin () + functor_type::address (i, size1_, j, size2_));
#endif
        }
        BOOST_UBLAS_INLINE
        iterator1 find1 (int /* rank */, size_type i, size_type j) {
#ifdef BOOST_UBLAS_USE_INDEXED_ITERATOR
            return iterator1 (*this, i, j);
#else
            return iterator1 (*this, data ().begin () + functor_type::address (i, size1_, j, size2_));
#endif
        }
        BOOST_UBLAS_INLINE
        const_iterator2 find2 (int /* rank */, size_type i, size_type j) const {
#ifdef BOOST_UBLAS_USE_INDEXED_ITERATOR
            return const_iterator2 (*this, i, j);
#else
            return const_iterator2 (*this, data ().begin () + functor_type::address (i, size1_, j, size2_));
#endif
        }
        BOOST_UBLAS_INLINE
        iterator2 find2 (int /* rank */, size_type i, size_type j) {
#ifdef BOOST_UBLAS_USE_INDEXED_ITERATOR
            return iterator2 (*this, i, j);
#else
            return iterator2 (*this, data ().begin () + functor_type::address (i, size1_, j, size2_));
#endif
        }


#ifndef BOOST_UBLAS_USE_INDEXED_ITERATOR
        class const_iterator1:
            public container_const_reference<matrix>,
            public random_access_iterator_base<dense_random_access_iterator_tag,
                                               const_iterator1, value_type> {
        public:
            typedef dense_random_access_iterator_tag iterator_category;
#ifdef BOOST_MSVC_STD_ITERATOR
            typedef const_reference reference;
#else
            typedef typename matrix::value_type value_type;
            typedef typename matrix::difference_type difference_type;
            typedef typename matrix::const_reference reference;
            typedef const typename matrix::pointer pointer;
#endif
            typedef const_iterator2 dual_iterator_type;
            typedef const_reverse_iterator2 dual_reverse_iterator_type;

            // Construction and destruction
            BOOST_UBLAS_INLINE
            const_iterator1 ():
                container_const_reference<self_type> (), it_ () {}
            BOOST_UBLAS_INLINE
            const_iterator1 (const self_type &m, const const_iterator_type &it):
                container_const_reference<self_type> (m), it_ (it) {}
            BOOST_UBLAS_INLINE
            const_iterator1 (const iterator1 &it):
                container_const_reference<self_type> (it ()), it_ (it.it_) {}

            // Arithmetic
            BOOST_UBLAS_INLINE
            const_iterator1 &operator ++ () {
                functor_type::increment1 (it_, (*this) ().size1 (), (*this) ().size2 ());
                return *this;
            }
            BOOST_UBLAS_INLINE
            const_iterator1 &operator -- () {
                functor_type::decrement1 (it_, (*this) ().size1 (), (*this) ().size2 ());
                return *this;
            }
            BOOST_UBLAS_INLINE
            const_iterator1 &operator += (difference_type n) {
                it_ += n * functor_type::one1 ((*this) ().size1 (), (*this) ().size2 ());
                return *this;
            }
            BOOST_UBLAS_INLINE
            const_iterator1 &operator -= (difference_type n) {
                it_ -= n * functor_type::one1 ((*this) ().size1 (), (*this) ().size2 ());
                return *this;
            }
            BOOST_UBLAS_INLINE
            difference_type operator - (const const_iterator1 &it) const {
                BOOST_UBLAS_CHECK (&(*this) () == &it (), external_logic ());
                return functor_type::distance1 (it_ - it.it_, (*this) ().size1 (), (*this) ().size2 ());
            }

            // Dereference
            BOOST_UBLAS_INLINE
            const_reference operator * () const {
                BOOST_UBLAS_CHECK (index1 () < (*this) ().size1 (), bad_index ());
                BOOST_UBLAS_CHECK (index2 () < (*this) ().size2 (), bad_index ());
                return *it_;
            }

#ifndef BOOST_UBLAS_NO_NESTED_CLASS_RELATION
            BOOST_UBLAS_INLINE
#ifdef BOOST_UBLAS_MSVC_NESTED_CLASS_RELATION
            typename self_type::
#endif
            const_iterator2 begin () const {
                const self_type &m = (*this) ();
                return m.find2 (1, index1 (), 0);
            }
            BOOST_UBLAS_INLINE
#ifdef BOOST_UBLAS_MSVC_NESTED_CLASS_RELATION
            typename self_type::
#endif
            const_iterator2 end () const {
                const self_type &m = (*this) ();
                return m.find2 (1, index1 (), m.size2 ());
            }
            BOOST_UBLAS_INLINE
#ifdef BOOST_UBLAS_MSVC_NESTED_CLASS_RELATION
            typename self_type::
#endif
            const_reverse_iterator2 rbegin () const {
                return const_reverse_iterator2 (end ());
            }
            BOOST_UBLAS_INLINE
#ifdef BOOST_UBLAS_MSVC_NESTED_CLASS_RELATION
            typename self_type::
#endif
            const_reverse_iterator2 rend () const {
                return const_reverse_iterator2 (begin ());
            }
#endif

            // Indices
            BOOST_UBLAS_INLINE
            size_type index1 () const {
                const self_type &m = (*this) ();
                return functor_type::index1 (it_ - m.begin1 ().it_, m.size1 (), m.size2 ());
            }
            BOOST_UBLAS_INLINE
            size_type index2 () const {
                const self_type &m = (*this) ();
                return functor_type::index2 (it_ - m.begin1 ().it_, m.size1 (), m.size2 ());
            }

            // Assignment
            BOOST_UBLAS_INLINE
            const_iterator1 &operator = (const const_iterator1 &it) {
                container_const_reference<self_type>::assign (&it ());
                it_ = it.it_;
                return *this;
            }

            // Comparison
            BOOST_UBLAS_INLINE
            bool operator == (const const_iterator1 &it) const {
                BOOST_UBLAS_CHECK (&(*this) () == &it (), external_logic ());
                return it_ == it.it_;
            }
            BOOST_UBLAS_INLINE
            bool operator < (const const_iterator1 &it) const {
                BOOST_UBLAS_CHECK (&(*this) () == &it (), external_logic ());
                return it_ < it.it_;
            }

        private:
            const_iterator_type it_;

            friend class iterator1;
        };
#endif

        BOOST_UBLAS_INLINE
        const_iterator1 begin1 () const {
            return find1 (0, 0, 0);
        }
        BOOST_UBLAS_INLINE
        const_iterator1 end1 () const {
            return find1 (0, size1_, 0);
        }

#ifndef BOOST_UBLAS_USE_INDEXED_ITERATOR
        class iterator1:
            public container_reference<matrix>,
            public random_access_iterator_base<dense_random_access_iterator_tag,
                                               iterator1, value_type> {
        public:
            typedef dense_random_access_iterator_tag iterator_category;
#ifndef BOOST_MSVC_STD_ITERATOR
            typedef typename matrix::value_type value_type;
            typedef typename matrix::difference_type difference_type;
            typedef typename matrix::reference reference;
            typedef typename matrix::pointer pointer;
#endif
            typedef iterator2 dual_iterator_type;
            typedef reverse_iterator2 dual_reverse_iterator_type;

            // Construction and destruction
            BOOST_UBLAS_INLINE
            iterator1 ():
                container_reference<self_type> (), it_ () {}
            BOOST_UBLAS_INLINE
            iterator1 (self_type &m, const iterator_type &it):
                container_reference<self_type> (m), it_ (it) {}

            // Arithmetic
            BOOST_UBLAS_INLINE
            iterator1 &operator ++ () {
                functor_type::increment1 (it_, (*this) ().size1 (), (*this) ().size2 ());
                return *this;
            }
            BOOST_UBLAS_INLINE
            iterator1 &operator -- () {
                functor_type::decrement1 (it_, (*this) ().size1 (), (*this) ().size2 ());
                return *this;
            }
            BOOST_UBLAS_INLINE
            iterator1 &operator += (difference_type n) {
                it_ += n * functor_type::one1 ((*this) ().size1 (), (*this) ().size2 ());
                return *this;
            }
            BOOST_UBLAS_INLINE
            iterator1 &operator -= (difference_type n) {
                it_ -= n * functor_type::one1 ((*this) ().size1 (), (*this) ().size2 ());
                return *this;
            }
            BOOST_UBLAS_INLINE
            difference_type operator - (const iterator1 &it) const {
                BOOST_UBLAS_CHECK (&(*this) () == &it (), external_logic ());
                return functor_type::distance1 (it_ - it.it_, (*this) ().size1 (), (*this) ().size2 ());
            }

            // Dereference
            BOOST_UBLAS_INLINE
            reference operator * () const {
                BOOST_UBLAS_CHECK (index1 () < (*this) ().size1 (), bad_index ());
                BOOST_UBLAS_CHECK (index2 () < (*this) ().size2 (), bad_index ());
                return *it_;
            }

#ifndef BOOST_UBLAS_NO_NESTED_CLASS_RELATION
            BOOST_UBLAS_INLINE
#ifdef BOOST_UBLAS_MSVC_NESTED_CLASS_RELATION
            typename self_type::
#endif
            iterator2 begin () const {
                self_type &m = (*this) ();
                return m.find2 (1, index1 (), 0);
            }
            BOOST_UBLAS_INLINE
#ifdef BOOST_UBLAS_MSVC_NESTED_CLASS_RELATION
            typename self_type::
#endif
            iterator2 end () const {
                self_type &m = (*this) ();
                return m.find2 (1, index1 (), m.size2 ());
            }
            BOOST_UBLAS_INLINE
#ifdef BOOST_UBLAS_MSVC_NESTED_CLASS_RELATION
            typename self_type::
#endif
            reverse_iterator2 rbegin () const {
                return reverse_iterator2 (end ());
            }
            BOOST_UBLAS_INLINE
#ifdef BOOST_UBLAS_MSVC_NESTED_CLASS_RELATION
            typename self_type::
#endif
            reverse_iterator2 rend () const {
                return reverse_iterator2 (begin ());
            }
#endif

            // Indices
            BOOST_UBLAS_INLINE
            size_type index1 () const {
                self_type &m = (*this) ();
                return functor_type::index1 (it_ - m.begin1 ().it_, m.size1 (), m.size2 ());
            }
            BOOST_UBLAS_INLINE
            size_type index2 () const {
                self_type &m = (*this) ();
                return functor_type::index2 (it_ - m.begin1 ().it_, m.size1 (), m.size2 ());
            }

            // Assignment
            BOOST_UBLAS_INLINE
            iterator1 &operator = (const iterator1 &it) {
                container_reference<self_type>::assign (&it ());
                it_ = it.it_;
                return *this;
            }

            // Comparison
            BOOST_UBLAS_INLINE
            bool operator == (const iterator1 &it) const {
                BOOST_UBLAS_CHECK (&(*this) () == &it (), external_logic ());
                return it_ == it.it_;
            }
            BOOST_UBLAS_INLINE
            bool operator < (const iterator1 &it) const {
                BOOST_UBLAS_CHECK (&(*this) () == &it (), external_logic ());
                return it_ < it.it_;
            }

        private:
            iterator_type it_;

            friend class const_iterator1;
        };
#endif

        BOOST_UBLAS_INLINE
        iterator1 begin1 () {
            return find1 (0, 0, 0);
        }
        BOOST_UBLAS_INLINE
        iterator1 end1 () {
            return find1 (0, size1_, 0);
        }

#ifndef BOOST_UBLAS_USE_INDEXED_ITERATOR
        class const_iterator2:
            public container_const_reference<matrix>,
            public random_access_iterator_base<dense_random_access_iterator_tag,
                                               const_iterator2, value_type> {
        public:
            typedef dense_random_access_iterator_tag iterator_category;
#ifdef BOOST_MSVC_STD_ITERATOR
            typedef const_reference reference;
#else
            typedef typename matrix::value_type value_type;
            typedef typename matrix::difference_type difference_type;
            typedef typename matrix::const_reference reference;
            typedef const typename matrix::pointer pointer;
#endif
            typedef const_iterator1 dual_iterator_type;
            typedef const_reverse_iterator1 dual_reverse_iterator_type;

            // Construction and destruction
            BOOST_UBLAS_INLINE
            const_iterator2 ():
                container_const_reference<self_type> (), it_ () {}
            BOOST_UBLAS_INLINE
            const_iterator2 (const self_type &m, const const_iterator_type &it):
                container_const_reference<self_type> (m), it_ (it) {}
            BOOST_UBLAS_INLINE
            const_iterator2 (const iterator2 &it):
                container_const_reference<self_type> (it ()), it_ (it.it_) {}

            // Arithmetic
            BOOST_UBLAS_INLINE
            const_iterator2 &operator ++ () {
                functor_type::increment2 (it_, (*this) ().size1 (), (*this) ().size2 ());
                return *this;
            }
            BOOST_UBLAS_INLINE
            const_iterator2 &operator -- () {
                functor_type::decrement2 (it_, (*this) ().size1 (), (*this) ().size2 ());
                return *this;
            }
            BOOST_UBLAS_INLINE
            const_iterator2 &operator += (difference_type n) {
                it_ += n * functor_type::one2 ((*this) ().size1 (), (*this) ().size2 ());
                return *this;
            }
            BOOST_UBLAS_INLINE
            const_iterator2 &operator -= (difference_type n) {
                it_ -= n * functor_type::one2 ((*this) ().size1 (), (*this) ().size2 ());
                return *this;
            }
            BOOST_UBLAS_INLINE
            difference_type operator - (const const_iterator2 &it) const {
                BOOST_UBLAS_CHECK (&(*this) () == &it (), external_logic ());
                return functor_type::distance2 (it_ - it.it_, (*this) ().size1 (), (*this) ().size2 ());
            }

            // Dereference
            BOOST_UBLAS_INLINE
            const_reference operator * () const {
                BOOST_UBLAS_CHECK (index1 () < (*this) ().size1 (), bad_index ());
                BOOST_UBLAS_CHECK (index2 () < (*this) ().size2 (), bad_index ());
                return *it_;
            }

#ifndef BOOST_UBLAS_NO_NESTED_CLASS_RELATION
            BOOST_UBLAS_INLINE
#ifdef BOOST_UBLAS_MSVC_NESTED_CLASS_RELATION
            typename self_type::
#endif
            const_iterator1 begin () const {
                const self_type &m = (*this) ();
                return m.find1 (1, 0, index2 ());
            }
            BOOST_UBLAS_INLINE
#ifdef BOOST_UBLAS_MSVC_NESTED_CLASS_RELATION
            typename self_type::
#endif
            const_iterator1 end () const {
                const self_type &m = (*this) ();
                return m.find1 (1, m.size1 (), index2 ());
            }
            BOOST_UBLAS_INLINE
#ifdef BOOST_UBLAS_MSVC_NESTED_CLASS_RELATION
            typename self_type::
#endif
            const_reverse_iterator1 rbegin () const {
                return const_reverse_iterator1 (end ());
            }
            BOOST_UBLAS_INLINE
#ifdef BOOST_UBLAS_MSVC_NESTED_CLASS_RELATION
            typename self_type::
#endif
            const_reverse_iterator1 rend () const {
                return const_reverse_iterator1 (begin ());
            }
#endif

            // Indices
            BOOST_UBLAS_INLINE
            size_type index1 () const {
                const self_type &m = (*this) ();
                return functor_type::index1 (it_ - m.begin2 ().it_, m.size1 (), m.size2 ());
            }
            BOOST_UBLAS_INLINE
            size_type index2 () const {
                const self_type &m = (*this) ();
                return functor_type::index2 (it_ - m.begin2 ().it_, m.size1 (), m.size2 ());
            }

            // Assignment
            BOOST_UBLAS_INLINE
            const_iterator2 &operator = (const const_iterator2 &it) {
                container_const_reference<self_type>::assign (&it ());
                it_ = it.it_;
                return *this;
            }

            // Comparison
            BOOST_UBLAS_INLINE
            bool operator == (const const_iterator2 &it) const {
                BOOST_UBLAS_CHECK (&(*this) () == &it (), external_logic ());
                return it_ == it.it_;
            }
            BOOST_UBLAS_INLINE
            bool operator < (const const_iterator2 &it) const {
                BOOST_UBLAS_CHECK (&(*this) () == &it (), external_logic ());
                return it_ < it.it_;
            }

        private:
            const_iterator_type it_;

            friend class iterator2;
        };
#endif

        BOOST_UBLAS_INLINE
        const_iterator2 begin2 () const {
            return find2 (0, 0, 0);
        }
        BOOST_UBLAS_INLINE
        const_iterator2 end2 () const {
            return find2 (0, 0, size2_);
        }

#ifndef BOOST_UBLAS_USE_INDEXED_ITERATOR
        class iterator2:
            public container_reference<matrix>,
            public random_access_iterator_base<dense_random_access_iterator_tag,
                                               iterator2, value_type> {
        public:
            typedef dense_random_access_iterator_tag iterator_category;
#ifndef BOOST_MSVC_STD_ITERATOR
            typedef typename matrix::value_type value_type;
            typedef typename matrix::difference_type difference_type;
            typedef typename matrix::reference reference;
            typedef typename matrix::pointer pointer;
#endif
            typedef iterator1 dual_iterator_type;
            typedef reverse_iterator1 dual_reverse_iterator_type;

            // Construction and destruction
            BOOST_UBLAS_INLINE
            iterator2 ():
                container_reference<self_type> (), it_ () {}
            BOOST_UBLAS_INLINE
            iterator2 (self_type &m, const iterator_type &it):
                container_reference<self_type> (m), it_ (it) {}

            // Arithmetic
            BOOST_UBLAS_INLINE
            iterator2 &operator ++ () {
                functor_type::increment2 (it_, (*this) ().size1 (), (*this) ().size2 ());
                return *this;
            }
            BOOST_UBLAS_INLINE
            iterator2 &operator -- () {
                functor_type::decrement2 (it_, (*this) ().size1 (), (*this) ().size2 ());
                return *this;
            }
            BOOST_UBLAS_INLINE
            iterator2 &operator += (difference_type n) {
                it_ += n * functor_type::one2 ((*this) ().size1 (), (*this) ().size2 ());
                return *this;
            }
            BOOST_UBLAS_INLINE
            iterator2 &operator -= (difference_type n) {
                it_ -= n * functor_type::one2 ((*this) ().size1 (), (*this) ().size2 ());
                return *this;
            }
            BOOST_UBLAS_INLINE
            difference_type operator - (const iterator2 &it) const {
                BOOST_UBLAS_CHECK (&(*this) () == &it (), external_logic ());
                return functor_type::distance2 (it_ - it.it_, (*this) ().size1 (), (*this) ().size2 ());
            }

            // Dereference
            BOOST_UBLAS_INLINE
            reference operator * () const {
                BOOST_UBLAS_CHECK (index1 () < (*this) ().size1 (), bad_index ());
                BOOST_UBLAS_CHECK (index2 () < (*this) ().size2 (), bad_index ());
                return *it_;
            }

#ifndef BOOST_UBLAS_NO_NESTED_CLASS_RELATION
            BOOST_UBLAS_INLINE
#ifdef BOOST_UBLAS_MSVC_NESTED_CLASS_RELATION
            typename self_type::
#endif
            iterator1 begin () const {
                self_type &m = (*this) ();
                return m.find1 (1, 0, index2 ());
            }
            BOOST_UBLAS_INLINE
#ifdef BOOST_UBLAS_MSVC_NESTED_CLASS_RELATION
            typename self_type::
#endif
            iterator1 end () const {
                self_type &m = (*this) ();
                return m.find1 (1, m.size1 (), index2 ());
            }
            BOOST_UBLAS_INLINE
#ifdef BOOST_UBLAS_MSVC_NESTED_CLASS_RELATION
            typename self_type::
#endif
            reverse_iterator1 rbegin () const {
                return reverse_iterator1 (end ());
            }
            BOOST_UBLAS_INLINE
#ifdef BOOST_UBLAS_MSVC_NESTED_CLASS_RELATION
            typename self_type::
#endif
            reverse_iterator1 rend () const {
                return reverse_iterator1 (begin ());
            }
#endif

            // Indices
            BOOST_UBLAS_INLINE
            size_type index1 () const {
                self_type &m = (*this) ();
                return functor_type::index1 (it_ - m.begin2 ().it_, m.size1 (), m.size2 ());
            }
            BOOST_UBLAS_INLINE
            size_type index2 () const {
                self_type &m = (*this) ();
                return functor_type::index2 (it_ - m.begin2 ().it_, m.size1 (), m.size2 ());
            }

            // Assignment
            BOOST_UBLAS_INLINE
            iterator2 &operator = (const iterator2 &it) {
                container_reference<self_type>::assign (&it ());
                it_ = it.it_;
                return *this;
            }

            // Comparison
            BOOST_UBLAS_INLINE
            bool operator == (const iterator2 &it) const {
                BOOST_UBLAS_CHECK (&(*this) () == &it (), external_logic ());
                return it_ == it.it_;
            }
            BOOST_UBLAS_INLINE
            bool operator < (const iterator2 &it) const {
                BOOST_UBLAS_CHECK (&(*this) () == &it (), external_logic ());
                return it_ < it.it_;
            }

        private:
            iterator_type it_;

            friend class const_iterator2;
        };
#endif

        BOOST_UBLAS_INLINE
        iterator2 begin2 () {
            return find2 (0, 0, 0);
        }
        BOOST_UBLAS_INLINE
        iterator2 end2 () {
            return find2 (0, 0, size2_);
        }

        // Reverse iterators

        BOOST_UBLAS_INLINE
        const_reverse_iterator1 rbegin1 () const {
            return const_reverse_iterator1 (end1 ());
        }
        BOOST_UBLAS_INLINE
        const_reverse_iterator1 rend1 () const {
            return const_reverse_iterator1 (begin1 ());
        }

        BOOST_UBLAS_INLINE
        reverse_iterator1 rbegin1 () {
            return reverse_iterator1 (end1 ());
        }
        BOOST_UBLAS_INLINE
        reverse_iterator1 rend1 () {
            return reverse_iterator1 (begin1 ());
        }

        BOOST_UBLAS_INLINE
        const_reverse_iterator2 rbegin2 () const {
            return const_reverse_iterator2 (end2 ());
        }
        BOOST_UBLAS_INLINE
        const_reverse_iterator2 rend2 () const {
            return const_reverse_iterator2 (begin2 ());
        }

        BOOST_UBLAS_INLINE
        reverse_iterator2 rbegin2 () {
            return reverse_iterator2 (end2 ());
        }
        BOOST_UBLAS_INLINE
        reverse_iterator2 rend2 () {
            return reverse_iterator2 (begin2 ());
        }

    private:
        size_type size1_;
        size_type size2_;
        array_type data_;
    };

    // Bounded matrix class
    template<class T, std::size_t M, std::size_t N, class F>
    class bounded_matrix:
        public matrix<T, F, bounded_array<T, M * N> > {

        typedef matrix<T, F, bounded_array<T, M * N> > matrix_type;
    public:
        typedef typename matrix_type::size_type size_type;
        BOOST_STATIC_CONSTANT (size_type, max_size1 = M);
        BOOST_STATIC_CONSTANT (size_type, max_size2 = N);

        // Construction and destruction
        BOOST_UBLAS_INLINE
        bounded_matrix ():
            matrix_type (M, N) {}
        BOOST_UBLAS_INLINE
        bounded_matrix (size_type size1, size_type size2):
            matrix_type (size1, size2) {}
        BOOST_UBLAS_INLINE
        bounded_matrix (const bounded_matrix &m):
            matrix_type (m) {}
        template<class A2>              // Allow matrix<T,bounded_array<M,N> > construction
        BOOST_UBLAS_INLINE
        bounded_matrix (const matrix<T, A2, F> &m):
            matrix_type (m) {}
        template<class AE>
        BOOST_UBLAS_INLINE
        bounded_matrix (const matrix_expression<AE> &ae):
            matrix_type (ae) {}
        BOOST_UBLAS_INLINE
        ~bounded_matrix () {}

        // Assignment
        BOOST_UBLAS_INLINE
        bounded_matrix &operator = (const bounded_matrix &m) {
            matrix_type::operator = (m);
            return *this;
        }
#ifndef BOOST_NO_TEMPLATE_PARTIAL_SPECIALIZATION
        template<class A2, class F2>        // Generic matrix assignment
        BOOST_UBLAS_INLINE
        bounded_matrix &operator = (const matrix<T, A2, F2> &m) {
            matrix_type::operator = (m);
            return *this;
        }
#endif
        template<class AE>
        BOOST_UBLAS_INLINE
        bounded_matrix &operator = (const matrix_expression<AE> &ae) {
            matrix_type::operator = (ae);
            return *this;
        }
    };

    // Array based matrix class
    template<class T, class F, class A>
    class vector_of_vector:
        public matrix_expression<vector_of_vector<T, F, A> > {
    public:
#ifndef BOOST_UBLAS_NO_PROXY_SHORTCUTS
        BOOST_UBLAS_USING matrix_expression<vector_of_vector<T, F, A> >::operator ();
#endif
        typedef typename A::size_type size_type;
        typedef typename A::difference_type difference_type;
        typedef T value_type;
        typedef const T &const_reference;
        typedef T &reference;
        typedef A array_type;
    private:
        typedef T *pointer;
        typedef F functor_type;
        typedef vector_of_vector<T, F, A> self_type;
    public:
#ifndef BOOST_UBLAS_CT_REFERENCE_BASE_TYPEDEFS
        typedef const matrix_const_reference<const self_type> const_closure_type;
#else
        typedef const matrix_reference<const self_type> const_closure_type;
#endif
        typedef matrix_reference<self_type> closure_type;
        typedef vector<T, typename A::value_type> vector_temporary_type;
        typedef self_type matrix_temporary_type;
        typedef dense_tag storage_category;
        // This could be better for performance,
        // typedef typename unknown_orientation_tag orientation_category;
        // but others depend on the orientation information...
        typedef typename functor_type::orientation_category orientation_category;
        typedef concrete_tag simd_category;

        // Construction and destruction
        BOOST_UBLAS_INLINE
        vector_of_vector ():
            matrix_expression<self_type> (),
            size1_ (0), size2_ (0), data_ (1) {}
        BOOST_UBLAS_INLINE
        vector_of_vector (size_type size1, size_type size2):
            matrix_expression<self_type> (),
            size1_ (size1), size2_ (size2), data_ (1) {
            resize (size1, size2, true);
        }
        BOOST_UBLAS_INLINE
        vector_of_vector (const vector_of_vector &m):
            matrix_expression<self_type> (),
            size1_ (m.size1_), size2_ (m.size2_), data_ (m.data_) {}
        template<class AE>
        BOOST_UBLAS_INLINE
        vector_of_vector (const matrix_expression<AE> &ae):
            matrix_expression<self_type> (),
            size1_ (ae ().size1 ()), size2_ (ae ().size2 ()), data_ (functor_type::size1 (size1_, size2_) + 1) {
            for (size_type k = 0; k < functor_type::size1 (size1_, size2_); ++ k)
                data ()[k].resize (functor_type::size2 (size1_, size2_));
            matrix_assign (scalar_assign<reference, BOOST_UBLAS_TYPENAME AE::value_type> (), *this, ae);
        }

        // Accessors
        BOOST_UBLAS_INLINE
        size_type size1 () const {
            return size1_;
        }
        BOOST_UBLAS_INLINE
        size_type size2 () const {
            return size2_;
        }
        BOOST_UBLAS_INLINE
        const array_type &data () const {
            return data_;
        }
        BOOST_UBLAS_INLINE
        array_type &data () {
            return data_;
        }

        // Resizing
        BOOST_UBLAS_INLINE
        void resize (size_type size1, size_type size2, bool preserve = true) {
            size1_ = size1;
            size2_ = size2;
            if (preserve)
                data ().resize (functor_type::size1 (size1, size2) + 1, BOOST_UBLAS_TYPENAME array_type::value_type ());
            else
                data ().resize (functor_type::size1 (size1, size2) + 1);
            for (size_type k = 0; k < functor_type::size1 (size1, size2); ++ k) {
                if (preserve)
                    data () [k].resize (functor_type::size2 (size1, size2), value_type ());
                else
                    data () [k].resize (functor_type::size2 (size1, size2));
            }
        }

        // Element access
        BOOST_UBLAS_INLINE
        const_reference operator () (size_type i, size_type j) const {
            return data () [functor_type::element1 (i, size1_, j, size2_)] [functor_type::element2 (i, size1_, j, size2_)];
        }
        BOOST_UBLAS_INLINE
        reference operator () (size_type i, size_type j) {
            return data () [functor_type::element1 (i, size1_, j, size2_)] [functor_type::element2 (i, size1_, j, size2_)];
        }

        // Assignment
        BOOST_UBLAS_INLINE
        vector_of_vector &operator = (const vector_of_vector &m) {
            size1_ = m.size1_;
            size2_ = m.size2_;
            data () = m.data ();
            return *this;
        }
        BOOST_UBLAS_INLINE
        vector_of_vector &assign_temporary (vector_of_vector &m) {
            swap (m);
            return *this;
        }
        template<class AE>
        BOOST_UBLAS_INLINE
        vector_of_vector &operator = (const matrix_expression<AE> &ae) {
            // return assign (self_type (ae));
            self_type temporary (ae);
            return assign_temporary (temporary);
        }
        template<class AE>
        BOOST_UBLAS_INLINE
        vector_of_vector &assign (const matrix_expression<AE> &ae) {
            matrix_assign (scalar_assign<reference, BOOST_UBLAS_TYPENAME AE::value_type> (), *this, ae);
            return *this;
        }
        template<class AE>
        BOOST_UBLAS_INLINE
        vector_of_vector& operator += (const matrix_expression<AE> &ae) {
            // return assign (self_type (*this + ae));
            self_type temporary (*this + ae);
            return assign_temporary (temporary);
        }
        template<class AE>
        BOOST_UBLAS_INLINE
        vector_of_vector &plus_assign (const matrix_expression<AE> &ae) {
            matrix_assign (scalar_plus_assign<reference, BOOST_UBLAS_TYPENAME AE::value_type> (), *this, ae);
            return *this;
        }
        template<class AE>
        BOOST_UBLAS_INLINE
        vector_of_vector& operator -= (const matrix_expression<AE> &ae) {
            // return assign (self_type (*this - ae));
            self_type temporary (*this - ae);
            return assign_temporary (temporary);
        }
        template<class AE>
        BOOST_UBLAS_INLINE
        vector_of_vector &minus_assign (const matrix_expression<AE> &ae) {
            matrix_assign (scalar_minus_assign<reference, BOOST_UBLAS_TYPENAME AE::value_type> (), *this, ae);
            return *this;
        }
        template<class AT>
        BOOST_UBLAS_INLINE
        vector_of_vector& operator *= (const AT &at) {
            matrix_assign_scalar (scalar_multiplies_assign<reference, AT> (), *this, at);
            return *this;
        }
        template<class AT>
        BOOST_UBLAS_INLINE
        vector_of_vector& operator /= (const AT &at) {
            matrix_assign_scalar (scalar_divides_assign<reference, AT> (), *this, at);
            return *this;
        }

        // Swapping
        BOOST_UBLAS_INLINE
        void swap (vector_of_vector &m) {
            if (this != &m) {
                std::swap (size1_, m.size1_);
                std::swap (size2_, m.size2_);
                data ().swap (m.data ());
            }
        }
#ifndef BOOST_UBLAS_NO_MEMBER_FRIENDS
        BOOST_UBLAS_INLINE
        friend void swap (vector_of_vector &m1, vector_of_vector &m2) {
            m1.swap (m2);
        }
#endif

        // Element insertion and erasure
        // These functions should work with std::vector.
        // Thanks to Kresimir Fresl for spotting this.
        BOOST_UBLAS_INLINE
        void insert (size_type i, size_type j, const_reference t) {
            BOOST_UBLAS_CHECK (data () [functor_type::element1 (i, size1_, j, size2_)] [functor_type::element2 (i, size1_, j, size2_)] == value_type (0), bad_index ());
            data () [functor_type::element1 (i, size1_, j, size2_)] [functor_type::element2 (i, size1_, j, size2_)] = t;
        }
        BOOST_UBLAS_INLINE
        void erase (size_type i, size_type j) {
            data () [functor_type::element1 (i, size1_, j, size2_)] [functor_type::element2 (i, size1_, j, size2_)] = value_type (0);
        }
        BOOST_UBLAS_INLINE
        void clear () {
            for (size_type k = 0; k < functor_type::size1 (size1_, size2_); ++ k)
                // data () [k].clear ();
                std::fill (data () [k].begin (), data () [k].end (), value_type (0));
        }

        // Iterator types
    private:
        // Use the vector iterator
        typedef typename A::const_iterator vector_const_iterator_type;
        typedef typename A::iterator vector_iterator_type;
        typedef typename A::value_type::const_iterator const_iterator_type;
        typedef typename A::value_type::iterator iterator_type;
    public:
#ifdef BOOST_UBLAS_USE_INDEXED_ITERATOR
        typedef indexed_iterator1<self_type, dense_random_access_iterator_tag> iterator1;
        typedef indexed_iterator2<self_type, dense_random_access_iterator_tag> iterator2;
        typedef indexed_const_iterator1<self_type, dense_random_access_iterator_tag> const_iterator1;
        typedef indexed_const_iterator2<self_type, dense_random_access_iterator_tag> const_iterator2;
#else
        class const_iterator1;
        class iterator1;
        class const_iterator2;
        class iterator2;
#endif
#ifdef BOOST_MSVC_STD_ITERATOR
        typedef reverse_iterator_base1<const_iterator1, value_type, const_reference> const_reverse_iterator1;
        typedef reverse_iterator_base1<iterator1, value_type, reference> reverse_iterator1;
        typedef reverse_iterator_base2<const_iterator2, value_type, const_reference> const_reverse_iterator2;
        typedef reverse_iterator_base2<iterator2, value_type, reference> reverse_iterator2;
#else
        typedef reverse_iterator_base1<const_iterator1> const_reverse_iterator1;
        typedef reverse_iterator_base1<iterator1> reverse_iterator1;
        typedef reverse_iterator_base2<const_iterator2> const_reverse_iterator2;
        typedef reverse_iterator_base2<iterator2> reverse_iterator2;
#endif

        // Element lookup
        BOOST_UBLAS_INLINE
        const_iterator1 find1 (int rank, size_type i, size_type j) const {
#ifdef BOOST_UBLAS_USE_INDEXED_ITERATOR
            return const_iterator1 (*this, i, j);
#else
            return const_iterator1 (*this, i, j, data () [functor_type::address1 (i, size1_, j, size2_)].begin ()  + functor_type::address2 (i, size1_, j, size2_));
#endif
        }
        BOOST_UBLAS_INLINE
        iterator1 find1 (int rank, size_type i, size_type j) {
#ifdef BOOST_UBLAS_USE_INDEXED_ITERATOR
            return iterator1 (*this, i, j);
#else
            return iterator1 (*this, i, j, data () [functor_type::address1 (i, size1_, j, size2_)].begin ()  + functor_type::address2 (i, size1_, j, size2_));
#endif
        }
        BOOST_UBLAS_INLINE
        const_iterator2 find2 (int rank, size_type i, size_type j) const {
#ifdef BOOST_UBLAS_USE_INDEXED_ITERATOR
            return const_iterator2 (*this, i, j);
#else
            return const_iterator2 (*this, i, j, data () [functor_type::address1 (i, size1_, j, size2_)].begin ()  + functor_type::address2 (i, size1_, j, size2_));
#endif
        }
        BOOST_UBLAS_INLINE
        iterator2 find2 (int rank, size_type i, size_type j) {
#ifdef BOOST_UBLAS_USE_INDEXED_ITERATOR
            return iterator2 (*this, i, j);
#else
            return iterator2 (*this, i, j, data () [functor_type::address1 (i, size1_, j, size2_)].begin () + functor_type::address2 (i, size1_, j, size2_));
#endif
        }


#ifndef BOOST_UBLAS_USE_INDEXED_ITERATOR
        class const_iterator1:
            public container_const_reference<vector_of_vector>,
            public random_access_iterator_base<dense_random_access_iterator_tag,
                                               const_iterator1, value_type> {
        public:
            typedef dense_random_access_iterator_tag iterator_category;
#ifdef BOOST_MSVC_STD_ITERATOR
            typedef const_reference reference;
#else
            typedef typename vector_of_vector::value_type value_type;
            typedef typename vector_of_vector::difference_type difference_type;
            typedef typename vector_of_vector::const_reference reference;
            typedef const typename vector_of_vector::pointer pointer;
#endif
            typedef const_iterator2 dual_iterator_type;
            typedef const_reverse_iterator2 dual_reverse_iterator_type;

            // Construction and destruction
            BOOST_UBLAS_INLINE
            const_iterator1 ():
                container_const_reference<self_type> (), i_ (), j_ (), it_ () {}
            BOOST_UBLAS_INLINE
            const_iterator1 (const self_type &m, size_type i, size_type j, const const_iterator_type &it):
                container_const_reference<self_type> (m), i_ (i), j_ (j), it_ (it) {}
            BOOST_UBLAS_INLINE
            const_iterator1 (const iterator1 &it):
                container_const_reference<self_type> (it ()), i_ (it.i_), j_ (it.j_), it_ (it.it_) {}

            // Arithmetic
            BOOST_UBLAS_INLINE
            const_iterator1 &operator ++ () {
                ++ i_;
                const self_type &m = (*this) ();
                if (functor_type::fast1 ())
                    ++ it_;
                else
                    it_ = m.find1 (1, i_, j_).it_;
                return *this;
            }
            BOOST_UBLAS_INLINE
            const_iterator1 &operator -- () {
                -- i_;
                const self_type &m = (*this) ();
                if (functor_type::fast1 ())
                    -- it_;
                else
                    it_ = m.find1 (1, i_, j_).it_;
                return *this;
            }
            BOOST_UBLAS_INLINE
            const_iterator1 &operator += (difference_type n) {
                i_ += n;
                const self_type &m = (*this) ();
                it_ = m.find1 (1, i_, j_).it_;
                return *this;
            }
            BOOST_UBLAS_INLINE
            const_iterator1 &operator -= (difference_type n) {
                i_ -= n;
                const self_type &m = (*this) ();
                it_ = m.find1 (1, i_, j_).it_;
                return *this;
            }
            BOOST_UBLAS_INLINE
            difference_type operator - (const const_iterator1 &it) const {
                BOOST_UBLAS_CHECK (&(*this) () == &it (), external_logic ());
                BOOST_UBLAS_CHECK (index2 () == it.index2 (), bad_index ());
                return index1 () - it.index1 ();
            }

            // Dereference
            BOOST_UBLAS_INLINE
            const_reference operator * () const {
                BOOST_UBLAS_CHECK (index1 () < (*this) ().size1 (), bad_index ());
                BOOST_UBLAS_CHECK (index2 () < (*this) ().size2 (), bad_index ());
                return *it_;
            }

#ifndef BOOST_UBLAS_NO_NESTED_CLASS_RELATION
            BOOST_UBLAS_INLINE
#ifdef BOOST_UBLAS_MSVC_NESTED_CLASS_RELATION
            typename self_type::
#endif
            const_iterator2 begin () const {
                const self_type &m = (*this) ();
                return m.find2 (1, index1 (), 0);
            }
            BOOST_UBLAS_INLINE
#ifdef BOOST_UBLAS_MSVC_NESTED_CLASS_RELATION
            typename self_type::
#endif
            const_iterator2 end () const {
                const self_type &m = (*this) ();
                return m.find2 (1, index1 (), m.size2 ());
            }
            BOOST_UBLAS_INLINE
#ifdef BOOST_UBLAS_MSVC_NESTED_CLASS_RELATION
            typename self_type::
#endif
            const_reverse_iterator2 rbegin () const {
                return const_reverse_iterator2 (end ());
            }
            BOOST_UBLAS_INLINE
#ifdef BOOST_UBLAS_MSVC_NESTED_CLASS_RELATION
            typename self_type::
#endif
            const_reverse_iterator2 rend () const {
                return const_reverse_iterator2 (begin ());
            }
#endif

            // Indices
            BOOST_UBLAS_INLINE
            size_type index1 () const {
                return i_;
            }
            BOOST_UBLAS_INLINE
            size_type index2 () const {
                return j_;
            }

            // Assignment
            BOOST_UBLAS_INLINE
            const_iterator1 &operator = (const const_iterator1 &it) {
                container_const_reference<self_type>::assign (&it ());
                it_ = it.it_;
                return *this;
            }

            // Comparison
            BOOST_UBLAS_INLINE
            bool operator == (const const_iterator1 &it) const {
                BOOST_UBLAS_CHECK (&(*this) () == &it (), external_logic ());
                BOOST_UBLAS_CHECK (index2 () == it.index2 (), bad_index ());
                return it_ == it.it_;
            }
            BOOST_UBLAS_INLINE
            bool operator < (const const_iterator1 &it) const {
                BOOST_UBLAS_CHECK (&(*this) () == &it (), external_logic ());
                BOOST_UBLAS_CHECK (index2 () == it.index2 (), bad_index ());
                return it_ < it.it_;
            }

        private:
            size_type i_;
            size_type j_;
            const_iterator_type it_;

            friend class iterator1;
        };
#endif

        BOOST_UBLAS_INLINE
        const_iterator1 begin1 () const {
            return find1 (0, 0, 0);
        }
        BOOST_UBLAS_INLINE
        const_iterator1 end1 () const {
            return find1 (0, size1_, 0);
        }

#ifndef BOOST_UBLAS_USE_INDEXED_ITERATOR
        class iterator1:
            public container_reference<vector_of_vector>,
            public random_access_iterator_base<dense_random_access_iterator_tag,
                                               iterator1, value_type> {
        public:
            typedef dense_random_access_iterator_tag iterator_category;
#ifndef BOOST_MSVC_STD_ITERATOR
            typedef typename vector_of_vector::value_type value_type;
            typedef typename vector_of_vector::difference_type difference_type;
            typedef typename vector_of_vector::reference reference;
            typedef typename vector_of_vector::pointer pointer;
#endif
            typedef iterator2 dual_iterator_type;
            typedef reverse_iterator2 dual_reverse_iterator_type;

            // Construction and destruction
            BOOST_UBLAS_INLINE
            iterator1 ():
                container_reference<self_type> (), i_ (), j_ (), it_ () {}
            BOOST_UBLAS_INLINE
            iterator1 (self_type &m, size_type i, size_type j, const iterator_type &it):
                container_reference<self_type> (m), i_ (i), j_ (j), it_ (it) {}

            // Arithmetic
            BOOST_UBLAS_INLINE
            iterator1 &operator ++ () {
                ++ i_;
                self_type &m = (*this) ();
                if (functor_type::fast1 ())
                    ++ it_;
                else
                    it_ = m.find1 (1, i_, j_).it_;
                return *this;
            }
            BOOST_UBLAS_INLINE
            iterator1 &operator -- () {
                -- i_;
                self_type &m = (*this) ();
                if (functor_type::fast1 ())
                    -- it_;
                else
                    it_ = m.find1 (1, i_, j_).it_;
                return *this;
            }
            BOOST_UBLAS_INLINE
            iterator1 &operator += (difference_type n) {
                i_ += n;
                self_type &m = (*this) ();
                it_ = m.find1 (1, i_, j_).it_;
                return *this;
            }
            BOOST_UBLAS_INLINE
            iterator1 &operator -= (difference_type n) {
                i_ -= n;
                self_type &m = (*this) ();
                it_ = m.find1 (1, i_, j_).it_;
                return *this;
            }
            BOOST_UBLAS_INLINE
            difference_type operator - (const iterator1 &it) const {
                BOOST_UBLAS_CHECK (&(*this) () == &it (), external_logic ());
                BOOST_UBLAS_CHECK (index2 () == it.index2 (), bad_index ());
                return index1 () - it.index1 ();
            }

            // Dereference
            BOOST_UBLAS_INLINE
            reference operator * () const {
                BOOST_UBLAS_CHECK (index1 () < (*this) ().size1 (), bad_index ());
                BOOST_UBLAS_CHECK (index2 () < (*this) ().size2 (), bad_index ());
                return *it_;
            }

#ifndef BOOST_UBLAS_NO_NESTED_CLASS_RELATION
            BOOST_UBLAS_INLINE
#ifdef BOOST_UBLAS_MSVC_NESTED_CLASS_RELATION
            typename self_type::
#endif
            iterator2 begin () const {
                self_type &m = (*this) ();
                return m.find2 (1, index1 (), 0);
            }
            BOOST_UBLAS_INLINE
#ifdef BOOST_UBLAS_MSVC_NESTED_CLASS_RELATION
            typename self_type::
#endif
            iterator2 end () const {
                self_type &m = (*this) ();
                return m.find2 (1, index1 (), m.size2 ());
            }
            BOOST_UBLAS_INLINE
#ifdef BOOST_UBLAS_MSVC_NESTED_CLASS_RELATION
            typename self_type::
#endif
            reverse_iterator2 rbegin () const {
                return reverse_iterator2 (end ());
            }
            BOOST_UBLAS_INLINE
#ifdef BOOST_UBLAS_MSVC_NESTED_CLASS_RELATION
            typename self_type::
#endif
            reverse_iterator2 rend () const {
                return reverse_iterator2 (begin ());
            }
#endif

            // Indices
            BOOST_UBLAS_INLINE
            size_type index1 () const {
                return i_;
            }
            BOOST_UBLAS_INLINE
            size_type index2 () const {
                return j_;
            }

            // Assignment
            BOOST_UBLAS_INLINE
            iterator1 &operator = (const iterator1 &it) {
                container_reference<self_type>::assign (&it ());
                it_ = it.it_;
                return *this;
            }

            // Comparison
            BOOST_UBLAS_INLINE
            bool operator == (const iterator1 &it) const {
                BOOST_UBLAS_CHECK (&(*this) () == &it (), external_logic ());
                BOOST_UBLAS_CHECK (index2 () == it.index2 (), bad_index ());
                return it_ == it.it_;
            }
            BOOST_UBLAS_INLINE
            bool operator < (const iterator1 &it) const {
                BOOST_UBLAS_CHECK (&(*this) () == &it (), external_logic ());
                BOOST_UBLAS_CHECK (index2 () == it.index2 (), bad_index ());
                return it_ < it.it_;
            }

        private:
            size_type i_;
            size_type j_;
            iterator_type it_;

            friend class const_iterator1;
        };
#endif

        BOOST_UBLAS_INLINE
        iterator1 begin1 () {
            return find1 (0, 0, 0);
        }
        BOOST_UBLAS_INLINE
        iterator1 end1 () {
            return find1 (0, size1_, 0);
        }

#ifndef BOOST_UBLAS_USE_INDEXED_ITERATOR
        class const_iterator2:
            public container_const_reference<vector_of_vector>,
            public random_access_iterator_base<dense_random_access_iterator_tag,
                                               const_iterator2, value_type> {
        public:
            typedef dense_random_access_iterator_tag iterator_category;
#ifdef BOOST_MSVC_STD_ITERATOR
            typedef const_reference reference;
#else
            typedef typename vector_of_vector::value_type value_type;
            typedef typename vector_of_vector::difference_type difference_type;
            typedef typename vector_of_vector::const_reference reference;
            typedef const typename vector_of_vector::pointer pointer;
#endif
            typedef const_iterator1 dual_iterator_type;
            typedef const_reverse_iterator1 dual_reverse_iterator_type;

            // Construction and destruction
            BOOST_UBLAS_INLINE
            const_iterator2 ():
                container_const_reference<self_type> (), i_ (), j_ (), it_ () {}
            BOOST_UBLAS_INLINE
            const_iterator2 (const self_type &m, size_type i, size_type j, const const_iterator_type &it):
                container_const_reference<self_type> (m), i_ (i), j_ (j), it_ (it) {}
            BOOST_UBLAS_INLINE
            const_iterator2 (const iterator2 &it):
                container_const_reference<self_type> (it ()), i_ (it.i_), j_ (it.j_), it_ (it.it_) {}

            // Arithmetic
            BOOST_UBLAS_INLINE
            const_iterator2 &operator ++ () {
                ++ j_;
                const self_type &m = (*this) ();
                if (functor_type::fast2 ())
                    ++ it_;
                else
                    it_ = m.find2 (1, i_, j_).it_;
                return *this;
            }
            BOOST_UBLAS_INLINE
            const_iterator2 &operator -- () {
                -- j_;
                const self_type &m = (*this) ();
                if (functor_type::fast2 ())
                    -- it_;
                else
                    it_ = m.find2 (1, i_, j_).it_;
                return *this;
            }
            BOOST_UBLAS_INLINE
            const_iterator2 &operator += (difference_type n) {
                j_ += n;
                const self_type &m = (*this) ();
                it_ = m.find2 (1, i_, j_).it_;
                return *this;
            }
            BOOST_UBLAS_INLINE
            const_iterator2 &operator -= (difference_type n) {
                j_ -= n;
                const self_type &m = (*this) ();
                it_ = m.find2 (1, i_, j_).it_;
                return *this;
            }
            BOOST_UBLAS_INLINE
            difference_type operator - (const const_iterator2 &it) const {
                BOOST_UBLAS_CHECK (&(*this) () == &it (), external_logic ());
                BOOST_UBLAS_CHECK (index1 () == it.index1 (), bad_index ());
                return index2 () - it.index2 ();
            }

            // Dereference
            BOOST_UBLAS_INLINE
            const_reference operator * () const {
                BOOST_UBLAS_CHECK (index1 () < (*this) ().size1 (), bad_index ());
                BOOST_UBLAS_CHECK (index2 () < (*this) ().size2 (), bad_index ());
                return *it_;
            }

#ifndef BOOST_UBLAS_NO_NESTED_CLASS_RELATION
            BOOST_UBLAS_INLINE
#ifdef BOOST_UBLAS_MSVC_NESTED_CLASS_RELATION
            typename self_type::
#endif
            const_iterator1 begin () const {
                const self_type &m = (*this) ();
                return m.find1 (1, 0, index2 ());
            }
            BOOST_UBLAS_INLINE
#ifdef BOOST_UBLAS_MSVC_NESTED_CLASS_RELATION
            typename self_type::
#endif
            const_iterator1 end () const {
                const self_type &m = (*this) ();
                return m.find1 (1, m.size1 (), index2 ());
            }
            BOOST_UBLAS_INLINE
#ifdef BOOST_UBLAS_MSVC_NESTED_CLASS_RELATION
            typename self_type::
#endif
            const_reverse_iterator1 rbegin () const {
                return const_reverse_iterator1 (end ());
            }
            BOOST_UBLAS_INLINE
#ifdef BOOST_UBLAS_MSVC_NESTED_CLASS_RELATION
            typename self_type::
#endif
            const_reverse_iterator1 rend () const {
                return const_reverse_iterator1 (begin ());
            }
#endif

            // Indices
            BOOST_UBLAS_INLINE
            size_type index1 () const {
                return i_;
            }
            BOOST_UBLAS_INLINE
            size_type index2 () const {
                return j_;
            }

            // Assignment
            BOOST_UBLAS_INLINE
            const_iterator2 &operator = (const const_iterator2 &it) {
                container_const_reference<self_type>::assign (&it ());
                it_ = it.it_;
                return *this;
            }

            // Comparison
            BOOST_UBLAS_INLINE
            bool operator == (const const_iterator2 &it) const {
                BOOST_UBLAS_CHECK (&(*this) () == &it (), external_logic ());
                BOOST_UBLAS_CHECK (index1 () == it.index1 (), bad_index ());
                return it_ == it.it_;
            }
            BOOST_UBLAS_INLINE
            bool operator < (const const_iterator2 &it) const {
                BOOST_UBLAS_CHECK (&(*this) () == &it (), external_logic ());
                BOOST_UBLAS_CHECK (index1 () == it.index1 (), bad_index ());
                return it_ < it.it_;
            }

        private:
            size_type i_;
            size_type j_;
            const_iterator_type it_;

            friend class iterator2;
        };
#endif

        BOOST_UBLAS_INLINE
        const_iterator2 begin2 () const {
            return find2 (0, 0, 0);
        }
        BOOST_UBLAS_INLINE
        const_iterator2 end2 () const {
            return find2 (0, 0, size2_);
        }

#ifndef BOOST_UBLAS_USE_INDEXED_ITERATOR
        class iterator2:
            public container_reference<vector_of_vector>,
            public random_access_iterator_base<dense_random_access_iterator_tag,
                                               iterator2, value_type> {
        public:
            typedef dense_random_access_iterator_tag iterator_category;
#ifndef BOOST_MSVC_STD_ITERATOR
            typedef typename vector_of_vector::value_type value_type;
            typedef typename vector_of_vector::difference_type difference_type;
            typedef typename vector_of_vector::reference reference;
            typedef typename vector_of_vector::pointer pointer;
#endif
            typedef iterator1 dual_iterator_type;
            typedef reverse_iterator1 dual_reverse_iterator_type;

            // Construction and destruction
            BOOST_UBLAS_INLINE
            iterator2 ():
                container_reference<self_type> (), i_ (), j_ (), it_ () {}
            BOOST_UBLAS_INLINE
            iterator2 (self_type &m, size_type i, size_type j, const iterator_type &it):
                container_reference<self_type> (m), i_ (i), j_ (j), it_ (it) {}

            // Arithmetic
            BOOST_UBLAS_INLINE
            iterator2 &operator ++ () {
                ++ j_;
                self_type &m = (*this) ();
                if (functor_type::fast2 ())
                    ++ it_;
                else
                    it_ = m.find2 (1, i_, j_).it_;
                return *this;
            }
            BOOST_UBLAS_INLINE
            iterator2 &operator -- () {
                -- j_;
                self_type &m = (*this) ();
                if (functor_type::fast2 ())
                    -- it_;
                else
                    it_ = m.find2 (1, i_, j_).it_;
                return *this;
            }
            BOOST_UBLAS_INLINE
            iterator2 &operator += (difference_type n) {
                j_ += n;
                self_type &m = (*this) ();
                it_ = m.find2 (1, i_, j_).it_;
                return *this;
            }
            BOOST_UBLAS_INLINE
            iterator2 &operator -= (difference_type n) {
                j_ -= n;
                self_type &m = (*this) ();
                it_ = m.find2 (1, i_, j_).it_;
                return *this;
            }
            BOOST_UBLAS_INLINE
            difference_type operator - (const iterator2 &it) const {
                BOOST_UBLAS_CHECK (&(*this) () == &it (), external_logic ());
                BOOST_UBLAS_CHECK (index1 () == it.index1 (), bad_index ());
                return index2 () - it.index2 ();
            }

            // Dereference
            BOOST_UBLAS_INLINE
            reference operator * () const {
                BOOST_UBLAS_CHECK (index1 () < (*this) ().size1 (), bad_index ());
                BOOST_UBLAS_CHECK (index2 () < (*this) ().size2 (), bad_index ());
                return *it_;
            }

#ifndef BOOST_UBLAS_NO_NESTED_CLASS_RELATION
            BOOST_UBLAS_INLINE
#ifdef BOOST_UBLAS_MSVC_NESTED_CLASS_RELATION
            typename self_type::
#endif
            iterator1 begin () const {
                self_type &m = (*this) ();
                return m.find1 (1, 0, index2 ());
            }
            BOOST_UBLAS_INLINE
#ifdef BOOST_UBLAS_MSVC_NESTED_CLASS_RELATION
            typename self_type::
#endif
            iterator1 end () const {
                self_type &m = (*this) ();
                return m.find1 (1, m.size1 (), index2 ());
            }
            BOOST_UBLAS_INLINE
#ifdef BOOST_UBLAS_MSVC_NESTED_CLASS_RELATION
            typename self_type::
#endif
            reverse_iterator1 rbegin () const {
                return reverse_iterator1 (end ());
            }
            BOOST_UBLAS_INLINE
#ifdef BOOST_UBLAS_MSVC_NESTED_CLASS_RELATION
            typename self_type::
#endif
            reverse_iterator1 rend () const {
                return reverse_iterator1 (begin ());
            }
#endif

            // Indices
            BOOST_UBLAS_INLINE
            size_type index1 () const {
                return i_;
            }
            BOOST_UBLAS_INLINE
            size_type index2 () const {
                return j_;
            }

            // Assignment
            BOOST_UBLAS_INLINE
            iterator2 &operator = (const iterator2 &it) {
                container_reference<self_type>::assign (&it ());
                it_ = it.it_;
                return *this;
            }

            // Comparison
            BOOST_UBLAS_INLINE
            bool operator == (const iterator2 &it) const {
                BOOST_UBLAS_CHECK (&(*this) () == &it (), external_logic ());
                BOOST_UBLAS_CHECK (index1 () == it.index1 (), bad_index ());
                return it_ == it.it_;
            }
            BOOST_UBLAS_INLINE
            bool operator < (const iterator2 &it) const {
                BOOST_UBLAS_CHECK (&(*this) () == &it (), external_logic ());
                BOOST_UBLAS_CHECK (index1 () == it.index1 (), bad_index ());
                return it_ < it.it_;
            }

        private:
            size_type i_;
            size_type j_;
            iterator_type it_;

            friend class const_iterator2;
        };
#endif

        BOOST_UBLAS_INLINE
        iterator2 begin2 () {
            return find2 (0, 0, 0);
        }
        BOOST_UBLAS_INLINE
        iterator2 end2 () {
            return find2 (0, 0, size2_);
        }

        // Reverse iterators

        BOOST_UBLAS_INLINE
        const_reverse_iterator1 rbegin1 () const {
            return const_reverse_iterator1 (end1 ());
        }
        BOOST_UBLAS_INLINE
        const_reverse_iterator1 rend1 () const {
            return const_reverse_iterator1 (begin1 ());
        }

        BOOST_UBLAS_INLINE
        reverse_iterator1 rbegin1 () {
            return reverse_iterator1 (end1 ());
        }
        BOOST_UBLAS_INLINE
        reverse_iterator1 rend1 () {
            return reverse_iterator1 (begin1 ());
        }

        BOOST_UBLAS_INLINE
        const_reverse_iterator2 rbegin2 () const {
            return const_reverse_iterator2 (end2 ());
        }
        BOOST_UBLAS_INLINE
        const_reverse_iterator2 rend2 () const {
            return const_reverse_iterator2 (begin2 ());
        }

        BOOST_UBLAS_INLINE
        reverse_iterator2 rbegin2 () {
            return reverse_iterator2 (end2 ());
        }
        BOOST_UBLAS_INLINE
        reverse_iterator2 rend2 () {
            return reverse_iterator2 (begin2 ());
        }

    private:
        size_type size1_;
        size_type size2_;
        array_type data_;
    };

    // Identity matrix class
    template<class T>
    class identity_matrix:
        public matrix_expression<identity_matrix<T> > {
    public:
#ifndef BOOST_UBLAS_NO_PROXY_SHORTCUTS
        BOOST_UBLAS_USING matrix_expression<identity_matrix<T> >::operator ();
#endif
        typedef std::size_t size_type;
        typedef std::ptrdiff_t difference_type;
        typedef T value_type;
        typedef const T &const_reference;
        typedef T &reference;
    private:
        typedef const T *const_pointer;
        typedef identity_matrix<T> self_type;
    public:
#ifndef BOOST_UBLAS_CT_REFERENCE_BASE_TYPEDEFS
        typedef const matrix_const_reference<const self_type> const_closure_type;
#else
        typedef const matrix_reference<const self_type> const_closure_type;
#endif
        typedef matrix_reference<self_type> closure_type;
        typedef packed_tag storage_category;
        typedef unknown_orientation_tag orientation_category;

        // Construction and destruction
        BOOST_UBLAS_INLINE
        identity_matrix ():
            matrix_expression<self_type> (),
            size1_ (0), size2_ (0) {}
        BOOST_UBLAS_INLINE
        identity_matrix (size_type size):
            matrix_expression<self_type> (),
            size1_ (size), size2_ (size) {}
        BOOST_UBLAS_INLINE
        identity_matrix (size_type size1, size_type size2):
            matrix_expression<self_type> (),
            size1_ (size1), size2_ (size2) {}
        BOOST_UBLAS_INLINE
        identity_matrix (const identity_matrix &m):
            matrix_expression<self_type> (),
            size1_ (m.size1_), size2_ (m.size2_) {}

        // Accessors
        BOOST_UBLAS_INLINE
        size_type size1 () const {
            return size1_;
        }
        BOOST_UBLAS_INLINE
        size_type size2 () const {
            return size2_;
        }

        // Resizing
        BOOST_UBLAS_INLINE
        void resize (size_type size, bool preserve = true) {
            size1_ = size;
            size2_ = size;
        }
        BOOST_UBLAS_INLINE
        void resize (size_type size1, size_type size2, bool preserve = true) {
            size1_ = size1;
            size2_ = size2;
        }

        // Element access
        BOOST_UBLAS_INLINE
        const_reference operator () (size_type i, size_type j) const {
            if (i == j)
                return one_;
            else
                return zero_;
        }

        // Assignment
        BOOST_UBLAS_INLINE
        identity_matrix &operator = (const identity_matrix &m) {
            size1_ = m.size1_;
            size2_ = m.size2_;
            return *this;
        }
        BOOST_UBLAS_INLINE
        identity_matrix &assign_temporary (identity_matrix &m) {
            swap (m);
            return *this;
        }

        // Swapping
        BOOST_UBLAS_INLINE
        void swap (identity_matrix &m) {
            if (this != &m) {
                std::swap (size1_, m.size1_);
                std::swap (size2_, m.size2_);
            }
        }
#ifndef BOOST_UBLAS_NO_MEMBER_FRIENDS
        BOOST_UBLAS_INLINE
        friend void swap (identity_matrix &m1, identity_matrix &m2) {
            m1.swap (m2);
        }
#endif

        // Iterator types
    private:
        // Use an index
        typedef size_type const_iterator_type;

    public:
#ifdef BOOST_UBLAS_USE_INDEXED_ITERATOR
        typedef indexed_const_iterator1<self_type, packed_random_access_iterator_tag> iterator1;
        typedef indexed_const_iterator2<self_type, packed_random_access_iterator_tag> iterator2;
        typedef indexed_const_iterator1<self_type, packed_random_access_iterator_tag> const_iterator1;
        typedef indexed_const_iterator2<self_type, packed_random_access_iterator_tag> const_iterator2;
#else
        class const_iterator1;
        class const_iterator2;
#endif
#ifdef BOOST_MSVC_STD_ITERATOR
        typedef reverse_iterator_base1<const_iterator1, value_type, const_reference> const_reverse_iterator1;
        typedef reverse_iterator_base2<const_iterator2, value_type, const_reference> const_reverse_iterator2;
#else
        typedef reverse_iterator_base1<const_iterator1> const_reverse_iterator1;
        typedef reverse_iterator_base2<const_iterator2> const_reverse_iterator2;
#endif

        // Element lookup
        BOOST_UBLAS_INLINE
        const_iterator1 find1 (int rank, size_type i, size_type j) const {
            if (rank == 1) {
                i = (std::max) (i, j);
                i = (std::min) (i, j + 1);
            }
            return const_iterator1 (*this, i, j);
        }
        BOOST_UBLAS_INLINE
        const_iterator2 find2 (int rank, size_type i, size_type j) const {
            if (rank == 1) {
                j = (std::max) (j, i);
                j = (std::min) (j, i + 1);
            }
            return const_iterator2 (*this, i, j);
        }


#ifndef BOOST_UBLAS_USE_INDEXED_ITERATOR
        class const_iterator1:
            public container_const_reference<identity_matrix>,
            public random_access_iterator_base<packed_random_access_iterator_tag,
                                               const_iterator1, value_type> {
        public:
            typedef packed_random_access_iterator_tag iterator_category;
#ifdef BOOST_MSVC_STD_ITERATOR
            typedef const_reference reference;
#else
            typedef typename identity_matrix::value_type value_type;
            typedef typename identity_matrix::difference_type difference_type;
            typedef typename identity_matrix::const_reference reference;
            typedef typename identity_matrix::const_pointer pointer;
#endif
            typedef const_iterator2 dual_iterator_type;
            typedef const_reverse_iterator2 dual_reverse_iterator_type;

            // Construction and destruction
            BOOST_UBLAS_INLINE
            const_iterator1 ():
                container_const_reference<self_type> (), it1_ (), it2_ () {}
            BOOST_UBLAS_INLINE
            const_iterator1 (const self_type &m, const const_iterator_type &it1, const const_iterator_type &it2):
                container_const_reference<self_type> (m), it1_ (it1), it2_ (it2) {}

            // Arithmetic
            BOOST_UBLAS_INLINE
            const_iterator1 &operator ++ () {
                ++ it1_;
                return *this;
            }
            BOOST_UBLAS_INLINE
            const_iterator1 &operator -- () {
                -- it1_;
                return *this;
            }
            BOOST_UBLAS_INLINE
            const_iterator1 &operator += (difference_type n) {
                it1_ += n;
                return *this;
            }
            BOOST_UBLAS_INLINE
            const_iterator1 &operator -= (difference_type n) {
                it1_ -= n;
                return *this;
            }
            BOOST_UBLAS_INLINE
            difference_type operator - (const const_iterator1 &it) const {
                BOOST_UBLAS_CHECK (&(*this) () == &it (), external_logic ());
                BOOST_UBLAS_CHECK (it2_ == it.it2_, external_logic ());
                return it1_ - it.it1_;
            }

            // Dereference
            BOOST_UBLAS_INLINE
            const_reference operator * () const {
                BOOST_UBLAS_CHECK (index1 () < (*this) ().size1 (), bad_index ());
                BOOST_UBLAS_CHECK (index2 () < (*this) ().size2 (), bad_index ());
                return (*this) () (index1 (), index2 ());
            }

#ifndef BOOST_UBLAS_NO_NESTED_CLASS_RELATION
            BOOST_UBLAS_INLINE
#ifdef BOOST_UBLAS_MSVC_NESTED_CLASS_RELATION
            typename self_type::
#endif
            const_iterator2 begin () const {
                const self_type &m = (*this) ();
                return m.find2 (1, index1 (), 0);
            }
            BOOST_UBLAS_INLINE
#ifdef BOOST_UBLAS_MSVC_NESTED_CLASS_RELATION
            typename self_type::
#endif
            const_iterator2 end () const {
                const self_type &m = (*this) ();
                return m.find2 (1, index1 (), m.size2 ());
            }
            BOOST_UBLAS_INLINE
#ifdef BOOST_UBLAS_MSVC_NESTED_CLASS_RELATION
            typename self_type::
#endif
            const_reverse_iterator2 rbegin () const {
                return const_reverse_iterator2 (end ());
            }
            BOOST_UBLAS_INLINE
#ifdef BOOST_UBLAS_MSVC_NESTED_CLASS_RELATION
            typename self_type::
#endif
            const_reverse_iterator2 rend () const {
                return const_reverse_iterator2 (begin ());
            }
#endif

            // Indices
            BOOST_UBLAS_INLINE
            size_type index1 () const {
                return it1_;
            }
            BOOST_UBLAS_INLINE
            size_type index2 () const {
                return it2_;
            }

            // Assignment
            BOOST_UBLAS_INLINE
            const_iterator1 &operator = (const const_iterator1 &it) {
                container_const_reference<self_type>::assign (&it ());
                it1_ = it.it1_;
                it2_ = it.it2_;
                return *this;
            }

            // Comparison
            BOOST_UBLAS_INLINE
            bool operator == (const const_iterator1 &it) const {
                BOOST_UBLAS_CHECK (&(*this) () == &it (), external_logic ());
                BOOST_UBLAS_CHECK (it2_ == it.it2_, external_logic ());
                return it1_ == it.it1_;
            }
            BOOST_UBLAS_INLINE
            bool operator < (const const_iterator1 &it) const {
                BOOST_UBLAS_CHECK (&(*this) () == &it (), external_logic ());
                BOOST_UBLAS_CHECK (it2_ == it.it2_, external_logic ());
                return it1_ < it.it1_;
            }

        private:
            const_iterator_type it1_;
            const_iterator_type it2_;
        };

        typedef const_iterator1 iterator1;
#endif

        BOOST_UBLAS_INLINE
        const_iterator1 begin1 () const {
            return find1 (0, 0, 0);
        }
        BOOST_UBLAS_INLINE
        const_iterator1 end1 () const {
            return find1 (0, size1_, 0);
        }

#ifndef BOOST_UBLAS_USE_INDEXED_ITERATOR
        class const_iterator2:
            public container_const_reference<identity_matrix>,
            public random_access_iterator_base<packed_random_access_iterator_tag,
                                               const_iterator2, value_type> {
        public:
            typedef packed_random_access_iterator_tag iterator_category;
#ifdef BOOST_MSVC_STD_ITERATOR
            typedef const_reference reference;
#else
            typedef typename identity_matrix::value_type value_type;
            typedef typename identity_matrix::difference_type difference_type;
            typedef typename identity_matrix::const_reference reference;
            typedef typename identity_matrix::const_pointer pointer;
#endif
            typedef const_iterator1 dual_iterator_type;
            typedef const_reverse_iterator1 dual_reverse_iterator_type;

            // Construction and destruction
            BOOST_UBLAS_INLINE
            const_iterator2 ():
                container_const_reference<self_type> (), it1_ (), it2_ () {}
            BOOST_UBLAS_INLINE
            const_iterator2 (const self_type &m, const const_iterator_type &it1, const const_iterator_type &it2):
                container_const_reference<self_type> (m), it1_ (it1), it2_ (it2) {}

            // Arithmetic
            BOOST_UBLAS_INLINE
            const_iterator2 &operator ++ () {
                ++ it2_;
                return *this;
            }
            BOOST_UBLAS_INLINE
            const_iterator2 &operator -- () {
                -- it2_;
                return *this;
            }
            BOOST_UBLAS_INLINE
            const_iterator2 &operator += (difference_type n) {
                it2_ += n;
                return *this;
            }
            BOOST_UBLAS_INLINE
            const_iterator2 &operator -= (difference_type n) {
                it2_ -= n;
                return *this;
            }
            BOOST_UBLAS_INLINE
            difference_type operator - (const const_iterator2 &it) const {
                BOOST_UBLAS_CHECK (&(*this) () == &it (), external_logic ());
                BOOST_UBLAS_CHECK (it1_ == it.it1_, external_logic ());
                return it2_ - it.it2_;
            }

            // Dereference
            BOOST_UBLAS_INLINE
            const_reference operator * () const {
                BOOST_UBLAS_CHECK (index1 () < (*this) ().size1 (), bad_index ());
                BOOST_UBLAS_CHECK (index2 () < (*this) ().size2 (), bad_index ());
                return (*this) () (index1 (), index2 ());
            }

#ifndef BOOST_UBLAS_NO_NESTED_CLASS_RELATION
            BOOST_UBLAS_INLINE
#ifdef BOOST_UBLAS_MSVC_NESTED_CLASS_RELATION
            typename self_type::
#endif
            const_iterator1 begin () const {
                const self_type &m = (*this) ();
                return m.find1 (1, 0, index2 ());
            }
            BOOST_UBLAS_INLINE
#ifdef BOOST_UBLAS_MSVC_NESTED_CLASS_RELATION
            typename self_type::
#endif
            const_iterator1 end () const {
                const self_type &m = (*this) ();
                return m.find1 (1, m.size1 (), index2 ());
            }
            BOOST_UBLAS_INLINE
#ifdef BOOST_UBLAS_MSVC_NESTED_CLASS_RELATION
            typename self_type::
#endif
            const_reverse_iterator1 rbegin () const {
                return const_reverse_iterator1 (end ());
            }
            BOOST_UBLAS_INLINE
#ifdef BOOST_UBLAS_MSVC_NESTED_CLASS_RELATION
            typename self_type::
#endif
            const_reverse_iterator1 rend () const {
                return const_reverse_iterator1 (begin ());
            }
#endif

            // Indices
            BOOST_UBLAS_INLINE
            size_type index1 () const {
                return it1_;
            }
            BOOST_UBLAS_INLINE
            size_type index2 () const {
                return it2_;
            }

            // Assignment
            BOOST_UBLAS_INLINE
            const_iterator2 &operator = (const const_iterator2 &it) {
                container_const_reference<self_type>::assign (&it ());
                it1_ = it.it1_;
                it2_ = it.it2_;
                return *this;
            }

            // Comparison
            BOOST_UBLAS_INLINE
            bool operator == (const const_iterator2 &it) const {
                BOOST_UBLAS_CHECK (&(*this) () == &it (), external_logic ());
                BOOST_UBLAS_CHECK (it1_ == it.it1_, external_logic ());
                return it2_ == it.it2_;
            }
            BOOST_UBLAS_INLINE
            bool operator < (const const_iterator2 &it) const {
                BOOST_UBLAS_CHECK (&(*this) () == &it (), external_logic ());
                BOOST_UBLAS_CHECK (it1_ == it.it1_, external_logic ());
                return it2_ < it.it2_;
            }

        private:
            const_iterator_type it1_;
            const_iterator_type it2_;
        };

        typedef const_iterator2 iterator2;
#endif

        BOOST_UBLAS_INLINE
        const_iterator2 begin2 () const {
            return find2 (0, 0, 0);
        }
        BOOST_UBLAS_INLINE
        const_iterator2 end2 () const {
            return find2 (0, 0, size2_);
        }

        // Reverse iterators

        BOOST_UBLAS_INLINE
        const_reverse_iterator1 rbegin1 () const {
            return const_reverse_iterator1 (end1 ());
        }
        BOOST_UBLAS_INLINE
        const_reverse_iterator1 rend1 () const {
            return const_reverse_iterator1 (begin1 ());
        }

        BOOST_UBLAS_INLINE
        const_reverse_iterator2 rbegin2 () const {
            return const_reverse_iterator2 (end2 ());
        }
        BOOST_UBLAS_INLINE
        const_reverse_iterator2 rend2 () const {
            return const_reverse_iterator2 (begin2 ());
        }

    private:
        size_type size1_;
        size_type size2_;
        static const value_type zero_;
        static const value_type one_;
    };

    template<class T>
    const typename identity_matrix<T>::value_type identity_matrix<T>::zero_
#ifdef BOOST_UBLAS_STATIC_OLD_INIT
        = BOOST_UBLAS_TYPENAME identity_matrix<T>::value_type
#endif
        (0);
    template<class T>
    const typename identity_matrix<T>::value_type identity_matrix<T>::one_
#ifdef BOOST_UBLAS_STATIC_OLD_INIT
        = BOOST_UBLAS_TYPENAME identity_matrix<T>::value_type
#endif
        (1);

    // Zero matrix class
    template<class T>
    class zero_matrix:
        public matrix_expression<zero_matrix<T> > {
    public:
#ifndef BOOST_UBLAS_NO_PROXY_SHORTCUTS
        BOOST_UBLAS_USING matrix_expression<zero_matrix<T> >::operator ();
#endif
        typedef std::size_t size_type;
        typedef std::ptrdiff_t difference_type;
        typedef T value_type;
        typedef const T &const_reference;
        typedef T &reference;
    private:
        typedef const T *const_pointer;
        typedef zero_matrix<T> self_type;
    public:
#ifndef BOOST_UBLAS_CT_REFERENCE_BASE_TYPEDEFS
        typedef const matrix_const_reference<const self_type> const_closure_type;
#else
        typedef const matrix_reference<const self_type> const_closure_type;
#endif
        typedef matrix_reference<self_type> closure_type;
        typedef sparse_tag storage_category;
        typedef unknown_orientation_tag orientation_category;

        // Construction and destruction
        BOOST_UBLAS_INLINE
        zero_matrix ():
            matrix_expression<self_type> (),
            size1_ (0), size2_ (0) {}
        BOOST_UBLAS_INLINE
        zero_matrix (size_type size):
            matrix_expression<self_type> (),
            size1_ (size), size2_ (size) {}
        BOOST_UBLAS_INLINE
        zero_matrix (size_type size1, size_type size2):
            matrix_expression<self_type> (),
            size1_ (size1), size2_ (size2) {}
        BOOST_UBLAS_INLINE
        zero_matrix (const zero_matrix &m):
            matrix_expression<self_type> (),
            size1_ (m.size1_), size2_ (m.size2_) {}

        // Accessors
        BOOST_UBLAS_INLINE
        size_type size1 () const {
            return size1_;
        }
        BOOST_UBLAS_INLINE
        size_type size2 () const {
            return size2_;
        }

        // Resizing
        BOOST_UBLAS_INLINE
        void resize (size_type size, bool preserve = true) {
            size1_ = size;
            size2_ = size;
        }
        BOOST_UBLAS_INLINE
        void resize (size_type size1, size_type size2, bool preserve = true) {
            size1_ = size1;
            size2_ = size2;
        }

        // Element access
        BOOST_UBLAS_INLINE
        const_reference operator () (size_type /* i */, size_type /* j */) const {
            return zero_;
        }

        // Assignment
        BOOST_UBLAS_INLINE
        zero_matrix &operator = (const zero_matrix &m) {
            size1_ = m.size1_;
            size2_ = m.size2_;
            return *this;
        }
        BOOST_UBLAS_INLINE
        zero_matrix &assign_temporary (zero_matrix &m) {
            swap (m);
            return *this;
        }

        // Swapping
        BOOST_UBLAS_INLINE
        void swap (zero_matrix &m) {
            if (this != &m) {
                std::swap (size1_, m.size1_);
                std::swap (size2_, m.size2_);
            }
        }
#ifndef BOOST_UBLAS_NO_MEMBER_FRIENDS
        BOOST_UBLAS_INLINE
        friend void swap (zero_matrix &m1, zero_matrix &m2) {
            m1.swap (m2);
        }
#endif

        // Iterator types
    private:
        // Use an index
        typedef size_type const_iterator_type;
    public:
#ifdef BOOST_UBLAS_USE_INDEXED_ITERATOR
        typedef indexed_const_iterator1<self_type, sparse_bidirectional_iterator_tag> iterator1;
        typedef indexed_const_iterator2<self_type, sparse_bidirectional_iterator_tag> iterator2;
        typedef indexed_const_iterator1<self_type, sparse_bidirectional_iterator_tag> const_iterator1;
        typedef indexed_const_iterator2<self_type, sparse_bidirectional_iterator_tag> const_iterator2;
#else
        class const_iterator1;
        class const_iterator2;
#endif
#ifdef BOOST_MSVC_STD_ITERATOR
        typedef reverse_iterator_base1<const_iterator1, value_type, const_reference> const_reverse_iterator1;
        typedef reverse_iterator_base2<const_iterator2, value_type, const_reference> const_reverse_iterator2;
#else
        typedef reverse_iterator_base1<const_iterator1> const_reverse_iterator1;
        typedef reverse_iterator_base2<const_iterator2> const_reverse_iterator2;
#endif

        // Element lookup
        BOOST_UBLAS_INLINE
        const_iterator1 find1 (int rank, size_type i, size_type j) const {
            if (rank == 1)
                i = j;
            return const_iterator1 (*this, i, j);
        }
        BOOST_UBLAS_INLINE
        const_iterator2 find2 (int rank, size_type i, size_type j) const {
            if (rank == 1)
                j = i;
            return const_iterator2 (*this, i, j);
        }


#ifndef BOOST_UBLAS_USE_INDEXED_ITERATOR
        class const_iterator1:
            public container_const_reference<zero_matrix>,
            public bidirectional_iterator_base<sparse_bidirectional_iterator_tag,
                                               const_iterator1, value_type> {
        public:
            typedef sparse_bidirectional_iterator_tag iterator_category;
#ifdef BOOST_MSVC_STD_ITERATOR
            typedef const_reference reference;
#else
            typedef typename zero_matrix::value_type value_type;
            typedef typename zero_matrix::difference_type difference_type;
            typedef typename zero_matrix::const_reference reference;
            typedef typename zero_matrix::const_pointer pointer;
#endif
            typedef const_iterator2 dual_iterator_type;
            typedef const_reverse_iterator2 dual_reverse_iterator_type;

            // Construction and destruction
            BOOST_UBLAS_INLINE
            const_iterator1 ():
                container_const_reference<self_type> (), it1_ (), it2_ () {}
            BOOST_UBLAS_INLINE
            const_iterator1 (const self_type &m, const const_iterator_type &it1, const const_iterator_type &it2):
                container_const_reference<self_type> (m), it1_ (it1), it2_ (it2) {}

            // Arithmetic
            BOOST_UBLAS_INLINE
            const_iterator1 &operator ++ () {
                ++ it1_;
                return *this;
            }
            BOOST_UBLAS_INLINE
            const_iterator1 &operator -- () {
                -- it1_;
                return *this;
            }
            BOOST_UBLAS_INLINE
            const_iterator1 &operator += (difference_type n) {
                it1_ += n;
                return *this;
            }
            BOOST_UBLAS_INLINE
            const_iterator1 &operator -= (difference_type n) {
                it1_ -= n;
                return *this;
            }
            BOOST_UBLAS_INLINE
            difference_type operator - (const const_iterator1 &it) const {
                BOOST_UBLAS_CHECK (&(*this) () == &it (), external_logic ());
                BOOST_UBLAS_CHECK (it2_ == it.it2_, external_logic ());
                return it1_ - it.it1_;
            }

            // Dereference
            BOOST_UBLAS_INLINE
            const_reference operator * () const {
                BOOST_UBLAS_CHECK (index1 () < (*this) ().size1 (), bad_index ());
                BOOST_UBLAS_CHECK (index2 () < (*this) ().size2 (), bad_index ());
                return (*this) () (index1 (), index2 ());
            }

#ifndef BOOST_UBLAS_NO_NESTED_CLASS_RELATION
            BOOST_UBLAS_INLINE
#ifdef BOOST_UBLAS_MSVC_NESTED_CLASS_RELATION
            typename self_type::
#endif
            const_iterator2 begin () const {
                const self_type &m = (*this) ();
                return m.find2 (1, index1 (), 0);
            }
            BOOST_UBLAS_INLINE
#ifdef BOOST_UBLAS_MSVC_NESTED_CLASS_RELATION
            typename self_type::
#endif
            const_iterator2 end () const {
                const self_type &m = (*this) ();
                return m.find2 (1, index1 (), m.size2 ());
            }
            BOOST_UBLAS_INLINE
#ifdef BOOST_UBLAS_MSVC_NESTED_CLASS_RELATION
            typename self_type::
#endif
            const_reverse_iterator2 rbegin () const {
                return const_reverse_iterator2 (end ());
            }
            BOOST_UBLAS_INLINE
#ifdef BOOST_UBLAS_MSVC_NESTED_CLASS_RELATION
            typename self_type::
#endif
            const_reverse_iterator2 rend () const {
                return const_reverse_iterator2 (begin ());
            }
#endif

            // Indices
            BOOST_UBLAS_INLINE
            size_type index1 () const {
                return it1_;
            }
            BOOST_UBLAS_INLINE
            size_type index2 () const {
                return it2_;
            }

            // Assignment
            BOOST_UBLAS_INLINE
            const_iterator1 &operator = (const const_iterator1 &it) {
                container_const_reference<self_type>::assign (&it ());
                it1_ = it.it1_;
                it2_ = it.it2_;
                return *this;
            }

            // Comparison
            BOOST_UBLAS_INLINE
            bool operator == (const const_iterator1 &it) const {
                BOOST_UBLAS_CHECK (&(*this) () == &it (), external_logic ());
                BOOST_UBLAS_CHECK (it2_ == it.it2_, external_logic ());
                return it1_ == it.it1_;
            }

        private:
            const_iterator_type it1_;
            const_iterator_type it2_;
        };

        typedef const_iterator1 iterator1;
#endif

        BOOST_UBLAS_INLINE
        const_iterator1 begin1 () const {
            return find1 (0, 0, 0);
        }
        BOOST_UBLAS_INLINE
        const_iterator1 end1 () const {
            return find1 (0, size1_, 0);
        }

#ifndef BOOST_UBLAS_USE_INDEXED_ITERATOR
        class const_iterator2:
            public container_const_reference<zero_matrix>,
            public bidirectional_iterator_base<sparse_bidirectional_iterator_tag,
                                               const_iterator2, value_type> {
        public:
            typedef sparse_bidirectional_iterator_tag iterator_category;
#ifdef BOOST_MSVC_STD_ITERATOR
            typedef const_reference reference;
#else
            typedef typename zero_matrix::value_type value_type;
            typedef typename zero_matrix::difference_type difference_type;
            typedef typename zero_matrix::const_reference reference;
            typedef typename zero_matrix::const_pointer pointer;
#endif
            typedef const_iterator1 dual_iterator_type;
            typedef const_reverse_iterator1 dual_reverse_iterator_type;

            // Construction and destruction
            BOOST_UBLAS_INLINE
            const_iterator2 ():
                container_const_reference<self_type> (), it1_ (), it2_ () {}
            BOOST_UBLAS_INLINE
            const_iterator2 (const self_type &m, const const_iterator_type &it1, const const_iterator_type &it2):
                container_const_reference<self_type> (m), it1_ (it1), it2_ (it2) {}

            // Arithmetic
            BOOST_UBLAS_INLINE
            const_iterator2 &operator ++ () {
                ++ it2_;
                return *this;
            }
            BOOST_UBLAS_INLINE
            const_iterator2 &operator -- () {
                -- it2_;
                return *this;
            }
            BOOST_UBLAS_INLINE
            const_iterator2 &operator += (difference_type n) {
                it2_ += n;
                return *this;
            }
            BOOST_UBLAS_INLINE
            const_iterator2 &operator -= (difference_type n) {
                it2_ -= n;
                return *this;
            }
            BOOST_UBLAS_INLINE
            difference_type operator - (const const_iterator2 &it) const {
                BOOST_UBLAS_CHECK (&(*this) () == &it (), external_logic ());
                BOOST_UBLAS_CHECK (it1_ == it.it1_, external_logic ());
                return it2_ - it.it2_;
            }

            // Dereference
            BOOST_UBLAS_INLINE
            const_reference operator * () const {
                BOOST_UBLAS_CHECK (index1 () < (*this) ().size1 (), bad_index ());
                BOOST_UBLAS_CHECK (index2 () < (*this) ().size2 (), bad_index ());
                return (*this) () (index1 (), index2 ());
            }

#ifndef BOOST_UBLAS_NO_NESTED_CLASS_RELATION
            BOOST_UBLAS_INLINE
#ifdef BOOST_UBLAS_MSVC_NESTED_CLASS_RELATION
            typename self_type::
#endif
            const_iterator1 begin () const {
                const self_type &m = (*this) ();
                return m.find1 (1, 0, index2 ());
            }
            BOOST_UBLAS_INLINE
#ifdef BOOST_UBLAS_MSVC_NESTED_CLASS_RELATION
            typename self_type::
#endif
            const_iterator1 end () const {
                const self_type &m = (*this) ();
                return m.find1 (1, m.size1 (), index2 ());
            }
            BOOST_UBLAS_INLINE
#ifdef BOOST_UBLAS_MSVC_NESTED_CLASS_RELATION
            typename self_type::
#endif
            const_reverse_iterator1 rbegin () const {
                return const_reverse_iterator1 (end ());
            }
            BOOST_UBLAS_INLINE
#ifdef BOOST_UBLAS_MSVC_NESTED_CLASS_RELATION
            typename self_type::
#endif
            const_reverse_iterator1 rend () const {
                return const_reverse_iterator1 (begin ());
            }
#endif

            // Indices
            BOOST_UBLAS_INLINE
            size_type index1 () const {
                return it1_;
            }
            BOOST_UBLAS_INLINE
            size_type index2 () const {
                return it2_;
            }

            // Assignment
            BOOST_UBLAS_INLINE
            const_iterator2 &operator = (const const_iterator2 &it) {
                container_const_reference<self_type>::assign (&it ());
                it1_ = it.it1_;
                it2_ = it.it2_;
                return *this;
            }

            // Comparison
            BOOST_UBLAS_INLINE
            bool operator == (const const_iterator2 &it) const {
                BOOST_UBLAS_CHECK (&(*this) () == &it (), external_logic ());
                BOOST_UBLAS_CHECK (it1_ == it.it1_, external_logic ());
                return it2_ == it.it2_;
            }
            BOOST_UBLAS_INLINE
            bool operator < (const const_iterator2 &it) const {
                BOOST_UBLAS_CHECK (&(*this) () == &it (), external_logic ());
                BOOST_UBLAS_CHECK (it1_ == it.it1_, external_logic ());
                return it2_ < it.it2_;
            }

        private:
            const_iterator_type it1_;
            const_iterator_type it2_;
        };

        typedef const_iterator2 iterator2;
#endif

        BOOST_UBLAS_INLINE
        const_iterator2 begin2 () const {
            return find2 (0, 0, 0);
        }
        BOOST_UBLAS_INLINE
        const_iterator2 end2 () const {
            return find2 (0, 0, size2_);
        }

        // Reverse iterators

        BOOST_UBLAS_INLINE
        const_reverse_iterator1 rbegin1 () const {
            return const_reverse_iterator1 (end1 ());
        }
        BOOST_UBLAS_INLINE
        const_reverse_iterator1 rend1 () const {
            return const_reverse_iterator1 (begin1 ());
        }

        BOOST_UBLAS_INLINE
        const_reverse_iterator2 rbegin2 () const {
            return const_reverse_iterator2 (end2 ());
        }
        BOOST_UBLAS_INLINE
        const_reverse_iterator2 rend2 () const {
            return const_reverse_iterator2 (begin2 ());
        }

    private:
        size_type size1_;
        size_type size2_;
        static const value_type zero_;
    };

    template<class T>
    const typename zero_matrix<T>::value_type zero_matrix<T>::zero_
#ifdef BOOST_UBLAS_STATIC_OLD_INIT
        = BOOST_UBLAS_TYPENAME zero_matrix<T>::value_type
#endif
        (0);

    // Scalar matrix class
    template<class T>
    class scalar_matrix:
        public matrix_expression<scalar_matrix<T> > {
    public:
#ifndef BOOST_UBLAS_NO_PROXY_SHORTCUTS
        BOOST_UBLAS_USING matrix_expression<scalar_matrix<T> >::operator ();
#endif
        typedef std::size_t size_type;
        typedef std::ptrdiff_t difference_type;
        typedef T value_type;
        typedef const T &const_reference;
        typedef T &reference;
    private:
        typedef const T *const_pointer;
        typedef scalar_matrix<T> self_type;
    public:
#ifndef BOOST_UBLAS_CT_REFERENCE_BASE_TYPEDEFS
        typedef const matrix_const_reference<const self_type> const_closure_type;
#else
        typedef const matrix_reference<const self_type> const_closure_type;
#endif
        typedef dense_tag storage_category;
        typedef unknown_orientation_tag orientation_category;

        // Construction and destruction
        BOOST_UBLAS_INLINE
        scalar_matrix ():
            matrix_expression<self_type> (),
            size1_ (0), size2_ (0), value_ () {}
        BOOST_UBLAS_INLINE
        scalar_matrix (size_type size1, size_type size2, const value_type &value = value_type(1)):
            matrix_expression<self_type> (),
            size1_ (size1), size2_ (size2), value_ (value) {}
        BOOST_UBLAS_INLINE
        scalar_matrix (const scalar_matrix &m):
            matrix_expression<self_type> (),
            size1_ (m.size1_), size2_ (m.size2_), value_ (m.value_) {}

        // Accessors
        BOOST_UBLAS_INLINE
        size_type size1 () const {
            return size1_;
        }
        BOOST_UBLAS_INLINE
        size_type size2 () const {
            return size2_;
        }

        // Resizing
        BOOST_UBLAS_INLINE
        void resize (size_type size1, size_type size2, bool preserve = true) {
            size1_ = size1;
            size2_ = size2;
        }

        // Element access
        BOOST_UBLAS_INLINE
        const_reference operator () (size_type i, size_type j) const {
            return value_;
        }

        // Assignment
        BOOST_UBLAS_INLINE
        scalar_matrix &operator = (const scalar_matrix &m) {
            size1_ = m.size1_;
            size2_ = m.size2_;
            value_ = m.value_;
            return *this;
        }
        BOOST_UBLAS_INLINE
        scalar_matrix &assign_temporary (scalar_matrix &m) {
            swap (m);
            return *this;
        }

        // Swapping
        BOOST_UBLAS_INLINE
        void swap (scalar_matrix &m) {
            if (this != &m) {
                std::swap (size1_, m.size1_);
                std::swap (size2_, m.size2_);
                std::swap (value_, m.value_);
            }
        }
#ifndef BOOST_UBLAS_NO_MEMBER_FRIENDS
        BOOST_UBLAS_INLINE
        friend void swap (scalar_matrix &m1, scalar_matrix &m2) {
            m1.swap (m2);
        }
#endif

        // Iterator types
    private:
        // Use an index
        typedef size_type const_iterator_type;

    public:
#ifdef BOOST_UBLAS_USE_INDEXED_ITERATOR
        typedef indexed_const_iterator1<self_type, dense_random_access_iterator_tag> iterator1;
        typedef indexed_const_iterator2<self_type, dense_random_access_iterator_tag> iterator2;
        typedef indexed_const_iterator1<self_type, dense_random_access_iterator_tag> const_iterator1;
        typedef indexed_const_iterator2<self_type, dense_random_access_iterator_tag> const_iterator2;
#else
        class const_iterator1;
        class const_iterator2;
#endif
#ifdef BOOST_MSVC_STD_ITERATOR
        typedef reverse_iterator_base1<const_iterator1, value_type, const_reference> const_reverse_iterator1;
        typedef reverse_iterator_base2<const_iterator2, value_type, const_reference> const_reverse_iterator2;
#else
        typedef reverse_iterator_base1<const_iterator1> const_reverse_iterator1;
        typedef reverse_iterator_base2<const_iterator2> const_reverse_iterator2;
#endif

        // Element lookup
        BOOST_UBLAS_INLINE
        const_iterator1 find1 (int rank, size_type i, size_type j) const {
            return const_iterator1 (*this, i, j);
        }
        BOOST_UBLAS_INLINE
        const_iterator2 find2 (int rank, size_type i, size_type j) const {
            return const_iterator2 (*this, i, j);
        }


#ifndef BOOST_UBLAS_USE_INDEXED_ITERATOR
        class const_iterator1:
            public container_const_reference<scalar_matrix>,
            public random_access_iterator_base<dense_random_access_iterator_tag,
                                               const_iterator1, value_type> {
        public:
            typedef dense_random_access_iterator_tag iterator_category;
#ifdef BOOST_MSVC_STD_ITERATOR
            typedef const_reference reference;
#else
            typedef typename scalar_matrix::value_type value_type;
            typedef typename scalar_matrix::difference_type difference_type;
            typedef typename scalar_matrix::const_reference reference;
            typedef typename scalar_matrix::const_pointer pointer;
#endif
            typedef const_iterator2 dual_iterator_type;
            typedef const_reverse_iterator2 dual_reverse_iterator_type;

            // Construction and destruction
            BOOST_UBLAS_INLINE
            const_iterator1 ():
                container_const_reference<scalar_matrix> (), it1_ (), it2_ () {}
            BOOST_UBLAS_INLINE
            const_iterator1 (const scalar_matrix &m, const const_iterator_type &it1, const const_iterator_type &it2):
                container_const_reference<scalar_matrix> (m), it1_ (it1), it2_ (it2) {}

            // Arithmetic
            BOOST_UBLAS_INLINE
            const_iterator1 &operator ++ () {
                ++ it1_;
                return *this;
            }
            BOOST_UBLAS_INLINE
            const_iterator1 &operator -- () {
                -- it1_;
                return *this;
            }
            BOOST_UBLAS_INLINE
            const_iterator1 &operator += (difference_type n) {
                it1_ += n;
                return *this;
            }
            BOOST_UBLAS_INLINE
            const_iterator1 &operator -= (difference_type n) {
                it1_ -= n;
                return *this;
            }
            BOOST_UBLAS_INLINE
            difference_type operator - (const const_iterator1 &it) const {
                BOOST_UBLAS_CHECK (&(*this) () == &it (), external_logic ());
                BOOST_UBLAS_CHECK (it2_ == it.it2_, external_logic ());
                return it1_ - it.it1_;
            }

            // Dereference
            BOOST_UBLAS_INLINE
            const_reference operator * () const {
                BOOST_UBLAS_CHECK (index1 () < (*this) ().size1 (), bad_index ());
                BOOST_UBLAS_CHECK (index2 () < (*this) ().size2 (), bad_index ());
                return (*this) () (index1 (), index2 ());
            }

#ifndef BOOST_UBLAS_NO_NESTED_CLASS_RELATION
            BOOST_UBLAS_INLINE
#ifdef BOOST_UBLAS_MSVC_NESTED_CLASS_RELATION
            typename self_type::
#endif
            const_iterator2 begin () const {
                const scalar_matrix &m = (*this) ();
                return m.find2 (1, index1 (), 0);
            }
            BOOST_UBLAS_INLINE
#ifdef BOOST_UBLAS_MSVC_NESTED_CLASS_RELATION
            typename self_type::
#endif
            const_iterator2 end () const {
                const scalar_matrix &m = (*this) ();
                return m.find2 (1, index1 (), m.size2 ());
            }
            BOOST_UBLAS_INLINE
#ifdef BOOST_UBLAS_MSVC_NESTED_CLASS_RELATION
            typename self_type::
#endif
            const_reverse_iterator2 rbegin () const {
                return const_reverse_iterator2 (end ());
            }
            BOOST_UBLAS_INLINE
#ifdef BOOST_UBLAS_MSVC_NESTED_CLASS_RELATION
            typename self_type::
#endif
            const_reverse_iterator2 rend () const {
                return const_reverse_iterator2 (begin ());
            }
#endif

            // Indices
            BOOST_UBLAS_INLINE
            size_type index1 () const {
                return it1_;
            }
            BOOST_UBLAS_INLINE
            size_type index2 () const {
                return it2_;
            }

            // Assignment
            BOOST_UBLAS_INLINE
            const_iterator1 &operator = (const const_iterator1 &it) {
                container_const_reference<scalar_matrix>::assign (&it ());
                it1_ = it.it1_;
                it2_ = it.it2_;
                return *this;
            }

            // Comparison
            BOOST_UBLAS_INLINE
            bool operator == (const const_iterator1 &it) const {
                BOOST_UBLAS_CHECK (&(*this) () == &it (), external_logic ());
                BOOST_UBLAS_CHECK (it2_ == it.it2_, external_logic ());
                return it1_ == it.it1_;
            }
            BOOST_UBLAS_INLINE
            bool operator < (const const_iterator1 &it) const {
                BOOST_UBLAS_CHECK (&(*this) () == &it (), external_logic ());
                BOOST_UBLAS_CHECK (it2_ == it.it2_, external_logic ());
                return it1_ < it.it1_;
            }

        private:
            const_iterator_type it1_;
            const_iterator_type it2_;
        };

        typedef const_iterator1 iterator1;
#endif

        BOOST_UBLAS_INLINE
        const_iterator1 begin1 () const {
            return find1 (0, 0, 0);
        }
        BOOST_UBLAS_INLINE
        const_iterator1 end1 () const {
            return find1 (0, size1_, 0);
        }

#ifndef BOOST_UBLAS_USE_INDEXED_ITERATOR
        class const_iterator2:
            public container_const_reference<scalar_matrix>,
            public random_access_iterator_base<dense_random_access_iterator_tag,
                                               const_iterator2, value_type> {
        public:
            typedef dense_random_access_iterator_tag iterator_category;
#ifdef BOOST_MSVC_STD_ITERATOR
            typedef const_reference reference;
#else
            typedef typename scalar_matrix::value_type value_type;
            typedef typename scalar_matrix::difference_type difference_type;
            typedef typename scalar_matrix::const_reference reference;
            typedef typename scalar_matrix::const_pointer pointer;
#endif
            typedef const_iterator1 dual_iterator_type;
            typedef const_reverse_iterator1 dual_reverse_iterator_type;

            // Construction and destruction
            BOOST_UBLAS_INLINE
            const_iterator2 ():
                container_const_reference<scalar_matrix> (), it1_ (), it2_ () {}
            BOOST_UBLAS_INLINE
            const_iterator2 (const scalar_matrix &m, const const_iterator_type &it1, const const_iterator_type &it2):
                container_const_reference<scalar_matrix> (m), it1_ (it1), it2_ (it2) {}

            // Arithmetic
            BOOST_UBLAS_INLINE
            const_iterator2 &operator ++ () {
                ++ it2_;
                return *this;
            }
            BOOST_UBLAS_INLINE
            const_iterator2 &operator -- () {
                -- it2_;
                return *this;
            }
            BOOST_UBLAS_INLINE
            const_iterator2 &operator += (difference_type n) {
                it2_ += n;
                return *this;
            }
            BOOST_UBLAS_INLINE
            const_iterator2 &operator -= (difference_type n) {
                it2_ -= n;
                return *this;
            }
            BOOST_UBLAS_INLINE
            difference_type operator - (const const_iterator2 &it) const {
                BOOST_UBLAS_CHECK (&(*this) () == &it (), external_logic ());
                BOOST_UBLAS_CHECK (it1_ == it.it1_, external_logic ());
                return it2_ - it.it2_;
            }

            // Dereference
            BOOST_UBLAS_INLINE
            const_reference operator * () const {
                BOOST_UBLAS_CHECK (index1 () < (*this) ().size1 (), bad_index ());
                BOOST_UBLAS_CHECK (index2 () < (*this) ().size2 (), bad_index ());
                return (*this) () (index1 (), index2 ());
            }

#ifndef BOOST_UBLAS_NO_NESTED_CLASS_RELATION
            BOOST_UBLAS_INLINE
#ifdef BOOST_UBLAS_MSVC_NESTED_CLASS_RELATION
            typename self_type::
#endif
            const_iterator1 begin () const {
                const scalar_matrix &m = (*this) ();
                return m.find1 (1, 0, index2 ());
            }
            BOOST_UBLAS_INLINE
#ifdef BOOST_UBLAS_MSVC_NESTED_CLASS_RELATION
            typename self_type::
#endif
            const_iterator1 end () const {
                const scalar_matrix &m = (*this) ();
                return m.find1 (1, m.size1 (), index2 ());
            }
            BOOST_UBLAS_INLINE
#ifdef BOOST_UBLAS_MSVC_NESTED_CLASS_RELATION
            typename self_type::
#endif
            const_reverse_iterator1 rbegin () const {
                return const_reverse_iterator1 (end ());
            }
            BOOST_UBLAS_INLINE
#ifdef BOOST_UBLAS_MSVC_NESTED_CLASS_RELATION
            typename self_type::
#endif
            const_reverse_iterator1 rend () const {
                return const_reverse_iterator1 (begin ());
            }
#endif

            // Indices
            BOOST_UBLAS_INLINE
            size_type index1 () const {
                return it1_;
            }
            BOOST_UBLAS_INLINE
            size_type index2 () const {
                return it2_;
            }

            // Assignment
            BOOST_UBLAS_INLINE
            const_iterator2 &operator = (const const_iterator2 &it) {
                container_const_reference<scalar_matrix>::assign (&it ());
                it1_ = it.it1_;
                it2_ = it.it2_;
                return *this;
            }

            // Comparison
            BOOST_UBLAS_INLINE
            bool operator == (const const_iterator2 &it) const {
                BOOST_UBLAS_CHECK (&(*this) () == &it (), external_logic ());
                BOOST_UBLAS_CHECK (it1_ == it.it1_, external_logic ());
                return it2_ == it.it2_;
            }
            BOOST_UBLAS_INLINE
            bool operator < (const const_iterator2 &it) const {
                BOOST_UBLAS_CHECK (&(*this) () == &it (), external_logic ());
                BOOST_UBLAS_CHECK (it1_ == it.it1_, external_logic ());
                return it2_ < it.it2_;
            }

        private:
            const_iterator_type it1_;
            const_iterator_type it2_;
        };

        typedef const_iterator2 iterator2;
#endif

        BOOST_UBLAS_INLINE
        const_iterator2 begin2 () const {
            return find2 (0, 0, 0);
        }
        BOOST_UBLAS_INLINE
        const_iterator2 end2 () const {
            return find2 (0, 0, size2_);
        }

        // Reverse iterators

        BOOST_UBLAS_INLINE
        const_reverse_iterator1 rbegin1 () const {
            return const_reverse_iterator1 (end1 ());
        }
        BOOST_UBLAS_INLINE
        const_reverse_iterator1 rend1 () const {
            return const_reverse_iterator1 (begin1 ());
        }

        BOOST_UBLAS_INLINE
        const_reverse_iterator2 rbegin2 () const {
            return const_reverse_iterator2 (end2 ());
        }
        BOOST_UBLAS_INLINE
        const_reverse_iterator2 rend2 () const {
            return const_reverse_iterator2 (begin2 ());
        }

    private:
        size_type size1_;
        size_type size2_;
        value_type value_;
    };

    // Array based matrix class
    template<class T, std::size_t N, std::size_t M>
    class c_matrix:
        public matrix_expression<c_matrix<T, N, M> > {
    public:
#ifndef BOOST_UBLAS_NO_PROXY_SHORTCUTS
        BOOST_UBLAS_USING matrix_expression<c_matrix<T, N, M> >::operator ();
#endif
        typedef std::size_t size_type;
        typedef std::ptrdiff_t difference_type;
        typedef T value_type;
        typedef const T &const_reference;
        typedef T &reference;
        typedef const T *const_pointer;
        typedef T *pointer;
    private:
        typedef c_matrix<T, N, M> self_type;
    public:
#ifndef BOOST_UBLAS_CT_REFERENCE_BASE_TYPEDEFS
        typedef const matrix_const_reference<const self_type> const_closure_type;
#else
        typedef const matrix_reference<const self_type> const_closure_type;
#endif
        typedef matrix_reference<self_type> closure_type;
        typedef c_vector<T, N * M> vector_temporary_type;     // vector able to store all elements of c_matrix
        typedef self_type matrix_temporary_type;
        typedef dense_tag storage_category;
        // This could be better for performance,
        // typedef typename unknown_orientation_tag orientation_category;
        // but others depend on the orientation information...
        typedef row_major_tag orientation_category;
        typedef concrete_tag simd_category;

        // Construction and destruction
        BOOST_UBLAS_INLINE
        c_matrix ():
            size1_ (N), size2_ (M) /* , data_ () */ {
            for (size_type i = 0; i < size1_; ++ i)
                std::fill (data_ [i], data_ [i] + size2_, value_type (0));
        }
        BOOST_UBLAS_INLINE
        c_matrix (size_type size1, size_type size2):
            size1_ (size1), size2_ (size2) /* , data_ () */ {
            if (size1_ > N || size2_ > M)
                bad_size ().raise ();
            for (size_type i = 0; i < size1_; ++ i)
                std::fill (data_ [i], data_ [i] + size2_, value_type (0));
        }
        BOOST_UBLAS_INLINE
        c_matrix (const c_matrix &m):
            size1_ (m.size1_), size2_ (m.size2_) /* , data_ () */ {
            if (size1_ > N || size2_ > M)
                bad_size ().raise ();
            *this = m;
        }
        template<class AE>
        BOOST_UBLAS_INLINE
        c_matrix (const matrix_expression<AE> &ae):
            size1_ (ae ().size1 ()), size2_ (ae ().size2 ()) /* , data_ () */ {
            if (size1_ > N || size2_ > M)
                bad_size ().raise ();
            matrix_assign (scalar_assign<reference, BOOST_UBLAS_TYPENAME AE::value_type> (), *this, ae);
        }

        // Accessors
        BOOST_UBLAS_INLINE
        size_type size1 () const {
            return size1_;
        }
        BOOST_UBLAS_INLINE
        size_type size2 () const {
            return size2_;
        }
        BOOST_UBLAS_INLINE
        const_pointer data () const {
            return reinterpret_cast<const_pointer> (data_);
        }
        BOOST_UBLAS_INLINE
        pointer data () {
            return reinterpret_cast<pointer> (data_);
        }

        // Resizing
        BOOST_UBLAS_INLINE
        void resize (size_type size1, size_type size2, bool preserve = true) {
            if (size1 > N || size2 > M)
                bad_size ().raise ();
            if (preserve) {
                self_type temporary (size1, size2);
                // Common elements to preserve
                const size_type size1_min = (std::min) (size1, size1_);
                const size_type size2_min = (std::min) (size2, size2_);
                for (size_type i = 0; i != size1_min; ++i) {    // indexing copy over major
                    for (size_type j = 0; j != size2_min; ++j) {
                        temporary.data_[i][j] = data_[i][j];
                    }
                }
                assign_temporary (temporary);
            }
            else {
                size1_ = size1;
                size2_ = size2;
            }
        }

        // Element access
        BOOST_UBLAS_INLINE
        const_reference operator () (size_type i, size_type j) const {
            BOOST_UBLAS_CHECK (i < size1_, bad_index ());
            BOOST_UBLAS_CHECK (j < size2_, bad_index ());
            return data_ [i] [j];
        }
        BOOST_UBLAS_INLINE
        reference operator () (size_type i, size_type j) {
            BOOST_UBLAS_CHECK (i < size1_, bad_index ());
            BOOST_UBLAS_CHECK (j < size2_, bad_index ());
            return data_ [i] [j];
        }

        // Assignment
        BOOST_UBLAS_INLINE
        c_matrix &operator = (const c_matrix &m) {
            size1_ = m.size1_;
            size2_ = m.size2_;
            for (size_type i = 0; i < m.size1_; ++ i)
                std::copy (m.data_ [i], m.data_ [i] + m.size2_, data_ [i]);
            return *this;
        }
        BOOST_UBLAS_INLINE
        c_matrix &assign_temporary (c_matrix &m) {
            swap (m);
            return *this;
        }
        template<class AE>
        BOOST_UBLAS_INLINE
        c_matrix &operator = (const matrix_expression<AE> &ae) {
            // return assign (self_type (ae));
            self_type temporary (ae);
            return assign_temporary (temporary);
        }
        template<class AE>
        BOOST_UBLAS_INLINE
        c_matrix &assign (const matrix_expression<AE> &ae) {
            matrix_assign (scalar_assign<reference, BOOST_UBLAS_TYPENAME AE::value_type> (), *this, ae);
            return *this;
        }
        template<class AE>
        BOOST_UBLAS_INLINE
        c_matrix& operator += (const matrix_expression<AE> &ae) {
            // return assign (self_type (*this + ae));
            self_type temporary (*this + ae);
            return assign_temporary (temporary);
        }
        template<class AE>
        BOOST_UBLAS_INLINE
        c_matrix &plus_assign (const matrix_expression<AE> &ae) {
            matrix_assign (scalar_plus_assign<reference, BOOST_UBLAS_TYPENAME AE::value_type> (), *this, ae);
            return *this;
        }
        template<class AE>
        BOOST_UBLAS_INLINE
        c_matrix& operator -= (const matrix_expression<AE> &ae) {
            // return assign (self_type (*this - ae));
            self_type temporary (*this - ae);
            return assign_temporary (temporary);
        }
        template<class AE>
        BOOST_UBLAS_INLINE
        c_matrix &minus_assign (const matrix_expression<AE> &ae) {
            matrix_assign (scalar_minus_assign<reference, BOOST_UBLAS_TYPENAME AE::value_type> (), *this, ae);
            return *this;
        }
        template<class AT>
        BOOST_UBLAS_INLINE
        c_matrix& operator *= (const AT &at) {
            matrix_assign_scalar (scalar_multiplies_assign<reference, AT> (), *this, at);
            return *this;
        }
        template<class AT>
        BOOST_UBLAS_INLINE
        c_matrix& operator /= (const AT &at) {
            matrix_assign_scalar (scalar_divides_assign<reference, AT> (), *this, at);
            return *this;
        }

        // Swapping
        BOOST_UBLAS_INLINE
        void swap (c_matrix &m) {
            if (this != &m) {
                BOOST_UBLAS_CHECK (size1_ == m.size1_, bad_size ());
                BOOST_UBLAS_CHECK (size2_ == m.size2_, bad_size ());
                std::swap (size1_, m.size1_);
                std::swap (size2_, m.size2_);
                for (size_type i = 0; i < size1_; ++ i)
                    std::swap_ranges (data_ [i], data_ [i] + size2_, m.data_ [i]);
            }
        }
#ifndef BOOST_UBLAS_NO_MEMBER_FRIENDS
        BOOST_UBLAS_INLINE
        friend void swap (c_matrix &m1, c_matrix &m2) {
            m1.swap (m2);
        }
#endif

        // Element insertion and erasure
        BOOST_UBLAS_INLINE
        void insert (size_type i, size_type j, const_reference t) {
            BOOST_UBLAS_CHECK (i < size1_, bad_index ());
            BOOST_UBLAS_CHECK (j < size2_, bad_index ());
            BOOST_UBLAS_CHECK (data_ [i] [j] == value_type (0), bad_index ());
            data_ [i] [j] = t;
        }
        BOOST_UBLAS_INLINE
        void erase (size_type i, size_type j) {
            BOOST_UBLAS_CHECK (i < size1_, bad_index ());
            BOOST_UBLAS_CHECK (j < size2_, bad_index ());
            data_ [i] [j] = value_type (0);
        }
        BOOST_UBLAS_INLINE
        void clear () {
            for (size_type i = 0; i < size1_; ++ i)
                std::fill (data_ [i], data_ [i] + size2_, value_type (0));
        }

        // Iterator types
    private:
        // Use pointers for iterator
        typedef const_pointer const_iterator_type;
        typedef pointer iterator_type;

    public:
#ifdef BOOST_UBLAS_USE_INDEXED_ITERATOR
        typedef indexed_iterator1<self_type, dense_random_access_iterator_tag> iterator1;
        typedef indexed_iterator2<self_type, dense_random_access_iterator_tag> iterator2;
        typedef indexed_const_iterator1<self_type, dense_random_access_iterator_tag> const_iterator1;
        typedef indexed_const_iterator2<self_type, dense_random_access_iterator_tag> const_iterator2;
#else
        class const_iterator1;
        class iterator1;
        class const_iterator2;
        class iterator2;
#endif
#ifdef BOOST_MSVC_STD_ITERATOR
        typedef reverse_iterator_base1<const_iterator1, value_type, const_reference> const_reverse_iterator1;
        typedef reverse_iterator_base1<iterator1, value_type, reference> reverse_iterator1;
        typedef reverse_iterator_base2<const_iterator2, value_type, const_reference> const_reverse_iterator2;
        typedef reverse_iterator_base2<iterator2, value_type, reference> reverse_iterator2;
#else
        typedef reverse_iterator_base1<const_iterator1> const_reverse_iterator1;
        typedef reverse_iterator_base1<iterator1> reverse_iterator1;
        typedef reverse_iterator_base2<const_iterator2> const_reverse_iterator2;
        typedef reverse_iterator_base2<iterator2> reverse_iterator2;
#endif

        // Element lookup
        BOOST_UBLAS_INLINE
        const_iterator1 find1 (int rank, size_type i, size_type j) const {
#ifdef BOOST_UBLAS_USE_INDEXED_ITERATOR
            return const_iterator1 (*this, i, j);
#else
            return const_iterator1 (*this, &data_ [i] [j]);
#endif
        }
        BOOST_UBLAS_INLINE
        iterator1 find1 (int rank, size_type i, size_type j) {
#ifdef BOOST_UBLAS_USE_INDEXED_ITERATOR
            return iterator1 (*this, i, j);
#else
            return iterator1 (*this, &data_ [i] [j]);
#endif
        }
        BOOST_UBLAS_INLINE
        const_iterator2 find2 (int rank, size_type i, size_type j) const {
#ifdef BOOST_UBLAS_USE_INDEXED_ITERATOR
            return const_iterator2 (*this, i, j);
#else
            return const_iterator2 (*this, &data_ [i] [j]);
#endif
        }
        BOOST_UBLAS_INLINE
        iterator2 find2 (int rank, size_type i, size_type j) {
#ifdef BOOST_UBLAS_USE_INDEXED_ITERATOR
            return iterator2 (*this, i, j);
#else
            return iterator2 (*this, &data_ [i] [j]);
#endif
        }


#ifndef BOOST_UBLAS_USE_INDEXED_ITERATOR
        class const_iterator1:
            public container_const_reference<c_matrix>,
            public random_access_iterator_base<dense_random_access_iterator_tag,
                                               const_iterator1, value_type> {
        public:
            typedef dense_random_access_iterator_tag iterator_category;
#ifdef BOOST_MSVC_STD_ITERATOR
            typedef const_reference reference;
#else
            typedef typename c_matrix::difference_type difference_type;
            typedef typename c_matrix::value_type value_type;
            typedef typename c_matrix::const_reference reference;
            typedef typename c_matrix::const_pointer pointer;
#endif
            typedef const_iterator2 dual_iterator_type;
            typedef const_reverse_iterator2 dual_reverse_iterator_type;

            // Construction and destruction
            BOOST_UBLAS_INLINE
            const_iterator1 ():
                container_const_reference<self_type> (), it_ () {}
            BOOST_UBLAS_INLINE
            const_iterator1 (const self_type &m, const const_iterator_type &it):
                container_const_reference<self_type> (m), it_ (it) {}
            BOOST_UBLAS_INLINE
            const_iterator1 (const iterator1 &it):
                container_const_reference<self_type> (it ()), it_ (it.it_) {}

            // Arithmetic
            BOOST_UBLAS_INLINE
            const_iterator1 &operator ++ () {
                it_ += M;
                return *this;
            }
            BOOST_UBLAS_INLINE
            const_iterator1 &operator -- () {
                it_ -= M;
                return *this;
            }
            BOOST_UBLAS_INLINE
            const_iterator1 &operator += (difference_type n) {
                it_ += n * M;
                return *this;
            }
            BOOST_UBLAS_INLINE
            const_iterator1 &operator -= (difference_type n) {
                it_ -= n * M;
                return *this;
            }
            BOOST_UBLAS_INLINE
            difference_type operator - (const const_iterator1 &it) const {
                BOOST_UBLAS_CHECK (&(*this) () == &it (), external_logic ());
                return (it_ - it.it_) / M;
            }

            // Dereference
            BOOST_UBLAS_INLINE
            const_reference operator * () const {
                BOOST_UBLAS_CHECK (index1 () < (*this) ().size1 (), bad_index ());
                BOOST_UBLAS_CHECK (index2 () < (*this) ().size2 (), bad_index ());
                return *it_;
            }

#ifndef BOOST_UBLAS_NO_NESTED_CLASS_RELATION
            BOOST_UBLAS_INLINE
#ifdef BOOST_UBLAS_MSVC_NESTED_CLASS_RELATION
            typename self_type::
#endif
            const_iterator2 begin () const {
                const self_type &m = (*this) ();
                return m.find2 (1, index1 (), 0);
            }
            BOOST_UBLAS_INLINE
#ifdef BOOST_UBLAS_MSVC_NESTED_CLASS_RELATION
            typename self_type::
#endif
            const_iterator2 end () const {
                const self_type &m = (*this) ();
                return m.find2 (1, index1 (), m.size2 ());
            }
            BOOST_UBLAS_INLINE
#ifdef BOOST_UBLAS_MSVC_NESTED_CLASS_RELATION
            typename self_type::
#endif
            const_reverse_iterator2 rbegin () const {
                return const_reverse_iterator2 (end ());
            }
            BOOST_UBLAS_INLINE
#ifdef BOOST_UBLAS_MSVC_NESTED_CLASS_RELATION
            typename self_type::
#endif
            const_reverse_iterator2 rend () const {
                return const_reverse_iterator2 (begin ());
            }
#endif

            // Indices
            BOOST_UBLAS_INLINE
            size_type index1 () const {
                const self_type &m = (*this) ();
                return (it_ - m.begin1 ().it_) / M;
            }
            BOOST_UBLAS_INLINE
            size_type index2 () const {
                const self_type &m = (*this) ();
                return (it_ - m.begin1 ().it_) % M;
            }

            // Assignment
            BOOST_UBLAS_INLINE
            const_iterator1 &operator = (const const_iterator1 &it) {
                container_const_reference<self_type>::assign (&it ());
                it_ = it.it_;
                return *this;
            }

            // Comparison
            BOOST_UBLAS_INLINE
            bool operator == (const const_iterator1 &it) const {
                BOOST_UBLAS_CHECK (&(*this) () == &it (), external_logic ());
                return it_ == it.it_;
            }
            BOOST_UBLAS_INLINE
            bool operator < (const const_iterator1 &it) const {
                BOOST_UBLAS_CHECK (&(*this) () == &it (), external_logic ());
                return it_ < it.it_;
            }

        private:
            const_iterator_type it_;

            friend class iterator1;
        };
#endif

        BOOST_UBLAS_INLINE
        const_iterator1 begin1 () const {
            return find1 (0, 0, 0);
        }
        BOOST_UBLAS_INLINE
        const_iterator1 end1 () const {
            return find1 (0, size1_, 0);
        }

#ifndef BOOST_UBLAS_USE_INDEXED_ITERATOR
        class iterator1:
            public container_reference<c_matrix>,
            public random_access_iterator_base<dense_random_access_iterator_tag,
                                               iterator1, value_type> {
        public:
            typedef dense_random_access_iterator_tag iterator_category;
#ifndef BOOST_MSVC_STD_ITERATOR
            typedef typename c_matrix::difference_type difference_type;
            typedef typename c_matrix::value_type value_type;
            typedef typename c_matrix::reference reference;
            typedef typename c_matrix::pointer pointer;
#endif
            typedef iterator2 dual_iterator_type;
            typedef reverse_iterator2 dual_reverse_iterator_type;

            // Construction and destruction
            BOOST_UBLAS_INLINE
            iterator1 ():
                container_reference<self_type> (), it_ () {}
            BOOST_UBLAS_INLINE
            iterator1 (self_type &m, const iterator_type &it):
                container_reference<self_type> (m), it_ (it) {}

            // Arithmetic
            BOOST_UBLAS_INLINE
            iterator1 &operator ++ () {
                it_ += M;
                return *this;
            }
            BOOST_UBLAS_INLINE
            iterator1 &operator -- () {
                it_ -= M;
                return *this;
            }
            BOOST_UBLAS_INLINE
            iterator1 &operator += (difference_type n) {
                it_ += n * M;
                return *this;
            }
            BOOST_UBLAS_INLINE
            iterator1 &operator -= (difference_type n) {
                it_ -= n * M;
                return *this;
            }
            BOOST_UBLAS_INLINE
            difference_type operator - (const iterator1 &it) const {
                BOOST_UBLAS_CHECK (&(*this) () == &it (), external_logic ());
                return (it_ - it.it_) / M;
            }

            // Dereference
            BOOST_UBLAS_INLINE
            reference operator * () const {
                BOOST_UBLAS_CHECK (index1 () < (*this) ().size1 (), bad_index ());
                BOOST_UBLAS_CHECK (index2 () < (*this) ().size2 (), bad_index ());
                return *it_;
            }

#ifndef BOOST_UBLAS_NO_NESTED_CLASS_RELATION
            BOOST_UBLAS_INLINE
#ifdef BOOST_UBLAS_MSVC_NESTED_CLASS_RELATION
            typename self_type::
#endif
            iterator2 begin () const {
                self_type &m = (*this) ();
                return m.find2 (1, index1 (), 0);
            }
            BOOST_UBLAS_INLINE
#ifdef BOOST_UBLAS_MSVC_NESTED_CLASS_RELATION
            typename self_type::
#endif
            iterator2 end () const {
                self_type &m = (*this) ();
                return m.find2 (1, index1 (), m.size2 ());
            }
            BOOST_UBLAS_INLINE
#ifdef BOOST_UBLAS_MSVC_NESTED_CLASS_RELATION
            typename self_type::
#endif
            reverse_iterator2 rbegin () const {
                return reverse_iterator2 (end ());
            }
            BOOST_UBLAS_INLINE
#ifdef BOOST_UBLAS_MSVC_NESTED_CLASS_RELATION
            typename self_type::
#endif
            reverse_iterator2 rend () const {
                return reverse_iterator2 (begin ());
            }
#endif

            // Indices
            BOOST_UBLAS_INLINE
            size_type index1 () const {
                const self_type &m = (*this) ();
                return (it_ - m.begin1 ().it_) / M;
            }
            BOOST_UBLAS_INLINE
            size_type index2 () const {
                const self_type &m = (*this) ();
                return (it_ - m.begin1 ().it_) % M;
            }

            // Assignment
            BOOST_UBLAS_INLINE
            iterator1 &operator = (const iterator1 &it) {
                container_reference<self_type>::assign (&it ());
                it_ = it.it_;
                return *this;
            }

            // Comparison
            BOOST_UBLAS_INLINE
            bool operator == (const iterator1 &it) const {
                BOOST_UBLAS_CHECK (&(*this) () == &it (), external_logic ());
                return it_ == it.it_;
            }
            BOOST_UBLAS_INLINE
            bool operator < (const iterator1 &it) const {
                BOOST_UBLAS_CHECK (&(*this) () == &it (), external_logic ());
                return it_ < it.it_;
            }

        private:
            iterator_type it_;

            friend class const_iterator1;
        };
#endif

        BOOST_UBLAS_INLINE
        iterator1 begin1 () {
            return find1 (0, 0, 0);
        }
        BOOST_UBLAS_INLINE
        iterator1 end1 () {
            return find1 (0, size1_, 0);
        }

#ifndef BOOST_UBLAS_USE_INDEXED_ITERATOR
        class const_iterator2:
            public container_const_reference<c_matrix>,
            public random_access_iterator_base<dense_random_access_iterator_tag,
                                               const_iterator2, value_type> {
        public:
            typedef dense_random_access_iterator_tag iterator_category;
#ifdef BOOST_MSVC_STD_ITERATOR
            typedef const_reference reference;
#else
            typedef typename c_matrix::difference_type difference_type;
            typedef typename c_matrix::value_type value_type;
            typedef typename c_matrix::const_reference reference;
            typedef typename c_matrix::const_reference pointer;
#endif
            typedef const_iterator1 dual_iterator_type;
            typedef const_reverse_iterator1 dual_reverse_iterator_type;

            // Construction and destruction
            BOOST_UBLAS_INLINE
            const_iterator2 ():
                container_const_reference<self_type> (), it_ () {}
            BOOST_UBLAS_INLINE
            const_iterator2 (const self_type &m, const const_iterator_type &it):
                container_const_reference<self_type> (m), it_ (it) {}
            BOOST_UBLAS_INLINE
            const_iterator2 (const iterator2 &it):
                container_const_reference<self_type> (it ()), it_ (it.it_) {}

            // Arithmetic
            BOOST_UBLAS_INLINE
            const_iterator2 &operator ++ () {
                ++ it_;
                return *this;
            }
            BOOST_UBLAS_INLINE
            const_iterator2 &operator -- () {
                -- it_;
                return *this;
            }
            BOOST_UBLAS_INLINE
            const_iterator2 &operator += (difference_type n) {
                it_ += n;
                return *this;
            }
            BOOST_UBLAS_INLINE
            const_iterator2 &operator -= (difference_type n) {
                it_ -= n;
                return *this;
            }
            BOOST_UBLAS_INLINE
            difference_type operator - (const const_iterator2 &it) const {
                BOOST_UBLAS_CHECK (&(*this) () == &it (), external_logic ());
                return it_ - it.it_;
            }

            // Dereference
            BOOST_UBLAS_INLINE
            const_reference operator * () const {
                BOOST_UBLAS_CHECK (index1 () < (*this) ().size1 (), bad_index ());
                BOOST_UBLAS_CHECK (index2 () < (*this) ().size2 (), bad_index ());
                return *it_;
            }

#ifndef BOOST_UBLAS_NO_NESTED_CLASS_RELATION
            BOOST_UBLAS_INLINE
#ifdef BOOST_UBLAS_MSVC_NESTED_CLASS_RELATION
            typename self_type::
#endif
            const_iterator1 begin () const {
                const self_type &m = (*this) ();
                return m.find1 (1, 0, index2 ());
            }
            BOOST_UBLAS_INLINE
#ifdef BOOST_UBLAS_MSVC_NESTED_CLASS_RELATION
            typename self_type::
#endif
            const_iterator1 end () const {
                const self_type &m = (*this) ();
                return m.find1 (1, m.size1 (), index2 ());
            }
            BOOST_UBLAS_INLINE
#ifdef BOOST_UBLAS_MSVC_NESTED_CLASS_RELATION
            typename self_type::
#endif
            const_reverse_iterator1 rbegin () const {
                return const_reverse_iterator1 (end ());
            }
            BOOST_UBLAS_INLINE
#ifdef BOOST_UBLAS_MSVC_NESTED_CLASS_RELATION
            typename self_type::
#endif
            const_reverse_iterator1 rend () const {
                return const_reverse_iterator1 (begin ());
            }
#endif

            // Indices
            BOOST_UBLAS_INLINE
            size_type index1 () const {
                const self_type &m = (*this) ();
                return (it_ - m.begin2 ().it_) / M;
            }
            BOOST_UBLAS_INLINE
            size_type index2 () const {
                const self_type &m = (*this) ();
                return (it_ - m.begin2 ().it_) % M;
            }

            // Assignment
            BOOST_UBLAS_INLINE
            const_iterator2 &operator = (const const_iterator2 &it) {
                container_const_reference<self_type>::assign (&it ());
                it_ = it.it_;
                return *this;
            }

            // Comparison
            BOOST_UBLAS_INLINE
            bool operator == (const const_iterator2 &it) const {
                BOOST_UBLAS_CHECK (&(*this) () == &it (), external_logic ());
                return it_ == it.it_;
            }
            BOOST_UBLAS_INLINE
            bool operator < (const const_iterator2 &it) const {
                BOOST_UBLAS_CHECK (&(*this) () == &it (), external_logic ());
                return it_ < it.it_;
            }

        private:
            const_iterator_type it_;

            friend class iterator2;
        };
#endif

        BOOST_UBLAS_INLINE
        const_iterator2 begin2 () const {
            return find2 (0, 0, 0);
        }
        BOOST_UBLAS_INLINE
        const_iterator2 end2 () const {
            return find2 (0, 0, size2_);
        }

#ifndef BOOST_UBLAS_USE_INDEXED_ITERATOR
        class iterator2:
            public container_reference<c_matrix>,
            public random_access_iterator_base<dense_random_access_iterator_tag,
                                               iterator2, value_type> {
        public:
            typedef dense_random_access_iterator_tag iterator_category;
#ifndef BOOST_MSVC_STD_ITERATOR
            typedef typename c_matrix::difference_type difference_type;
            typedef typename c_matrix::value_type value_type;
            typedef typename c_matrix::reference reference;
            typedef typename c_matrix::pointer pointer;
#endif
            typedef iterator1 dual_iterator_type;
            typedef reverse_iterator1 dual_reverse_iterator_type;

            // Construction and destruction
            BOOST_UBLAS_INLINE
            iterator2 ():
                container_reference<self_type> (), it_ () {}
            BOOST_UBLAS_INLINE
            iterator2 (self_type &m, const iterator_type &it):
                container_reference<self_type> (m), it_ (it) {}

            // Arithmetic
            BOOST_UBLAS_INLINE
            iterator2 &operator ++ () {
                ++ it_;
                return *this;
            }
            BOOST_UBLAS_INLINE
            iterator2 &operator -- () {
                -- it_;
                return *this;
            }
            BOOST_UBLAS_INLINE
            iterator2 &operator += (difference_type n) {
                it_ += n;
                return *this;
            }
            BOOST_UBLAS_INLINE
            iterator2 &operator -= (difference_type n) {
                it_ -= n;
                return *this;
            }
            BOOST_UBLAS_INLINE
            difference_type operator - (const iterator2 &it) const {
                BOOST_UBLAS_CHECK (&(*this) () == &it (), external_logic ());
                return it_ - it.it_;
            }

            // Dereference
            BOOST_UBLAS_INLINE
            reference operator * () const {
                BOOST_UBLAS_CHECK (index1 () < (*this) ().size1 (), bad_index ());
                BOOST_UBLAS_CHECK (index2 () < (*this) ().size2 (), bad_index ());
                return *it_;
            }

#ifndef BOOST_UBLAS_NO_NESTED_CLASS_RELATION
            BOOST_UBLAS_INLINE
#ifdef BOOST_UBLAS_MSVC_NESTED_CLASS_RELATION
            typename self_type::
#endif
            iterator1 begin () const {
                self_type &m = (*this) ();
                return m.find1 (1, 0, index2 ());
            }
            BOOST_UBLAS_INLINE
#ifdef BOOST_UBLAS_MSVC_NESTED_CLASS_RELATION
            typename self_type::
#endif
            iterator1 end () const {
                self_type &m = (*this) ();
                return m.find1 (1, m.size1 (), index2 ());
            }
            BOOST_UBLAS_INLINE
#ifdef BOOST_UBLAS_MSVC_NESTED_CLASS_RELATION
            typename self_type::
#endif
            reverse_iterator1 rbegin () const {
                return reverse_iterator1 (end ());
            }
            BOOST_UBLAS_INLINE
#ifdef BOOST_UBLAS_MSVC_NESTED_CLASS_RELATION
            typename self_type::
#endif
            reverse_iterator1 rend () const {
                return reverse_iterator1 (begin ());
            }
#endif

            // Indices
            BOOST_UBLAS_INLINE
            size_type index1 () const {
                const self_type &m = (*this) ();
                return (it_ - m.begin2 ().it_) / M;
            }
            BOOST_UBLAS_INLINE
            size_type index2 () const {
                const self_type &m = (*this) ();
                return (it_ - m.begin2 ().it_) % M;
            }

            // Assignment
            BOOST_UBLAS_INLINE
            iterator2 &operator = (const iterator2 &it) {
                container_reference<self_type>::assign (&it ());
                it_ = it.it_;
                return *this;
            }

            // Comparison
            BOOST_UBLAS_INLINE
            bool operator == (const iterator2 &it) const {
                BOOST_UBLAS_CHECK (&(*this) () == &it (), external_logic ());
                return it_ == it.it_;
            }
            BOOST_UBLAS_INLINE
            bool operator < (const iterator2 &it) const {
                BOOST_UBLAS_CHECK (&(*this) () == &it (), external_logic ());
                return it_ < it.it_;
            }

        private:
            iterator_type it_;

            friend class const_iterator2;
        };
#endif

        BOOST_UBLAS_INLINE
        iterator2 begin2 () {
            return find2 (0, 0, 0);
        }
        BOOST_UBLAS_INLINE
        iterator2 end2 () {
            return find2 (0, 0, size2_);
        }

        // Reverse iterators

        BOOST_UBLAS_INLINE
        const_reverse_iterator1 rbegin1 () const {
            return const_reverse_iterator1 (end1 ());
        }
        BOOST_UBLAS_INLINE
        const_reverse_iterator1 rend1 () const {
            return const_reverse_iterator1 (begin1 ());
        }

        BOOST_UBLAS_INLINE
        reverse_iterator1 rbegin1 () {
            return reverse_iterator1 (end1 ());
        }
        BOOST_UBLAS_INLINE
        reverse_iterator1 rend1 () {
            return reverse_iterator1 (begin1 ());
        }

        BOOST_UBLAS_INLINE
        const_reverse_iterator2 rbegin2 () const {
            return const_reverse_iterator2 (end2 ());
        }
        BOOST_UBLAS_INLINE
        const_reverse_iterator2 rend2 () const {
            return const_reverse_iterator2 (begin2 ());
        }

        BOOST_UBLAS_INLINE
        reverse_iterator2 rbegin2 () {
            return reverse_iterator2 (end2 ());
        }
        BOOST_UBLAS_INLINE
        reverse_iterator2 rend2 () {
            return reverse_iterator2 (begin2 ());
        }

    private:
        size_type size1_;
        size_type size2_;
        value_type data_ [N] [M];
    };

}}}

#endif
