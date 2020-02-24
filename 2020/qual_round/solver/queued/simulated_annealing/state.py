import random


class State:
  def score(self):
    raise NotImplementedError

  def random_mutation(self):
    raise NotImplementedError

  def apply_mutation(self, mutation):
    raise NotImplementedError

  def improvement(self, mutation):
    raise NotImplementedError


class Mutation:
  pass
