//
//=======================================================================
// Copyright 1997, 1998, 1999, 2000 University of Notre Dame.
// Authors: Andrew Lumsdaine, Lie-Quan Lee, Jeremy G. Siek
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
#ifndef BOOST_GRAPH_UNDIRECTED_DFS_HPP
#define BOOST_GRAPH_UNDIRECTED_DFS_HPP

#include <boost/graph/depth_first_search.hpp>

namespace boost {

  namespace detail {

    template <typename IncidenceGraph, typename DFSVisitor,
              typename VertexColorMap, typename EdgeColorMap>
    void undir_dfv_impl
      (const IncidenceGraph& g,
       typename graph_traits<IncidenceGraph>::vertex_descriptor u,
       DFSVisitor& vis,  // pass-by-reference here, important!
       VertexColorMap vertex_color,
       EdgeColorMap edge_color)
    {
      function_requires<IncidenceGraphConcept<IncidenceGraph> >();
      function_requires<DFSVisitorConcept<DFSVisitor, IncidenceGraph> >();
      typedef typename graph_traits<IncidenceGraph>::vertex_descriptor Vertex;
      typedef typename graph_traits<IncidenceGraph>::edge_descriptor Edge;
      function_requires<ReadWritePropertyMapConcept<VertexColorMap,Vertex> >();
      function_requires<ReadWritePropertyMapConcept<EdgeColorMap,Edge> >();
      typedef typename property_traits<VertexColorMap>::value_type ColorValue;
      typedef typename property_traits<EdgeColorMap>::value_type EColorValue;
      function_requires< ColorValueConcept<ColorValue> >();
      function_requires< ColorValueConcept<EColorValue> >();
      typedef color_traits<ColorValue> Color;
      typedef color_traits<EColorValue> EColor;
      typename graph_traits<IncidenceGraph>::out_edge_iterator ei, ei_end;

      put(vertex_color, u, Color::gray());   vis.discover_vertex(u, g);
      for (tie(ei, ei_end) = out_edges(u, g); ei != ei_end; ++ei) {
        Vertex v = target(*ei, g);           vis.examine_edge(*ei, g);
        ColorValue v_color = get(vertex_color, v);
        EColorValue uv_color = get(edge_color, *ei);
        put(edge_color, *ei, EColor::black());
        if (v_color == Color::white()) {     vis.tree_edge(*ei, g);
          undir_dfv_impl(g, v, vis, vertex_color, edge_color);
        } else if (v_color == Color::gray() && uv_color == EColor::white())
                                             vis.back_edge(*ei, g);
      }
      put(vertex_color, u, Color::black());  vis.finish_vertex(u, g);
    }
  } // namespace detail

  template <typename Graph, typename DFSVisitor,
            typename VertexColorMap, typename EdgeColorMap,
            typename Vertex>
  void
  undirected_dfs(const Graph& g, DFSVisitor vis,
                 VertexColorMap vertex_color, EdgeColorMap edge_color,
                 Vertex start_vertex)
  {
    function_requires<DFSVisitorConcept<DFSVisitor, Graph> >();
      function_requires<EdgeListGraphConcept<Graph> >();

    typedef typename property_traits<VertexColorMap>::value_type ColorValue;
    typedef color_traits<ColorValue> Color;

    typename graph_traits<Graph>::vertex_iterator ui, ui_end;
    for (tie(ui, ui_end) = vertices(g); ui != ui_end; ++ui) {
      put(vertex_color, *ui, Color::white());   vis.initialize_vertex(*ui, g);
    }
    typename graph_traits<Graph>::edge_iterator ei, ei_end;
    for (tie(ei, ei_end) = edges(g); ei != ei_end; ++ei)
      put(edge_color, *ei, Color::white());

    if (start_vertex != *vertices(g).first){ vis.start_vertex(start_vertex, g);
      detail::undir_dfv_impl(g, start_vertex, vis, vertex_color, edge_color);
    }

    for (tie(ui, ui_end) = vertices(g); ui != ui_end; ++ui) {
      ColorValue u_color = get(vertex_color, *ui);
      if (u_color == Color::white()) {       vis.start_vertex(*ui, g);
        detail::undir_dfv_impl(g, *ui, vis, vertex_color, edge_color);
      }
    }
  }

  template <typename Graph, typename DFSVisitor, typename VertexColorMap,
    typename EdgeColorMap>
  void
  undirected_dfs(const Graph& g, DFSVisitor vis,
                 VertexColorMap vertex_color, EdgeColorMap edge_color)
  {
    undirected_dfs(g, vis, vertex_color, edge_color, *vertices(g).first);
  }

  namespace detail {
    template <typename VertexColorMap>
    struct udfs_dispatch {

      template <typename Graph, typename Vertex,
                typename DFSVisitor, typename EdgeColorMap,
                typename P, typename T, typename R>
      static void
      apply(const Graph& g, DFSVisitor vis, Vertex start_vertex,
            const bgl_named_params<P, T, R>&,
            EdgeColorMap edge_color,
            VertexColorMap vertex_color)
      {
        undirected_dfs(g, vis, vertex_color, edge_color, start_vertex);
      }
    };

    template <>
    struct udfs_dispatch<detail::error_property_not_found> {
      template <typename Graph, typename Vertex, typename DFSVisitor,
                typename EdgeColorMap,
                typename P, typename T, typename R>
      static void
      apply(const Graph& g, DFSVisitor vis, Vertex start_vertex,
            const bgl_named_params<P, T, R>& params,
            EdgeColorMap edge_color,
            detail::error_property_not_found)
      {
        std::vector<default_color_type> color_vec(num_vertices(g));
        default_color_type c = white_color; // avoid warning about un-init
        undirected_dfs
          (g, vis, make_iterator_property_map
           (color_vec.begin(),
            choose_const_pmap(get_param(params, vertex_index),
                              g, vertex_index), c),
           edge_color,
           start_vertex);
      }
    };

  } // namespace detail


  // Named Parameter Variant
  template <typename Graph, typename P, typename T, typename R>
  void
  undirected_dfs(const Graph& g,
                 const bgl_named_params<P, T, R>& params)
  {
    typedef typename property_value< bgl_named_params<P, T, R>,
      vertex_color_t>::type C;
    detail::udfs_dispatch<C>::apply
      (g,
       choose_param(get_param(params, graph_visitor),
                    make_dfs_visitor(null_visitor())),
       choose_param(get_param(params, root_vertex_t()),
                    *vertices(g).first),
       params,
       get_param(params, edge_color),
       get_param(params, vertex_color)
       );
  }


  template <typename IncidenceGraph, typename DFSVisitor,
    typename VertexColorMap, typename EdgeColorMap>
  void undirected_depth_first_visit
    (const IncidenceGraph& g,
     typename graph_traits<IncidenceGraph>::vertex_descriptor u,
     DFSVisitor vis, VertexColorMap vertex_color, EdgeColorMap edge_color)
  {
    detail::undir_dfv_impl(g, u, vis, vertex_color, edge_color);
  }


} // namespace boost


#endif
