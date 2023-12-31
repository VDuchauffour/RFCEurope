#ifndef BOOST_SERIALIZATION_BASIC_OSERIALIZER_HPP
#define BOOST_SERIALIZATION_BASIC_OSERIALIZER_HPP

// MS compatible compilers support #pragma once
#if defined(_MSC_VER) && (_MSC_VER >= 1020)
# pragma once
#endif

/////////1/////////2/////////3/////////4/////////5/////////6/////////7/////////8
// basic_oserializer.hpp: extenstion of type_info required for serialization.

// (C) Copyright 2002 Robert Ramey - http://www.rrsd.com .
// Use, modification and distribution is subject to the Boost Software
// License, Version 1.0. (See accompanying file LICENSE_1_0.txt or copy at
// http://www.boost.org/LICENSE_1_0.txt)

//  See http://www.boost.org for updates, documentation, and revision history.

#include <boost/archive/detail/basic_serializer.hpp>

namespace boost {

namespace serialization {
    class extended_type_info;
} // namespace serialization

// forward declarations
namespace archive {
namespace detail {

class basic_oarchive;
class basic_pointer_oserializer;

class basic_oserializer : public basic_serializer
{
private:
    basic_pointer_oserializer *bpos;
protected:
    explicit basic_oserializer(
            const boost::serialization::extended_type_info & type_
    ) :
        basic_serializer(type_),
        bpos(NULL)
    {}
    virtual ~basic_oserializer(){}
public:
    bool serialized_as_pointer() const {
        return bpos != NULL;
    }
    void set_bpos(basic_pointer_oserializer *bpos_){
        bpos = bpos_;
    }
    const basic_pointer_oserializer * get_bpos() const {
        return bpos;
    }
    virtual void save_object_data(
        basic_oarchive & ar, const void * x
    ) const = 0;
    // returns true if class_info should be saved
    virtual bool class_info() const = 0;
    // returns true if objects should be tracked
    virtual bool tracking() const = 0;
    // returns class version
    virtual unsigned int version() const = 0;
    // returns true if this class is polymorphic
    virtual bool is_polymorphic() const = 0;
};

} // namespace detail
} // namespace serialization
} // namespace boost

#endif // BOOST_SERIALIZATION_BASIC_OSERIALIZER_HPP
