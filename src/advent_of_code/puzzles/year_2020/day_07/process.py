import copy
import collections
import timeit

import networkx as nx


class HandyHaversacks:
    def __init__(self, bag_input=None):
        bag_input = bag_input if bag_input is not None else self._read_file()
        self.bags = self._preprocess(bag_input)
        self.bag_graph = self._create_graph()
        print()

    def _read_file(self):
        with open("input.txt") as f:
            return f.read()

    def _preprocess(self, bag_input):
        bags = collections.defaultdict(dict)
        for raw_line in bag_input.splitlines():
            line = raw_line.replace(".", "")
            raw_containing, raw_contains = line.split(" contain ")
            containing_desc, containing_colour, _ = raw_containing.split()
            containing = f"{containing_desc} {containing_colour}"
            if raw_contains == "no other bags":
                bags[containing] = {}
                continue
            raw_contains_by_bag = raw_contains.split(", ")
            for bag in raw_contains_by_bag:
                number, contains_desc, contains_colour, _ = bag.split()
                contains = f"{contains_desc} {contains_colour}"
                bags[containing][contains] = int(number)
        return bags

    def _create_graph(self):
        graph_input = []
        for contains_bag, containing_bags in self.bags.items():
            for containing_bag, number in containing_bags.items():
                graph_input.append((contains_bag, containing_bag, number))
        bag_graph = nx.DiGraph()
        bag_graph.add_weighted_edges_from(graph_input)
        return bag_graph

    def contains_shiny_gold_bag(self):
        return len(nx.ancestors(self.bag_graph, "shiny gold"))

    def bags_inside_shiny_gold_bag(self):
        graph = copy.deepcopy(self.bag_graph)
        while any(
            desc
            for desc in nx.descendants(graph, "shiny gold")
            if graph.out_degree(desc)
        ):
            outer_nodes = [
                desc
                for desc in nx.descendants(graph, "shiny gold")
                if not graph.out_degree(desc)
            ]
            for outer_node in outer_nodes:
                for pred in graph.pred[outer_node].copy():
                    if pred == "shiny gold":
                        continue
                    pred_outer_weight = graph[pred][outer_node]["weight"]
                    new_edge_name = f"{pred};{outer_node}"
                    for inner_pred in graph.pred[pred]:
                        inner_pred_pred_weight = graph[inner_pred][pred]["weight"]
                        cum_weight = inner_pred_pred_weight * pred_outer_weight
                        graph.add_edge(inner_pred, new_edge_name, weight=cum_weight)
                    graph.remove_edge(pred, outer_node)
        return sum(
            graph["shiny gold"][desc]["weight"]
            for desc in nx.descendants(graph, "shiny gold")
        )


def main():
    handy_haversacks = HandyHaversacks()
    print(
        f"Number of bags that contain a shiny gold bag: {handy_haversacks.contains_shiny_gold_bag()}"
    )
    print(
        f"Bags inside a shiny gold bag: {handy_haversacks.bags_inside_shiny_gold_bag()}"
    )


if __name__ == "__main__":
    print(f"Completed in {timeit.timeit(main, number=1)} seconds")
