from typing import Tuple

from .models import RouteAction, RouteObservation, EnvState


class PollutionEnv:
    def __init__(self):
        self.state = None

    def reset(self) -> EnvState:
        """
        Initialize environment state
        """
        self.state = EnvState(
            current_location="START",
            total_exposure=0.0
        )
        return self.state

    def step(self, action: RouteAction) -> Tuple[RouteObservation, float, bool, dict]:
        """
        Execute one step in environment using routing output
        """

        # ---------------- USE ROUTING OUTPUT ----------------
        path = action.path
        exposure = action.exposure

        # ---------------- DERIVED METRICS ----------------
        # Temporary AQI estimation (replace later with real data)
        avg_aqi = exposure / max(1, len(path))

        # ---------------- SCORING ----------------
        max_exposure = 10000  # normalization constant
        score = max(0, 100 - (exposure / max_exposure) * 100)

        # ---------------- STATE UPDATE ----------------
        self.state.current_location = path[-1]
        self.state.total_exposure += exposure

        # ---------------- REWARD (RL DESIGN) ----------------
        reward = -exposure  # lower exposure = better

        # ---------------- OBSERVATION ----------------
        observation = RouteObservation(
            path=path,
            avg_aqi=avg_aqi,
            exposure=exposure,
            score=score
        )

        # Single-step episode for now
        done = True

        return observation, reward, done, {}