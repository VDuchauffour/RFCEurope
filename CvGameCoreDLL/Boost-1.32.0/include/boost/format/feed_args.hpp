// ----------------------------------------------------------------------------
//  feed_args.hpp :  functions for processing each argument
//                      (feed, feed_manip, and distribute)
// ----------------------------------------------------------------------------

//  Copyright Samuel Krempp 2003. Use, modification, and distribution are
//  subject to the Boost Software License, Version 1.0. (See accompanying
//  file LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)

//  See http://www.boost.org/libs/format for library home page

// ----------------------------------------------------------------------------

#ifndef BOOST_FORMAT_FEED_ARGS_HPP
#define BOOST_FORMAT_FEED_ARGS_HPP

#include <boost/config.hpp>
#include <boost/assert.hpp>
#include <boost/throw_exception.hpp>

#include <boost/format/format_class.hpp>
#include <boost/format/group.hpp>
#include <boost/format/detail/msvc_disambiguater.hpp>

namespace boost {
namespace io {
namespace detail {

    template<class Ch, class Tr, class Alloc>
    void mk_str( std::basic_string<Ch,Tr, Alloc> & res,
                 const Ch * beg,
                 std::streamsize size,
                 std::streamsize w,
                 const Ch fill_char,
                 std::ios_base::fmtflags f,
                 const Ch prefix_space, // 0 if no space-padding
                 bool center)
    // applies centered/left/right  padding  to the string  [beg, beg+size[
    // Effects : the result is placed in res.
    {
        res.resize(0);
        std::streamsize n=w-size-!!prefix_space;
        std::streamsize n_after = 0, n_before = 0;

        if(n<=0) { // no need to pad.
            res.reserve(size + !!prefix_space);
        }
        else {
            res.reserve(w); // allocate once for the 2 inserts
            if(center)
                n_after = n/2, n_before = n - n_after;
            else
                if(f & std::ios_base::left)
                    n_after = n;
                else
                    n_before = n;
        }
        // now make the res string :
        if(n_before) res.append(n_before, fill_char);
        if(prefix_space)
            res.append(1, prefix_space);
        res.append(beg, size);
        if(n_after) res.append(n_after, fill_char);
    } // -mk_str(..)


#if BOOST_WORKAROUND( BOOST_MSVC, <= 1300)
// MSVC needs to be tricked to disambiguate this simple overload..
// the trick is in "boost/format/msvc_disambiguater.hpp"

    template< class Ch, class Tr, class T> inline
    void put_head (BOOST_IO_STD basic_ostream<Ch, Tr> & os, const T& x ) {
        disambiguater<Ch, Tr, T>::put_head(os, x, 1L);
    }
    template< class Ch, class Tr, class T> inline
    void put_last (BOOST_IO_STD basic_ostream<Ch, Tr> & os, const T& x ) {
        disambiguater<Ch, Tr, T>::put_last(os, x, 1L);
    }

#else

    template< class Ch, class Tr, class T> inline
    void put_head (BOOST_IO_STD basic_ostream<Ch, Tr> &, const T& ) {
    }

    template< class Ch, class Tr, class T> inline
    void put_head( BOOST_IO_STD basic_ostream<Ch, Tr> & os, const group1<T>& x ) {
        os << group_head(x.a1_); // send the first N-1 items, not the last
    }

    template< class Ch, class Tr, class T> inline
    void put_last( BOOST_IO_STD basic_ostream<Ch, Tr> & os, const T& x ) {
        os << x ;
    }

    template< class Ch, class Tr, class T> inline
    void put_last( BOOST_IO_STD basic_ostream<Ch, Tr> & os, const group1<T>& x ) {
        os << group_last(x.a1_); // this selects the last element
    }

#ifndef BOOST_NO_OVERLOAD_FOR_NON_CONST
    template< class Ch, class Tr, class T> inline
    void put_head( BOOST_IO_STD basic_ostream<Ch, Tr> &, T& ) {
    }

    template< class Ch, class Tr, class T> inline
    void put_last( BOOST_IO_STD basic_ostream<Ch, Tr> & os, T& x) {
        os << x ;
    }
#endif
#endif  // -msvc workaround


    template< class Ch, class Tr, class Alloc, class T>
    void put( T x,
              const format_item<Ch, Tr, Alloc>& specs,
              typename basic_format<Ch, Tr, Alloc>::string_type& res,
              typename basic_format<Ch, Tr, Alloc>::internal_streambuf_t & buf,
              io::detail::locale_t *loc_p = NULL)
    {
        // does the actual conversion of x, with given params, into a string
        // using the supplied stringbuf.

        typedef typename basic_format<Ch, Tr, Alloc>::string_type   string_type;
        typedef typename basic_format<Ch, Tr, Alloc>::format_item_t format_item_t;
        typedef typename string_type::size_type size_type;

        basic_oaltstringstream<Ch, Tr, Alloc>  oss( &buf);
        specs.fmtstate_.apply_on(oss, loc_p);

        // the stream format state can be modified by manipulators in the argument :
        put_head( oss, x );
        // in case x is a group, apply the manip part of it,
        // in order to find width

        const std::ios_base::fmtflags fl=oss.flags();
        const bool internal = (fl & std::ios_base::internal) != 0;
        const std::streamsize w = oss.width();
        const bool two_stepped_padding= internal && (w!=0);

        res.resize(0);
        if(! two_stepped_padding) {
            if(w>0) // handle padding via mk_str, not natively in stream
                oss.width(0);
            put_last( oss, x);
            const Ch * res_beg = buf.pbase();
            Ch prefix_space = 0;
            if(specs.pad_scheme_ & format_item_t::spacepad)
                if(buf.pcount()== 0 ||
                   (res_beg[0] !=oss.widen('+') && res_beg[0] !=oss.widen('-')  ))
                    prefix_space = oss.widen(' ');
            std::streamsize res_size = (std::min)(
                static_cast<std::streamsize>(specs.truncate_ - !!prefix_space),
                buf.pcount() );
            mk_str(res, res_beg, res_size, w, oss.fill(), fl,
                   prefix_space, (specs.pad_scheme_ & format_item_t::centered) !=0 );
        }
        else  { // 2-stepped padding
            // internal can be implied by zeropad, or user-set.
            // left, right, and centered alignment overrule internal,
            // but spacepad or truncate might be mixed with internal (using manipulator)
            put_last( oss, x); // may pad
            const Ch * res_beg = buf.pbase();
            std::streamsize res_size = buf.pcount();
            bool prefix_space=false;
            if(specs.pad_scheme_ & format_item_t::spacepad)
                if(buf.pcount()== 0 ||
                   (res_beg[0] !=oss.widen('+') && res_beg[0] !=oss.widen('-')  ))
                    prefix_space = true;
            if(res_size == w && w<=specs.truncate_ && !prefix_space) {
                // okay, only one thing was printed and padded, so res is fine
                res.assign(res_beg, res_size);
            }
            else { //   length w exceeded
                // either it was multi-output with first output padding up all width..
                // either it was one big arg and we are fine.
                // Note that res_size<w is possible  (in case of bad user-defined formatting)
                res.assign(res_beg, res_size);
                res_beg=NULL;  // invalidate pointers.

                // make a new stream, to start re-formatting from scratch :
                buf.clear_buffer();
                basic_oaltstringstream<Ch, Tr, Alloc>  oss2( &buf);
                specs.fmtstate_.apply_on(oss2, loc_p);
                put_head( oss2, x );

                oss2.width(0);
                if(prefix_space)
                    oss2 << ' ';
                put_last(oss2, x );
                if(buf.pcount()==0 && specs.pad_scheme_ & format_item_t::spacepad) {
                    prefix_space =true;
                    oss2 << ' ';
                }
                // we now have the minimal-length output
                const Ch * tmp_beg = buf.pbase();
                std::streamsize tmp_size = (std::min)(static_cast<std::streamsize>(specs.truncate_),
                                                    buf.pcount() );

                std::streamsize d;
                if( (d=w - tmp_size) <=0 ) {
                    // minimal length is already >= w, so no padding (cool!)
                        res.assign(tmp_beg, tmp_size);
                }
                else { // hum..  we need to pad (multi_output, or spacepad present)
                    std::streamsize i = prefix_space;
                    //find where we should pad
                    std::streamsize sz = (std::min)(res_size+prefix_space, tmp_size);
                    for(; i<sz && tmp_beg[i] == res[i-prefix_space]; ++i) {}
                    if(i>=tmp_size) i=prefix_space;
                    res.assign(tmp_beg, i);
                    if(d>0) res.append(static_cast<size_type>( d ), oss2.fill());
                    res.append(tmp_beg+i, tmp_size-i);
                    BOOST_ASSERT(i+(tmp_size-i)+(std::max)(d,(std::streamsize)0) == w);
                    BOOST_ASSERT(res.size() == (std::size_t)w);
                }
            }
        }
        buf.clear_buffer();
    } // end- put(..)


    template< class Ch, class Tr, class Alloc, class T>
    void distribute (basic_format<Ch,Tr, Alloc>& self, T x) {
        // call put(x, ..) on every occurence of the current argument :
        if(self.cur_arg_ >= self.num_args_)  {
            if( self.exceptions() & too_many_args_bit )
                boost::throw_exception(too_many_args(self.cur_arg_, self.num_args_));
            else return;
        }
        for(unsigned long i=0; i < self.items_.size(); ++i) {
            if(self.items_[i].argN_ == self.cur_arg_) {
                put<Ch, Tr, Alloc, T> (x, self.items_[i], self.items_[i].res_,
                                self.buf_, boost::get_pointer(self.loc_) );
            }
        }
    }

    template<class Ch, class Tr, class Alloc, class T>
    basic_format<Ch, Tr, Alloc>&
    feed (basic_format<Ch,Tr, Alloc>& self, T x) {
        if(self.dumped_) self.clear();
        distribute<Ch, Tr, Alloc, T> (self, x);
        ++self.cur_arg_;
        if(self.bound_.size() != 0) {
                while( self.cur_arg_ < self.num_args_ && self.bound_[self.cur_arg_] )
                    ++self.cur_arg_;
        }
        return self;
    }

} // namespace detail
} // namespace io
} // namespace boost


#endif //  BOOST_FORMAT_FEED_ARGS_HPP
