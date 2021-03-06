# coding=utf-8
from __future__ import absolute_import, division, print_function, \
  unicode_literals

from threading import Thread
from time import sleep
from unittest import TestCase

from mock import Mock, patch

from cornode import Address
from cornode.crypto.addresses import AddressGenerator, MemoryAddressCache
from cornode.crypto.signing import KeyIterator
from cornode.crypto.types import Digest, Seed


class AddressGeneratorTestCase(TestCase):
  # noinspection SpellCheckingInspection
  def setUp(self):
    super(AddressGeneratorTestCase, self).setUp()

    # Addresses that correspond to the digests defined in
    # :py:meth:`_mock_get_digest`.
    self.addy0 =\
      Address(
        b'VOPYUSDRHYGGOHLAYDWCLLOFWBLK99PYYKENW9IQ'
        b'IVIOYMLCCPXGICDBZKCQVJLDWWJLTTUVIXCTOZ9TN'
      )

    self.addy1 =\
      Address(
        b'SKKMQAGLZMXWSXRVVRFWMGN9TIXDACQMCXZJRPMS'
        b'UFNSXMFOGEBZZPUJBVKVSJNYPSGSXQIUHTRKECVQE'
      )

    self.addy2 =\
      Address(
        b'VMMFSGEYJ9SANRULNIMKEZUYVRTWMVR9UKCYDZXW'
        b'9TENBWIRMFODOSNMDH9QOVBLQWALOHMSBGEVIXSXY'
      )

    self.addy3 =\
      Address(
        b'G9PLHPOMET9NWIBGRGMIF9HFVETTWGKCXWGFYRNG'
        b'CFANWBQFGMFKITZBJDSYLGXYUIQVCMXFWSWFRNHRV'
      )

  # noinspection SpellCheckingInspection
  def test_address_from_digest(self):
    """
    Generating an address from a private key digest.
    """
    digest =\
      Digest(
        trytes =
          b'ABQXVJNER9MPMXMBPNMFBMDGTXRWSYHNZKGAGUOI'
          b'JKOJGZVGHCUXXGFZEMMGDSGWDCKJXO9ILLFAKGGZE',

        key_index = 0,
      )

    self.assertEqual(
      AddressGenerator.address_from_digest(digest),

      Address(
        b'QLOEDSBXXOLLUJYLEGKEPYDRIJJTPIMEPKMFHUVJ'
        b'MPMLYYCLPQPANEVDSERQWPVNHCAXYRLAYMBHJLWWR'
      ),
    )

  def test_get_addresses_single(self):
    """
    Generating a single address.
    """
    # Seed is not important for this test; it is only used by
    # :py:class:`KeyGenerator`, which we will mock in this test.
    ag = AddressGenerator(seed=b'')

    # noinspection PyUnresolvedReferences
    with patch.object(ag, '_get_digest', self._mock_get_digest):
      addresses = ag.get_addresses(start=0)

    self.assertListEqual(addresses, [self.addy0])

    # noinspection PyUnresolvedReferences
    with patch.object(ag, '_get_digest', self._mock_get_digest):
      # You can provide any positive integer as the ``start`` value.
      addresses = ag.get_addresses(start=2)

    self.assertListEqual(addresses, [self.addy2])

  def test_get_addresses_multiple(self):
    """
    Generating multiple addresses in one go.
    """
    # Seed is not important for this test; it is only used by
    # :py:class:`KeyGenerator`, which we will mock in this test.
    ag = AddressGenerator(seed=b'')

    # noinspection PyUnresolvedReferences
    with patch.object(ag, '_get_digest', self._mock_get_digest):
      addresses = ag.get_addresses(start=1, count=2)

    self.assertListEqual(addresses, [self.addy1, self.addy2])

  def test_get_addresses_error_start_too_small(self):
    """
    Providing a negative ``start`` value to ``get_addresses``.

    :py:class:`AddressGenerator` can potentially generate an infinite
    number of addresses, so there is no "end" to offset against.
    """
    ag = AddressGenerator(seed=b'')

    with self.assertRaises(ValueError):
      ag.get_addresses(start=-1)

  def test_get_addresses_error_count_too_small(self):
    """
    Providing a ``count`` value less than 1 to ``get_addresses``.

    :py:class:`AddressGenerator` can potentially generate an infinite
    number of addresses, so there is no "end" to offset against.
    """
    ag = AddressGenerator(seed=b'')

    with self.assertRaises(ValueError):
      ag.get_addresses(start=0, count=0)

  def test_get_addresses_error_step_zero(self):
    """
    Providing a ``step`` value of 0 to ``get_addresses``.
    """
    ag = AddressGenerator(seed=b'')

    with self.assertRaises(ValueError):
      ag.get_addresses(start=0, step=0)

  def test_get_addresses_step_negative(self):
    """
    Providing a negative ``step`` value to ``get_addresses``.

    This is probably a weird use case, but what the heck.
    """
    # Seed is not important for this test; it is only used by
    # :py:class:`KeyGenerator`, which we will mock in this test.
    ag = AddressGenerator(seed=b'')

    # noinspection PyUnresolvedReferences
    with patch.object(ag, '_get_digest', self._mock_get_digest):
      addresses = ag.get_addresses(start=1, count=2, step=-1)

    self.assertListEqual(
      addresses,

      # This is the same as ``ag.get_addresses(start=0, count=2)``, but
      # the order is reversed.
      [self.addy1, self.addy0],
    )

  def test_generator(self):
    """
    Creating a generator.
    """
    # Seed is not important for this test; it is only used by
    # :py:class:`KeyGenerator`, which we will mock in this test.
    ag = AddressGenerator(seed=b'')

    # noinspection PyUnresolvedReferences
    with patch.object(ag, '_get_digest', self._mock_get_digest):
      generator = ag.create_iterator()

      self.assertEqual(next(generator), self.addy0)
      self.assertEqual(next(generator), self.addy1)
      # ... ad infinitum ...

  def test_generator_with_offset(self):
    """
    Creating a generator that starts at an offset greater than 0.
    """
    # Seed is not important for this test; it is only used by
    # :py:class:`KeyGenerator`, which we will mock in this test.
    ag = AddressGenerator(seed=b'')

    # noinspection PyUnresolvedReferences
    with patch.object(ag, '_get_digest', self._mock_get_digest):
      generator = ag.create_iterator(start=1, step=2)

      self.assertEqual(next(generator), self.addy1)
      self.assertEqual(next(generator), self.addy3)

  @staticmethod
  def _mock_get_digest(key_iterator):
    # type: (KeyIterator) -> Digest
    """
    Mocks the behavior of :py:class:`KeyGenerator`, to speed up unit
    tests.

    Note that :py:class:`KeyGenerator` has its own test case, so we're
    not impacting the stability of the codebase by doing this.
    """
    # noinspection SpellCheckingInspection
    digests = [
      b'KDWISSPKPF9DZNKMYEVPPYI9CXMFZRAAKCQNMFJI'
      b'JIQLT9IPMEVVNYBTIBTN9CBCJMYTUMSRJAEMUUMIA',

      b'XUWRYOZQYEVM9CRZZPZQRTAHBMLM9EYMZZIYRFV9'
      b'GZST9XGK9LWUDGIXCCRFLWHUJPYQ9MMYDZEMAJZOI',

      b'SEJHPHEF9NXPPZQUOVGZNUZSP9DQOBRVSAGADUAD'
      b'EPRDFQJPXTOJGFPEXUPRQUYTTSD9GVPXTWWZQSGXA',

      b'LNXDEKQCP9OXMBNDUJCZIMVRVGJLKFVMMRPHROSH'
      b'XCWW9M9QGYVUMPXCR9ANPEPVGBI9WOERTFDAGKCVZ',
    ]

    key_index = key_iterator.current

    # Simulate generating the key.
    key_iterator.current += key_iterator.step

    # This should still behave like the real thing, so that we can
    # verify that :py:class`AddressGenerator` is invoking the key
    # generator correctly.
    return Digest(digests[key_index], key_index)


class MemoryAddressCacheTestCase(TestCase):
  def setUp(self):
    super(MemoryAddressCacheTestCase, self).setUp()

    # Define some values we can reuse across tests.
    # noinspection SpellCheckingInspection
    self.addy =\
      Address(
        trytes =
          b'TESTVALUE9DONTUSEINPRODUCTION99999J9XDHH'
          b'LHKET9PHTEUAHFFCDCP9ECIDPALFMFSCTCIHMD9CY',

        key_index = 42,
      )

  def tearDown(self):
    super(MemoryAddressCacheTestCase, self).tearDown()

    # Disable the global cache, in case the test installed one.
    AddressGenerator.cache = None

  def test_global_cache(self):
    """
    Installing a cache that affects all :py:class:`AddressGenerator`
    instances.
    """
    # Install the cache globally.
    AddressGenerator.cache = MemoryAddressCache()

    mock_generate_address = Mock(return_value=self.addy)

    with patch(
        'cornode.crypto.addresses.AddressGenerator._generate_address',
        mock_generate_address,
    ):
      generator1 = AddressGenerator(Seed.random())

      addy1 = generator1.get_addresses(42)
      mock_generate_address.assert_called_once()

      # The second time we try to generate the same address, it is
      # fetched from the cache.
      addy2 = generator1.get_addresses(42)
      mock_generate_address.assert_called_once()
      self.assertEqual(addy2, addy1)

      # Create a new AddressGenerator and verify it uses the same
      # cache.
      generator2 = AddressGenerator(generator1.seed)

      # Cache is global, so the cached address is returned again.
      addy3 = generator2.get_addresses(42)
      mock_generate_address.assert_called_once()
      self.assertEqual(addy3, addy1)

  def test_local_cache(self):
    """
    Installing a cache only for a single instance of
    :py:class:`AddressGenerator`.
    """
    mock_generate_address = Mock(return_value=self.addy)

    with patch(
        'cornode.crypto.addresses.AddressGenerator._generate_address',
        mock_generate_address,
    ):
      generator1 = AddressGenerator(Seed.random())

      # Install the cache locally.
      generator1.cache = MemoryAddressCache()

      addy1 = generator1.get_addresses(42)
      mock_generate_address.assert_called_once()

      # The second time we try to generate the same address, it is
      # fetched from the cache.
      addy2 = generator1.get_addresses(42)
      mock_generate_address.assert_called_once()
      self.assertEqual(addy2, addy1)

      # Create a new instance to verify it has its own cache.
      generator2 = AddressGenerator(generator1.seed)

      # The generator has its own cache instance, so even though the
      # resulting address is the same, it is not fetched from cache.
      addy3 = generator2.get_addresses(42)
      self.assertEqual(mock_generate_address.call_count, 2)
      self.assertEqual(addy3, addy1)

  def test_cache_miss_key_index(self):
    """
    Cached addresses are keyed by key index.
    """
    AddressGenerator.cache = MemoryAddressCache()

    mock_generate_address = Mock(return_value=self.addy)

    with patch(
        'cornode.crypto.addresses.AddressGenerator._generate_address',
        mock_generate_address,
    ):
      generator = AddressGenerator(Seed.random())

      generator.get_addresses(42)
      mock_generate_address.assert_called_once()

      generator.get_addresses(43)
      self.assertEqual(mock_generate_address.call_count, 2)

  def test_cache_miss_seed(self):
    """
    Cached addresses are keyed by seed.
    """
    AddressGenerator.cache = MemoryAddressCache()

    mock_generate_address = Mock(return_value=self.addy)

    with patch(
        'cornode.crypto.addresses.AddressGenerator._generate_address',
        mock_generate_address,
    ):
      generator1 = AddressGenerator(Seed.random())
      generator1.get_addresses(42)
      mock_generate_address.assert_called_once()

      generator2 = AddressGenerator(Seed.random())
      generator2.get_addresses(42)
      self.assertEqual(mock_generate_address.call_count, 2)

  def test_thread_safety(self):
    """
    Address cache is thread-safe, eliminating invalid cache misses when
    multiple threads attempt to access the cache concurrently.
    """
    AddressGenerator.cache = MemoryAddressCache()

    seed = Seed.random()

    generated = []

    def get_address():
      generator = AddressGenerator(seed)
      generated.extend(generator.get_addresses(0))

    # noinspection PyUnusedLocal
    def mock_generate_address(address_generator, key_iterator):
      # type: (AddressGenerator, KeyIterator) -> Address
      # Insert a teensy delay, to make it more likely that multiple
      # threads hit the cache concurrently.
      sleep(0.01)

      # Note that in this test, the address generator always returns a
      # new instance.
      return Address(self.addy, key_index=key_iterator.current)

    with patch(
        'cornode.crypto.addresses.AddressGenerator._generate_address',
        mock_generate_address,
    ):
      threads = [Thread(target=get_address) for _ in range(100)]

      for t in threads:
        t.start()

      for t in threads:
        t.join()

    # Quick sanity check.
    self.assertEqual(len(generated), len(threads))

    # If the cache is operating in a thread-safe manner, then it will
    # always return the exact same instance, given the same seed and
    # key index.
    expected = generated[0]
    for actual in generated[1:]:
      # Compare `id` values instead of using ``self.assertIs`` because
      # the failure message is a bit easier to understand.
      self.assertEqual(id(actual), id(expected))
