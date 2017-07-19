# coding=utf-8
from __future__ import absolute_import, division, print_function, \
  unicode_literals

import filters as f

from cornode import Address
from cornode.commands import FilterCommand, RequestFilter, ResponseFilter
from cornode.filters import Trytes

__all__ = [
  'GetTipsCommand',
]


class GetTipsCommand(FilterCommand):
  """
  Executes ``getTips`` command.

  See :py:meth:`cornode.api.Strictcornode.get_tips`.
  """
  command = 'getTips'

  def get_request_filter(self):
    return GetTipsRequestFilter()

  def get_response_filter(self):
    return GetTipsResponseFilter()


class GetTipsRequestFilter(RequestFilter):
  def __init__(self):
    # `getTips` doesn't accept any parameters.
    # Using a filter here just to enforce that the request is empty.
    super(GetTipsRequestFilter, self).__init__({})


class GetTipsResponseFilter(ResponseFilter):
  def __init__(self):
    super(GetTipsResponseFilter, self).__init__({
      'hashes': (
          f.Array
        | f.FilterRepeater(
              f.ByteString(encoding='ascii')
            | Trytes(result_type=Address)
          )
      ),
    })
