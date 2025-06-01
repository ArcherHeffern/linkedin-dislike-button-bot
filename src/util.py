
from logging import DEBUG


def dprint(s: str):
  if DEBUG:
    print(f"Error: {s}")