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

#ifndef BOOST_UBLAS_STORAGE_H
#define BOOST_UBLAS_STORAGE_H

#include <algorithm>

#ifdef BOOST_UBLAS_SHALLOW_ARRAY_ADAPTOR
#include <boost/shared_array.hpp>
#endif

#include <boost/numeric/ublas/config.hpp>
#include <boost/numeric/ublas/exception.hpp>
#include <boost/numeric/ublas/iterator.hpp>
#include <boost/numeric/ublas/traits.hpp>

namespace boost { namespace numeric { namespace ublas {

#ifndef BOOST_UBLAS_USE_FAST_SAME
// FIXME: for performance reasons we better use macros
//    template<class T>
//    BOOST_UBLAS_INLINE
//    const T &same_impl (const T &size1, const T &size2) {
//        BOOST_UBLAS_CHECK (size1 == size2, bad_argument ());
//        return (std::min) (size1, size2);
//    }
// #define BOOST_UBLAS_SAME(size1, size2) same_impl ((size1), (size2))
    template<class T>
    BOOST_UBLAS_INLINE
    // Kresimir Fresl and Dan Muller reported problems with COMO.
    // We better change the signature instead of libcomo ;-)
    // const T &same_impl_ex (const T &size1, const T &size2, const char *file, int line) {
    T same_impl_ex (const T &size1, const T &size2, const char *file, int line) {
        BOOST_UBLAS_CHECK_EX (size1 == size2, file, line, bad_argument ());
        return (std::min) (size1, size2);
    }
#define BOOST_UBLAS_SAME(size1, size2) same_impl_ex ((size1), (size2), __FILE__, __LINE__)
#else
// FIXME: for performance reasons we better use macros
//    template<class T>
//    BOOST_UBLAS_INLINE
//    const T &same_impl (const T &size1, const T &size2) {
//        return size1;
//    }
// #define BOOST_UBLAS_SAME(size1, size2) same_impl ((size1), (size2))
#define BOOST_UBLAS_SAME(size1, size2) (size1)
#endif

// If no standard allocator assume it is because hint must be specified. This fixes VC6
#ifdef BOOST_NO_STD_ALLOCATOR
#define BOOST_UBLAS_ALLOCATOR_HINT , 0
#else
#define BOOST_UBLAS_ALLOCATOR_HINT
#endif


    // Base class for Storage Arrays - see the Barton Nackman trick
    template<class E>
    class storage_array:
        private nonassignable {
    };


    // Unbounded array - with allocator
    template<class T, class ALLOC>
    class unbounded_array:
        public storage_array<unbounded_array<T, ALLOC> > {
    public:
        typedef ALLOC allocator_type;
        typedef typename ALLOC::size_type size_type;
        typedef typename ALLOC::difference_type difference_type;
        typedef T value_type;
        typedef const T &const_reference;
        typedef T &reference;
        typedef const T *const_pointer;
        typedef T *pointer;
        typedef const_pointer const_iterator;
        typedef pointer iterator;
    private:
        typedef unbounded_array<T, ALLOC> self_type;

    public:
        // Construction and destruction
        explicit BOOST_UBLAS_INLINE
        unbounded_array (const ALLOC &a = ALLOC()):
            alloc_ (a), size_ (0), data_ (0) {
        }
        explicit BOOST_UBLAS_INLINE
        unbounded_array (size_type size, const ALLOC &a = ALLOC()):
            alloc_(a), size_ (size) {
            if (size_) {
                data_ = alloc_.allocate (size_ BOOST_UBLAS_ALLOCATOR_HINT);
                // ISSUE some compilers may zero POD here
#ifdef BOOST_UBLAS_USEFUL_ARRAY_PLACEMENT_NEW
                // array form fails on some compilers due to size cookie, is it standard conforming?
                new (data_) value_type[size_];
#else
                for (pointer d = data_; d != data_ + size_; ++d)
                    new (d) value_type;
#endif
            }
        }
        // No value initialised, but still be default constructed
        BOOST_UBLAS_INLINE
        unbounded_array (size_type size, const value_type &init, const ALLOC &a = ALLOC()):
            alloc_ (a), size_ (size) {
            if (size_) {
                data_ = alloc_.allocate (size_ BOOST_UBLAS_ALLOCATOR_HINT);
                std::uninitialized_fill (begin(), end(), init);
            }
        }
        BOOST_UBLAS_INLINE
        unbounded_array (const unbounded_array &c):
            storage_array<self_type> (),
            alloc_ (c.alloc_), size_ (c.size_) {
            if (size_) {
                data_ = alloc_.allocate (size_ BOOST_UBLAS_ALLOCATOR_HINT);
                std::uninitialized_copy (c.begin(), c.end(), begin());
            }
            else
                data_ = 0;
        }
        BOOST_UBLAS_INLINE
        ~unbounded_array () {
            if (size_) {
                const iterator i_end = end();
                for (iterator i = begin (); i != i_end; ++i) {
                    iterator_destroy (i);
                }
                alloc_.deallocate (data_, size_);
            }
        }

        // Resizing
    private:
        BOOST_UBLAS_INLINE
        void resize_internal (size_type size, value_type init, bool preserve) {
            if (size != size_) {
                pointer data;
                if  (size) {
                    data = alloc_.allocate (size BOOST_UBLAS_ALLOCATOR_HINT);
                    if (preserve) {
                        const_iterator si = begin ();
                        pointer di = data;
                        if (size < size_) {
                            for (; di != data + size; ++di) {
                                alloc_.construct (di, *si);
                                ++si;
                            }
                        }
                        else {
                            for (const_iterator si_end = end (); si != si_end; ++si) {
                                alloc_.construct (di, *si);
                                ++di;
                            }
                            for (; di != data + size; ++di) {
                                alloc_.construct (di, init);
                            }
                        }
                    }
                    else {
                        // ISSUE some compilers may zero POD here
#ifdef BOOST_UBLAS_USEFUL_ARRAY_PLACEMENT_NEW
                        // array form fails on some compilers due to size cookie, is it standard conforming?
                        new (data) value_type[size];
#else
                        for (pointer d = data; d != data + size; ++d)
                            new (d) value_type;
#endif
                    }
                }
                else
                    data = 0;
                if (size_) {
                    const iterator i_end = end();
                    for (iterator i = begin(); i != i_end; ++i) {
                        iterator_destroy (i);
                    }
                    alloc_.deallocate (data_, size_);
                }
                size_ = size;
                data_ = data;
            }
        }
    public:
        BOOST_UBLAS_INLINE
        void resize (size_type size) {
            resize_internal (size, value_type (), false);
        }
        BOOST_UBLAS_INLINE
        void resize (size_type size, value_type init) {
            resize_internal (size, init, true);
        }

        BOOST_UBLAS_INLINE
        size_type size () const {
            return size_;
        }

        // Element access
        BOOST_UBLAS_INLINE
        const_reference operator [] (size_type i) const {
            BOOST_UBLAS_CHECK (i < size_, bad_index ());
            return data_ [i];
        }
        BOOST_UBLAS_INLINE
        reference operator [] (size_type i) {
            BOOST_UBLAS_CHECK (i < size_, bad_index ());
            return data_ [i];
        }

        // Assignment
        BOOST_UBLAS_INLINE
        unbounded_array &operator = (const unbounded_array &a) {
            if (this != &a) {
                resize (a.size_);
                std::copy (a.data_, a.data_ + a.size_, data_);
            }
            return *this;
        }
        BOOST_UBLAS_INLINE
        unbounded_array &assign_temporary (unbounded_array &a) {
            swap (a);
            return *this;
        }

        // Swapping
        BOOST_UBLAS_INLINE
        void swap (unbounded_array &a) {
            if (this != &a) {
                std::swap (size_, a.size_);
                std::swap (data_, a.data_);
            }
        }
#ifndef BOOST_UBLAS_NO_MEMBER_FRIENDS
        BOOST_UBLAS_INLINE
        friend void swap (unbounded_array &a1, unbounded_array &a2) {
            a1.swap (a2);
        }
#endif

        BOOST_UBLAS_INLINE
        const_iterator begin () const {
            return data_;
        }
        BOOST_UBLAS_INLINE
        const_iterator end () const {
            return data_ + size_;
        }

        BOOST_UBLAS_INLINE
        iterator begin () {
            return data_;
        }
        BOOST_UBLAS_INLINE
        iterator end () {
            return data_ + size_;
        }

        // Reverse iterators

#ifdef BOOST_MSVC_STD_ITERATOR
        typedef std::reverse_iterator<const_iterator, value_type, const_reference> const_reverse_iterator;
#else
        typedef std::reverse_iterator<const_iterator> const_reverse_iterator;
#endif

        BOOST_UBLAS_INLINE
        const_reverse_iterator rbegin () const {
            return const_reverse_iterator (end ());
        }
        BOOST_UBLAS_INLINE
        const_reverse_iterator rend () const {
            return const_reverse_iterator (begin ());
        }

#ifdef BOOST_MSVC_STD_ITERATOR
        typedef std::reverse_iterator<iterator, value_type, reference> reverse_iterator;
#else
        typedef std::reverse_iterator<iterator> reverse_iterator;
#endif

        BOOST_UBLAS_INLINE
        reverse_iterator rbegin () {
            return reverse_iterator (end ());
        }
        BOOST_UBLAS_INLINE
        reverse_iterator rend () {
            return reverse_iterator (begin ());
        }

        // Allocator
        allocator_type get_allocator () {
            return alloc_;
        }

    private:
        // Handle explict destroy on a (possibly indexed) iterator
        BOOST_UBLAS_INLINE
        static void iterator_destroy (iterator &i) {
            (&(*i)) -> ~value_type ();
        }
        ALLOC alloc_;
        size_type size_;
        pointer data_;
    };

    // Bounded array - with allocator for size_type and difference_type
    template<class T, std::size_t N, class ALLOC>
    class bounded_array:
        public storage_array<bounded_array<T, N, ALLOC> > {
    public:
        // No allocator_type as ALLOC is not used for allocation
        typedef typename ALLOC::size_type size_type;
        typedef typename ALLOC::difference_type difference_type;
        typedef T value_type;
        typedef const T &const_reference;
        typedef T &reference;
        typedef const T *const_pointer;
        typedef T *pointer;
        typedef const_pointer const_iterator;
        typedef pointer iterator;
    private:
        typedef bounded_array<T, N, ALLOC> self_type;

    public:
        // Construction and destruction
        BOOST_UBLAS_INLINE
        bounded_array ():
            size_ (0), data_ () {   // size 0 - use bounded_vector to default construct with size N
        }
        explicit BOOST_UBLAS_INLINE
        bounded_array (size_type size):
            size_ (size) /*, data_ ()*/ {
            if (size_ > N)
                bad_size ().raise ();
            // data_ (an array) elements are already default constructed
        }
        BOOST_UBLAS_INLINE
        bounded_array (size_type size, const value_type &init):
            size_ (size) /*, data_ ()*/ {
            if (size_ > N)
                bad_size ().raise ();
            // ISSUE elements should be value constructed here, but we must fill instead as already default constructed
            std::fill (begin(), end(), init) ;
        }
        BOOST_UBLAS_INLINE
        bounded_array (const bounded_array &c):
            storage_array<self_type> (),
            size_ (c.size_)  {
            // ISSUE elements should be copy constructed here, but we must copy instead as already default constructed
            std::copy (c.data_, c.data_ + c.size_, data_);
        }

        // Resizing
        BOOST_UBLAS_INLINE
        void resize (size_type size) {
            if (size > N)
                bad_size ().raise ();
            size_ = size;
        }
        BOOST_UBLAS_INLINE
        void resize (size_type size, value_type init) {
            if (size > N)
                bad_size ().raise ();
            if (size > size_)
                std::fill (data_ + size_, data_ + size, init);
            size_ = size;
        }

        BOOST_UBLAS_INLINE
        size_type size () const {
            return size_;
        }

        // Element access
        BOOST_UBLAS_INLINE
        const_reference operator [] (size_type i) const {
            BOOST_UBLAS_CHECK (i < size_, bad_index ());
            return data_ [i];
        }
        BOOST_UBLAS_INLINE
        reference operator [] (size_type i) {
            BOOST_UBLAS_CHECK (i < size_, bad_index ());
            return data_ [i];
        }

        // Assignment
        BOOST_UBLAS_INLINE
        bounded_array &operator = (const bounded_array &a) {
            if (this != &a) {
                resize (a.size_);
                std::copy (a.data_, a.data_ + a.size_, data_);
            }
            return *this;
        }
        BOOST_UBLAS_INLINE
        bounded_array &assign_temporary (bounded_array &a) {
            *this = a;
            return *this;
        }

        // Swapping
        BOOST_UBLAS_INLINE
        void swap (bounded_array &a) {
            if (this != &a) {
                std::swap (size_, a.size_);
                std::swap_ranges (data_, data_ + (std::max) (size_, a.size_), a.data_);
            }
        }
#ifndef BOOST_UBLAS_NO_MEMBER_FRIENDS
        BOOST_UBLAS_INLINE
        friend void swap (bounded_array &a1, bounded_array &a2) {
            a1.swap (a2);
        }
#endif

        BOOST_UBLAS_INLINE
        const_iterator begin () const {
            return data_;
        }
        BOOST_UBLAS_INLINE
        const_iterator end () const {
            return data_ + size_;
        }

        BOOST_UBLAS_INLINE
        iterator begin () {
            return data_;
        }
        BOOST_UBLAS_INLINE
        iterator end () {
            return data_ + size_;
        }

        // Reverse iterators

#ifdef BOOST_MSVC_STD_ITERATOR
        typedef std::reverse_iterator<const_iterator, value_type, const_reference> const_reverse_iterator;
#else
        typedef std::reverse_iterator<const_iterator> const_reverse_iterator;
#endif

        BOOST_UBLAS_INLINE
        const_reverse_iterator rbegin () const {
            return const_reverse_iterator (end ());
        }
        BOOST_UBLAS_INLINE
        const_reverse_iterator rend () const {
            return const_reverse_iterator (begin ());
        }

#ifdef BOOST_MSVC_STD_ITERATOR
        typedef std::reverse_iterator<iterator, value_type, reference> reverse_iterator;
#else
        typedef std::reverse_iterator<iterator> reverse_iterator;
#endif

        BOOST_UBLAS_INLINE
        reverse_iterator rbegin () {
            return reverse_iterator (end ());
        }
        BOOST_UBLAS_INLINE
        reverse_iterator rend () {
            return reverse_iterator (begin ());
        }

    private:
        size_type size_;
        BOOST_UBLAS_BOUNDED_ARRAY_ALIGN value_type data_ [N];
    };


    // Array adaptor with normal deep copy semantics of elements
    template<class T>
    class array_adaptor:
        public storage_array<array_adaptor<T> > {
    public:
        typedef std::size_t size_type;
        typedef std::ptrdiff_t difference_type;
        typedef T value_type;
        typedef const T &const_reference;
        typedef T &reference;
        typedef const T *const_pointer;
        typedef T *pointer;
    private:
        typedef array_adaptor<T> self_type;

    public:
        // Construction and destruction
        BOOST_UBLAS_INLINE
        array_adaptor ():
            size_ (0), own_ (true), data_ (new value_type [0]) {
        }
        explicit BOOST_UBLAS_INLINE
        array_adaptor (size_type size):
            size_ (size), own_ (true), data_ (new value_type [size]) {
        }
        BOOST_UBLAS_INLINE
        array_adaptor (size_type size, const value_type &init):
            size_ (size), own_ (true), data_ (new value_type [size]) {
            std::fill (data_, data_ + size_, init);
        }
        BOOST_UBLAS_INLINE
        array_adaptor (size_type size, pointer data):
            size_ (size), own_ (false), data_ (data) {}
        BOOST_UBLAS_INLINE
        array_adaptor (const array_adaptor &a):
            storage_array<self_type> (),
            size_ (a.size_), own_ (true), data_ (new value_type [a.size_]) {
            *this = a;
        }
        BOOST_UBLAS_INLINE
        ~array_adaptor () {
            if (own_) {
                delete [] data_;
            }
        }

        // Resizing
    private:
        BOOST_UBLAS_INLINE
        void resize_internal (size_type size, value_type init, bool preserve = true) {
           if (size != size_) {
                pointer data = new value_type [size];
                if (preserve) {
                    std::copy (data_, data_ + (std::min) (size, size_), data);
                    std::fill (data + (std::min) (size, size_), data + size, init);
                }
                if (own_)
                    delete [] data_;
                size_ = size;
                own_ = true;
                data_ = data;
            }
        }
        BOOST_UBLAS_INLINE
        void resize_internal (size_type size, pointer data, value_type init, bool preserve = true) {
            if (data != data_) {
                if (preserve) {
                    std::copy (data_, data_ + (std::min) (size, size_), data);
                    std::fill (data + (std::min) (size, size_), data + size, value_type (0));
                }
                if (own_)
                    delete [] data_;
                own_ = false;
                data_ = data;
            }
            else {
                std::fill (data + (std::min) (size, size_), data + size, value_type (0));
            }
            size_ = size;
        }
    public:
        BOOST_UBLAS_INLINE
        void resize (size_type size) {
            resize_internal (size, value_type (), false);
        }
        BOOST_UBLAS_INLINE
        void resize (size_type size, value_type init) {
            resize_internal (size, init, true);
        }
        BOOST_UBLAS_INLINE
        void resize (size_type size, pointer data) {
            resize_internal (size, data, value_type (), false);
        }
        BOOST_UBLAS_INLINE
        void resize (size_type size, pointer data, value_type init) {
            resize_internal (size, data, init, true);
        }

        BOOST_UBLAS_INLINE
        size_type size () const {
            return size_;
        }

        // Element access
        BOOST_UBLAS_INLINE
        const_reference operator [] (size_type i) const {
            BOOST_UBLAS_CHECK (i < size_, bad_index ());
            return data_ [i];
        }
        BOOST_UBLAS_INLINE
        reference operator [] (size_type i) {
            BOOST_UBLAS_CHECK (i < size_, bad_index ());
            return data_ [i];
        }

        // Assignment
        BOOST_UBLAS_INLINE
        array_adaptor &operator = (const array_adaptor &a) {
            if (this != &a) {
                resize (a.size_);
                std::copy (a.data_, a.data_ + a.size_, data_);
            }
            return *this;
        }
        BOOST_UBLAS_INLINE
        array_adaptor &assign_temporary (array_adaptor &a) {
            if (own_ && a.own_)
                swap (a);
            else
                *this = a;
            return *this;
        }

        // Swapping
        BOOST_UBLAS_INLINE
        void swap (array_adaptor &a) {
            if (this != &a) {
                std::swap (size_, a.size_);
                std::swap (own_, a.own_);
                std::swap (data_, a.data_);
            }
        }
#ifndef BOOST_UBLAS_NO_MEMBER_FRIENDS
        BOOST_UBLAS_INLINE
        friend void swap (array_adaptor &a1, array_adaptor &a2) {
            a1.swap (a2);
        }
#endif

        // Iterators simply are pointers.

        typedef const_pointer const_iterator;

        BOOST_UBLAS_INLINE
        const_iterator begin () const {
            return data_;
        }
        BOOST_UBLAS_INLINE
        const_iterator end () const {
            return data_ + size_;
        }

        typedef pointer iterator;

        BOOST_UBLAS_INLINE
        iterator begin () {
            return data_;
        }
        BOOST_UBLAS_INLINE
        iterator end () {
            return data_ + size_;
        }

        // Reverse iterators

#ifdef BOOST_MSVC_STD_ITERATOR
        typedef std::reverse_iterator<const_iterator, value_type, const_reference> const_reverse_iterator;
#else
        typedef std::reverse_iterator<const_iterator> const_reverse_iterator;
#endif

        BOOST_UBLAS_INLINE
        const_reverse_iterator rbegin () const {
            return const_reverse_iterator (end ());
        }
        BOOST_UBLAS_INLINE
        const_reverse_iterator rend () const {
            return const_reverse_iterator (begin ());
        }

#ifdef BOOST_MSVC_STD_ITERATOR
        typedef std::reverse_iterator<iterator, value_type, reference> reverse_iterator;
#else
        typedef std::reverse_iterator<iterator> reverse_iterator;
#endif

        BOOST_UBLAS_INLINE
        reverse_iterator rbegin () {
            return reverse_iterator (end ());
        }
        BOOST_UBLAS_INLINE
        reverse_iterator rend () {
            return reverse_iterator (begin ());
        }

    private:
        size_type size_;
        bool own_;
        pointer data_;
    };

#ifdef BOOST_UBLAS_SHALLOW_ARRAY_ADAPTOR
    // Array adaptor with shallow (reference) copy semantics of elements.
    // shared_array are used maitain reference counting.
    // This class breaks the normal copy semantics for a storage container and is very dangerous!
    template<class T>
    class shallow_array_adaptor:
        public storage_array<shallow_array_adaptor<T> > {

        template<class T>
        struct leaker {
            typedef void result_type;
            typedef T *argument_type;

            BOOST_UBLAS_INLINE
            result_type operator () (argument_type x) {}
        };
    public:
        typedef std::size_t size_type;
        typedef std::ptrdiff_t difference_type;
        typedef T value_type;
        typedef const T &const_reference;
        typedef T &reference;
        typedef const T *const_pointer;
        typedef T *pointer;
    private:
        typedef shallow_array_adaptor<T> self_type;

    public:
        // Construction and destruction
        BOOST_UBLAS_INLINE
        shallow_array_adaptor ():
            size_ (0), own_ (true), data_ (new value_type [0]) {
        }
        explicit BOOST_UBLAS_INLINE
        shallow_array_adaptor (size_type size):
            size_ (size), own_ (true), data_ (new value_type [size]) {
        }
        BOOST_UBLAS_INLINE
        shallow_array_adaptor (size_type size, const value_type &init):
            size_ (size), own_ (true), data_ (new value_type [size]) {
            std::fill (data_.get (), data_.get () + size_, init);
        }
        BOOST_UBLAS_INLINE
        shallow_array_adaptor (size_type size, pointer data):
            size_ (size), own_ (false), data_ (data, leaker<value_type> ()) {}

        BOOST_UBLAS_INLINE
        shallow_array_adaptor (const shallow_array_adaptor &a):
            storage_array<self_type> (),
            size_ (a.size_), own_ (a.own_), data_ (a.data_) {}

        BOOST_UBLAS_INLINE
        ~shallow_array_adaptor () {
        }

        // Resizing
    private:
        BOOST_UBLAS_INLINE
        void resize_internal (size_type size, value_type init, bool preserve = true) {
            if (size != size_) {
                shared_array<value_type> data (new value_type [size]);
                if (preserve) {
                    std::copy (data_.get (), data_.get () + (std::min) (size, size_), data.get ());
                    std::fill (data.get () + (std::min) (size, size_), data.get () + size, init);
                }
                size_ = size;
                data_ = data;
            }
        }
        BOOST_UBLAS_INLINE
        void resize_internal (size_type size, pointer data, value_type init, bool preserve = true) {
            if (preserve) {
                std::copy (data_.get (), data_.get () + (std::min) (size, size_), data);
                std::fill (data + (std::min) (size, size_), data + size, init);
            }
            size_ = size;
            data_ = data;
        }
    public:
        BOOST_UBLAS_INLINE
        void resize (size_type size) {
            resize_internal (size, value_type (), false);
        }
        BOOST_UBLAS_INLINE
        void resize (size_type size, value_type init) {
            resize_internal (size, init, true);
        }
        BOOST_UBLAS_INLINE
        void resize (size_type size, pointer data) {
            resize_internal (size, data, value_type (), false);
        }
        BOOST_UBLAS_INLINE
        void resize (size_type size, pointer data, value_type init) {
            resize_internal (size, data, init, true);
        }

        BOOST_UBLAS_INLINE
        size_type size () const {
            return size_;
        }

        // Element access
        BOOST_UBLAS_INLINE
        const_reference operator [] (size_type i) const {
            BOOST_UBLAS_CHECK (i < size_, bad_index ());
            return data_ [i];
        }
        BOOST_UBLAS_INLINE
        reference operator [] (size_type i) {
            BOOST_UBLAS_CHECK (i < size_, bad_index ());
            return data_ [i];
        }

        // Assignment
        BOOST_UBLAS_INLINE
        shallow_array_adaptor &operator = (const shallow_array_adaptor &a) {
            if (this != &a) {
                resize (a.size_);
                std::copy (a.data_.get (), a.data_.get () + a.size_, data_.get ());
            }
            return *this;
        }
        BOOST_UBLAS_INLINE
        shallow_array_adaptor &assign_temporary (shallow_array_adaptor &a) {
            if (own_ && a.own_)
                swap (a);
            else
                *this = a;
            return *this;
        }

        // Swapping
        BOOST_UBLAS_INLINE
        void swap (shallow_array_adaptor &a) {
            if (this != &a) {
                std::swap (size_, a.size_);
                std::swap (own_, a.own_);
                std::swap (data_, a.data_);
            }
        }
#ifndef BOOST_UBLAS_NO_MEMBER_FRIENDS
        BOOST_UBLAS_INLINE
        friend void swap (shallow_array_adaptor &a1, shallow_array_adaptor &a2) {
            a1.swap (a2);
        }
#endif

        // Iterators simply are pointers.

        typedef const_pointer const_iterator;

        BOOST_UBLAS_INLINE
        const_iterator begin () const {
            return data_.get ();
        }
        BOOST_UBLAS_INLINE
        const_iterator end () const {
            return data_.get () + size_;
        }

        typedef pointer iterator;

        BOOST_UBLAS_INLINE
        iterator begin () {
            return data_.get ();
        }
        BOOST_UBLAS_INLINE
        iterator end () {
            return data_.get () + size_;
        }

        // Reverse iterators

#ifdef BOOST_MSVC_STD_ITERATOR
        typedef std::reverse_iterator<const_iterator, value_type, const_reference> const_reverse_iterator;
#else
        typedef std::reverse_iterator<const_iterator> const_reverse_iterator;
#endif

        BOOST_UBLAS_INLINE
        const_reverse_iterator rbegin () const {
            return const_reverse_iterator (end ());
        }
        BOOST_UBLAS_INLINE
        const_reverse_iterator rend () const {
            return const_reverse_iterator (begin ());
        }

#ifdef BOOST_MSVC_STD_ITERATOR
        typedef std::reverse_iterator<iterator, value_type, reference> reverse_iterator;
#else
        typedef std::reverse_iterator<iterator> reverse_iterator;
#endif

        BOOST_UBLAS_INLINE
        reverse_iterator rbegin () {
            return reverse_iterator (end ());
        }
        BOOST_UBLAS_INLINE
        reverse_iterator rend () {
            return reverse_iterator (begin ());
        }

    private:
        size_type size_;
        bool own_;
        shared_array<value_type> data_;
    };

#endif

    // Range class
    template <class I, class D>
    class basic_range {
    public:
        typedef I size_type;
        typedef D difference_type;
        typedef size_type value_type;
        typedef value_type const_reference;
        typedef const_reference reference;
        typedef const value_type *const_pointer;
        typedef value_type *pointer;
    private:
        typedef basic_range<I, D> self_type;

    public:
        // Construction and destruction
        BOOST_UBLAS_INLINE
        basic_range ():
            start_ (0), size_ (0) {}
        BOOST_UBLAS_INLINE
        basic_range (size_type start, size_type stop):
            start_ (start), size_ (stop - start) {
            BOOST_UBLAS_CHECK (start_ <= stop, bad_index ());
        }

        BOOST_UBLAS_INLINE
        size_type start () const {
            return start_;
        }
        BOOST_UBLAS_INLINE
        size_type size () const {
            return size_;
        }

        // Element access
        BOOST_UBLAS_INLINE
        const_reference operator () (size_type i) const {
            BOOST_UBLAS_CHECK (i < size_, bad_index ());
            return start_ + i;
        }

        // Composition
        BOOST_UBLAS_INLINE
        basic_range compose (const basic_range &r) const {
            return basic_range (start_ + r.start_, start_ + r.start_ + r.size_);
        }

        // Comparison
        BOOST_UBLAS_INLINE
        bool operator == (const basic_range &r) const {
            return start_ == r.start_ && size_ == r.size_;
        }
        BOOST_UBLAS_INLINE
        bool operator != (const basic_range &r) const {
            return ! (*this == r);
        }

        // Iterator types
    private:
        // Use and index
        typedef size_type const_iterator_type;

    public:
#ifdef BOOST_UBLAS_USE_INDEXED_ITERATOR
        typedef indexed_const_iterator<self_type, std::random_access_iterator_tag> const_iterator;
#else
        class const_iterator:
            public container_const_reference<basic_range>,
            public random_access_iterator_base<std::random_access_iterator_tag,
                                               const_iterator, value_type> {
        public:
#ifdef BOOST_MSVC_STD_ITERATOR
            typedef const_reference reference;
#else
            typedef typename basic_range::value_type value_type;
            typedef typename basic_range::difference_type difference_type;
            typedef typename basic_range::const_reference reference;
            typedef typename basic_range::const_pointer pointer;
#endif

            // Construction and destruction
            BOOST_UBLAS_INLINE
            const_iterator ():
                container_const_reference<basic_range> (), it_ () {}
            BOOST_UBLAS_INLINE
            const_iterator (const basic_range &r, const const_iterator_type &it):
                container_const_reference<basic_range> (r), it_ (it) {}

            // Arithmetic
            BOOST_UBLAS_INLINE
            const_iterator &operator ++ () {
                ++ it_;
                return *this;
            }
            BOOST_UBLAS_INLINE
            const_iterator &operator -- () {
                BOOST_UBLAS_CHECK (it_ > 0, bad_index ());
                -- it_;
                return *this;
            }
            BOOST_UBLAS_INLINE
            const_iterator &operator += (difference_type n) {
                BOOST_UBLAS_CHECK (n >= 0 || it_ >= size_type(-n), bad_index ());
                it_ += n;
                return *this;
            }
            BOOST_UBLAS_INLINE
            const_iterator &operator -= (difference_type n) {
                BOOST_UBLAS_CHECK (n <= 0 || it_ >= size_type(n), bad_index ());
                it_ -= n;
                return *this;
            }
            BOOST_UBLAS_INLINE
            difference_type operator - (const const_iterator &it) const {
                return it_ - it.it_;
            }

            // Dereference
            BOOST_UBLAS_INLINE
            const_reference operator * () const {
                BOOST_UBLAS_CHECK ((*this) ().start () <= it_, bad_index ());
                BOOST_UBLAS_CHECK (it_ < (*this) ().start () + (*this) ().size (), bad_index ());
                return it_;
            }

            // Index
            BOOST_UBLAS_INLINE
            size_type index () const {
                BOOST_UBLAS_CHECK ((*this) ().start () <= it_, bad_index ());
                BOOST_UBLAS_CHECK (it_ < (*this) ().start () + (*this) ().size (), bad_index ());
                return it_ - (*this) ().start ();
            }

            // Assignment
            BOOST_UBLAS_INLINE
            const_iterator &operator = (const const_iterator &it) {
                // Comeau recommends...
                this->assign (&it ());
                it_ = it.it_;
                return *this;
            }

            // Comparison
            BOOST_UBLAS_INLINE
            bool operator == (const const_iterator &it) const {
                BOOST_UBLAS_CHECK ((*this) () == it (), external_logic ());
                return it_ == it.it_;
            }
            BOOST_UBLAS_INLINE
            bool operator < (const const_iterator &it) const {
                BOOST_UBLAS_CHECK ((*this) () == it (), external_logic ());
                return it_ < it.it_;
            }

        private:
            const_iterator_type it_;
        };
#endif

        BOOST_UBLAS_INLINE
        const_iterator begin () const {
            return const_iterator (*this, start_);
        }
        BOOST_UBLAS_INLINE
        const_iterator end () const {
            return const_iterator (*this, start_ + size_);
        }

        // Reverse iterator

#ifdef BOOST_MSVC_STD_ITERATOR
        typedef std::reverse_iterator<const_iterator, value_type, const_reference> const_reverse_iterator;
#else
        typedef std::reverse_iterator<const_iterator> const_reverse_iterator;
#endif

        BOOST_UBLAS_INLINE
        const_reverse_iterator rbegin () const {
            return const_reverse_iterator (end ());
        }
        BOOST_UBLAS_INLINE
        const_reverse_iterator rend () const {
            return const_reverse_iterator (begin ());
        }

        BOOST_UBLAS_INLINE
        basic_range preprocess (size_type size) const {
            if (*this != all ())
                return *this;
            return basic_range (0, size);
        }
        static
        BOOST_UBLAS_INLINE
        basic_range all () {
            return basic_range (0, size_type (-1));
        }

    private:
        size_type start_;
        size_type size_;
    };

    // Slice class
    template <class I, class D>
    class basic_slice {
    public:
        typedef I size_type;
        typedef D difference_type;
        typedef size_type value_type;
        typedef value_type const_reference;
        typedef const_reference reference;
        typedef const value_type *const_pointer;
        typedef value_type *pointer;
    private:
        typedef basic_slice<I, D> self_type;

    public:
        // Construction and destruction
        BOOST_UBLAS_INLINE
        basic_slice ():
            start_ (0), stride_ (0), size_ (0) {}
        BOOST_UBLAS_INLINE
        basic_slice (size_type start, difference_type stride, size_type size):
            start_ (start), stride_ (stride), size_ (size) {}

        BOOST_UBLAS_INLINE
        size_type start () const {
            return start_;
        }
        BOOST_UBLAS_INLINE
        difference_type stride () const {
            return stride_;
        }
        BOOST_UBLAS_INLINE
        size_type size () const {
            return size_;
        }

        // Element access
        BOOST_UBLAS_INLINE
        const_reference operator () (size_type i) const {
            BOOST_UBLAS_CHECK (i < size_, bad_index ());
            BOOST_UBLAS_CHECK (stride_ >= 0 || start_ >= i * -stride_, bad_index ());
            return start_ + i * stride_;
        }

        // Composition
        BOOST_UBLAS_INLINE
        basic_slice compose (const basic_range<size_type, difference_type> &r) const {
            BOOST_UBLAS_CHECK (stride_ >=0 || start_ >= -stride_ * r.start(), bad_index ());
            return basic_slice (start_ + stride_ * r.start (), stride_, r.size ());
        }
        BOOST_UBLAS_INLINE
        basic_slice compose (const basic_slice &s) const {
            BOOST_UBLAS_CHECK (stride_ >=0 || start_ >= -stride_ * s.start_, bad_index ());
            return basic_slice (start_ + stride_ * s.start_, stride_ * s.stride_, s.size_);
        }

        // Comparison
        BOOST_UBLAS_INLINE
        bool operator == (const basic_slice &s) const {
            return start_ == s.start_ && stride_ == s.stride_ && size_ == s.size_;
        }
        BOOST_UBLAS_INLINE
        bool operator != (const basic_slice &s) const {
            return ! (*this == s);
        }

        // Iterator types
    private:
        // Use and index
        typedef size_type const_iterator_type;

    public:
#ifdef BOOST_UBLAS_USE_INDEXED_ITERATOR
        typedef indexed_const_iterator<self_type, std::random_access_iterator_tag> const_iterator;
#else
        class const_iterator:
            public container_const_reference<basic_slice>,
            public random_access_iterator_base<std::random_access_iterator_tag,
                                               const_iterator, value_type> {
        public:
#ifdef BOOST_MSVC_STD_ITERATOR
            typedef const_reference reference;
#else
            typedef typename basic_slice::value_type value_type;
            typedef typename basic_slice::difference_type difference_type;
            typedef typename basic_slice::const_reference reference;
            typedef typename basic_slice::const_pointer pointer;
#endif

            // Construction and destruction
            BOOST_UBLAS_INLINE
            const_iterator ():
                container_const_reference<basic_slice> (), it_ () {}
            BOOST_UBLAS_INLINE
            const_iterator (const basic_slice &s, const const_iterator_type &it):
                container_const_reference<basic_slice> (s), it_ (it) {}

            // Arithmetic
            BOOST_UBLAS_INLINE
            const_iterator &operator ++ () {
                ++it_;
                return *this;
            }
            BOOST_UBLAS_INLINE
            const_iterator &operator -- () {
                BOOST_UBLAS_CHECK (it_ > 0, bad_index ());
                --it_;
                return *this;
            }
            BOOST_UBLAS_INLINE
            const_iterator &operator += (difference_type n) {
                BOOST_UBLAS_CHECK (n >= 0 || it_ >= size_type(-n), bad_index ());
                it_ += n;
                return *this;
            }
            BOOST_UBLAS_INLINE
            const_iterator &operator -= (difference_type n) {
                BOOST_UBLAS_CHECK (n <= 0 || it_ >= size_type(n), bad_index ());
                it_ -= n;
                return *this;
            }
            BOOST_UBLAS_INLINE
            difference_type operator - (const const_iterator &it) const {
                return it_ - it.it_;
            }

            // Dereference
            BOOST_UBLAS_INLINE
            const_reference operator * () const {
                BOOST_UBLAS_CHECK (it_ < (*this) ().size (), bad_index ());
                return (*this) ().start () + it_* (*this) ().stride ();
            }

            // Index
            BOOST_UBLAS_INLINE
            size_type index () const {
                BOOST_UBLAS_CHECK (it_ < (*this) ().size (), bad_index ());
                return it_;
            }

            // Assignment
            BOOST_UBLAS_INLINE
            const_iterator &operator = (const const_iterator &it) {
                // Comeau recommends...
                this->assign (&it ());
                it_ = it.it_;
                return *this;
            }

            // Comparison
            BOOST_UBLAS_INLINE
            bool operator == (const const_iterator &it) const {
                BOOST_UBLAS_CHECK ((*this) () == it (), external_logic ());
                return it_ == it.it_;
            }
            BOOST_UBLAS_INLINE
            bool operator < (const const_iterator &it) const {
                BOOST_UBLAS_CHECK ((*this) () == it (), external_logic ());
                return it_ < it.it_;
            }

        private:
            const_iterator_type it_;
        };
#endif

        BOOST_UBLAS_INLINE
        const_iterator begin () const {
            return const_iterator (*this, 0);
        }
        BOOST_UBLAS_INLINE
        const_iterator end () const {
            return const_iterator (*this, size_);
        }

        // Reverse iterator

#ifdef BOOST_MSVC_STD_ITERATOR
        typedef std::reverse_iterator<const_iterator, value_type, const_reference> const_reverse_iterator;
#else
        typedef std::reverse_iterator<const_iterator> const_reverse_iterator;
#endif

        BOOST_UBLAS_INLINE
        const_reverse_iterator rbegin () const {
            return const_reverse_iterator (end ());
        }
        BOOST_UBLAS_INLINE
        const_reverse_iterator rend () const {
            return const_reverse_iterator (begin ());
        }

        BOOST_UBLAS_INLINE
        basic_slice preprocess (size_type size) const {
            if (*this != all ())
                return *this;
            return basic_slice (0, 1, size);
        }
        static
        BOOST_UBLAS_INLINE
        basic_slice all () {
            return basic_slice (0, 1, size_type (-1));
        }

    private:
        size_type start_;
        difference_type stride_;
        size_type size_;
    };

    // Indirect array class
    template<class A>
    class indirect_array {
    public:
        typedef A array_type;
        typedef const A const_array_type;
        typedef typename A::size_type size_type;
        typedef typename A::difference_type difference_type;
        typedef typename A::value_type value_type;
        typedef typename A::const_reference const_reference;
        typedef typename A::reference reference;
        typedef typename A::const_pointer const_pointer;
        typedef typename A::pointer pointer;
    private:
        typedef indirect_array<A> self_type;

    public:
        // Construction and destruction
        BOOST_UBLAS_INLINE
        indirect_array ():
            size_ (), data_ () {}
        explicit BOOST_UBLAS_INLINE
        indirect_array (size_type size):
            size_ (size), data_ (size) {}
        BOOST_UBLAS_INLINE
        indirect_array (size_type size, const array_type &data):
            size_ (size), data_ (data) {}
        BOOST_UBLAS_INLINE
        indirect_array (pointer start, pointer stop):
            size_ (stop - start), data_ (stop - start) {
            std::copy (start, stop, data_.begin ());
        }

        BOOST_UBLAS_INLINE
        size_type size () const {
            return size_;
        }
        BOOST_UBLAS_INLINE
        const_array_type data () const {
            return data_;
        }
        BOOST_UBLAS_INLINE
        array_type data () {
            return data_;
        }

        // Element access
        BOOST_UBLAS_INLINE
        const_reference operator () (size_type i) const {
            BOOST_UBLAS_CHECK (i < size_, bad_index ());
            return data_ [i];
        }
        BOOST_UBLAS_INLINE
        reference operator () (size_type i) {
            BOOST_UBLAS_CHECK (i < size_, bad_index ());
            return data_ [i];
        }

        BOOST_UBLAS_INLINE
        const_reference operator [] (size_type i) const {
            return (*this) (i);
        }
        BOOST_UBLAS_INLINE
        reference operator [] (size_type i) {
            return (*this) (i);
        }

        // Composition
        BOOST_UBLAS_INLINE
        indirect_array compose (const basic_range<size_type, difference_type> &r) const {
            BOOST_UBLAS_CHECK (r.start () + r.size () <= size_, bad_size ());
            array_type data (r.size ());
            for (size_type i = 0; i < r.size (); ++ i)
                data [i] = data_ [r.start () + i];
            return indirect_array (r.size (), data);
        }
        BOOST_UBLAS_INLINE
        indirect_array compose (const basic_slice<size_type, difference_type> &s) const {
            BOOST_UBLAS_CHECK (s.start () + s.stride () * (s.size () - (s.size () > 0)) <= size (), bad_size ());
            array_type data (s.size ());
            for (size_type i = 0; i < s.size (); ++ i)
                data [i] = data_ [s.start () + s.stride () * i];
            return indirect_array (s.size (), data);
        }
        BOOST_UBLAS_INLINE
        indirect_array compose (const indirect_array &ia) const {
            array_type data (ia.size_);
            for (size_type i = 0; i < ia.size_; ++ i) {
                BOOST_UBLAS_CHECK (ia.data_ [i] <= size_, bad_size ());
                data [i] = data_ [ia.data_ [i]];
            }
            return indirect_array (ia.size_, data);
        }

        // Comparison
        template<class OA>
        BOOST_UBLAS_INLINE
        bool operator == (const indirect_array<OA> &ia) const {
            if (size_ != ia.size_)
                return false;
            for (size_type i = 0; i < BOOST_UBLAS_SAME (size_, ia.size_); ++ i)
                if (data_ [i] != ia.data_ [i])
                    return false;
            return true;
        }
        template<class OA>
        BOOST_UBLAS_INLINE
        bool operator != (const indirect_array<OA> &ia) const {
            return ! (*this == ia);
        }

        // Iterator types
    private:
        // Use a index difference
        typedef difference_type const_iterator_type;

    public:
#ifdef BOOST_UBLAS_USE_INDEXED_ITERATOR
        typedef indexed_const_iterator<indirect_array, std::random_access_iterator_tag> const_iterator;
#else
        class const_iterator:
            public container_const_reference<indirect_array>,
            public random_access_iterator_base<std::random_access_iterator_tag,
                                               const_iterator, value_type> {
        public:
#ifdef BOOST_MSVC_STD_ITERATOR
            typedef const_reference reference;
#else
            typedef typename indirect_array::value_type value_type;
            typedef typename indirect_array::difference_type difference_type;
            typedef typename indirect_array::const_reference reference;
            typedef typename indirect_array::const_pointer pointer;
#endif

            // Construction and destruction
            BOOST_UBLAS_INLINE
            const_iterator ():
                container_const_reference<indirect_array> (), it_ () {}
            BOOST_UBLAS_INLINE
            const_iterator (const indirect_array &ia, const const_iterator_type &it):
                container_const_reference<indirect_array> (ia), it_ (it) {}

            // Arithmetic
            BOOST_UBLAS_INLINE
            const_iterator &operator ++ () {
                ++ it_;
                return *this;
            }
            BOOST_UBLAS_INLINE
            const_iterator &operator -- () {
                -- it_;
                return *this;
            }
            BOOST_UBLAS_INLINE
            const_iterator &operator += (difference_type n) {
                it_ += n;
                return *this;
            }
            BOOST_UBLAS_INLINE
            const_iterator &operator -= (difference_type n) {
                it_ -= n;
                return *this;
            }
            BOOST_UBLAS_INLINE
            difference_type operator - (const const_iterator &it) const {
                return it_ - it.it_;
            }

            // Dereference
            BOOST_UBLAS_INLINE
            const_reference operator * () const {
                return (*this) () (it_);
            }

            // Index
            BOOST_UBLAS_INLINE
            size_type index () const {
                return it_;
            }

            // Assignment
            BOOST_UBLAS_INLINE
            const_iterator &operator = (const const_iterator &it) {
                // Comeau recommends...
                this->assign (&it ());
                it_ = it.it_;
                return *this;
            }

            // Comparison
            BOOST_UBLAS_INLINE
            bool operator == (const const_iterator &it) const {
                BOOST_UBLAS_CHECK ((*this) () == it (), external_logic ());
                return it_ == it.it_;
            }
            BOOST_UBLAS_INLINE
            bool operator < (const const_iterator &it) const {
                BOOST_UBLAS_CHECK ((*this) () == it (), external_logic ());
                return it_ < it.it_;
            }

        private:
            const_iterator_type it_;
        };
#endif

        BOOST_UBLAS_INLINE
        const_iterator begin () const {
            return const_iterator (*this, 0);
        }
        BOOST_UBLAS_INLINE
        const_iterator end () const {
            return const_iterator (*this, size_);
        }

        // Reverse iterator

#ifdef BOOST_MSVC_STD_ITERATOR
        typedef std::reverse_iterator<const_iterator, value_type, const_reference> const_reverse_iterator;
#else
        typedef std::reverse_iterator<const_iterator> const_reverse_iterator;
#endif

        BOOST_UBLAS_INLINE
        const_reverse_iterator rbegin () const {
            return const_reverse_iterator (end ());
        }
        BOOST_UBLAS_INLINE
        const_reverse_iterator rend () const {
            return const_reverse_iterator (begin ());
        }

        BOOST_UBLAS_INLINE
        indirect_array preprocess (size_type size) const {
            if (*this != all ())
                return *this;
            indirect_array ia (size);
            for (size_type i = 0; i < size; ++ i)
               ia (i) = i;
            return ia;
        }
        static
        BOOST_UBLAS_INLINE
        const indirect_array &all () {
            return all_;
        }

    private:
        size_type size_;
        array_type data_;
        static const indirect_array all_;
    };

    template<class A>
    const indirect_array<A> indirect_array<A>::all_;



    // Gunter Winkler contributed the classes index_pair, index_pair_array,
    // index_triple and index_triple_array to enable inplace sort of parallel arrays.

    template <class V>
    class index_pair :
        private boost::noncopyable,
        public container_reference<V> {
    public:
        typedef index_pair<V> self_type;
        typedef typename V::size_type size_type;

        BOOST_UBLAS_INLINE
        index_pair(V& v, size_type i) :
            container_reference<V>(v), i_(i),
            v1_(v.data1_[i]), v2_(v.data2_[i]), dirty_(false) {}
        BOOST_UBLAS_INLINE
        index_pair(const self_type& rhs) :
            container_reference<V>(rhs()), i_(rhs.i_),
            v1_(rhs.v1_), v2_(rhs.v2_), dirty_(false) {}
        BOOST_UBLAS_INLINE
        ~index_pair() {
            if (dirty_) {
                (*this)().data1_[i_] = v1_;
                (*this)().data2_[i_] = v2_;
            }
        }

        BOOST_UBLAS_INLINE
        self_type& operator=(const self_type& rhs) {
            v1_ = rhs.v1_;
            v2_ = rhs.v2_;
            dirty_ = true;
            return *this;
        }

        BOOST_UBLAS_INLINE
        void swap(self_type rhs) {
            self_type tmp(rhs);
            rhs = *this;
            *this = tmp;
        }
#ifndef BOOST_UBLAS_NO_MEMBER_FRIENDS
        BOOST_UBLAS_INLINE
        friend void swap(self_type lhs, self_type rhs) {
            lhs.swap(rhs);
        }
#endif

        BOOST_UBLAS_INLINE
        bool equal(const self_type& rhs) const {
            return (v1_ == rhs.v1_);
        }
        bool less(const self_type& rhs) const {
            return (v1_ < rhs.v1_);
        }
#ifndef BOOST_UBLAS_NO_MEMBER_FRIENDS
        BOOST_UBLAS_INLINE
        friend bool operator == (const self_type& lhs, const self_type& rhs) {
            return lhs.equal(rhs);
        }
        BOOST_UBLAS_INLINE
        friend bool operator != (const self_type& lhs, const self_type& rhs) {
            return !lhs.equal(rhs);
        }
        BOOST_UBLAS_INLINE
        friend bool operator < (const self_type& lhs, const self_type& rhs) {
            return lhs.less(rhs);
        }
#endif

    private:
        size_type i_;
        typename V::value1_type v1_;
        typename V::value2_type v2_;
        bool dirty_;
    };

#ifdef BOOST_UBLAS_NO_MEMBER_FRIENDS
    template<class V>
    BOOST_UBLAS_INLINE
    void swap(index_pair<V> lhs, index_pair<V> rhs) {
        lhs.swap(rhs);
    }

    template<class V>
    BOOST_UBLAS_INLINE
    bool operator == (const index_pair<V>& lhs, const index_pair<V>& rhs) {
        return lhs.equal(rhs);
    }
    template<class V>
    BOOST_UBLAS_INLINE
    bool operator != (const index_pair<V>& lhs, const index_pair<V>& rhs) {
        return !lhs.equal(rhs);
    }
    template<class V>
    BOOST_UBLAS_INLINE
    bool operator < (const index_pair<V>& lhs, const index_pair<V>& rhs) {
        return lhs.less(rhs);
    }
#endif

    template <class V1, class V2>
    class index_pair_array:
        private boost::noncopyable {
    public:
        typedef index_pair_array<V1, V2> self_type;
        typedef typename V1::value_type value1_type;
        typedef typename V2::value_type value2_type;

        typedef typename V1::size_type size_type;
        typedef typename V1::difference_type difference_type;
        typedef index_pair<self_type> value_type;
        // There is nothing that can be referenced directly. Always return a copy of the index_pair
        typedef value_type reference;
        typedef const value_type const_reference;

        BOOST_UBLAS_INLINE
        index_pair_array(size_type size, V1& data1, V2& data2) :
              size_(size),data1_(data1),data2_(data2) {}

        BOOST_UBLAS_INLINE
        size_type size() const {
            return size_;
        }

        BOOST_UBLAS_INLINE
        const_reference operator () (size_type i) const {
            return value_type((*this), i);
        }
        BOOST_UBLAS_INLINE
        reference operator () (size_type i) {
            return value_type((*this), i);
        }

        typedef indexed_iterator<self_type, std::random_access_iterator_tag> iterator;
        typedef indexed_const_iterator<self_type, std::random_access_iterator_tag> const_iterator;

        BOOST_UBLAS_INLINE
        iterator begin() {
            return iterator( (*this), 0);
        }
        BOOST_UBLAS_INLINE
        iterator end() {
            return iterator( (*this), size());
        }

        BOOST_UBLAS_INLINE
        const_iterator begin() const {
            return const_iterator( (*this), 0);
        }
        BOOST_UBLAS_INLINE
        const_iterator end() const {
            return const_iterator( (*this), size());
        }

        // unnecessary function:
        BOOST_UBLAS_INLINE
        bool equal(size_type i1, size_type i2) const {
            return data1_[i1] == data1_[i2];
        }
        BOOST_UBLAS_INLINE
        bool less(size_type i1, size_type i2) const {
            return data1_[i1] < data1_[i2];
        }

        // gives a large speedup
        BOOST_UBLAS_INLINE
        friend void iter_swap(const iterator& lhs, const iterator& rhs) {
            const size_type i1 = lhs.index();
            const size_type i2 = rhs.index();
            std::swap(lhs().data1_[i1], rhs().data1_[i2]);
            std::swap(lhs().data2_[i1], rhs().data2_[i2]);
        }

    private:
        size_type size_;
        V1& data1_;
        V2& data2_;

        // friend class value_type;
        friend class index_pair<self_type>;
    };

    template <class M>
    class index_triple :
        private boost::noncopyable,
        public container_reference<M> {
    public:
        typedef index_triple<M> self_type;
        typedef typename M::size_type size_type;

        BOOST_UBLAS_INLINE
        index_triple(M& m, size_type i) :
            container_reference<M>(m), i_(i),
            v1_(m.data1_[i]), v2_(m.data2_[i]), v3_(m.data3_[i]), dirty_(false) {}
        BOOST_UBLAS_INLINE
        index_triple(const self_type& rhs) :
            container_reference<M>(rhs()), i_(rhs.i_),
            v1_(rhs.v1_), v2_(rhs.v2_), v3_(rhs.v3_), dirty_(false) {}
        BOOST_UBLAS_INLINE
        ~index_triple() {
            if (dirty_) {
                (*this)().data1_[i_] = v1_;
                (*this)().data2_[i_] = v2_;
                (*this)().data3_[i_] = v3_;
            }
        }

        BOOST_UBLAS_INLINE
        self_type& operator=(const self_type& rhs) {
            v1_ = rhs.v1_;
            v2_ = rhs.v2_;
            v3_ = rhs.v3_;
            dirty_ = true;
            return *this;
        }

        BOOST_UBLAS_INLINE
        void swap(self_type rhs) {
            self_type tmp(rhs);
            rhs = *this;
            *this = tmp;
        }
#ifndef BOOST_UBLAS_NO_MEMBER_FRIENDS
        BOOST_UBLAS_INLINE
        friend void swap(self_type lhs, self_type rhs) {
            lhs.swap(rhs);
        }
#endif

        BOOST_UBLAS_INLINE
        bool equal(const self_type& rhs) const {
            return ((v1_ == rhs.v1_) && (v2_ == rhs.v2_));
        }
        BOOST_UBLAS_INLINE
        bool less(const self_type& rhs) const {
            return ((v1_ < rhs.v1_) ||
                    (v1_ == rhs.v1_ && v2_ < rhs.v2_));
        }
#ifndef BOOST_UBLAS_NO_MEMBER_FRIENDS
        BOOST_UBLAS_INLINE
        friend bool operator == (const self_type& lhs, const self_type& rhs) {
            return lhs.equal(rhs);
        }
        BOOST_UBLAS_INLINE
        friend bool operator != (const self_type& lhs, const self_type& rhs) {
            return !lhs.equal(rhs);
        }
        BOOST_UBLAS_INLINE
        friend bool operator < (const self_type& lhs, const self_type& rhs) {
            return lhs.less(rhs);
        }
#endif

    private:
        size_type i_;
        typename M::value1_type v1_;
        typename M::value2_type v2_;
        typename M::value3_type v3_;
        bool dirty_;
    };

#ifdef BOOST_UBLAS_NO_MEMBER_FRIENDS
    template<class M>
    BOOST_UBLAS_INLINE
    void swap(index_triple<M> lhs, index_triple<M> rhs) {
        lhs.swap(rhs);
    }

    template<class M>
    BOOST_UBLAS_INLINE
    bool operator == (const index_triple<M>& lhs, const index_triple<M>& rhs) {
        return lhs.equal(rhs);
    }
    template<class M>
    BOOST_UBLAS_INLINE
    bool operator != (const index_triple<M>& lhs, const index_triple<M>& rhs) {
        return !lhs.equal(rhs);
    }
    template<class M>
    BOOST_UBLAS_INLINE
    bool operator < (const index_triple<M>& lhs, const index_triple<M>& rhs) {
        return lhs.less(rhs);
    }
#endif

    template <class V1, class V2, class V3>
    class index_triple_array:
        private boost::noncopyable {
    public:
        typedef index_triple_array<V1, V2, V3> self_type;
        typedef typename V1::value_type value1_type;
        typedef typename V2::value_type value2_type;
        typedef typename V3::value_type value3_type;

        typedef typename V1::size_type size_type;
        typedef typename V1::difference_type difference_type;
        typedef index_triple<self_type> value_type;
        // There is nothing that can be referenced directly. Always return a copy of the index_triple
        typedef value_type reference;
        typedef const value_type const_reference;

        BOOST_UBLAS_INLINE
        index_triple_array(size_type size, V1& data1, V2& data2, V3& data3) :
              size_(size),data1_(data1),data2_(data2),data3_(data3) {}

        BOOST_UBLAS_INLINE
        size_type size() const {
            return size_;
        }

        BOOST_UBLAS_INLINE
        const_reference operator () (size_type i) const {
            return value_type((*this), i);
        }
        BOOST_UBLAS_INLINE
        reference operator () (size_type i) {
            return value_type((*this), i);
        }

        typedef indexed_iterator<self_type, std::random_access_iterator_tag> iterator;
        typedef indexed_const_iterator<self_type, std::random_access_iterator_tag> const_iterator;

        BOOST_UBLAS_INLINE
        iterator begin() {
            return iterator( (*this), 0);
        }
        BOOST_UBLAS_INLINE
        iterator end() {
            return iterator( (*this), size());
        }

        BOOST_UBLAS_INLINE
        const_iterator begin() const {
            return const_iterator( (*this), 0);
        }
        BOOST_UBLAS_INLINE
        const_iterator end() const {
            return const_iterator( (*this), size());
        }

        // unnecessary function:
        BOOST_UBLAS_INLINE
        bool equal(size_type i1, size_type i2) const {
            return ((data1_[i1] == data1_[i2]) && (data2_[i1] == data2_[i2]));
        }
        BOOST_UBLAS_INLINE
        bool less(size_type i1, size_type i2) const {
            return ((data1_[i1] < data1_[i2]) ||
                    (data1_[i1] == data1_[i2] && data2_[i1] < data2_[i2]));
        }

        // gives a large speedup
        BOOST_UBLAS_INLINE
        friend void iter_swap(const iterator& lhs, const iterator& rhs) {
            const size_type i1 = lhs.index();
            const size_type i2 = rhs.index();
            std::swap(lhs().data1_[i1], rhs().data1_[i2]);
            std::swap(lhs().data2_[i1], rhs().data2_[i2]);
            std::swap(lhs().data3_[i1], rhs().data3_[i2]);
        }

    private:
        size_type size_;
        V1& data1_;
        V2& data2_;
        V3& data3_;

        // friend class value_type;
        friend class index_triple<self_type>;
    };

}}}

#endif
