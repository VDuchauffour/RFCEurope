#ifndef  BOOST_SERIALIZATION_VECTOR_HPP
#define BOOST_SERIALIZATION_VECTOR_HPP

// MS compatible compilers support #pragma once
#if defined(_MSC_VER) && (_MSC_VER >= 1020)
# pragma once
#endif

/////////1/////////2/////////3/////////4/////////5/////////6/////////7/////////8
// vector.hpp: serialization for stl vector templates

// (C) Copyright 2002 Robert Ramey - http://www.rrsd.com .
// Use, modification and distribution is subject to the Boost Software
// License, Version 1.0. (See accompanying file LICENSE_1_0.txt or copy at
// http://www.boost.org/LICENSE_1_0.txt)

//  See http://www.boost.org for updates, documentation, and revision history.

#include <vector>

#include <boost/config.hpp>
#include <boost/detail/workaround.hpp>

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

/////////1/////////2/////////3/////////4/////////5/////////6/////////7/////////8
// vector<T>
template<class Archive, class U, class Allocator>
inline void save(
    Archive & ar,
    const STD::vector<U, Allocator> &t,
    const unsigned int /* file_version */
){
    boost::serialization::stl::save_collection<Archive, STD::vector<U, Allocator> >(
        ar, t
    );
}

template<class Archive, class U, class Allocator>
inline void load(
    Archive & ar,
    STD::vector<U, Allocator> &t,
    const unsigned int /* file_version */
){
    boost::serialization::stl::load_collection<
        Archive,
        STD::vector<U, Allocator>,
        boost::serialization::stl::archive_input_seq<
            Archive, STD::vector<U, Allocator>
        >,
        boost::serialization::stl::reserve_imp<STD::vector<U, Allocator> >
    >(ar, t);
}

// split non-intrusive serialization function member into separate
// non intrusive save/load member functions
template<class Archive, class U, class Allocator>
inline void serialize(
    Archive & ar,
    STD::vector<U, Allocator> & t,
    const unsigned int file_version
){
    boost::serialization::split_free(ar, t, file_version);
}

#if ! BOOST_WORKAROUND(BOOST_MSVC, <= 1300)

/////////1/////////2/////////3/////////4/////////5/////////6/////////7/////////8
// vector<bool>
template<class Archive, class Allocator>
inline void save(
    Archive & ar,
    const STD::vector<bool, Allocator> &t,
    const unsigned int /* file_version */
){
    // record number of elements
    unsigned int count = t.size();
    ar << BOOST_SERIALIZATION_NVP(count);
    STD::vector<bool>::const_iterator it = t.begin();
    while(count-- > 0){
        bool tb = *it++;
        ar << boost::serialization::make_nvp("item", tb);
    }
}

template<class Archive, class Allocator>
inline void load(
    Archive & ar,
    STD::vector<bool, Allocator> &t,
    const unsigned int /* file_version */
){
    // retrieve number of elements
    unsigned int count;
    ar >> BOOST_SERIALIZATION_NVP(count);
    t.clear();
    while(count-- > 0){
        bool i;
        ar >> boost::serialization::make_nvp("item", i);
        t.push_back(i);
    }
}

// split non-intrusive serialization function member into separate
// non intrusive save/load member functions
template<class Archive, class Allocator>
inline void serialize(
    Archive & ar,
    STD::vector<bool, Allocator> & t,
    const unsigned int file_version
){
    boost::serialization::split_free(ar, t, file_version);
}

#endif // BOOST_WORKAROUND

#ifdef BOOST_NO_ARGUMENT_DEPENDENT_LOOKUP
}} // namespace boost::serialization
#else
} // namspace STD
#endif

#include <boost/serialization/collection_traits.hpp>

BOOST_SERIALIZATION_COLLECTION_TRAITS(STD::vector)
#undef STD

#endif // BOOST_SERIALIZATION_VECTOR_HPP
