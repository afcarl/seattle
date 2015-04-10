# -*- coding: utf-8 -*-
### Automatically generated by repyhelper.py ### /Users/wojciech/seattle/demokit/base64.repy

### THIS FILE WILL BE OVERWRITTEN!
### DO NOT MAKE CHANGES HERE, INSTEAD EDIT THE ORIGINAL SOURCE FILE
###
### If changes to the src aren't propagating here, try manually deleting this file. 
### Deleting this file forces regeneration of a repy translation


from repyportability import *
import repyhelper
mycontext = repyhelper.get_shared_context()
callfunc = 'import'
callargs = []

"""
<Program Name>
  $Id: base64.repy 2527 2009-07-26 22:48:38Z cemeyer $

<Started>
  April 12, 2009

<Author>
  Michael Phan-Ba

<Purpose>
  Provides data encoding and decoding as specified in RFC 3548. This
  module implements a subset of the Python module base64 interface.

  b32encode(), b32decode(), b16encode(), b16decode(), decode(),
  decodestring(), encode(), and encodestring() are not currently
  implemented.

<Changes>

  2009-04-12  Michael Phan-Ba  <mdphanba@gmail.com>

  * Initial release

  2009-05-23  Michael Phan-Ba  <mdphanba@gmail.com>

  * (b64encode, b64decode, standard_b64encode, standard_b64decode,
    urlsafe_encode, urlsafe_decode): Renamed functions with base64 prefix

  2009-05-24  Michael Phan-Ba  <mdphanba@gmail.com>

  * Set property svn:keyword to "Id" 

"""

# The Base64 for use in encoding
BASE64_ALPHABET = \
  "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"

def base64_b64encode(s, altchars=None):
  """
  <Purpose>
    Encode a string using Base64.

  <Arguments>
    s:
      The string to encode.

    altchars:
      An optional string of at least length 2 (additional characters are
      ignored) which specifies an alternative alphabet for the + and /
      characters.  The default is None, for which the standard Base64
      alphabet is used.

  <Exceptions>
    None.

  <Side Effects>
    None.

  <Returns>
    The encoded string.

  """
  # Build the local alphabet.
  if altchars is None:
    base64_alphabet = BASE64_ALPHABET
  else:
    base64_alphabet = BASE64_ALPHABET[:62] + altchars

  # Change from characters to integers for binary operations.
  bytes = []
  for x in s:
    bytes.append(ord(x))

  # Encode the 8-bit words into 6-bit words.
  x6bit_words = []
  index = 0
  while True:

    # Encode the first 6 bits from three 8-bit values.
    try:
      x8bits = bytes[index]
    except IndexError:
      break
    else:
      x6bits = x8bits >> 2
      leftover_bits = x8bits & 3
      x6bit_words.append(base64_alphabet[x6bits])

    # Encode the next 8 bits.
    try:
      x8bits = bytes[index + 1]
    except IndexError:
      x6bits = leftover_bits << 4
      x6bit_words.extend([base64_alphabet[x6bits], "=="])
      break
    else:
      x6bits = (leftover_bits << 4) | (x8bits >> 4)
      leftover_bits = x8bits & 15
      x6bit_words.append(base64_alphabet[x6bits])

    # Encode the final 8 bits.
    try:
      x8bits = bytes[index + 2]
    except IndexError:
      x6bits = leftover_bits << 2
      x6bit_words.extend([base64_alphabet[x6bits], "="])
      break
    else:
      x6bits = (leftover_bits << 2) | (x8bits >> 6)
      x6bit_words.append(base64_alphabet[x6bits])
      x6bits = x8bits & 63
      x6bit_words.append(base64_alphabet[x6bits])

    index += 3

  return "".join(x6bit_words)

def base64_b64decode(s, altchars=None):
  """
  <Purpose>
    Decode a Base64 encoded string.  The decoder ignores all non
    characters not in the Base64 alphabet for compatibility with the
    Python library.  However, this introduces a security loophole in
    which covert or malicious data may be passed.

  <Arguments>
    s:
      The string to decode.

    altchars:
      An optional string of at least length 2 (additional characters are
      ignored) which specifies an alternative alphabet for the + and /
      characters.  The default is None, for which the standard Base64
      alphabet is used.

  <Exceptions>
    None.

  <Side Effects>
    TypeError on decoding error.

  <Returns>
    The decoded string.

  """
  # Build the local alphabet.
  if altchars is None:
    base64_alphabet = BASE64_ALPHABET
  else:
    base64_alphabet = BASE64_ALPHABET[:62] + altchars

  # Generate the translation maps for decoding a Base64 string.
  translate_chars = []
  for x in xrange(256):
    char = chr(x)
    translate_chars.append(char)

  # Build the strings of characters to delete.
  delete_chars = []
  for x in translate_chars:
    if x not in base64_alphabet:
      delete_chars.append(x)
  delete_chars = "".join(delete_chars)

  # Insert the 6-bit Base64 values into the translation string.
  k = 0
  for v in base64_alphabet:
    translate_chars[ord(v)] = chr(k)
    k += 1
  translate_chars = "".join(translate_chars)

  # Count the number of padding characters at the end of the string.
  num_pad = 0
  i = len(s) - 1
  while i >= 0:
    if s[i] == "=":
      num_pad += 1
    else:
      break
    i -= 1

  # Translate the string into 6-bit characters and delete extraneous
  # characters.
  s = s.translate(translate_chars, delete_chars)

  # Determine correct alignment by calculating the number of padding
  # characters needed for compliance to the specification.
  align = (4 - (len(s) & 3)) & 3
  if align == 3:
    raise TypeError("Incorrectly encoded base64 data (has 6 bits of trailing garbage)")
  if align > num_pad:
    # Technically, this isn't correctly padded. But it's recoverable, so let's
    # not care.
    pass

  # Change from characters to integers for binary operations.
  x6bit_words = []
  for x in s:
    x6bit_words.append(ord(x))
  for x in xrange(align):
    x6bit_words.append(-1)

  # Decode the 6-bit words into 8-bit words.
  bytes = []
  index = 0
  while True:

    # Work on four 6-bit quantities at a time.  End when no more data is
    # available.
    try:
      (x6bits1, x6bits2, x6bits3, x6bits4) = x6bit_words[index:index + 4]
    except ValueError:
      break

    # Save an 8-bit quantity.
    bytes.append((x6bits1 << 2) | (x6bits2 >> 4))

    # End of valid data.
    if x6bits3 < 0:
      break

    # Save an 8-bit quantity.
    bytes.append(((x6bits2 & 15) << 4) | (x6bits3 >> 2))

    # End of valid data.
    if x6bits4 < 0:
      break

    # Save an 8-bit quantity.
    bytes.append(((x6bits3 & 3) << 6) | x6bits4)

    # Next four 6-bit quantities.
    index += 4

  return "".join([chr(x) for x in bytes])

def base64_standard_b64encode(s):
  """
  <Purpose>
    Encode a string using the standard Base64 alphabet.

  <Arguments>
    s:
      The string to encode.

  <Exceptions>
    None.

  <Side Effects>
    None.

  <Returns>
    The encoded string.

  """
  return base64_b64encode(s)

def base64_standard_b64decode(s):
  """
  <Purpose>
    Decode a Base64 encoded string using the standard Base64 alphabet.

  <Arguments>
    s:
      The string to decode.

  <Exceptions>
    None.

  <Side Effects>
    TypeError on decoding error.

  <Returns>
    The decoded string.

  """
  return base64_b64decode(s)


def base64_urlsafe_b64encode(s):
  """
  <Purpose>
    Encode a string using a URL-safe alphabet, which substitutes -
    instead of + and _ instead of / in the standard Base64 alphabet.

  <Arguments>
    s:
      The string to encode.

  <Exceptions>
    None.

  <Side Effects>
    None.

  <Returns>
    The encoded string.

  """
  return base64_b64encode(s, "-_")


def base64_urlsafe_b64decode(s):
  """
  <Purpose>
    Decode a Base64 encoded string using a URL-safe alphabet, which
    substitutes - instead of + and _ instead of / in the standard Base64
    alphabet.

  <Arguments>
    s:
      The string to decode.

  <Exceptions>
    None.

  <Side Effects>
    TypeError on decoding error.

  <Returns>
    The decoded string.

  """
  return base64_b64decode(s, "-_")

### Automatically generated by repyhelper.py ### /Users/wojciech/seattle/demokit/base64.repy
