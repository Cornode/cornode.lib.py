# coding=utf-8
from __future__ import absolute_import, division, print_function, \
  unicode_literals

from cornode.commands import FilterCommand, RequestFilter

__all__ = [
  'InterruptAttachingToTangleCommand',
]


class InterruptAttachingToTangleCommand(FilterCommand):
  """
  Executes ``interruptAttachingToTangle`` command.

  See :py:meth:`cornode.api.Strictcornode.interrupt_attaching_to_tangle`.
  """
  command = 'interruptAttachingToTangle'

  def get_request_filter(self):
    return InterruptAttachingToTangleRequestFilter()

  def get_response_filter(self):
    pass


class InterruptAttachingToTangleRequestFilter(RequestFilter):
  def __init__(self):
    # `interruptAttachingToTangle` takes no parameters.
    # Using a filter here just to enforce that the request is empty.
    super(InterruptAttachingToTangleRequestFilter, self).__init__({})
