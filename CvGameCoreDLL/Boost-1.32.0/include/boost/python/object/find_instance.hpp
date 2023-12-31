// Copyright David Abrahams 2002.
// Distributed under the Boost Software License, Version 1.0. (See
// accompanying file LICENSE_1_0.txt or copy at
// http://www.boost.org/LICENSE_1_0.txt)
#ifndef FIND_INSTANCE_DWA2002312_HPP
# define FIND_INSTANCE_DWA2002312_HPP

# include <boost/python/type_id.hpp>

namespace boost { namespace python { namespace objects {

// Given a type_id, find the instance data which corresponds to it, or
// return 0 in case no such type is held.
BOOST_PYTHON_DECL void* find_instance_impl(PyObject*, type_info);

}}} // namespace boost::python::objects

#endif // FIND_INSTANCE_DWA2002312_HPP
