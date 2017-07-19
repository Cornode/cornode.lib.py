# coding=utf-8
from __future__ import absolute_import, division, print_function, \
  unicode_literals

import filters as f

from cornode.commands import FilterCommand, RequestFilter
from cornode.filters import NodeUri

__all__ = [
  'RemoveNeighborsCommand',
]


class RemoveNeighborsCommand(FilterCommand):
  """
  Executes ``removeNeighbors`` command.

  See :py:meth:`cornode.api.Strictcornode.remove_neighbors`.
  """
  command = 'removeNeighbors'

  def get_request_filter(self):
    return RemoveNeighborsRequestFilter()

  def get_response_filter(self):
    pass


class RemoveNeighborsRequestFilter(RequestFilter):
  def __init__(self):
    super(RemoveNeighborsRequestFilter, self).__init__({
      'uris': f.Required | f.Array | f.FilterRepeater(f.Required | NodeUri),
    })
