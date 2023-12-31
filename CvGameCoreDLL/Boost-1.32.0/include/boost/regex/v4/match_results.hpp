/*
 *
 * Copyright (c) 1998-2002
 * Dr John Maddock
 *
 * Use, modification and distribution are subject to the
 * Boost Software License, Version 1.0. (See accompanying file
 * LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
 *
 */

 /*
  *   LOCATION:    see http://www.boost.org for most recent version.
  *   FILE         match_results.cpp
  *   VERSION      see <boost/version.hpp>
  *   DESCRIPTION: Declares template class match_results.
  */

#ifndef BOOST_REGEX_V4_MATCH_RESULTS_HPP
#define BOOST_REGEX_V4_MATCH_RESULTS_HPP

#ifdef BOOST_HAS_ABI_HEADERS
#  include BOOST_ABI_PREFIX
#endif

namespace boost{

template <class BidiIterator
         , class Allocator = BOOST_DEFAULT_ALLOCATOR(sub_match<BidiIterator> )
         >
class match_results
{
private:
#ifndef BOOST_NO_STD_ALLOCATOR
   typedef          std::vector<sub_match<BidiIterator>, Allocator> vector_type;
#else
   typedef          std::vector<sub_match<BidiIterator> >           vector_type;
#endif
public:
   typedef          sub_match<BidiIterator>                         value_type;
#if  !defined(BOOST_NO_STD_ALLOCATOR) && !(defined(BOOST_MSVC) && defined(_STLPORT_VERSION))
   typedef typename Allocator::const_reference                              const_reference;
#else
   typedef          const value_type&                                       const_reference;
#endif
   typedef          const_reference                                         reference;
   typedef typename vector_type::const_iterator                             const_iterator;
   typedef          const_iterator                                          iterator;
   typedef typename re_detail::regex_iterator_traits<
                                    BidiIterator>::difference_type  difference_type;
   typedef typename Allocator::size_type                                    size_type;
   typedef          Allocator                                               allocator_type;
   typedef typename re_detail::regex_iterator_traits<
                                    BidiIterator>::value_type       char_type;
   typedef          std::basic_string<char_type>                            string_type;

   // construct/copy/destroy:
   explicit match_results(const Allocator& a = Allocator())
#ifndef BOOST_NO_STD_ALLOCATOR
      : m_subs(a), m_base() {}
#else
      : m_subs(), m_base() { (void)a; }
#endif
   match_results(const match_results& m)
      : m_subs(m.m_subs), m_base(m.m_base) {}
   match_results& operator=(const match_results& m)
   {
      m_subs = m.m_subs;
      m_base = m.m_base;
      return *this;
   }
   ~match_results(){}

   // size:
   size_type size() const
   { return (m_subs.size() >= 2) ? m_subs.size() - 2 : 0; }
   size_type max_size() const
   { return m_subs.max_size(); }
   bool empty() const
   { return m_subs.size() < 2; }
   // element access:
   difference_type length(int sub = 0) const
   {
      sub += 2;
      if((sub < (int)m_subs.size()) && (sub > 0))
         return m_subs[sub].length();
      return 0;
   }
   difference_type position(unsigned int sub = 0) const
   {
      sub += 2;
      if(sub < m_subs.size())
      {
         const sub_match<BidiIterator>& s = m_subs[sub];
         if(s.matched)
         {
            return boost::re_detail::distance((BidiIterator)(m_base), (BidiIterator)(s.first));
         }
      }
      return ~static_cast<difference_type>(0);
   }
   string_type str(int sub = 0) const
   {
      sub += 2;
      string_type result;
      if(sub < (int)m_subs.size() && (sub > 0))
      {
         const sub_match<BidiIterator>& s = m_subs[sub];
         if(s.matched)
         {
            result = s;
         }
      }
      return result;
   }
   const_reference operator[](int sub) const
   {
      sub += 2;
      if(sub < (int)m_subs.size() && (sub >= 0))
      {
         return m_subs[sub];
      }
      return m_null;
   }

   const_reference prefix() const
   {
      return (*this)[-1];
   }

   const_reference suffix() const
   {
      return (*this)[-2];
   }
   const_iterator begin() const
   {
      return (m_subs.size() >= 2) ? (m_subs.begin() + 2) : m_subs.end();
   }
   const_iterator end() const
   {
      return m_subs.end();
   }
   // format:
   template <class OutputIterator>
   OutputIterator format(OutputIterator out,
                         const string_type& fmt,
                         match_flag_type flags = format_default) const
   {
      return regex_format(out, *this, fmt, flags);
   }
   string_type format(const string_type& fmt,
                      match_flag_type flags = format_default) const
   {
      return regex_format(*this, fmt, flags);
   }

   allocator_type get_allocator() const
   {
#ifndef BOOST_NO_STD_ALLOCATOR
      return m_subs.get_allocator();
#else
     return allocator_type();
#endif
   }
   void swap(match_results& that)
   {
      std::swap(m_subs, that.m_subs);
      std::swap(m_base, that.m_base);
   }
   bool operator==(const match_results& that)const
   {
      return (m_subs == that.m_subs) && (m_base == that.m_base);
   }
   bool operator!=(const match_results& that)const
   { return !(*this == that); }

#ifdef BOOST_REGEX_MATCH_EXTRA
   typedef typename sub_match<BidiIterator>::capture_sequence_type capture_sequence_type;

   const capture_sequence_type& captures(int i)const
   {
      return (*this)[i].captures();
   }
#endif

   //
   // private access functions:
   void BOOST_REGEX_CALL set_second(BidiIterator i)
   {
      assert(m_subs.size() > 2);
      m_subs[2].second = i;
      m_subs[2].matched = true;
      m_subs[0].first = i;
      m_subs[0].matched = (m_subs[0].first != m_subs[0].second);
      m_null.first = i;
      m_null.second = i;
      m_null.matched = false;
   }

   void BOOST_REGEX_CALL set_second(BidiIterator i, size_type pos, bool m = true)
   {
      pos += 2;
      assert(m_subs.size() > pos);
      m_subs[pos].second = i;
      m_subs[pos].matched = m;
      if(pos == 2)
      {
         m_subs[0].first = i;
         m_subs[0].matched = (m_subs[0].first != m_subs[0].second);
         m_null.first = i;
         m_null.second = i;
         m_null.matched = false;
      }
   }
   void BOOST_REGEX_CALL set_size(size_type n, BidiIterator i, BidiIterator j)
   {
      value_type v(j);
      size_type len = m_subs.size();
      if(len > n + 2)
      {
         m_subs.erase(m_subs.begin()+n+2, m_subs.end());
         std::fill(m_subs.begin(), m_subs.end(), v);
      }
      else
      {
         std::fill(m_subs.begin(), m_subs.end(), v);
         if(n+2 != len)
            m_subs.insert(m_subs.end(), n+2-len, v);
      }
      m_subs[1].first = i;
   }
   void BOOST_REGEX_CALL set_base(BidiIterator pos)
   {
      m_base = pos;
   }
   void BOOST_REGEX_CALL set_first(BidiIterator i)
   {
      // set up prefix:
      m_subs[1].second = i;
      m_subs[1].matched = (m_subs[1].first != i);
      // set up $0:
      m_subs[2].first = i;
      // zero out everything else:
      for(size_type n = 3; n < m_subs.size(); ++n)
      {
         m_subs[n].first = m_subs[n].second = m_subs[0].second;
         m_subs[n].matched = false;
      }
   }
   void BOOST_REGEX_CALL set_first(BidiIterator i, size_type pos)
   {
      assert(pos+2 < m_subs.size());
      if(pos)
         m_subs[pos+2].first = i;
      else
         set_first(i);
   }
   void BOOST_REGEX_CALL maybe_assign(const match_results<BidiIterator, Allocator>& m);


private:
   vector_type            m_subs; // subexpressions
   BidiIterator   m_base; // where the search started from
   sub_match<BidiIterator> m_null; // a null match
};

template <class BidiIterator, class Allocator>
void BOOST_REGEX_CALL match_results<BidiIterator, Allocator>::maybe_assign(const match_results<BidiIterator, Allocator>& m)
{
   const_iterator p1, p2;
   p1 = begin();
   p2 = m.begin();
   BidiIterator base = (*this)[-1].first;
   std::size_t len1 = 0;
   std::size_t len2 = 0;
   std::size_t base1 = 0;
   std::size_t base2 = 0;
   std::size_t i;
   for(i = 0; i < size(); ++i)
   {
      //
      // leftmost takes priority over longest:
      base1 = boost::re_detail::distance(base, p1->first);
      base2 = boost::re_detail::distance(base, p2->first);
      if(base1 < base2) return;
      if(base2 < base1) break;

      len1 = boost::re_detail::distance((BidiIterator)p1->first, (BidiIterator)p1->second);
      len2 = boost::re_detail::distance((BidiIterator)p2->first, (BidiIterator)p2->second);
      if((len1 != len2) || ((p1->matched == false) && (p2->matched == true)))
         break;
      if((p1->matched == true) && (p2->matched == false))
         return;
      ++p1;
      ++p2;
   }
   if(i == size())
      return;
   if(base2 < base1)
      *this = m;
   else if((len2 > len1) || ((p1->matched == false) && (p2->matched == true)) )
      *this = m;
}

template <class BidiIterator, class Allocator>
void swap(match_results<BidiIterator, Allocator>& a, match_results<BidiIterator, Allocator>& b)
{
   a.swap(b);
}

#ifndef BOOST_NO_STD_LOCALE
template <class charT, class traits, class BidiIterator, class Allocator>
std::basic_ostream<charT, traits>&
   operator << (std::basic_ostream<charT, traits>& os,
                const match_results<BidiIterator, Allocator>& s)
{
   return (os << s.str());
}
#else
template <class BidiIterator, class Allocator>
std::ostream& operator << (std::ostream& os,
                           const match_results<BidiIterator, Allocator>& s)
{
   return (os << s.str());
}
#endif

} // namespace boost

#ifdef BOOST_HAS_ABI_HEADERS
#  include BOOST_ABI_SUFFIX
#endif

#endif
