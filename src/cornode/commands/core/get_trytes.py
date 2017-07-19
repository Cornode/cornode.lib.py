# coding=utf-8
from __future__ import absolute_import, division, print_function, \
  unicode_literals

import filters as f

from cornode import TransactionHash
from cornode.commands import FilterCommand, RequestFilter, ResponseFilter
from cornode.filters import Trytes

__all__ = [
  'GetTrytesCommand',
]


class GetTrytesCommand(FilterCommand):
  """
  Executes ``getTrytes`` command.

  See :py:meth:`cornode.api.Strictcornode.get_trytes`.
  """
  command = 'getTrytes'

  def get_request_filter(self):
    return GetTrytesRequestFilter()

  def get_response_filter(self):
    return GetTrytesResponseFilter()


class GetTrytesRequestFilter(RequestFilter):
  def __init__(self):
    super(GetTrytesRequestFilter, self).__init__({
      'hashes': (
          f.Required
        | f.Array
        | f.FilterRepeater(f.Required | Trytes(result_type=TransactionHash))
      ),
    })


class GetTrytesResponseFilter(ResponseFilter):
  def __init__(self):
    super(GetTrytesResponseFilter, self).__init__({
      'trytes': (
          f.Array
        | f.FilterRepeater(f.ByteString(encoding='ascii') | Trytes)
      ),
    })