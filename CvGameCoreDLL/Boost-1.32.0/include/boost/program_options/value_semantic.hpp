// Copyright Vladimir Prus 2004.
// Distributed under the Boost Software License, Version 1.0.
// (See accompanying file LICENSE_1_0.txt
// or copy at http://www.boost.org/LICENSE_1_0.txt)

#ifndef BOOST_VALUE_SEMANTIC_HPP_VP_2004_02_24
#define BOOST_VALUE_SEMANTIC_HPP_VP_2004_02_24

#include <boost/program_options/config.hpp>
#include <boost/program_options/errors.hpp>

#include <boost/any.hpp>
#include <boost/function/function1.hpp>
#include <boost/lexical_cast.hpp>



#include <string>
#include <vector>

namespace boost { namespace program_options {

    /** Class which specifies how the option's value is to be parsed
        and converted into C++ types.
    */
    class BOOST_PROGRAM_OPTIONS_DECL value_semantic {
    public:
        /** Returns the name of the option. The name is only meaningful
            for automatic help message.
         */
        virtual std::string name() const = 0;

        /** Returns true if value cannot be specified in source at all.
            Other methods can still set the value somehow, but
            user can't affect it.
        */
        virtual bool is_zero_tokens() const = 0;

        /** Returns true if values from different sources should be composed.
            Otherwise, value from the first source is used and values from
            other sources are discarded.
        */
        virtual bool is_composing() const = 0;

        /** Returns true if explicit value of an option can be omitted.
        */
        virtual bool is_implicit() const = 0;

        /** Returns true if value can span several token in input source. */
        virtual bool is_multitoken() const = 0;

        /** Parses a group of tokens that specify a value of option.
            Stores the result in 'value_store', using whatever representation
            is desired. May be be called several times if value of the same
            option is specified more than once.
        */
        virtual void parse(boost::any& value_store,
                           const std::vector<std::string>& new_tokens,
                           bool utf8) const
            = 0;

        /** Called to assign default value to 'value_store'. Returns
            true if default value is assigned, and false if no default
            value exists. */
        virtual bool apply_default(boost::any& value_store) const = 0;

        /** Called when final value of an option is determined.
        */
        virtual void notify(const boost::any& value_store) const = 0;

        virtual ~value_semantic() {}
    };

    /** Helper class which perform necessary character conversions in the
        'parse' method and forwards the data further.
    */
    template<class charT>
    class value_semantic_codecvt_helper {
        // Nothing here. Specializations to follow.
    };

    template<>
    class BOOST_PROGRAM_OPTIONS_DECL
    value_semantic_codecvt_helper<char> : public value_semantic {
    private: // base overrides
        void parse(boost::any& value_store,
                   const std::vector<std::string>& new_tokens,
                   bool utf8) const;
    protected: // interface for derived classes.
        virtual void xparse(boost::any& value_store,
                            const std::vector<std::string>& new_tokens)
            const = 0;
    };

    template<>
    class BOOST_PROGRAM_OPTIONS_DECL
    value_semantic_codecvt_helper<wchar_t> : public value_semantic {
    private: // base overrides
        void parse(boost::any& value_store,
                   const std::vector<std::string>& new_tokens,
                   bool utf8) const;
    protected: // interface for derived classes.
#if !defined(BOOST_NO_STD_WSTRING)
        virtual void xparse(boost::any& value_store,
                            const std::vector<std::wstring>& new_tokens)
            const = 0;
#endif
    };
    /** Class which specifies a simple handling of a value: the value will
        have string type and only one token is allowed. */
    class BOOST_PROGRAM_OPTIONS_DECL
    untyped_value : public value_semantic_codecvt_helper<char>  {
    public:
        untyped_value(bool zero_tokens = false)
        : m_zero_tokens(zero_tokens)
        {}

        std::string name() const;

        bool is_zero_tokens() const { return m_zero_tokens; }
        bool is_composing() const { return false; }
        bool is_implicit() const { return false; }
        bool is_multitoken() const { return false; }

        /** If 'value_store' is already initialized, or new_tokens
            has more than one elements, throws. Otherwise, assigns
            the first string from 'new_tokens' to 'value_store', without
            any modifications.
         */
        void xparse(boost::any& value_store,
                    const std::vector<std::string>& new_tokens) const;

        /** Does nothing. */
        bool apply_default(boost::any&) const { return false; }

        /** Does nothing. */
        void notify(const boost::any&) const {}
    private:
        bool m_zero_tokens;
    };

    /** Class which handles value of a specific type. */
    template<class T, class charT = char>
    class typed_value : public value_semantic_codecvt_helper<charT>  {
    public:
        /** Ctor. The 'store_to' parameter tells where to store
            the value when it's known. The parameter can be NULL. */
        typed_value(T* store_to)
        : m_store_to(store_to), m_composing(false),
          m_implicit(false), m_multitoken(false), m_zero_tokens(false)
        {}

        /** Specifies default value, which will be used
            if none is explicitly specified. The type 'T' should
            provide operator<< for ostream.
        */
        typed_value* default_value(const T& v)
        {
            m_default_value = boost::any(v);
            m_default_value_as_text = boost::lexical_cast<std::string>(v);
            return this;
        }

        /** Specifies default value, which will be used
            if none is explicitly specified. Unlike the above overload,
            the type 'T' need not provide operator<< for ostream,
            but textual representation of default value must be provided
            by the user.
        */
        typed_value* default_value(const T& v, const std::string& textual)
        {
            m_default_value = boost::any(v);
            m_default_value_as_text = textual;
            return this;
        }

        /** Specifies a function to be called when the final value
            is determined. */
        typed_value* notifier(function1<void, const T&> f)
        {
            m_notifier = f;
            return this;
        }

        /** Specifies that the value is composing. See the 'is_composing'
            method for explanation.
        */
        typed_value* composing()
        {
            m_composing = true;
            return this;
        }

        /** Specifies that the value is implicit. */
        typed_value* implicit()
        {
            m_implicit =  true;
            return this;
        }

        /** Specifies that the value can span multiple tokens. */
        typed_value* multitoken()
        {
            m_multitoken = true;
            return this;
        }

        typed_value* zero_tokens()
        {
            m_zero_tokens = true;
            return this;
        }


    public: // value semantic overrides

        std::string name() const;

        bool is_zero_tokens() const { return m_zero_tokens; }
        bool is_composing() const { return m_composing; }
        bool is_implicit() const { return m_implicit; }
        bool is_multitoken() const { return m_multitoken; }


        /** Creates an instance of the 'validator' class and calls
            its operator() to perform athe ctual conversion. */
        void xparse(boost::any& value_store,
                    const std::vector< std::basic_string<charT> >& new_tokens)
            const;

        /** If default value was specified via previous call to
            'default_value', stores that value into 'value_store'.
            Returns true if default value was stored.
        */
        virtual bool apply_default(boost::any& value_store) const
        {
            if (m_default_value.empty()) {
                return false;
            } else {
                value_store = m_default_value;
                return true;
            }
        }

        /** If an address of variable to store value was specified
            when creating *this, stores the value there. Otherwise,
            does nothing. */
        void notify(const boost::any& value_store) const;


    private:
        T* m_store_to;

        // Default value is stored as boost::any and not
        // as boost::optional to avoid unnecessary instantiations.
        boost::any m_default_value;
        std::string m_default_value_as_text;
        bool m_composing, m_implicit, m_multitoken, m_zero_tokens;
        boost::function1<void, const T&> m_notifier;
    };


    /** Creates a typed_value<T> instance. This function is the primary
        method to create value_semantic instance for a specific type, which
        can later be passed to 'option_description' constructor.
        The second overload is used when it's additionally desired to store the
        value of option into program variable.
    */
    template<class T>
    typed_value<T>*
    value();

    /** @overload
    */
    template<class T>
    typed_value<T>*
    value(T* v);

    /** Creates a typed_value<T> instance. This function is the primary
        method to create value_semantic instance for a specific type, which
        can later be passed to 'option_description' constructor.
    */
    template<class T>
    typed_value<T, wchar_t>*
    wvalue();

    /** @overload
    */
    template<class T>
    typed_value<T, wchar_t>*
    wvalue(T* v);

    /** Works the same way as the 'value<bool>' function, but the created
        value_semantic won't accept any explicit value. So, if the option
        is present on the command line, the value will be 'true'.
    */
    BOOST_PROGRAM_OPTIONS_DECL typed_value<bool>*
    bool_switch();

    /** @overload
    */
    BOOST_PROGRAM_OPTIONS_DECL typed_value<bool>*
    bool_switch(bool* v);

}}

#include "detail/value_semantic.hpp"

#endif
