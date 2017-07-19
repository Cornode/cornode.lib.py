# coding=utf-8
from __future__ import absolute_import, division, print_function, \
  unicode_literals

import filters as f

from cornode import TransactionTrytes
from cornode.commands import FilterCommand, RequestFilter
from cornode.filters import Trytes

__all__ = [
  'BroadcastTransactionsCommand',
]


class BroadcastTransactionsCommand(FilterCommand):
  """
  Executes `broadcastTransactions` command.

  See :py:meth:`cornode.api.Strictcornode.broadcast_transactions`.
  """
  command = 'broadcastTransactions'

  def get_request_filter(self):
    return BroadcastTransactionsRequestFilter()

  def get_response_filter(self):
    pass


class BroadcastTransactionsRequestFilter(RequestFilter):
  def __init__(self):
    super(BroadcastTransactionsRequestFilter, self).__init__({
      'trytes':
          f.Required
        | f.Array
        | f.FilterRepeater(f.Required | Trytes(result_type=TransactionTrytes)),
    })
