//  Boost version.hpp configuration header file  ------------------------------//

//  (C) Copyright John maddock 1999. Distributed under the Boost
//  Software License, Version 1.0. (See accompanying file
//  LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)

//  See http://www.boost.org/libs/config for documentation

#ifndef BOOST_VERSION_HPP
#define BOOST_VERSION_HPP

//
//  Caution, this is the only boost header that is guarenteed
//  to change with every boost release, including this header
//  will cause a recompile every time a new boost version is
//  released.
//
//  BOOST_VERSION % 100 is the sub-minor version
//  BOOST_VERSION / 100 % 1000 is the minor version
//  BOOST_VERSION / 100000 is the major version

#define BOOST_VERSION 103200

//
//  BOOST_LIB_VERSION must be defined to be the same as BOOST_VERSION
//  but as a *string* in the form "x_y" where x is the major version
//  number and y is the minor version number.  This is used by
//  <config/auto_link.hpp> to select which library version to link to.

#define BOOST_LIB_VERSION "1_32"

#endif
