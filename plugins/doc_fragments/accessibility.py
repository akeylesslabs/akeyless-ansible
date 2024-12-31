from __future__ import annotations

class ModuleDocFragment(object):

    DOCUMENTATION = """
    options:
      accessibility:
        description:
          - In case of an item in a user's personal folder.
        type: str
        choices:
          - regular
          - personal
        default: regular
    """