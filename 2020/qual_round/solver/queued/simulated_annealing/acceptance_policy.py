import math
import random


class AcceptancePolicy:
  def accept(self, state, mutation, temperature):
    raise NotImplementedError


class GreedyAcceptancePolicy(AcceptancePolicy):
  def accept(self, state, mutation, temperature):
    return state.improvement(mutation) > 0


class ExpAcceptancePolicy(AcceptancePolicy):
  def prob(self, improvement, temperature):
    if temperature == 0 or improvement / temperature > 100:
      return 1 if improvement > 0 else 0
    else:
      return math.exp(improvement / temperature)

  def accept(self, state, mutation, temperature):
    return random.random() < self.prob(state.improvement(mutation), temperature)
