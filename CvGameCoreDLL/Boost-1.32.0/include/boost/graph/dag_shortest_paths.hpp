//=======================================================================
// Copyright 2002 Indiana University.
// Authors: Andrew Lumsdaine, Lie-Quan Lee, Jeremy G. Siek
//
// This file is part of the Boost Graph Library
//
// You should have received a copy of the License Agreement for the
// Boost Graph Library along with the software; see the file LICENSE.
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

#ifndef BOOST_GRAPH_DAG_SHORTEST_PATHS_HPP
#define BOOST_GRAPH_DAG_SHORTEST_PATHS_HPP

#include <boost/graph/topological_sort.hpp>
#include <boost/graph/dijkstra_shortest_paths.hpp>

// single-source shortest paths for a Directed Acyclic Graph (DAG)

namespace boost {

  // Initalize distances and call depth first search
  template <class VertexListGraph, class DijkstraVisitor,
            class DistanceMap, class WeightMap, class ColorMap,
            class PredecessorMap,
            class Compare, class Combine,
            class DistInf, class DistZero>
  inline void
  dag_shortest_paths
    (const VertexListGraph& g,
     typename graph_traits<VertexListGraph>::vertex_descriptor s,
     DistanceMap distance, WeightMap weight, ColorMap color,
     PredecessorMap pred,
     DijkstraVisitor vis, Compare compare, Combine combine,
     DistInf inf, DistZero zero)
  {
    typedef typename graph_traits<VertexListGraph>::vertex_descriptor Vertex;
    std::vector<Vertex> rev_topo_order;
    rev_topo_order.reserve(num_vertices(g));
    topological_sort(g, std::back_inserter(rev_topo_order));

    typename graph_traits<VertexListGraph>::vertex_iterator ui, ui_end;
    for (tie(ui, ui_end) = vertices(g); ui != ui_end; ++ui) {
      put(distance, *ui, inf);
      put(pred, *ui, *ui);
    }

    put(distance, s, zero);
    vis.discover_vertex(s, g);
    typename std::vector<Vertex>::reverse_iterator i;
    for (i = rev_topo_order.rbegin(); i != rev_topo_order.rend(); ++i) {
      Vertex u = *i;
      vis.examine_vertex(u, g);
      typename graph_traits<VertexListGraph>::out_edge_iterator e, e_end;
      for (tie(e, e_end) = out_edges(u, g); e != e_end; ++e) {
        vis.discover_vertex(target(*e, g), g);
        bool decreased = relax(*e, g, weight, pred, distance,
                               combine, compare);
        if (decreased)
          vis.edge_relaxed(*e, g);
        else
          vis.edge_not_relaxed(*e, g);
      }
      vis.finish_vertex(u, g);
    }
  }

  namespace detail {

    // Defaults are the same as Dijkstra's algorithm

    // Handle Distance Compare, Combine, Inf and Zero defaults
    template <class VertexListGraph, class DijkstraVisitor,
      class DistanceMap, class WeightMap, class ColorMap,
      class IndexMap, class Params>
    inline void
    dag_sp_dispatch2
      (const VertexListGraph& g,
       typename graph_traits<VertexListGraph>::vertex_descriptor s,
       DistanceMap distance, WeightMap weight, ColorMap color, IndexMap id,
       DijkstraVisitor vis, const Params& params)
    {
      typedef typename property_traits<DistanceMap>::value_type D;
      dummy_property_map p_map;
      dag_shortest_paths
        (g, s, distance, weight, color,
         choose_param(get_param(params, vertex_predecessor), p_map),
         vis,
         choose_param(get_param(params, distance_compare_t()), std::less<D>()),
         choose_param(get_param(params, distance_combine_t()), closed_plus<D>()),
         choose_param(get_param(params, distance_inf_t()),
                      (std::numeric_limits<D>::max)()),
         choose_param(get_param(params, distance_zero_t()),
                      D()));
    }

    // Handle DistanceMap and ColorMap defaults
    template <class VertexListGraph, class DijkstraVisitor,
              class DistanceMap, class WeightMap, class ColorMap,
              class IndexMap, class Params>
    inline void
    dag_sp_dispatch1
      (const VertexListGraph& g,
       typename graph_traits<VertexListGraph>::vertex_descriptor s,
       DistanceMap distance, WeightMap weight, ColorMap color, IndexMap id,
       DijkstraVisitor vis, const Params& params)
    {
      typedef typename property_traits<WeightMap>::value_type T;
      typename std::vector<T>::size_type n;
      n = is_default_param(distance) ? num_vertices(g) : 1;
      std::vector<T> distance_map(n);
      n = is_default_param(color) ? num_vertices(g) : 1;
      std::vector<default_color_type> color_map(n);

      dag_sp_dispatch2
        (g, s,
         choose_param(distance,
                      make_iterator_property_map(distance_map.begin(), id,
                                                 distance_map[0])),
         weight,
         choose_param(color,
                      make_iterator_property_map(color_map.begin(), id,
                                                 color_map[0])),
         id, vis, params);
    }

  } // namespace detail

  template <class VertexListGraph, class Param, class Tag, class Rest>
  inline void
  dag_shortest_paths
    (const VertexListGraph& g,
     typename graph_traits<VertexListGraph>::vertex_descriptor s,
     const bgl_named_params<Param,Tag,Rest>& params)
  {
    // assert that the graph is directed...
    null_visitor null_vis;
    detail::dag_sp_dispatch1
      (g, s,
       get_param(params, vertex_distance),
       choose_const_pmap(get_param(params, edge_weight), g, edge_weight),
       get_param(params, vertex_color),
       choose_const_pmap(get_param(params, vertex_index), g, vertex_index),
       choose_param(get_param(params, graph_visitor),
                    make_dijkstra_visitor(null_vis)),
       params);
  }

} // namespace boost

#endif // BOOST_GRAPH_DAG_SHORTEST_PATHS_HPP
