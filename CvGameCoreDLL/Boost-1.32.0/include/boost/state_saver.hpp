#ifndef BOOST_STATE_SAVER_HPP
#define BOOST_STATE_SAVER_HPP

// MS compatible compilers support #pragma once
#if defined(_MSC_VER) && (_MSC_VER >= 1020)
# pragma once
#endif

/////////1/////////2/////////3/////////4/////////5/////////6/////////7/////////8
// state_saver.hpp:

// (C) Copyright 2003-4 Pavel Vozenilek and Robert Ramey - http://www.rrsd.com.
// Use, modification and distribution is subject to the Boost Software
// License, Version 1.0. (See accompanying file LICENSE_1_0.txt or copy at
// http://www.boost.org/LICENSE_1_0.txt)

//  See http://www.boost.org for updates, documentation, and revision history.

// Inspired by Daryle Walker's iostate_saver concept.  This saves the original
// value of a variable when a state_saver is constructed and restores
// upon destruction.  Useful for being sure that state is restored to
// variables upon exit from scope.


#include <boost/config.hpp>
#ifndef BOOST_NO_EXCEPTIONS
    #include <exception>
#endif

#include <boost/call_traits.hpp>
#include <boost/noncopyable.hpp>
#include <boost/type_traits/has_nothrow_copy.hpp>

#include <boost/mpl/eval_if.hpp>
#include <boost/mpl/identity.hpp>

namespace boost {

template<class T>
// T requirements:
//  - POD or object semantic (cannot be reference, function, ...)
//  - copy constructor
//  - operator = (no-throw one preferred)
class state_saver : private boost::noncopyable
{
private:
    const T previous_value;
    T & previous_ref;

    struct restore {
        static void invoke(T & previous_ref, const T & previous_value){
            previous_ref = previous_value; // won't throw
        }
    };

    struct restore_with_exception {
        static void invoke(T & previous_ref, const T & previous_value){
            #ifndef BOOST_NO_EXCEPTIONS
                try{
                    previous_ref = previous_value;
                }
                catch(::std::exception &) {
                    // we must ignore it - we are in destructor
                }
            #else
                previous_ref = previous_value;
            #endif
        }
    };

public:
    state_saver(
        T & object
    ) :
        previous_value(object),
        previous_ref(object)
    {}

    ~state_saver() {
        typedef BOOST_DEDUCED_TYPENAME mpl::eval_if<
            has_nothrow_copy<T>,
            mpl::identity<restore>,
            mpl::identity<restore_with_exception>
        >::type typex;
        typex::invoke(previous_ref, previous_value);
    }

}; // state_saver<>

} // boost

#undef BOOST_TRY
#undef BOOST_CATCH

#endif //BOOST_STATE_SAVER_HPP
