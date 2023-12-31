//
//=======================================================================
// Copyright 1997-2001 University of Notre Dame.
// Authors: Jeremy G. Siek, Lie-Quan Lee, Andrew Lumsdaine
//
// This file is part of the Boost Graph Library
//
// You should have received a copy of the License Agreement for the
// Boost Graph Library along with the software; see the file LICENSE.
// If not, contact Office of Research, University of Notre Dame, Notre
// Dame, IN 46556.
//
// Permission to modify the code and to distribute modified code is
// granted, provided the text of this NOTICE is retained, a notice that
// the code was modified is included with the above COPYRIGHT NOTICE and
// with the COPYRIGHT NOTICE in the LICENSE file, and that the LICENSE
// file is distributed with the modified code.
//
// LICENSOR MAKES NO REPRESENTATIONS OR WARRANTIES, EXPRESS OR IMPLIED.
// By way of example, but not limitation, Licensor MAKES NO
// REPRESENTATIONS OR WARRANTIES OF MERCHANTABILITY OR FITNESS FOR ANY
// PARTICULAR PURPOSE OR THAT THE USE OF THE LICENSED SOFTWARE COMPONENTS
// OR DOCUMENTATION WILL NOT INFRINGE ANY PATENTS, COPYRIGHTS, TRADEMARKS
// OR OTHER RIGHTS.
//=======================================================================
//

/*
  This file implements the following functions:


  template <typename VertexListGraph, typename MutableGraph>
  void copy_graph(const VertexListGraph& g_in, MutableGraph& g_out)

  template <typename VertexListGraph, typename MutableGraph,
    class P, class T, class R>
  void copy_graph(const VertexListGraph& g_in, MutableGraph& g_out,
                  const bgl_named_params<P, T, R>& params)


  template <typename IncidenceGraph, typename MutableGraph>
  typename graph_traits<MutableGraph>::vertex_descriptor
  copy_component(IncidenceGraph& g_in,
                 typename graph_traits<IncidenceGraph>::vertex_descriptor src,
                 MutableGraph& g_out)

  template <typename IncidenceGraph, typename MutableGraph,
           typename P, typename T, typename R>
  typename graph_traits<MutableGraph>::vertex_descriptor
  copy_component(IncidenceGraph& g_in,
                 typename graph_traits<IncidenceGraph>::vertex_descriptor src,
                 MutableGraph& g_out,
                 const bgl_named_params<P, T, R>& params)
 */


#ifndef BOOST_GRAPH_COPY_HPP
#define BOOST_GRAPH_COPY_HPP

#include <boost/config.hpp>
#include <vector>
#include <boost/graph/graph_traits.hpp>
#include <boost/property_map.hpp>
#include <boost/graph/named_function_params.hpp>
#include <boost/graph/breadth_first_search.hpp>
#include <boost/type_traits/conversion_traits.hpp>

namespace boost {

  namespace detail {

    // Default edge and vertex property copiers

    template <typename Graph1, typename Graph2>
    struct edge_copier {
      edge_copier(const Graph1& g1, Graph2& g2)
        : edge_all_map1(get(edge_all, g1)),
          edge_all_map2(get(edge_all, g2)) { }

      template <typename Edge1, typename Edge2>
      void operator()(const Edge1& e1, Edge2& e2) const {
        put(edge_all_map2, e2, get(edge_all_map1, e1));
      }
      typename property_map<Graph1, edge_all_t>::const_type edge_all_map1;
      mutable typename property_map<Graph2, edge_all_t>::type edge_all_map2;
    };
    template <typename Graph1, typename Graph2>
    inline edge_copier<Graph1,Graph2>
    make_edge_copier(const Graph1& g1, Graph2& g2)
    {
      return edge_copier<Graph1,Graph2>(g1, g2);
    }

    template <typename Graph1, typename Graph2>
    struct vertex_copier {
      vertex_copier(const Graph1& g1, Graph2& g2)
        : vertex_all_map1(get(vertex_all, g1)),
          vertex_all_map2(get(vertex_all, g2)) { }

      template <typename Vertex1, typename Vertex2>
      void operator()(const Vertex1& v1, Vertex2& v2) const {
        put(vertex_all_map2, v2, get(vertex_all_map1, v1));
      }
      typename property_map<Graph1, vertex_all_t>::const_type vertex_all_map1;
      mutable typename property_map<Graph2, vertex_all_t>::type
        vertex_all_map2;
    };
    template <typename Graph1, typename Graph2>
    inline vertex_copier<Graph1,Graph2>
    make_vertex_copier(const Graph1& g1, Graph2& g2)
    {
      return vertex_copier<Graph1,Graph2>(g1, g2);
    }

    // Copy all the vertices and edges of graph g_in into graph g_out.
    // The copy_vertex and copy_edge function objects control how vertex
    // and edge properties are copied.

    template <int Version>
    struct copy_graph_impl { };

    template <> struct copy_graph_impl<0>
    {
      template <typename Graph, typename MutableGraph,
        typename CopyVertex, typename CopyEdge, typename IndexMap,
        typename Orig2CopyVertexIndexMap>
      static void apply(const Graph& g_in, MutableGraph& g_out,
                        CopyVertex copy_vertex, CopyEdge copy_edge,
                        Orig2CopyVertexIndexMap orig2copy, IndexMap)
      {
        typename graph_traits<Graph>::vertex_iterator vi, vi_end;
        for (tie(vi, vi_end) = vertices(g_in); vi != vi_end; ++vi) {
          typename graph_traits<MutableGraph>::vertex_descriptor
            new_v = add_vertex(g_out);
          put(orig2copy, *vi, new_v);
          copy_vertex(*vi, new_v);
        }
        typename graph_traits<Graph>::edge_iterator ei, ei_end;
        for (tie(ei, ei_end) = edges(g_in); ei != ei_end; ++ei) {
          typename graph_traits<MutableGraph>::edge_descriptor new_e;
          bool inserted;
          tie(new_e, inserted) = add_edge(get(orig2copy, source(*ei, g_in)),
                                          get(orig2copy, target(*ei, g_in)),
                                          g_out);
          copy_edge(*ei, new_e);
        }
      }
    };

    // for directed graphs
    template <> struct copy_graph_impl<1>
    {
      template <typename Graph, typename MutableGraph,
        typename CopyVertex, typename CopyEdge, typename IndexMap,
        typename Orig2CopyVertexIndexMap>
      static void apply(const Graph& g_in, MutableGraph& g_out,
                        CopyVertex copy_vertex, CopyEdge copy_edge,
                        Orig2CopyVertexIndexMap orig2copy, IndexMap)
      {
        typename graph_traits<Graph>::vertex_iterator vi, vi_end;
        for (tie(vi, vi_end) = vertices(g_in); vi != vi_end; ++vi) {
          typename graph_traits<MutableGraph>::vertex_descriptor
            new_v = add_vertex(g_out);
          put(orig2copy, *vi, new_v);
          copy_vertex(*vi, new_v);
        }
        for (tie(vi, vi_end) = vertices(g_in); vi != vi_end; ++vi) {
          typename graph_traits<Graph>::out_edge_iterator ei, ei_end;
          for (tie(ei, ei_end) = out_edges(*vi, g_in); ei != ei_end; ++ei) {
            typename graph_traits<MutableGraph>::edge_descriptor new_e;
            bool inserted;
            tie(new_e, inserted) = add_edge(get(orig2copy, source(*ei, g_in)),
                                            get(orig2copy, target(*ei, g_in)),
                                            g_out);
            copy_edge(*ei, new_e);
          }
        }
      }
    };

    // for undirected graphs
    template <> struct copy_graph_impl<2>
    {
      template <typename Graph, typename MutableGraph,
        typename CopyVertex, typename CopyEdge, typename IndexMap,
        typename Orig2CopyVertexIndexMap>
      static void apply(const Graph& g_in, MutableGraph& g_out,
                        CopyVertex copy_vertex, CopyEdge copy_edge,
                        Orig2CopyVertexIndexMap orig2copy,
                        IndexMap index_map)
      {
        typedef color_traits<default_color_type> Color;
        std::vector<default_color_type>
          color(num_vertices(g_in), Color::white());
        typename graph_traits<Graph>::vertex_iterator vi, vi_end;
        for (tie(vi, vi_end) = vertices(g_in); vi != vi_end; ++vi) {
          typename graph_traits<MutableGraph>::vertex_descriptor
            new_v = add_vertex(g_out);
          put(orig2copy, *vi, new_v);
          copy_vertex(*vi, new_v);
        }
        for (tie(vi, vi_end) = vertices(g_in); vi != vi_end; ++vi) {
          typename graph_traits<Graph>::out_edge_iterator ei, ei_end;
          for (tie(ei, ei_end) = out_edges(*vi, g_in); ei != ei_end; ++ei) {
            typename graph_traits<MutableGraph>::edge_descriptor new_e;
            bool inserted;
            if (color[get(index_map, target(*ei, g_in))] == Color::white()) {
              tie(new_e, inserted) = add_edge(get(orig2copy, source(*ei,g_in)),
                                              get(orig2copy, target(*ei,g_in)),
                                              g_out);
              copy_edge(*ei, new_e);
            }
          }
          color[get(index_map, *vi)] = Color::black();
        }
      }
    };

    template <class Graph>
    struct choose_graph_copy {
      typedef typename Graph::traversal_category Trv;
      typedef typename Graph::directed_category Dr;
      enum { algo =
             (is_convertible<Trv, vertex_list_graph_tag>::value
              && is_convertible<Trv, edge_list_graph_tag>::value)
             ? 0 : is_convertible<Dr, directed_tag>::value ? 1 : 2 };
      typedef copy_graph_impl<algo> type;
    };

    //-------------------------------------------------------------------------
    struct choose_copier_parameter {
      template <class P, class G1, class G2>
      struct bind_ {
        typedef const P& result_type;
        static result_type apply(const P& p, const G1&, G2&)
        { return p; }
      };
    };
    struct choose_default_edge_copier {
      template <class P, class G1, class G2>
      struct bind_ {
        typedef edge_copier<G1, G2> result_type;
        static result_type apply(const P&, const G1& g1, G2& g2) {
          return result_type(g1, g2);
        }
      };
    };
    template <class Param>
    struct choose_edge_copy {
      typedef choose_copier_parameter type;
    };
    template <>
    struct choose_edge_copy<detail::error_property_not_found> {
      typedef choose_default_edge_copier type;
    };
    template <class Param, class G1, class G2>
    struct choose_edge_copier_helper {
      typedef typename choose_edge_copy<Param>::type Selector;
      typedef typename Selector:: template bind_<Param, G1, G2> Bind;
      typedef Bind type;
      typedef typename Bind::result_type result_type;
    };
    template <typename Param, typename G1, typename G2>
    typename detail::choose_edge_copier_helper<Param,G1,G2>::result_type
    choose_edge_copier(const Param& params, const G1& g_in, G2& g_out)
    {
      typedef typename
        detail::choose_edge_copier_helper<Param,G1,G2>::type Choice;
      return Choice::apply(params, g_in, g_out);
    }


    struct choose_default_vertex_copier {
      template <class P, class G1, class G2>
      struct bind_ {
        typedef vertex_copier<G1, G2> result_type;
        static result_type apply(const P&, const G1& g1, G2& g2) {
          return result_type(g1, g2);
        }
      };
    };
    template <class Param>
    struct choose_vertex_copy {
      typedef choose_copier_parameter type;
    };
    template <>
    struct choose_vertex_copy<detail::error_property_not_found> {
      typedef choose_default_vertex_copier type;
    };
    template <class Param, class G1, class G2>
    struct choose_vertex_copier_helper {
      typedef typename choose_vertex_copy<Param>::type Selector;
      typedef typename Selector:: template bind_<Param, G1, G2> Bind;
      typedef Bind type;
      typedef typename Bind::result_type result_type;
    };
    template <typename Param, typename G1, typename G2>
    typename detail::choose_vertex_copier_helper<Param,G1,G2>::result_type
    choose_vertex_copier(const Param& params, const G1& g_in, G2& g_out)
    {
      typedef typename
        detail::choose_vertex_copier_helper<Param,G1,G2>::type Choice;
      return Choice::apply(params, g_in, g_out);
    }

  } // namespace detail


  template <typename VertexListGraph, typename MutableGraph>
  void copy_graph(const VertexListGraph& g_in, MutableGraph& g_out)
  {
    if (num_vertices(g_in) == 0)
      return;
    typedef typename graph_traits<MutableGraph>::vertex_descriptor vertex_t;
    std::vector<vertex_t> orig2copy(num_vertices(g_in));
    typedef typename detail::choose_graph_copy<VertexListGraph>::type
      copy_impl;
    copy_impl::apply
      (g_in, g_out,
       detail::make_vertex_copier(g_in, g_out),
       detail::make_edge_copier(g_in, g_out),
       make_iterator_property_map(orig2copy.begin(),
                                  get(vertex_index, g_in), orig2copy[0]),
       get(vertex_index, g_in)
       );
  }

  template <typename VertexListGraph, typename MutableGraph,
    class P, class T, class R>
  void copy_graph(const VertexListGraph& g_in, MutableGraph& g_out,
                  const bgl_named_params<P, T, R>& params)
  {
    typename std::vector<T>::size_type n;
      n = is_default_param(get_param(params, orig_to_copy_t()))
        ? num_vertices(g_in) : 1;
    if (n == 0)
      return;
    std::vector<BOOST_DEDUCED_TYPENAME graph_traits<MutableGraph>::vertex_descriptor>
      orig2copy(n);

    typedef typename detail::choose_graph_copy<VertexListGraph>::type
      copy_impl;
    copy_impl::apply
      (g_in, g_out,
       detail::choose_vertex_copier(get_param(params, vertex_copy_t()),
                                    g_in, g_out),
       detail::choose_edge_copier(get_param(params, edge_copy_t()),
                                  g_in, g_out),
       choose_param(get_param(params, orig_to_copy_t()),
                    make_iterator_property_map
                    (orig2copy.begin(),
                     choose_const_pmap(get_param(params, vertex_index),
                                 g_in, vertex_index), orig2copy[0])),
       choose_const_pmap(get_param(params, vertex_index), g_in, vertex_index)
       );
  }

  namespace detail {

    template <class NewGraph, class Copy2OrigIndexMap,
      class CopyVertex, class CopyEdge>
    struct graph_copy_visitor : public bfs_visitor<>
    {
      graph_copy_visitor(NewGraph& graph, Copy2OrigIndexMap c,
                         CopyVertex cv, CopyEdge ce)
        : g_out(graph), orig2copy(c), copy_vertex(cv), copy_edge(ce) { }

      template <class Vertex, class Graph>
      void examine_vertex(Vertex u, const Graph& g_in) const {
        typename graph_traits<NewGraph>::vertex_descriptor
          new_u = add_vertex(g_out);
        put(orig2copy, u, new_u);
        copy_vertex(u, new_u);
      }

      template <class Edge, class Graph>
      void examine_edge(Edge e, const Graph& g_in) const {
        typename graph_traits<NewGraph>::edge_descriptor new_e;
        bool inserted;
        tie(new_e, inserted) = add_edge(get(orig2copy, source(e, g_in)),
                                        get(orig2copy, target(e, g_in)),
                                        g_out);
        copy_edge(e, new_e);
      }
    private:
      NewGraph& g_out;
      Copy2OrigIndexMap orig2copy;
      CopyVertex copy_vertex;
      CopyEdge copy_edge;
    };

    template <typename Graph, typename MutableGraph,
              typename CopyVertex, typename CopyEdge,
              typename Orig2CopyVertexIndexMap, typename Params>
    typename graph_traits<MutableGraph>::vertex_descriptor
    copy_component_impl
      (const Graph& g_in,
       typename graph_traits<Graph>::vertex_descriptor src,
       MutableGraph& g_out,
       CopyVertex copy_vertex, CopyEdge copy_edge,
       Orig2CopyVertexIndexMap orig2copy,
       const Params& params)
    {
      graph_copy_visitor<MutableGraph, Orig2CopyVertexIndexMap,
        CopyVertex, CopyEdge> vis(g_out, orig2copy, copy_vertex, copy_edge);
      breadth_first_search(g_in, src, params.visitor(vis));
      return get(orig2copy, src);
    }

  } // namespace detail


  // Copy all the vertices and edges of graph g_in that are reachable
  // from the source vertex into graph g_out. Return the vertex
  // in g_out that matches the source vertex of g_in.
  template <typename IncidenceGraph, typename MutableGraph,
           typename P, typename T, typename R>
  typename graph_traits<MutableGraph>::vertex_descriptor
  copy_component(IncidenceGraph& g_in,
                 typename graph_traits<IncidenceGraph>::vertex_descriptor src,
                 MutableGraph& g_out,
                 const bgl_named_params<P, T, R>& params)
  {
    typename std::vector<T>::size_type n;
      n = is_default_param(get_param(params, orig_to_copy_t()))
        ? num_vertices(g_in) : 1;
    std::vector<typename graph_traits<IncidenceGraph>::vertex_descriptor>
      orig2copy(n);

    return detail::copy_component_impl
      (g_in, src, g_out,
       detail::choose_vertex_copier(get_param(params, vertex_copy_t()),
                                    g_in, g_out),
       detail::choose_edge_copier(get_param(params, edge_copy_t()),
                                  g_in, g_out),
       choose_param(get_param(params, orig_to_copy_t()),
                    make_iterator_property_map
                    (orig2copy.begin(),
                     choose_pmap(get_param(params, vertex_index),
                                 g_in, vertex_index), orig2copy[0])),
       params
       );
  }

  template <typename IncidenceGraph, typename MutableGraph>
  typename graph_traits<MutableGraph>::vertex_descriptor
  copy_component(IncidenceGraph& g_in,
                 typename graph_traits<IncidenceGraph>::vertex_descriptor src,
                 MutableGraph& g_out)
  {
    std::vector<typename graph_traits<IncidenceGraph>::vertex_descriptor>
      orig2copy(num_vertices(g_in));

    return detail::copy_component_impl
      (g_in, src, g_out,
       make_vertex_copier(g_in, g_out),
       make_edge_copier(g_in, g_out),
       make_iterator_property_map(orig2copy.begin(),
                                  get(vertex_index, g_in), orig2copy[0]),
       bgl_named_params<char,char>('x') // dummy param object
       );
  }

} // namespace boost

#endif // BOOST_GRAPH_COPY_HPP
