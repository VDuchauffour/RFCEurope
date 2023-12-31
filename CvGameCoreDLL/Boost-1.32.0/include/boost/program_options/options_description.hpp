// Copyright Vladimir Prus 2002-2004.
// Distributed under the Boost Software License, Version 1.0.
// (See accompanying file LICENSE_1_0.txt
// or copy at http://www.boost.org/LICENSE_1_0.txt)


#ifndef BOOST_OPTION_DESCRIPTION_VP_2003_05_19
#define BOOST_OPTION_DESCRIPTION_VP_2003_05_19

#include <boost/program_options/config.hpp>
#include <boost/program_options/errors.hpp>
#include <boost/program_options/value_semantic.hpp>

#include <boost/function.hpp>
#include <boost/shared_ptr.hpp>
#include <boost/detail/workaround.hpp>
#include <boost/any.hpp>

#include <string>
#include <vector>
#include <set>
#include <map>
#include <stdexcept>

#include <iosfwd>

/** Boost namespace */
namespace boost {
/** Namespace for the library. */
namespace program_options {

    /** Describes one possible command line/config file option. There are two
        kinds of properties of an option. First describe it syntactically and
        are used only to validate input. Second affect interpretation of the
        option, for example default value for it or function that should be
        called  when the value is finally known. Routines which perform parsing
        never use second kind of properties -- they are side effect free.
        @sa options_description
    */
    class BOOST_PROGRAM_OPTIONS_DECL option_description {
    public:

        option_description();

        /** Initializes the object with the passed data.

            Note: it would be nice to make the second parameter auto_ptr,
            to explicitly pass ownership. Unfortunately, it's often needed to
            create objects of types derived from 'value_semantic':
               options_description d;
               d.add_options()("a", parameter<int>("n")->default_value(1));
            Here, the static type returned by 'parameter' should be derived
            from value_semantic.

            Alas, derived->base conversion for auto_ptr does not really work,
            see
            http://anubis.dkuug.dk/jtc1/sc22/wg21/docs/papers/2000/n1232.pdf
            http://std.dkuug.dk/jtc1/sc22/wg21/docs/cwg_defects.html#84

            So, we have to use plain old pointers. Besides, users are not
            expected to use the constructor directly.


            The 'name' parameter is interpreted by the following rules:
            - if there's no "," character in 'name', it specifies long name
            - otherwise, the part before "," specifies long name and the part
            after -- long name.
        */
        option_description(const char* name,
                           const value_semantic* s);

        /** Initializes the class with the passed data.
         */
        option_description(const char* name,
                           const value_semantic* s,
                           const char* description);

        virtual ~option_description();

        /// Name to be used with short-style option ("-w").
        const std::string& short_name() const;

        /// Name to be used with long-style option ("--whatever").
        const std::string& long_name() const;
        /// Explanation of this option
        const std::string& description() const;

        /// Semantic of option's value
        shared_ptr<const value_semantic> semantic() const;

        /// Returns the option name, formatted suitably for usage message.
        std::string format_name() const;

        /** Return the parameter name and properties, formatted suitably for
            usage message. */
        std::string format_parameter() const;

    private:

        option_description& name(const char* name);

        std::string m_short_name, m_long_name, m_description;
        std::string m_default_value, m_default_parameter;
        // shared_ptr is needed to simplify memory management in
        // copy ctor and destructor.
        shared_ptr<const value_semantic> m_value_semantic;
    };

    class options_description;

    /** Class which provides convenient creation syntax to option_description.
     */
    class BOOST_PROGRAM_OPTIONS_DECL options_description_easy_init {
    public:
        options_description_easy_init(options_description* owner);

        options_description_easy_init&
        operator()(const char* name,
                   const char* description);

        options_description_easy_init&
        operator()(const char* name,
                   const value_semantic* s);

        options_description_easy_init&
        operator()(const char* name,
                   const value_semantic* s,
                   const char* description);

    private:
        options_description* owner;
    };


    /** A set of option descriptions. This provides convenient interface for
        adding new option (the add_options) method, and facilities to search
        for options by name.

        See @ref a_adding_options "here" for option adding interface discussion.
        @sa option_description
    */
    class BOOST_PROGRAM_OPTIONS_DECL options_description {
    public:

        /** Creates the instance. */
        options_description();
        /** Creates the instance. The 'caption' parameter gives the name of
            this 'options_description' instance. Primarily useful for output.
        */
        options_description(const std::string& caption);
        /** Adds new variable description. Throws duplicate_variable_error if
            either short or long name matches that of already present one.
        */
        void add(shared_ptr<option_description> desc);
        /** Adds a group of option description. This has the same
            effect as adding all option_descriptions in 'desc'
            individually, except that output operator will show
            a separate group.
            Returns *this.
        */
        options_description& add(const options_description& desc);

    public:
        /** Returns an object of implementation-defined type suitable for adding
            options to options_description. The returned object will
            have overloaded operator() with parameter type matching
            'option_description' constructors. Calling the operator will create
            new option_description instance and add it.
        */
        options_description_easy_init add_options();

        /** Count the number of option descriptions with given name.
            Returns 0 or 1.
            The 'name' parameter can be either name of long option, and short
            option prefixed by '-'.
        */
        unsigned count(const std::string& name) const;
        /** Count the number of descriptions having the given string as
            prefix. This makes sense only for long options.
        */
        unsigned count_approx(const std::string& prefix) const;
        /** Returns description given a name.
            @pre count(name) == 1
        */
        const option_description& find(const std::string& name) const;
        /** Returns description given a prefix. Throws
            @pre count_approx(name) == 1
        */
        const option_description& find_approx(const std::string& prefix) const;
        /// Returns all such strings x for which count(x) == 1
        std::set<std::string> keys() const;
        /** For each option description stored, contains long name if not empty,
            if it is empty, short name is returned.
        */
        std::set<std::string> primary_keys() const;
        /// Returns all such long options for which 'prefix' is prefix
        std::set<std::string> approximations(const std::string& prefix) const;

        /** Produces a human readable output of 'desc', listing options,
            their descriptions and allowed parameters. Other options_description
            instances previously passed to add will be output separately. */
        friend BOOST_PROGRAM_OPTIONS_DECL std::ostream& operator<<(std::ostream& os,
                                             const options_description& desc);

        /** Output 'desc' to the specified stream, calling 'f' to output each
            option_description element. */
        void print(std::ostream& os) const;

    private:
        typedef std::map<std::string, int>::const_iterator name2index_iterator;
        typedef std::pair<name2index_iterator, name2index_iterator>
            approximation_range;


        approximation_range find_approximation(const std::string& prefix) const;

        std::string m_caption;
        // Data organization is chosen because:
        // - there could be two names for one option
        // - option_add_proxy needs to know the last added option
        std::vector< shared_ptr<option_description> > options;
        std::map<std::string, int> name2index;
        // Whether the option comes from one of declared groups.
#if BOOST_WORKAROUND(BOOST_DINKUMWARE_STDLIB, BOOST_TESTED_AT(313))
        // vector<bool> is buggy there, see
        // http://support.microsoft.com/default.aspx?scid=kb;en-us;837698
        std::vector<char> belong_to_group;
#else
        std::vector<bool> belong_to_group;
#endif

        std::vector< shared_ptr<options_description> > groups;

    };

    /** Class thrown when duplicate option description is found. */
    class BOOST_PROGRAM_OPTIONS_DECL duplicate_option_error : public error {
    public:
        duplicate_option_error(const std::string& what) : error(what) {}
    };
}}

#endif
