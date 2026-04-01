class PollutionEnv:

    def __init__(self, graph, start="A", destination="F"):
        self.graph = graph
        self.start = start
        self.destination = destination

        self.current_location = start
        self.total_exposure = 0
        self.steps_taken = 0
        self.max_steps = 50

    def reset(self):
        self.current_location = self.start
        self.total_exposure = 0
        self.steps_taken = 0
        return self.current_location

    def get_possible_actions(self):
        neighbors = self.graph.get_neighbors(self.current_location)
        return [n for n, _, _ in neighbors]

    def step(self, action: str):
        neighbors = self.graph.get_neighbors(self.current_location)

        edge = None
        for n, dist, pol in neighbors:
            if n == action:
                edge = (n, dist, pol)
                break

        if edge is None:
            raise ValueError(f"Invalid action: {action}")

        next_node, distance, pollution = edge

        exposure = distance * pollution
        self.total_exposure += exposure

        self.current_location = next_node
        self.steps_taken += 1

        reward = -(pollution * 0.7 + distance * 0.3)
        reward += 0.5 * max(0, 10 - pollution)

        if hasattr(self.graph, "heuristic"):
            reward -= 0.1 * self.graph.heuristic(next_node, self.destination)

        done = next_node == self.destination

        if done:
            reward += 100

        if self.steps_taken >= self.max_steps:
            reward -= 50
            done = True

        info = {
            "total_exposure": self.total_exposure,
            "steps": self.steps_taken
        }

        return next_node, reward, done, info