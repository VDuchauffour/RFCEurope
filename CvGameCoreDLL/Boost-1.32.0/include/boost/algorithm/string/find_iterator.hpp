//  Boost string_algo library find_iterator.hpp header file  ---------------------------//

//  Copyright Pavol Droba 2002-2004. Use, modification and
//  distribution is subject to the Boost Software License, Version
//  1.0. (See accompanying file LICENSE_1_0.txt or copy at
//  http://www.boost.org/LICENSE_1_0.txt)
//  See http://www.boost.org for updates, documentation, and revision history.

#ifndef BOOST_STRING_FIND_ITERATOR_HPP
#define BOOST_STRING_FIND_ITERATOR_HPP


#include <boost/algorithm/string/config.hpp>
#include <boost/algorithm/string/collection_traits.hpp>
#include <boost/algorithm/string/iterator_range.hpp>
#include <boost/algorithm/string/detail/find_iterator.hpp>
#include <boost/iterator/iterator_facade.hpp>
#include <boost/iterator/iterator_categories.hpp>

/*! \file
    Defines find iterator classes. Find iterator repeatly applies a Finder
    to the specified input string to search for matches. Dereferencing
    the iterator yields the current match or a range between the last and the current
    match depending on the iterator used.
*/

namespace boost {
    namespace algorithm {

//  find_iterator -----------------------------------------------//

        //! find_iterator
        /*!
            Find iterator encapsulates a Finder and allows
            for incremental searching in a string.
            Each increment moves the iterator to the next match.

            Find iterator is a readable forward traversal iterator.

            Dereferencing the iterator yields an iterator_range delimiting
            the current match.
        */
        template<typename IteratorT>
        class find_iterator :
            public iterator_facade<
                find_iterator<IteratorT>,
                const iterator_range<IteratorT>,
                forward_traversal_tag >,
            private detail::find_iterator_base<IteratorT>
        {
        private:
            // facade support
            friend class ::boost::iterator_core_access;

            // base type
            typedef iterator_facade<
                find_iterator<IteratorT>,
                const iterator_range<IteratorT>,
                forward_traversal_tag> facade_type;

        private:
        // typedefs

            typedef detail::find_iterator_base<IteratorT> base_type;
            typedef BOOST_STRING_TYPENAME
                base_type::input_iterator_type input_iterator_type;
            typedef BOOST_STRING_TYPENAME
                base_type::match_type match_type;

        public:
            //! Default constructor
            /*!
                Construct null iterator. All null iterators are equal.

                \post eof()==true
            */
            find_iterator() {}

            //! Copy constructor
            /*!
                Construct a copy of the find_iterator
            */
            find_iterator( const find_iterator& Other ) :
                base_type(Other),
                m_Match(Other.m_Match),
                m_End(Other.m_End) {}

            //! Constructor
            /*!
                Construct new find_iterator for a given finder
                and a range.
            */
            template<typename FinderT>
            find_iterator(
                    IteratorT Begin,
                    IteratorT End,
                    FinderT Finder ) :
                detail::find_iterator_base<IteratorT>(Finder,0),
                m_Match(Begin,Begin),
                m_End(End)
            {
                increment();
            }

            //! Constructor
            /*!
                Construct new find_iterator for a given finder
                and a collection.
            */
            template<typename FinderT, typename CollectionT>
            find_iterator(
                    CollectionT& Col,
                    FinderT Finder ) :
                detail::find_iterator_base<IteratorT>(Finder,0),
                m_Match(begin(Col),begin(Col)),
                m_End(end(Col))
            {
                increment();
            }

        private:
        // iterator operations

            // dereference
            const match_type& dereference() const
            {
                return m_Match;
            }

            // increment
            void increment()
            {
                m_Match=this->do_find(m_Match.end(),m_End);
            }

            // comparison
            bool equal( const find_iterator& Other ) const
            {
                bool bEof=eof();
                bool bOtherEof=Other.eof();

                return bEof || bOtherEof ? bEof==bOtherEof :
                    (
                        m_Match==Other.m_Match &&
                        m_End==Other.m_End
                    );
            }

        public:
        // operations

            //! Eof check
            /*!
                Check the eof condition. Eof condition means that
                there is nothing more to be searched i.e. find_iterator
                is after the last match.
            */
            bool eof() const
            {
                return
                    this->is_null() ||
                    (
                        m_Match.begin() == m_End &&
                        m_Match.end() == m_End
                    );
            }

        private:
        // Attributes
            match_type m_Match;
            input_iterator_type m_End;
        };

        //! find iterator construction helper
        /*!
         *    Construct a find iterator to iterate through the specified string
         */
        template<typename CollectionT, typename FinderT>
        inline find_iterator<
            BOOST_STRING_TYPENAME result_iterator_of<CollectionT>::type>
        make_find_iterator(
            CollectionT& Collection,
            FinderT Finder)
        {
            return find_iterator<BOOST_STRING_TYPENAME result_iterator_of<CollectionT>::type>(
                begin(Collection), end(Collection), Finder);
        }

//  split iterator -----------------------------------------------//

        //! split_iterator
        /*!
            Split iterator encapsulates a Finder and allows
            for incremental searching in a string.
            Unlike the find iterator, split iterator iterates
            through gaps between matches.

            Find iterator is a readable forward traversal iterator.

            Dereferencing the iterator yields an iterator_range delimiting
            the current match.
        */
        template<typename IteratorT>
        class split_iterator :
            public iterator_facade<
                split_iterator<IteratorT>,
                const iterator_range<IteratorT>,
                forward_traversal_tag >,
            private detail::find_iterator_base<IteratorT>
        {
        private:
            // facade support
            friend class ::boost::iterator_core_access;

            // base type
            typedef iterator_facade<
                find_iterator<IteratorT>,
                iterator_range<IteratorT>,
                forward_traversal_tag> facade_type;

        private:
        // typedefs

            typedef detail::find_iterator_base<IteratorT> base_type;
            typedef BOOST_STRING_TYPENAME
                base_type::input_iterator_type input_iterator_type;
            typedef BOOST_STRING_TYPENAME
                base_type::match_type match_type;

        public:
            //! Default constructor
            /*!
                Construct null iterator. All null iterators are equal.

                \post eof()==true
            */
            split_iterator() {}
            //! Copy constructor
            /*!
                Construct a copy of the split_iterator
            */
            split_iterator( const split_iterator& Other ) :
                base_type(Other),
                m_Match(Other.m_Match),
                m_Next(Other.m_Next),
                m_End(Other.m_End) {}

            //! Constructor
            /*!
                Construct new split_iterator for a given finder
                and a range.
            */
            template<typename FinderT>
            split_iterator(
                    IteratorT Begin,
                    IteratorT End,
                    FinderT Finder ) :
                detail::find_iterator_base<IteratorT>(Finder,0),
                m_Match(Begin,Begin),
                m_Next(Begin),
                m_End(End)
            {
                increment();
            }
            //! Constructor
            /*!
                Construct new split_iterator for a given finder
                and a collection.
            */
            template<typename FinderT, typename CollectionT>
            split_iterator(
                    CollectionT& Col,
                    FinderT Finder ) :
                detail::find_iterator_base<IteratorT>(Finder,0),
                m_Match(begin(Col),begin(Col)),
                m_Next(begin(Col)),
                m_End(end(Col))
            {
                increment();
            }


        private:
        // iterator operations

            // dereference
            const match_type& dereference() const
            {
                return m_Match;
            }

            // increment
            void increment()
            {
                match_type FindMatch=this->do_find( m_Next, m_End );
                m_Match=match_type( m_Next, FindMatch.begin() );
                m_Next=FindMatch.end();
            }

            // comparison
            bool equal( const split_iterator& Other ) const
            {
                bool bEof=eof();
                bool bOtherEof=Other.eof();

                return bEof || bOtherEof ? bEof==bOtherEof :
                    (
                        m_Match==Other.m_Match &&
                        m_Next==Other.m_Next &&
                        m_End==Other.m_End
                    );
            }

        public:
        // operations

            //! Eof check
            /*!
                Check the eof condition. Eof condition means that
                there is nothing more to be searched i.e. find_iterator
                is after the last match.
            */
            bool eof() const
            {
                return
                    this->is_null() ||
                    (
                        m_Match.begin() == m_End &&
                        m_Match.end() == m_End
                    );
            }

        private:
        // Attributes
            match_type m_Match;
            input_iterator_type m_Next;
            input_iterator_type m_End;
        };

        //! split iterator construction helper
        /*!
         *    Construct a split iterator to iterate through the specified collection
         */
        template<typename CollectionT, typename FinderT>
        inline split_iterator<
            BOOST_STRING_TYPENAME result_iterator_of<CollectionT>::type>
        make_split_iterator(
            CollectionT& Collection,
            FinderT Finder)
        {
            return split_iterator<BOOST_STRING_TYPENAME result_iterator_of<CollectionT>::type>(
                begin(Collection), end(Collection), Finder);
        }


    } // namespace algorithm

    // pull names to the boost namespace
    using algorithm::find_iterator;
    using algorithm::make_find_iterator;
    using algorithm::split_iterator;
    using algorithm::make_split_iterator;

} // namespace boost


#endif  // BOOST_STRING_FIND_ITERATOR_HPP
