/*=============================================================================
    Copyright (c) 1998-2003 Joel de Guzman
    http://spirit.sourceforge.net/

    Use, modification and distribution is subject to the Boost Software
    License, Version 1.0. (See accompanying file LICENSE_1_0.txt or copy at
    http://www.boost.org/LICENSE_1_0.txt)
=============================================================================*/
#if !defined(BOOST_SPIRIT_RULE_ALIAS_HPP)
#define BOOST_SPIRIT_RULE_ALIAS_HPP

#include <boost/spirit/core/parser.hpp>

namespace boost { namespace spirit {

    ///////////////////////////////////////////////////////////////////////////
    //
    //  rule_alias class
    //
    ///////////////////////////////////////////////////////////////////////////
    template <typename ParserT>
    class rule_alias :
        public parser<rule_alias<ParserT> >
    {
    public:

        typedef rule_alias<ParserT> self_t;

        template <typename ScannerT>
        struct result
        {
            typedef typename parser_result<ParserT, ScannerT>::type type;
        };

        rule_alias()
        : ptr(0) {}

        rule_alias(ParserT const& p)
        : ptr(&p) {}

        rule_alias&
        operator=(ParserT const& p)
        {
            ptr = &p;
            return *this;
        }

        template <typename ScannerT>
        typename parser_result<ParserT, ScannerT>::type
        parse(ScannerT const& scan) const
        {
            if (ptr)
                return ptr->parse(scan);
            else
                return scan.no_match();
        }

        ParserT const&
        get() const
        {
            assert(ptr != 0);
            return *ptr;
        }

    private:

        ParserT const* ptr; // hold it by pointer
    };

}} // namespace boost::spirit

#endif
