# coding=utf-8
from __future__ import absolute_import, division, print_function, \
  unicode_literals

import filters as f

from cornode import TransactionHash
from cornode.commands import FilterCommand, RequestFilter
from cornode.filters import Trytes

__all__ = [
  'GetInclusionStatesCommand',
]


class GetInclusionStatesCommand(FilterCommand):
  """
  Executes ``getInclusionStates`` command.

  See :py:meth:`cornode.api.Strictcornode.get_inclusion_states`.
  """
  command = 'getInclusionStates'

  def get_request_filter(self):
    return GetInclusionStatesRequestFilter()

  def get_response_filter(self):
    pass


class GetInclusionStatesRequestFilter(RequestFilter):
  def __init__(self):
    super(GetInclusionStatesRequestFilter, self).__init__(
      {
        # Required parameters.
        'transactions': (
            f.Required
          | f.Array
          | f.FilterRepeater(f.Required | Trytes(result_type=TransactionHash))
        ),

        # Optional parameters.
        'tips': (
            f.Array
          | f.FilterRepeater(f.Required | Trytes(result_type=TransactionHash))
          | f.Optional(default=[])
        ),
      },

      allow_missing_keys = {
        'tips',
      },
    )
