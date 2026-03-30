import heapq


# ===================== GRAPH =====================

class Graph:
    def __init__(self):
        self.graph = {}

    def add_city(self, city):
        if city not in self.graph:
            self.graph[city] = []

    def add_road(self, city1, city2, distance, pollution):
        self.add_city(city1)
        self.add_city(city2)

        # Undirected graph
        self.graph[city1].append((city2, distance, pollution))
        self.graph[city2].append((city1, distance, pollution))

    def get_graph(self):
        return self.graph


# ===================== ROUTING =====================

class Routing:
    def __init__(self, graph):
        self.graph = graph

    def dijkstra(self, start, end, mode="distance", alpha=0.6):
        pq = [(0, start, [], 0, 0, 0)]
        # (cost, node, path, distance, pollution, exposure)

        visited = set()

        while pq:
            cost, node, path, dist_sum, poll_sum, exp_sum = heapq.heappop(pq)

            if node in visited:
                continue

            path = path + [node]
            visited.add(node)

            if node == end:
                return {
                    "path": path,
                    "total_cost": cost,
                    "total_distance": dist_sum,
                    "total_pollution": poll_sum,
                    "total_exposure": exp_sum,
                    "mode": mode
                }

            for neighbor, distance, pollution in self.graph[node]:
                if neighbor not in visited:

                    new_dist = dist_sum + distance
                    new_poll = poll_sum + pollution

                    exposure = distance * pollution
                    new_exp = exp_sum + exposure

                    if mode == "distance":
                        new_cost = cost + distance

                    elif mode == "eco":
                        new_cost = cost + exposure

                    elif mode == "hybrid":
                        beta = 1 - alpha
                        new_cost = cost + (alpha * distance + beta * exposure)

                    else:
                        raise ValueError("Invalid mode")

                    heapq.heappush(
                        pq,
                        (new_cost, neighbor, path, new_dist, new_poll, new_exp)
                    )

        return None


def get_route(graph, start, end, mode="distance", alpha=0.6):
    router = Routing(graph)
    return router.dijkstra(start, end, mode, alpha)


# ===================== MODELS =====================

class RouteAction:
    def __init__(self, path, exposure):
        self.path = path
        self.exposure = exposure


class RouteObservation:
    def __init__(self, path, exposure, score):
        self.path = path
        self.exposure = exposure
        self.score = score


# ===================== ENV =====================

class PollutionEnv:
    def __init__(self):
        self.total_exposure = 0

    def step(self, action: RouteAction):
        # USE exposure from routing (IMPORTANT)
        exposure = action.exposure

        # scoring
        max_exposure = 10000
        score = max(0, 100 - (exposure / max_exposure) * 100)

        reward = -exposure  # lower exposure = better

        self.total_exposure += exposure

        observation = RouteObservation(
            path=action.path,
            exposure=exposure,
            score=score
        )

        done = True

        return observation, reward, done, {}


# ===================== SIMULATION =====================

def run_simulation():
    # Create graph
    g = Graph()

    g.add_road("A", "B", 5, 10)
    g.add_road("A", "C", 8, 3)
    g.add_road("B", "D", 2, 2)
    g.add_road("C", "D", 4, 6)
    g.add_road("C", "E", 7, 1)
    g.add_road("D", "E", 1, 2)
    g.add_road("D", "F", 6, 8)
    g.add_road("E", "F", 3, 1)

    graph = g.get_graph()

    # Initialize env
    env = PollutionEnv()

    # Get route
    route_data = get_route(graph, "A", "F", mode="hybrid", alpha=0.5)

    # Convert to action
    action = RouteAction(
        path=route_data["path"],
        exposure=route_data["total_exposure"]
    )

    # Run environment
    observation, reward, done, _ = env.step(action)

    # Output
    print("\n🚀 FINAL OUTPUT")
    print("Path:", " → ".join(observation.path))
    print("Mode:", route_data["mode"])
    print("Total Distance:", route_data["total_distance"])
    print("Total Pollution:", route_data["total_pollution"])
    print("Total Exposure:", observation.exposure)
    print("Score:", observation.score)
    print("Reward:", reward)


# ===================== RUN =====================

if __name__ == "__main__":
    run_simulation()