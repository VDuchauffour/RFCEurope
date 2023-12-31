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
  *   FILE         cregex.cpp
  *   VERSION      see <boost/version.hpp>
  *   DESCRIPTION: Declares POSIX API functions
  *                + boost::RegEx high level wrapper.
  */

#ifndef BOOST_RE_CREGEX_HPP_INCLUDED
#define BOOST_RE_CREGEX_HPP_INCLUDED

#ifndef BOOST_REGEX_CONFIG_HPP
#include <boost/regex/config.hpp>
#endif

#ifdef __BORLANDC__
   #pragma option push -a8 -b -Vx -Ve -pc
#endif

/* include these defs only for POSIX compatablity */
#ifdef __cplusplus
namespace boost{
extern "C" {
#endif

#if defined(__cplusplus) && !defined(BOOST_NO_STDC_NAMESPACE)
typedef std::ptrdiff_t regoff_t;
typedef std::size_t regsize_t;
#else
typedef ptrdiff_t regoff_t;
typedef size_t regsize_t;
#endif

typedef struct
{
   unsigned int re_magic;
   unsigned int re_nsub;      /* number of parenthesized subexpressions */
   const char* re_endp;       /* end pointer for REG_PEND */
   void* guts;             /* none of your business :-) */
   unsigned int eflags;       /* none of your business :-) */
} regex_tA;

#ifndef BOOST_NO_WREGEX
typedef struct
{
   unsigned int re_magic;
   unsigned int re_nsub;      /* number of parenthesized subexpressions */
   const wchar_t* re_endp;       /* end pointer for REG_PEND */
   void* guts;             /* none of your business :-) */
   unsigned int eflags;       /* none of your business :-) */
} regex_tW;
#endif

typedef struct
{
   regoff_t rm_so;      /* start of match */
   regoff_t rm_eo;      /* end of match */
} regmatch_t;

/* regcomp() flags */
typedef enum{
   REG_BASIC = 0000,
   REG_EXTENDED = 0001,
   REG_ICASE = 0002,
   REG_NOSUB = 0004,
   REG_NEWLINE = 0010,
   REG_NOSPEC = 0020,
   REG_PEND = 0040,
   REG_DUMP = 0200,
   REG_NOCOLLATE = 0400,
   REG_ESCAPE_IN_LISTS = 01000,
   REG_NEWLINE_ALT = 02000,

   REG_PERL = REG_EXTENDED | REG_NOCOLLATE | REG_ESCAPE_IN_LISTS,
   REG_AWK = REG_EXTENDED | REG_ESCAPE_IN_LISTS,
   REG_GREP = REG_BASIC | REG_NEWLINE_ALT,
   REG_EGREP = REG_EXTENDED | REG_NEWLINE_ALT,

   REG_ASSERT = 15,
   REG_INVARG = 16,
   REG_ATOI = 255,   /* convert name to number (!) */
   REG_ITOA = 0400   /* convert number to name (!) */
} reg_comp_flags;

/* regexec() flags */
typedef enum{
   REG_NOTBOL =    00001,
   REG_NOTEOL =    00002,
   REG_STARTEND =  00004
} reg_exec_flags;

BOOST_REGEX_DECL int BOOST_REGEX_CCALL regcompA(regex_tA*, const char*, int);
BOOST_REGEX_DECL regsize_t BOOST_REGEX_CCALL regerrorA(int, const regex_tA*, char*, regsize_t);
BOOST_REGEX_DECL int BOOST_REGEX_CCALL regexecA(const regex_tA*, const char*, regsize_t, regmatch_t*, int);
BOOST_REGEX_DECL void BOOST_REGEX_CCALL regfreeA(regex_tA*);

#ifndef BOOST_NO_WREGEX
BOOST_REGEX_DECL int BOOST_REGEX_CCALL regcompW(regex_tW*, const wchar_t*, int);
BOOST_REGEX_DECL regsize_t BOOST_REGEX_CCALL regerrorW(int, const regex_tW*, wchar_t*, regsize_t);
BOOST_REGEX_DECL int BOOST_REGEX_CCALL regexecW(const regex_tW*, const wchar_t*, regsize_t, regmatch_t*, int);
BOOST_REGEX_DECL void BOOST_REGEX_CCALL regfreeW(regex_tW*);
#endif

#ifdef UNICODE
#define regcomp regcompW
#define regerror regerrorW
#define regexec regexecW
#define regfree regfreeW
#define regex_t regex_tW
#else
#define regcomp regcompA
#define regerror regerrorA
#define regexec regexecA
#define regfree regfreeA
#define regex_t regex_tA
#endif

/* regerror() flags */
typedef enum
{
  REG_NOERROR = 0,   /* Success.  */
  REG_NOMATCH = 1,      /* Didn't find a match (for regexec).  */

  /* POSIX regcomp return error codes.  (In the order listed in the
     standard.)  */
  REG_BADPAT = 2,    /* Invalid pattern.  */
  REG_ECOLLATE = 3,  /* Undefined collating element.  */
  REG_ECTYPE = 4,    /* Invalid character class name.  */
  REG_EESCAPE = 5,   /* Trailing backslash.  */
  REG_ESUBREG = 6,   /* Invalid back reference.  */
  REG_EBRACK = 7,    /* Unmatched left bracket.  */
  REG_EPAREN = 8,    /* Parenthesis imbalance.  */
  REG_EBRACE = 9,    /* Unmatched \{.  */
  REG_BADBR = 10,    /* Invalid contents of \{\}.  */
  REG_ERANGE = 11,   /* Invalid range end.  */
  REG_ESPACE = 12,   /* Ran out of memory.  */
  REG_BADRPT = 13,   /* No preceding re for repetition op.  */
  REG_EEND = 14,     /* unexpected end of expression */
  REG_ESIZE = 15,    /* expression too big */
  REG_ERPAREN = 16,   /* unmatched right parenthesis */
  REG_EMPTY = 17,    /* empty expression */
  REG_E_MEMORY = REG_ESIZE, /* out of memory */
  REG_E_UNKNOWN = 18 /* unknown error */
} reg_errcode_t;

enum match_flags
{
   match_default = 0,
   match_not_bol = 1,                                // first is not start of line
   match_not_eol = match_not_bol << 1,               // last is not end of line
   match_not_bob = match_not_eol << 1,               // first is not start of buffer
   match_not_eob = match_not_bob << 1,               // last is not end of buffer
   match_not_bow = match_not_eob << 1,               // first is not start of word
   match_not_eow = match_not_bow << 1,               // last is not end of word
   match_not_dot_newline = match_not_eow << 1,       // \n is not matched by '.'
   match_not_dot_null = match_not_dot_newline << 1,  // '\0' is not matched by '.'
   match_prev_avail = match_not_dot_null << 1,       // *--first is a valid expression
   match_init = match_prev_avail << 1,               // internal use
   match_any = match_init << 1,                      // don't care what we match
   match_not_null = match_any << 1,                  // string can't be null
   match_continuous = match_not_null << 1,           // each grep match must continue from
                                                     // uninterupted from the previous one
   match_partial = match_continuous << 1,            // find partial matches

   match_stop = match_partial << 1,                  // stop after first match (grep)
   match_all = match_stop << 1,                      // must find the whole of input even if match_any is set
   match_max = match_all
};

typedef unsigned long match_flag_type;

#ifdef __cplusplus
} // extern "C"
} // namespace
#endif


#ifdef __BORLANDC__
 #if __BORLANDC__ > 0x520
  #pragma option pop
 #endif
#endif


//
// C++ high level wrapper goes here:
//
#if defined(__cplusplus)
#include <string>
#include <vector>
namespace boost{

#ifdef __BORLANDC__
   #if __BORLANDC__ == 0x530
    #pragma option push -a4 -b
   #elif __BORLANDC__ > 0x530
    #pragma option push -a8 -b
   #endif
#endif

class RegEx;

namespace re_detail{

class RegExData;
struct pred1;
struct pred2;
struct pred3;
struct pred4;

}  // namespace re_detail

#if defined(BOOST_MSVC) || defined(__BORLANDC__)
typedef bool (__cdecl *GrepCallback)(const RegEx& expression);
typedef bool (__cdecl *GrepFileCallback)(const char* file, const RegEx& expression);
typedef bool (__cdecl *FindFilesCallback)(const char* file);
#else
typedef bool (*GrepCallback)(const RegEx& expression);
typedef bool (*GrepFileCallback)(const char* file, const RegEx& expression);
typedef bool (*FindFilesCallback)(const char* file);
#endif

class BOOST_REGEX_DECL RegEx
{
private:
   re_detail::RegExData* pdata;
public:
   RegEx();
   RegEx(const RegEx& o);
   ~RegEx();
   explicit RegEx(const char* c, bool icase = false);
   explicit RegEx(const std::string& s, bool icase = false);
   RegEx& operator=(const RegEx& o);
   RegEx& operator=(const char* p);
   RegEx& operator=(const std::string& s){ return this->operator=(s.c_str()); }
   unsigned int SetExpression(const char* p, bool icase = false);
   unsigned int SetExpression(const std::string& s, bool icase = false){ return SetExpression(s.c_str(), icase); }
   std::string Expression()const;
   unsigned int error_code()const;
   //
   // now matching operators:
   //
   bool Match(const char* p, match_flag_type flags = match_default);
   bool Match(const std::string& s, match_flag_type flags = match_default) { return Match(s.c_str(), flags); }
   bool Search(const char* p, match_flag_type flags = match_default);
   bool Search(const std::string& s, match_flag_type flags = match_default) { return Search(s.c_str(), flags); }
   unsigned int Grep(GrepCallback cb, const char* p, match_flag_type flags = match_default);
   unsigned int Grep(GrepCallback cb, const std::string& s, match_flag_type flags = match_default) { return Grep(cb, s.c_str(), flags); }
   unsigned int Grep(std::vector<std::string>& v, const char* p, match_flag_type flags = match_default);
   unsigned int Grep(std::vector<std::string>& v, const std::string& s, match_flag_type flags = match_default) { return Grep(v, s.c_str(), flags); }
   unsigned int Grep(std::vector<std::size_t>& v, const char* p, match_flag_type flags = match_default);
   unsigned int Grep(std::vector<std::size_t>& v, const std::string& s, match_flag_type flags = match_default) { return Grep(v, s.c_str(), flags); }
#ifndef BOOST_REGEX_NO_FILEITER
   unsigned int GrepFiles(GrepFileCallback cb, const char* files, bool recurse = false, match_flag_type flags = match_default);
   unsigned int GrepFiles(GrepFileCallback cb, const std::string& files, bool recurse = false, match_flag_type flags = match_default) { return GrepFiles(cb, files.c_str(), recurse, flags); }
   unsigned int FindFiles(FindFilesCallback cb, const char* files, bool recurse = false, match_flag_type flags = match_default);
   unsigned int FindFiles(FindFilesCallback cb, const std::string& files, bool recurse = false, match_flag_type flags = match_default) { return FindFiles(cb, files.c_str(), recurse, flags); }
#endif

   std::string Merge(const std::string& in, const std::string& fmt,
                       bool copy = true, match_flag_type flags = match_default);
   std::string Merge(const char* in, const char* fmt,
                       bool copy = true, match_flag_type flags = match_default);

   std::size_t Split(std::vector<std::string>& v, std::string& s, match_flag_type flags = match_default, unsigned max_count = ~0);
   //
   // now operators for returning what matched in more detail:
   //
   std::size_t Position(int i = 0)const;
   std::size_t Length(int i = 0)const;
   bool Matched(int i = 0)const;
   unsigned int Line()const;
   unsigned int Marks()const;
   std::string What(int i = 0)const;
   std::string operator[](int i)const { return What(i); }

   static const unsigned int npos;

   friend struct re_detail::pred1;
   friend struct re_detail::pred2;
   friend struct re_detail::pred3;
   friend struct re_detail::pred4;
};

#ifdef __BORLANDC__
  #pragma option pop
#endif

} // namespace boost

#endif

#endif // include guard
