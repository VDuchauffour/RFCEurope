//  Boost string_algo library finder.hpp header file  ---------------------------//

//  Copyright Pavol Droba 2002-2003. Use, modification and
//  distribution is subject to the Boost Software License, Version
//  1.0. (See accompanying file LICENSE_1_0.txt or copy at
//  http://www.boost.org/LICENSE_1_0.txt)

//  See http://www.boost.org for updates, documentation, and revision history.

#ifndef BOOST_STRING_FINDER_DETAIL_HPP
#define BOOST_STRING_FINDER_DETAIL_HPP

#include <boost/algorithm/string/config.hpp>
#include <boost/algorithm/string/constants.hpp>
#include <boost/detail/iterator.hpp>
#include <boost/algorithm/string/collection_traits.hpp>
#include <boost/algorithm/string/iterator_range.hpp>

namespace boost {
    namespace algorithm {
        namespace detail {


//  find first functor -----------------------------------------------//

            // find a subsequence in the sequence ( functor )
            /*
                Returns a pair <begin,end> marking the subsequence in the sequence.
                If the find fails, functor returns <End,End>
            */
            template<typename SearchIteratorT,typename PredicateT>
            struct first_finderF
            {
                typedef SearchIteratorT search_iterator_type;

                // Construction
                template< typename SearchT >
                first_finderF( const SearchT& Search, PredicateT Comp ) :
                    m_Search(begin(Search), end(Search)), m_Comp(Comp) {}
                first_finderF(
                        search_iterator_type SearchBegin,
                        search_iterator_type SearchEnd,
                        PredicateT Comp ) :
                    m_Search(SearchBegin, SearchEnd), m_Comp(Comp) {}

                // Operation
                template< typename ForwardIteratorT >
                iterator_range<ForwardIteratorT>
                operator()(
                    ForwardIteratorT Begin,
                    ForwardIteratorT End ) const
                {
                    typedef iterator_range<ForwardIteratorT> result_type;
                    typedef ForwardIteratorT input_iterator_type;

                    // Outer loop
                    for(input_iterator_type OuterIt=Begin;
                        OuterIt!=End;
                        ++OuterIt)
                    {
                        // Sanity check
                        if( empty(m_Search) )
                            return result_type( End, End );

                        input_iterator_type InnerIt=OuterIt;
                        search_iterator_type SubstrIt=m_Search.begin();
                        for(;
                            InnerIt!=End && SubstrIt!=m_Search.end();
                            ++InnerIt,++SubstrIt)
                        {
                            if( !( m_Comp(*InnerIt,*SubstrIt) ) )
                                break;
                        }

                        // Substring matching succeeded
                        if ( SubstrIt==m_Search.end() )
                            return result_type( OuterIt, InnerIt );
                    }

                    return result_type( End, End );
                }

            private:
                iterator_range<search_iterator_type> m_Search;
                PredicateT m_Comp;
            };

//  find last functor -----------------------------------------------//

            // find the last match a subsequnce in the sequence ( functor )
            /*
                Returns a pair <begin,end> marking the subsequence in the sequence.
                If the find fails, returns <End,End>
            */
            template<typename SearchIteratorT, typename PredicateT>
            struct last_finderF
            {
                typedef SearchIteratorT search_iterator_type;
                typedef first_finderF<
                    search_iterator_type,
                    PredicateT> first_finder_type;

                // Construction
                template< typename SearchT >
                last_finderF( const SearchT& Search, PredicateT Comp ) :
                    m_Search(begin(Search), end(Search)), m_Comp(Comp) {}
                last_finderF(
                        search_iterator_type SearchBegin,
                        search_iterator_type SearchEnd,
                        PredicateT Comp ) :
                    m_Search(SearchBegin, SearchEnd), m_Comp(Comp) {}

                // Operation
                template< typename ForwardIteratorT >
                iterator_range<ForwardIteratorT>
                operator()(
                    ForwardIteratorT Begin,
                    ForwardIteratorT End ) const
                {
                    typedef iterator_range<ForwardIteratorT> result_type;

                    if( empty(m_Search) )
                        return result_type( End, End );

                    typedef BOOST_STRING_TYPENAME boost::detail::
                        iterator_traits<ForwardIteratorT>::iterator_category category;

                    return findit( Begin, End, category() );
                }

            private:
                // forward iterator
                template< typename ForwardIteratorT >
                iterator_range<ForwardIteratorT>
                findit(
                    ForwardIteratorT Begin,
                    ForwardIteratorT End,
                    std::forward_iterator_tag ) const
                {
                    typedef ForwardIteratorT input_iterator_type;
                    typedef iterator_range<ForwardIteratorT> result_type;

                    first_finder_type first_finder(
                        m_Search.begin(), m_Search.end(), m_Comp );

                    result_type M=first_finder( Begin, End );
                    result_type Last=M;

                    while( M )
                    {
                        Last=M;
                        M=first_finder( end(M), End );
                    }

                    return Last;
                }

                // bidirectional iterator
                template< typename ForwardIteratorT >
                iterator_range<ForwardIteratorT>
                findit(
                    ForwardIteratorT Begin,
                    ForwardIteratorT End,
                    std::bidirectional_iterator_tag ) const
                {
                    typedef iterator_range<ForwardIteratorT> result_type;
                    typedef ForwardIteratorT input_iterator_type;

                    // Outer loop
                    for(input_iterator_type OuterIt=End;
                        OuterIt!=Begin; )
                    {
                        input_iterator_type OuterIt2=--OuterIt;

                        input_iterator_type InnerIt=OuterIt2;
                        search_iterator_type SubstrIt=m_Search.begin();
                        for(;
                            InnerIt!=End && SubstrIt!=m_Search.end();
                            ++InnerIt,++SubstrIt)
                        {
                            if( !( m_Comp(*InnerIt,*SubstrIt) ) )
                                break;
                        }

                        // Substring matching succeeded
                        if( SubstrIt==m_Search.end() )
                            return result_type( OuterIt2, InnerIt );
                    }

                    return result_type( End, End );
                }

            private:
                iterator_range<search_iterator_type> m_Search;
                PredicateT m_Comp;
            };

//  find n-th functor -----------------------------------------------//

            // find the n-th match of a subsequnce in the sequence ( functor )
            /*
                Returns a pair <begin,end> marking the subsequence in the sequence.
                If the find fails, returns <End,End>
            */
            template<typename SearchIteratorT, typename PredicateT>
            struct nth_finderF
            {
                typedef SearchIteratorT search_iterator_type;
                typedef first_finderF<
                    search_iterator_type,
                    PredicateT> first_finder_type;

                // Construction
                template< typename SearchT >
                nth_finderF(
                        const SearchT& Search,
                        unsigned int Nth,
                        PredicateT Comp) :
                    m_Search(begin(Search), end(Search)),
                    m_Nth(Nth),
                    m_Comp(Comp) {}
                nth_finderF(
                        search_iterator_type SearchBegin,
                        search_iterator_type SearchEnd,
                        unsigned int Nth,
                        PredicateT Comp) :
                    m_Search(SearchBegin, SearchEnd),
                    m_Nth(Nth),
                    m_Comp(Comp) {}

                // Operation
                template< typename ForwardIteratorT >
                iterator_range<ForwardIteratorT>
                operator()(
                    ForwardIteratorT Begin,
                    ForwardIteratorT End ) const
                {
                    typedef ForwardIteratorT input_iterator_type;
                    typedef iterator_range<ForwardIteratorT> result_type;

                    // Sanity check
                    if( empty(m_Search) )
                        return result_type( End, End );

                    // Instantiate find funtor
                    first_finder_type first_finder(
                        m_Search.begin(), m_Search.end(), m_Comp );

                    result_type M( Begin, Begin );

                    for( unsigned int n=0; n<=m_Nth; ++n )
                    {
                        // find next match
                        M=first_finder( end(M), End );

                        if ( !M )
                        {
                            // Subsequence not found, return
                            return M;
                        }
                    }

                    return M;
                }

            private:
                iterator_range<search_iterator_type> m_Search;
                unsigned int m_Nth;
                PredicateT m_Comp;
            };

//  find head functor -----------------------------------------------//

            // find a head in the sequence ( functor )
            /*
                This functor find a head of the specified range. For
                a specified N, the head is a subsequence of N starting
                elements of the range.
            */
            struct head_finderF
            {
                // Construction
                head_finderF( unsigned int N ) : m_N(N) {}

                // Operation
                template< typename ForwardIteratorT >
                iterator_range<ForwardIteratorT>
                operator()(
                    ForwardIteratorT Begin,
                    ForwardIteratorT End ) const
                {
                    typedef BOOST_STRING_TYPENAME boost::detail::
                        iterator_traits<ForwardIteratorT>::iterator_category category;

                    return findit( Begin, End, category() );
                }

            private:
                // Find operation implementation
                template< typename ForwardIteratorT >
                    iterator_range<ForwardIteratorT>
                findit(
                    ForwardIteratorT Begin,
                    ForwardIteratorT End,
                    std::forward_iterator_tag ) const
                {
                    typedef ForwardIteratorT input_iterator_type;
                    typedef iterator_range<ForwardIteratorT> result_type;

                    input_iterator_type It=Begin;
                    for(
                        unsigned int Index=0;
                        Index<m_N && It!=End; ++Index,++It ) {};

                    return result_type( Begin, It );
                }

                template< typename ForwardIteratorT >
                    iterator_range<ForwardIteratorT>
                findit(
                    ForwardIteratorT Begin,
                    ForwardIteratorT End,
                    std::random_access_iterator_tag ) const
                {
                    typedef ForwardIteratorT input_iterator_type;
                    typedef iterator_range<ForwardIteratorT> result_type;

                    if ( (End<=Begin) || ( static_cast<unsigned int>(End-Begin) < m_N ) )
                        return result_type( Begin, End );

                    return result_type(Begin,Begin+m_N);
                }

            private:
                unsigned int m_N;
            };

//  find tail functor -----------------------------------------------//

            // find a tail in the sequence ( functor )
            /*
                This functor find a tail of the specified range. For
                a specified N, the head is a subsequence of N starting
                elements of the range.
            */
            struct tail_finderF
            {
                // Construction
                tail_finderF( unsigned int N ) : m_N(N) {}

                // Operation
                template< typename ForwardIteratorT >
                iterator_range<ForwardIteratorT>
                operator()(
                    ForwardIteratorT Begin,
                    ForwardIteratorT End ) const
                {
                    typedef BOOST_STRING_TYPENAME boost::detail::
                        iterator_traits<ForwardIteratorT>::iterator_category category;

                    return findit( Begin, End, category() );
                }

            private:
                // Find operation implementation
                template< typename ForwardIteratorT >
                    iterator_range<ForwardIteratorT>
                findit(
                    ForwardIteratorT Begin,
                    ForwardIteratorT End,
                    std::forward_iterator_tag ) const
                {
                    typedef ForwardIteratorT input_iterator_type;
                    typedef iterator_range<ForwardIteratorT> result_type;

                    unsigned int Index=0;
                    input_iterator_type It=Begin;
                    input_iterator_type It2=Begin;

                    // Advance It2 by N incremets
                    for( Index=0; Index<m_N && It2!=End; ++Index,++It2 ) {};

                    // Advance It, It2 to the end
                    for(; It2!=End; ++It,++It2 ) {};

                    return result_type( It, It2 );
                }

                template< typename ForwardIteratorT >
                    iterator_range<ForwardIteratorT>
                findit(
                    ForwardIteratorT Begin,
                    ForwardIteratorT End,
                    std::bidirectional_iterator_tag ) const
                {
                    typedef ForwardIteratorT input_iterator_type;
                    typedef iterator_range<ForwardIteratorT> result_type;

                    input_iterator_type It=End;
                    for(
                        unsigned int Index=0;
                        Index<m_N && It!=Begin; ++Index,--It ) {};

                    return result_type( It, End );
                }

                template< typename ForwardIteratorT >
                    iterator_range<ForwardIteratorT>
                findit(
                    ForwardIteratorT Begin,
                    ForwardIteratorT End,
                    std::random_access_iterator_tag ) const
                {
                    typedef ForwardIteratorT input_iterator_type;
                    typedef iterator_range<ForwardIteratorT> result_type;

                    if ( (End<=Begin) || ( static_cast<unsigned int>(End-Begin) < m_N ) )
                        return result_type( Begin, End );

                    return result_type( End-m_N, End );
                }


            private:
                unsigned int m_N;
            };

//  find token functor -----------------------------------------------//

            // find a token in a sequence ( functor )
            /*
                This find functor finds a token specified be a predicate
                in a sequence. It is equivalent of std::find algorithm,
                with an exception that it return range instead of a single
                iterator.

                If bCompress is set to true, adjacent matching tokens are
                concatenated into one match.
            */
            template< typename PredicateT >
            struct token_finderF
            {
                // Construction
                token_finderF(
                    PredicateT Pred,
                    token_compress_mode_type eCompress=token_compress_off ) :
                        m_Pred(Pred), m_eCompress(eCompress) {}

                // Operation
                template< typename ForwardIteratorT >
                iterator_range<ForwardIteratorT>
                operator()(
                    ForwardIteratorT Begin,
                    ForwardIteratorT End ) const
                {
                    typedef iterator_range<ForwardIteratorT> result_type;

                    ForwardIteratorT It=std::find_if( Begin, End, m_Pred );

                    if( It==End )
                    {
                        return result_type( End, End );
                    }
                    else
                    {
                        ForwardIteratorT It2=It;

                        if( m_eCompress==token_compress_on )
                        {
                            // Find first non-matching character
                            while( m_Pred(*It2) && It2!=End ) ++It2;
                        }
                        else
                        {
                            // Advance by one possition
                            ++It2;
                        }

                        return result_type( It, It2 );
                    }
                }

            private:
                PredicateT m_Pred;
                token_compress_mode_type m_eCompress;
            };

//  find range functor -----------------------------------------------//

            // find a range in the sequence ( functor )
            /*
                This functor actually does not perform any find operation.
                It always returns given iterator range as a result.
            */
            template<typename ForwardIterator1T>
            struct range_finderF
            {
                typedef ForwardIterator1T input_iterator_type;
                typedef iterator_range<input_iterator_type> result_type;

                // Construction
                range_finderF(
                    input_iterator_type Begin,
                    input_iterator_type End ) : m_Range(Begin, End) {}

                range_finderF(const iterator_range<input_iterator_type>& Range) :
                    m_Range(Range) {}

                // Operation
                template< typename ForwardIterator2T >
                iterator_range<ForwardIterator2T>
                operator()(
                    ForwardIterator2T,
                    ForwardIterator2T ) const
                {
                    return m_Range;
                }

            private:
                iterator_range<input_iterator_type> m_Range;
            };


        } // namespace detail
    } // namespace algorithm
} // namespace boost

#endif  // BOOST_STRING_FINDER_DETAIL_HPP
