#ifndef  BOOST_SERIALIZATION_STRING_HPP
#define BOOST_SERIALIZATION_STRING_HPP

// MS compatible compilers support #pragma once
#if defined(_MSC_VER) && (_MSC_VER >= 1020)
# pragma once
#endif

/////////1/////////2/////////3/////////4/////////5/////////6/////////7/////////8
// serialization/string.hpp:
// serialization for stl string templates

// (C) Copyright 2002 Robert Ramey - http://www.rrsd.com .
// Use, modification and distribution is subject to the Boost Software
// License, Version 1.0. (See accompanying file LICENSE_1_0.txt or copy at
// http://www.boost.org/LICENSE_1_0.txt)

//  See http://www.boost.org for updates, documentation, and revision history.

#include <string>

#include <boost/config.hpp>
#include <boost/serialization/level.hpp>

BOOST_CLASS_IMPLEMENTATION(std::string, boost::serialization::primitive_type)
#ifndef BOOST_NO_STD_WSTRING
BOOST_CLASS_IMPLEMENTATION(std::wstring, boost::serialization::primitive_type)
#endif

// left over from a previous incarnation - strings are now always primitive types
#if 0
#include <string>
#include <boost/serialization/collections_save_imp.hpp>
#include <boost/serialization/collections_load_imp.hpp>
#include <boost/serialization/split_free.hpp>

// function specializations must be defined in the appropriate
// namespace - boost::serialization
#if defined(__SGI_STL_PORT) || defined(_STLPORT_VERSION)
#define STD _STLP_STD
#else
#define STD std
#endif

#ifdef BOOST_NO_ARGUMENT_DEPENDENT_LOOKUP
namespace boost { namespace serialization {
#else
namespace STD {
#endif

// basic_string - general case
template<class Archive, class U, class Allocator>
inline void save(
    Archive & ar,
    const STD::basic_string<U, Allocator> &t,
    const unsigned int file_version
){
    boost::serialization::stl::save_collection<
        Archive, STD::basic_string<U, Allocator>
    >(ar, t);
}

template<class Archive, class U, class Allocator>
inline void load(
    Archive & ar,
    STD::basic_string<U, Allocator> &t,
    const unsigned int file_version
){
    boost::serialization::stl::load_collection<
        Archive,
        STD::basic_string<U, Allocator>,
        boost::serialization::stl::archive_input_seq<
            Archive,
            STD::basic_string<U, Allocator>
        >,
        boost::serialization::stl::reserve_imp<
            STD::basic_string<U, Allocator>
        >
    >(ar, t);
}

// split non-intrusive serialization function member into separate
// non intrusive save/load member functions
template<class Archive, class U, class Allocator>
inline void serialize(
    Archive & ar,
    STD::basic_string<U, Allocator> & t,
    const unsigned int file_version
){
    boost::serialization::split_free(ar, t, file_version);
}

#ifdef BOOST_NO_ARGUMENT_DEPENDENT_LOOKUP
}} // namespace boost::serialization
#else
} // std
#endif

#include <boost/serialization/collection_traits.hpp>

BOOST_SERIALIZATION_COLLECTION_TRAITS(STD::vector)
#undef STD

#endif

#endif // BOOST_SERIALIZATION_STRING_HPP
