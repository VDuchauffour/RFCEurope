/*
 *
 * Copyright (c) 2002
 * Dr John Maddock
 *
 * Use, modification and distribution are subject to the
 * Boost Software License, Version 1.0. (See accompanying file
 * LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
 *
 */

 /*
  *   LOCATION:    see http://www.boost.org for most recent version.
  *   FILE         perl_matcher_common.cpp
  *   VERSION      see <boost/version.hpp>
  *   DESCRIPTION: Definitions of perl_matcher member functions that are
  *                specific to the recursive implementation.
  */

#ifndef BOOST_REGEX_V4_PERL_MATCHER_RECURSIVE_HPP
#define BOOST_REGEX_V4_PERL_MATCHER_RECURSIVE_HPP

#ifdef BOOST_HAS_ABI_HEADERS
#  include BOOST_ABI_PREFIX
#endif

namespace boost{
namespace re_detail{

template <class BidiIterator>
class backup_subex
{
   int index;
   sub_match<BidiIterator> sub;
public:
   template <class A>
   backup_subex(const match_results<BidiIterator, A>& w, int i)
      : index(i), sub(w[i], false) {}
   template <class A>
   void restore(match_results<BidiIterator, A>& w)
   {
      w.set_first(sub.first, index);
      w.set_second(sub.second, index, sub.matched);
   }
   const sub_match<BidiIterator>& get() { return sub; }
};

template <class BidiIterator, class Allocator, class traits, class Allocator2>
bool perl_matcher<BidiIterator, Allocator, traits, Allocator2>::match_all_states()
{
   static matcher_proc_type const s_match_vtable[26] =
   {
      (&perl_matcher<BidiIterator, Allocator, traits, Allocator2>::match_startmark),
      &perl_matcher<BidiIterator, Allocator, traits, Allocator2>::match_endmark,
      &perl_matcher<BidiIterator, Allocator, traits, Allocator2>::match_literal,
      &perl_matcher<BidiIterator, Allocator, traits, Allocator2>::match_start_line,
      &perl_matcher<BidiIterator, Allocator, traits, Allocator2>::match_end_line,
      &perl_matcher<BidiIterator, Allocator, traits, Allocator2>::match_wild,
      &perl_matcher<BidiIterator, Allocator, traits, Allocator2>::match_match,
      &perl_matcher<BidiIterator, Allocator, traits, Allocator2>::match_word_boundary,
      &perl_matcher<BidiIterator, Allocator, traits, Allocator2>::match_within_word,
      &perl_matcher<BidiIterator, Allocator, traits, Allocator2>::match_word_start,
      &perl_matcher<BidiIterator, Allocator, traits, Allocator2>::match_word_end,
      &perl_matcher<BidiIterator, Allocator, traits, Allocator2>::match_buffer_start,
      &perl_matcher<BidiIterator, Allocator, traits, Allocator2>::match_buffer_end,
      &perl_matcher<BidiIterator, Allocator, traits, Allocator2>::match_backref,
      &perl_matcher<BidiIterator, Allocator, traits, Allocator2>::match_long_set,
      &perl_matcher<BidiIterator, Allocator, traits, Allocator2>::match_set,
      &perl_matcher<BidiIterator, Allocator, traits, Allocator2>::match_jump,
      &perl_matcher<BidiIterator, Allocator, traits, Allocator2>::match_alt,
      &perl_matcher<BidiIterator, Allocator, traits, Allocator2>::match_rep,
      &perl_matcher<BidiIterator, Allocator, traits, Allocator2>::match_combining,
      &perl_matcher<BidiIterator, Allocator, traits, Allocator2>::match_soft_buffer_end,
      &perl_matcher<BidiIterator, Allocator, traits, Allocator2>::match_restart_continue,
      (::boost::is_random_access_iterator<BidiIterator>::value ? &perl_matcher<BidiIterator, Allocator, traits, Allocator2>::match_dot_repeat_fast : &perl_matcher<BidiIterator, Allocator, traits, Allocator2>::match_dot_repeat_slow),
      &perl_matcher<BidiIterator, Allocator, traits, Allocator2>::match_char_repeat,
      &perl_matcher<BidiIterator, Allocator, traits, Allocator2>::match_set_repeat,
      &perl_matcher<BidiIterator, Allocator, traits, Allocator2>::match_long_set_repeat,
   };

   if(state_count > max_state_count)
      raise_error(traits_inst, REG_ESPACE);
   while(pstate)
   {
      matcher_proc_type proc = s_match_vtable[pstate->type];
      ++state_count;
      if(!(this->*proc)())
      {
         if((m_match_flags & match_partial) && (position == last))
            m_has_partial_match = true;
         return 0;
      }
   }
   return true;
}

template <class BidiIterator, class Allocator, class traits, class Allocator2>
bool perl_matcher<BidiIterator, Allocator, traits, Allocator2>::match_startmark()
{
   int index = static_cast<const re_brace*>(pstate)->index;
   bool r = true;
   switch(index)
   {
   case 0:
      pstate = pstate->next.p;
      break;
   case -1:
   case -2:
      {
         // forward lookahead assert:
         BidiIterator old_position(position);
         const re_syntax_base* next_pstate = static_cast<const re_jump*>(pstate->next.p)->alt.p->next.p;
         pstate = pstate->next.p->next.p;
         r = match_all_states();
         pstate = next_pstate;
         position = old_position;
         if((r && (index != -1)) || (!r && (index != -2)))
            r = false;
         else
            r = true;
         break;
      }
   case -3:
      {
         // independent sub-expression:
         const re_syntax_base* next_pstate = static_cast<const re_jump*>(pstate->next.p)->alt.p->next.p;
         pstate = pstate->next.p->next.p;
         r = match_all_states();
         pstate = next_pstate;
#ifdef BOOST_REGEX_MATCH_EXTRA
         if(r && (m_match_flags & match_extra))
         {
            //
            // our captures have been stored in *m_presult
            // we need to unpack them, and insert them
            // back in the right order when we unwind the stack:
            //
            unsigned i;
            match_results<BidiIterator, Allocator> tm(*m_presult);
            for(i = 0; i < tm.size(); ++i)
               (*m_presult)[i].get_captures().clear();
            // match everything else:
            r = match_all_states();
            // now place the stored captures back:
            for(i = 0; i < tm.size(); ++i)
            {
               typedef typename sub_match<BidiIterator>::capture_sequence_type seq;
               seq& s1 = (*m_presult)[i].get_captures();
               const seq& s2 = tm[i].captures();
               s1.insert(
                  s1.end(),
                  s2.begin(),
                  s2.end());
            }
         }
#endif
         break;
      }
   default:
   {
      assert(index > 0);
      if((m_match_flags & match_nosubs) == 0)
      {
         backup_subex<BidiIterator> sub(*m_presult, index);
         m_presult->set_first(position, index);
         pstate = pstate->next.p;
         r = match_all_states();
         if(r == false)
            sub.restore(*m_presult);
#ifdef BOOST_REGEX_MATCH_EXTRA
         //
         // we have a match, push the capture information onto the stack:
         //
         else if(sub.get().matched && (match_extra & m_match_flags))
            ((*m_presult)[index]).get_captures().push_back(sub.get());
#endif
      }
      else
      {
         pstate = pstate->next.p;
      }
      break;
   }
   }
   return r;
}

template <class BidiIterator, class Allocator, class traits, class Allocator2>
bool perl_matcher<BidiIterator, Allocator, traits, Allocator2>::match_alt()
{
   bool take_first, take_second;
   const re_jump* jmp = static_cast<const re_jump*>(pstate);

   // find out which of these two alternatives we need to take:
   if(position == last)
   {
      take_first = jmp->can_be_null & mask_take;
      take_second = jmp->can_be_null & mask_skip;
   }
   else
   {
      take_first = access::can_start(*position, jmp->_map, (unsigned char)mask_take);
      take_second = access::can_start(*position, jmp->_map, (unsigned char)mask_skip);
  }

   if(take_first)
   {
      // we can take the first alternative,
      // see if we need to push next alternative:
      if(take_second)
      {
         BidiIterator oldposition(position);
         const re_syntax_base* old_pstate = jmp->alt.p;
         pstate = pstate->next.p;
         if(!match_all_states())
         {
            pstate = old_pstate;
            position = oldposition;
         }
         return true;
      }
      pstate = pstate->next.p;
      return true;
   }
   if(take_second)
   {
      pstate = jmp->alt.p;
      return true;
   }
   return false;  // neither option is possible
}

template <class BidiIterator, class Allocator, class traits, class Allocator2>
bool perl_matcher<BidiIterator, Allocator, traits, Allocator2>::match_rep()
{
#ifdef BOOST_MSVC
#pragma warning(push)
#pragma warning(disable:4127 4244)
#endif
   const re_repeat* rep = static_cast<const re_repeat*>(pstate);
   if(next_count->get_id() != rep->id)
   {
      // we're moving to a different repeat from the last
      // one, so set up a counter object and recurse:
      repeater_count<BidiIterator> r(rep->id, &next_count, position);
      return match_rep();
   }
   //
   // If we've had at least one repeat already, and the last one
   // matched the NULL string then set the repeat count to
   // maximum:
   //
   next_count->check_null_repeat(position, rep->max);

   // find out which of these two alternatives we need to take:
   bool take_first, take_second;
   if(position == last)
   {
      take_first = rep->can_be_null & mask_take;
      take_second = rep->can_be_null & mask_skip;
   }
   else
   {
      take_first = access::can_start(*position, rep->_map, (unsigned char)mask_take);
      take_second = access::can_start(*position, rep->_map, (unsigned char)mask_skip);
   }

   if(next_count->get_count() < rep->min)
   {
      // we must take the repeat:
      if(take_first)
      {
         // increase the counter:
         ++(*next_count);
         pstate = rep->next.p;
         return match_all_states();
      }
      return false;
   }

   if(rep->greedy)
   {
      // try and take the repeat if we can:
      if((next_count->get_count() < rep->max) && take_first)
      {
         // store position in case we fail:
         BidiIterator pos = position;
         // increase the counter:
         ++(*next_count);
         pstate = rep->next.p;
         if(match_all_states())
            return true;
         // failed repeat, reset posistion and fall through for alternative:
         position = pos;
      }
      if(take_second)
      {
         pstate = rep->alt.p;
         return true;
      }
      return false; // can't take anything, fail...
   }
   else // non-greedy
   {
      // try and skip the repeat if we can:
      if(take_second)
      {
         // store position in case we fail:
         BidiIterator pos = position;
         pstate = rep->alt.p;
         if(match_all_states())
            return true;
         // failed alternative, reset posistion and fall through for repeat:
         position = pos;
      }
      if((next_count->get_count() < rep->max) && take_first)
      {
         // increase the counter:
         ++(*next_count);
         pstate = rep->next.p;
         return match_all_states();
      }
   }
   return false;
#ifdef BOOST_MSVC
#pragma warning(pop)
#endif
}

template <class BidiIterator, class Allocator, class traits, class Allocator2>
bool perl_matcher<BidiIterator, Allocator, traits, Allocator2>::match_dot_repeat_slow()
{
#ifdef BOOST_MSVC
#pragma warning(push)
#pragma warning(disable:4127)
#endif
   unsigned count = 0;
   const re_repeat* rep = static_cast<const re_repeat*>(pstate);
   re_syntax_base* psingle = rep->next.p;
   // match compulsary repeats first:
   while(count < rep->min)
   {
      pstate = psingle;
      if(!match_wild())
         return false;
      ++count;
   }
   if(rep->greedy)
   {
      // normal repeat:
      while(count < rep->max)
      {
         pstate = psingle;
         if(!match_wild())
            break;
         ++count;
      }
      if((rep->leading) && (count < rep->max))
         restart = position;
      pstate = rep;
      return backtrack_till_match(count - rep->min);
   }
   else
   {
      // non-greedy, keep trying till we get a match:
      BidiIterator save_pos;
      do
      {
         if((rep->leading) && (rep->max == UINT_MAX))
            restart = position;
         pstate = rep->alt.p;
         save_pos = position;
         ++state_count;
         if(match_all_states())
            return true;
         if(count >= rep->max)
            return false;
         ++count;
         pstate = psingle;
         position = save_pos;
         if(!match_wild())
            return false;
      }while(true);
   }
#ifdef BOOST_MSVC
#pragma warning(pop)
#endif
}

template <class BidiIterator, class Allocator, class traits, class Allocator2>
bool perl_matcher<BidiIterator, Allocator, traits, Allocator2>::match_dot_repeat_fast()
{
#ifdef BOOST_MSVC
#pragma warning(push)
#pragma warning(disable:4127)
#endif
   if(m_match_flags & (match_not_dot_newline | match_not_dot_null))
      return match_dot_repeat_slow();
   //
   // start by working out how much we can skip:
   //
   const re_repeat* rep = static_cast<const re_repeat*>(pstate);
   unsigned count = (std::min)(static_cast<unsigned>(re_detail::distance(position, last)), (rep->greedy ? rep->max : rep->min));
   if(rep->min > count)
      return false;  // not enough text left to match
   std::advance(position, count);
   if((rep->leading) && (count < rep->max) && (rep->greedy))
      restart = position;
   if(rep->greedy)
      return backtrack_till_match(count - rep->min);

   // non-greedy, keep trying till we get a match:
   BidiIterator save_pos;
   do
   {
      while((position != last) && (count < rep->max) && !access::can_start(*position, rep->_map, mask_skip))
      {
         ++position;
         ++count;
      }
      if((rep->leading) && (count == UINT_MAX))
         restart = position;
      pstate = rep->alt.p;
      save_pos = position;
      ++state_count;
      if(match_all_states())
         return true;
      if(count >= rep->max)
         return false;
      if(position == last)
         return false;
      position = ++save_pos;
      ++count;
   }while(true);
#ifdef BOOST_MSVC
#pragma warning(pop)
#endif
}

template <class BidiIterator, class Allocator, class traits, class Allocator2>
bool perl_matcher<BidiIterator, Allocator, traits, Allocator2>::match_char_repeat()
{
#ifdef BOOST_MSVC
#pragma warning(push)
#pragma warning(disable:4127)
#endif
#ifdef __BORLANDC__
#pragma option push -w-8008 -w-8066 -w-8004
#endif
   const re_repeat* rep = static_cast<const re_repeat*>(pstate);
   assert(1 == static_cast<const re_literal*>(rep->next.p)->length);
   const char_type what = *reinterpret_cast<const char_type*>(static_cast<const re_literal*>(rep->next.p) + 1);
   unsigned count = 0;
   //
   // start by working out how much we can skip:
   //
   unsigned desired = rep->greedy ? rep->max : rep->min;
   if(::boost::is_random_access_iterator<BidiIterator>::value)
   {
      BidiIterator end = position;
      std::advance(end, (std::min)((unsigned)re_detail::distance(position, last), desired));
      BidiIterator origin(position);
      while((position != end) && (traits_inst.translate(*position, icase) == what))
      {
         ++position;
      }
      count = (unsigned)re_detail::distance(origin, position);
   }
   else
   {
      while((count < desired) && (position != last) && (traits_inst.translate(*position, icase) == what))
      {
         ++position;
         ++count;
      }
   }
   if((rep->leading) && (count < rep->max) && (rep->greedy))
      restart = position;
   if(count < rep->min)
      return false;

   if(rep->greedy)
      return backtrack_till_match(count - rep->min);

   // non-greedy, keep trying till we get a match:
   BidiIterator save_pos;
   do
   {
      while((position != last) && (count < rep->max) && !access::can_start(*position, rep->_map, mask_skip))
      {
         if((traits_inst.translate(*position, icase) == what))
         {
            ++position;
            ++count;
         }
         else
            return false;  // counldn't repeat even though it was the only option
      }
      if((rep->leading) && (rep->max == UINT_MAX))
         restart = position;
      pstate = rep->alt.p;
      save_pos = position;
      ++state_count;
      if(match_all_states())
         return true;
      if(count >= rep->max)
         return false;
      if(position == last)
         return false;
      position = save_pos;
      if(traits_inst.translate(*position, icase) == what)
      {
         ++position;
         ++count;
      }
      else
      {
         return false;
      }
   }while(true);
#ifdef __BORLANDC__
#pragma option pop
#endif
#ifdef BOOST_MSVC
#pragma warning(pop)
#endif
}

template <class BidiIterator, class Allocator, class traits, class Allocator2>
bool perl_matcher<BidiIterator, Allocator, traits, Allocator2>::match_set_repeat()
{
#ifdef BOOST_MSVC
#pragma warning(push)
#pragma warning(disable:4127)
#endif
#ifdef __BORLANDC__
#pragma option push -w-8008 -w-8066 -w-8004
#endif
   const re_repeat* rep = static_cast<const re_repeat*>(pstate);
   const unsigned char* map = static_cast<const re_set*>(rep->next.p)->_map;
   unsigned count = 0;
   //
   // start by working out how much we can skip:
   //
   unsigned desired = rep->greedy ? rep->max : rep->min;
   if(::boost::is_random_access_iterator<BidiIterator>::value)
   {
      BidiIterator end = position;
      std::advance(end, (std::min)((unsigned)re_detail::distance(position, last), desired));
      BidiIterator origin(position);
      while((position != end) && map[(traits_uchar_type)traits_inst.translate(*position, icase)])
      {
         ++position;
      }
      count = (unsigned)re_detail::distance(origin, position);
   }
   else
   {
      while((count < desired) && (position != last) && map[(traits_uchar_type)traits_inst.translate(*position, icase)])
      {
         ++position;
         ++count;
      }
   }
   if((rep->leading) && (count < rep->max) && (rep->greedy))
      restart = position;
   if(count < rep->min)
      return false;

   if(rep->greedy)
      return backtrack_till_match(count - rep->min);

   // non-greedy, keep trying till we get a match:
   BidiIterator save_pos;
   do
   {
      while((position != last) && (count < rep->max) && !access::can_start(*position, rep->_map, mask_skip))
      {
         if(map[(traits_uchar_type)traits_inst.translate(*position, icase)])
         {
            ++position;
            ++count;
         }
         else
            return false;  // counldn't repeat even though it was the only option
      }
      if((rep->leading) && (rep->max == UINT_MAX))
         restart = position;
      pstate = rep->alt.p;
      save_pos = position;
      ++state_count;
      if(match_all_states())
         return true;
      if(count >= rep->max)
         return false;
      if(position == last)
         return false;
      position = save_pos;
      if(map[(traits_uchar_type)traits_inst.translate(*position, icase)])
      {
         ++position;
         ++count;
      }
      else
      {
         return false;
      }
   }while(true);
#ifdef __BORLANDC__
#pragma option pop
#endif
#ifdef BOOST_MSVC
#pragma warning(pop)
#endif
}

template <class BidiIterator, class Allocator, class traits, class Allocator2>
bool perl_matcher<BidiIterator, Allocator, traits, Allocator2>::match_long_set_repeat()
{
#ifdef BOOST_MSVC
#pragma warning(push)
#pragma warning(disable:4127)
#endif
#ifdef __BORLANDC__
#pragma option push -w-8008 -w-8066 -w-8004
#endif
   const re_repeat* rep = static_cast<const re_repeat*>(pstate);
   const re_set_long* set = static_cast<const re_set_long*>(pstate->next.p);
   unsigned count = 0;
   //
   // start by working out how much we can skip:
   //
   unsigned desired = rep->greedy ? rep->max : rep->min;
   if(::boost::is_random_access_iterator<BidiIterator>::value)
   {
      BidiIterator end = position;
      std::advance(end, (std::min)((unsigned)re_detail::distance(position, last), desired));
      BidiIterator origin(position);
      while((position != end) && (position != re_is_set_member(position, last, set, re)))
      {
         ++position;
      }
      count = (unsigned)re_detail::distance(origin, position);
   }
   else
   {
      while((count < desired) && (position != last) && (position != re_is_set_member(position, last, set, re)))
      {
         ++position;
         ++count;
      }
   }
   if((rep->leading) && (count < rep->max) && (rep->greedy))
      restart = position;
   if(count < rep->min)
      return false;

   if(rep->greedy)
      return backtrack_till_match(count - rep->min);

   // non-greedy, keep trying till we get a match:
   BidiIterator save_pos;
   do
   {
      while((position != last) && (count < rep->max) && !access::can_start(*position, rep->_map, mask_skip))
      {
         if(position != re_is_set_member(position, last, set, re))
         {
            ++position;
            ++count;
         }
         else
            return false;  // counldn't repeat even though it was the only option
      }
      if((rep->leading) && (rep->max == UINT_MAX))
         restart = position;
      pstate = rep->alt.p;
      save_pos = position;
      ++state_count;
      if(match_all_states())
         return true;
      if(count >= rep->max)
         return false;
      if(position == last)
         return false;
      position = save_pos;
      if(position != re_is_set_member(position, last, set, re))
      {
         ++position;
         ++count;
      }
      else
      {
         return false;
      }
   }while(true);
#ifdef __BORLANDC__
#pragma option pop
#endif
#ifdef BOOST_MSVC
#pragma warning(pop)
#endif
}

template <class BidiIterator, class Allocator, class traits, class Allocator2>
bool perl_matcher<BidiIterator, Allocator, traits, Allocator2>::backtrack_till_match(unsigned count)
{
#ifdef BOOST_MSVC
#pragma warning(push)
#pragma warning(disable:4127)
#endif
   if((m_match_flags & match_partial) && (position == last))
      m_has_partial_match = true;

   const re_repeat* rep = static_cast<const re_repeat*>(pstate);
   BidiIterator backtrack = position;
   if(position == last)
   {
      if(rep->can_be_null & mask_skip)
      {
         pstate = rep->alt.p;
         if(match_all_states())
            return true;
      }
      if(count)
      {
         position = --backtrack;
         --count;
      }
      else
         return false;
   }
   do
   {
      while(count && !access::can_start(*position, rep->_map, mask_skip))
      {
         --position;
         --count;
         ++state_count;
      }
      pstate = rep->alt.p;
      backtrack = position;
      if(match_all_states())
         return true;
      if(count == 0)
         return false;
      position = --backtrack;
      ++state_count;
      --count;
   }while(true);
#ifdef BOOST_MSVC
#pragma warning(pop)
#endif
}

} // namespace re_detail
} // namespace boost

#ifdef BOOST_HAS_ABI_HEADERS
#  include BOOST_ABI_SUFFIX
#endif

#endif
