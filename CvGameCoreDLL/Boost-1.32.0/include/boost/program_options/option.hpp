// Copyright Vladimir Prus 2004.
// Distributed under the Boost Software License, Version 1.0.
// (See accompanying file LICENSE_1_0.txt
// or copy at http://www.boost.org/LICENSE_1_0.txt)

#ifndef BOOST_OPTION_HPP_VP_2004_02_25
#define BOOST_OPTION_HPP_VP_2004_02_25

#include <boost/program_options/config.hpp>

#include <string>
#include <vector>

namespace boost { namespace program_options {

    /** Option found in input source.
        Contains a key and a value. The key, in turn, can be a string (name of
        an option), or an integer (position in input source) -- in case no name
        is specified. The latter is only possible for command line.
        The template parameter specifies the type of char used for storing the
        option's value.
    */
    template<class charT>
    class basic_option {
    public:
        basic_option() : position_key(-1) {}
        basic_option(const std::string& string_key,
               const std::vector< std::string> &value)
        : string_key(string_key), value(value)
        {}

        /** String key of this option. Intentionally independent of the template
            parameter. */
        std::string string_key;
        /** Position key of this option. All options without an explicit name are
            sequentially numbered starting from 0. If an option has explicit name,
            'position_key' is equal to -1. It is possible that both
            position_key and string_key is specified, in case name is implicitly
            added.
         */
        int position_key;
        /** Option's value */
        std::vector< std::basic_string<charT> > value;
    };
    typedef basic_option<char> option;
    typedef basic_option<wchar_t> woption;

}}

#endif
