# -*- coding: utf-8 -*-
### Automatically generated by repyhelper.py ### /Users/wojciech/seattle/demokit/random.repy

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
  random.repy

<Author>
  Justin Cappos: random_sample

  Modified by Anthony Honstain
    random_nbit_int and random_long_to_bytes is modified from 
    Python Cryptography Toolkit and was part of pycrypto which 
    is maintained by Dwayne C. Litzenberger
    
    random_range, random_randint, and random_int_below are modified 
    from the Python 2.6.1 random.py module. Which was:
    Translated by Guido van Rossum from C source provided by
    Adrian Baddeley.  Adapted by Raymond Hettinger for use with
    the Mersenne Twister  and os.urandom() core generators.  

<Purpose>
  Random routines (similar to random module in Python)
  
  
<Updates needed when emulmisc.py adds randombytes function>
  TODO-
    random_nbit_int currently uses random_randombytes as a source 
    of random bytes, this is not a permanent fix (the extraction 
    of random bytes from the float is not portable). The change will
    likely be made to random_randombytes (since calls os.urandom will
    likely be restricted to a limited number of bytes).  
  TODO - 
    random_randombytes will remained but serve as a helper function
    to collect the required number of bytes. Calls to randombytes
    will be restricted to a set number of bytes at a time, since
    allowing an arbitrary request to os.urandom would circumvent 
    performance restrictions. 
  TODO - 
    _random_long_to_bytes will no longer be needed.  
      
"""

repyhelper.translate_and_import('math.repy')

def random_randombytes(num_bytes, random_float=None):
  """
   <Purpose>
     Return a string of length num_bytes, made of random bytes 
     suitable for cryptographic use (because randomfloat draws
     from a os provided random source).
      
     *WARNING* If python implements float as a C single precision
     floating point number instead of a double precision then
     there will not be 53 bits of data in the coefficient.

   <Arguments>
     num_bytes:
               The number of bytes to request from os.urandom. 
               Must be a positive integer value.
     random_float:
                  Should not be used, available only for testing
                  so that predetermined floats can be provided.
    
   <Exceptions>
     None

   <Side Effects>
     This function results in one or more calls to randomfloat 
     which uses a OS source of random data which is metered.

   <Returns>
     A string of num_bytes random bytes suitable for cryptographic use.
  """
  # To ensure accurate testing, this allows the source
  # of random floats to be supplied.
  if random_float is None: 
    random_float = randomfloat()
  
  randombytes = ''
  
  # num_bytes/6 + 1 is used because at most a single float
  # can only result in 6 bytes of random data. So an additional
  # 6 bytes is added and them trimmed to the desired size.
  for byte in range(num_bytes/6 + 1):
    
    # Convert the float back to a integer by multiplying
    # it by 2**53, 53 is used because the expected precision
    # of a python float will be a C type double with a 53 bit 
    # coefficient, this will still depend on the implementation
    # but the standard is to expect 53 bits.
    randomint = int(random_float * (2**53)) 
    # 53 bits trimmed down to 48bits
    # and 48bits is equal to 6 bytes
    randomint = randomint >> 5  
    
    # Transform the randomint into a byte string, 6 bytes were
    # used to create this integer, but several of the leading 
    # bytes could have been trimmed off in the process.
    sixbytes = _random_long_to_bytes(randomint)
    
    # Add on the zeroes that should be there.
    if len(sixbytes) < 6: 
      # pad additions binary zeroes that were lost during 
      # the floats creation.
      sixbytes = '\x00'*(6-len(sixbytes)) + sixbytes 
    randombytes += sixbytes
  
  return randombytes[6 - num_bytes % 6:]
  
  
  
def _random_long_to_bytes(long_int):
  """
  <Purpose>
    Convert a long integer to a byte string.   
    Used by random_randombytes to convert integers recovered
    from random floats into its byte representation.
    Used by random_randombytes, random_randombytes is responsible
    for padding any required binary zeroes that are lost in the
    conversion process.     
  """

  long_int = long(long_int)
  byte_string = ''
  temp_int = 0
  
  # Special case to ensure that a non-empty string
  # is always returned.
  if long_int == 0:
    return '\000'
  
  while long_int > 0:
    # Use a bitwise AND to get the last 8 bits from the long.
    #    long_int  -->   1010... 010000001 (base 2)
    #    0xFF      -->            11111111
    #              _______________________
    #  Bitwise AND result -->     10000001
    tmp_int = long_int & 0xFF
    # Place the new character at the front of the string.
    byte_string = "%s%s" % (chr(tmp_int), byte_string)
    # Bitshift the long because the trailing 8 bits have just been read.
    long_int = long_int >> 8
      
  return byte_string



def random_nbit_int(num_bits):  
  """
  <Purpose>
    Returns an random integer that was constructed with
    num_bits many random bits. The result will be an
    integer [0, 2**(num_bits) - 1] inclusive.
     
    For Example:
     If a 10bit number is needed, random_nbit_int(10).
     Min should be greater or equal to 0
     Max should be less than or equal to 1023

    TODO-
      This function currently uses random_randombytes as a source 
      of random bytes, this is not a permanent fix (the extraction 
      of random bytes from the float is not portable). The change will
      likely be made to random_randombytes (since calls os.urandom will
      likely be restricted to a limited number of bytes).

  <Arguments>
    num_bits:
             The number of random bits to be used for construction
             of the random integer to be returned.

  <Exceptions>
    TypeError if non-integer values for num_bits.
      Will accept floats of the type 1.0, 2.0, ...
    
    ValueError if the num_bits is negative or 0.

  <Side Effects>
    This function results in one or more calls to randomfloat 
    which uses a OS source of random data which is metered.

  <Returns>
    Returns a random integer between [0, 2**(num_bits) - 1] inclusive.
  
  <Walkthrough of functions operation>
    This will be a step by step walk through of the key operations
    defined in this function, with the largest possible
    10 bit integer returned.
    
    num_bits = 10
    
    randstring = random_randombytes(10/8)  for our example we
    will suppose that the byte returned was '\xff' (which is the
    same as chr(255)).
    
    odd_bits = 10 % 8 = 2
    Once again we assume that random_randombytes(1) returns the
    maximum possible, which is '\xff'  
    chr = ord('\xff') >> (8 - odd_bits)
    -> chr = 255 >> (8 - 2)
    -> chr = 255 >> 6 = 3   Note 3 is the largest 2 bit number
    chr(3) is appended to randstring resulting in
    randstring = '\x03\xff' 
    
    value = 0
    length = 2
    
    STEP 1 (i = 0):
      value = value << 8 
      -> value = 0
      value = value + ord(randstring[0])
      -> value = 3
    
    STEP 2 (i = 1):
      value = value << 8
      -> value = 768
      value = value + ord(randstring[1])
      -> value = 1023
    
    return 1023
    This is the maximum possible 10 bit integer.
  """
  if num_bits <= 0:
    raise ValueError('number of bits must be greater than zero')
  if num_bits != int(num_bits):
    raise TypeError('number of bits should be an integer')
  
  # The number of bits requested may not be a multiple of
  # 8, then an additional byte will trimmed down.
  randstring = random_randombytes(num_bits/8)

  odd_bits = num_bits % 8
  # A single random byte be converted to an integer (which will
  # be an element of [0,255]) it will then be shifted to the required
  # number of bits.
  # Example: if odd_bits = 3, then the 8 bit retrieved from the 
  # single byte will be shifted right by 5.
  if odd_bits != 0:
    char = ord(random_randombytes(1)) >> (8 - odd_bits)
    randstring = chr(char) + randstring
  
  # the random bytes in randstring will be read from left to right
  result = 0L
  length = len(randstring)
  for i in range(0, length):
    # While result = 0, the bitshift left will still result in 0
    # Since we are dealing with integers, this does not result
    # in the loss of any information.
    result = (result << 8) 
    result = result + ord(randstring[i]) 
  
  assert(result < (2 ** num_bits))
  assert(result >= 0)

  return result



def random_int_below(upper_bound):
  """
  <Purpose>
    Returns an random integer in the range [0,upper_bound)
    
    Handles the case where upper_bound has more bits than returned
    by a single call to the underlying generator.
     
    For Example:
     For a 10bit number, random_int_below(10).
     results would be an element in of the set 0,1,2,..,9.
     
    NOTE: This function is a port from the random.py file in 
    python 2.6.2. For large numbers I have experienced inconsistencies
    when using a naive logarithm function to determine the
    size of a number in bits.  

  <Arguments>
    upper_bound:
           The random integer returned will be in [0, upper_bound).
           Results will be integers less than this argument.

  <Exceptions>
    TypeError if non-integer values for upper_bound.
    ValueError if the upper_bound is negative or 0.

  <Side Effects>
    This function results in one or more calls to randomfloat 
    which uses a OS source of random data which is metered.

  <Returns>
    Returns a random integer between [0, upper_bound).
  
  """
  
  try:
    upper_bound = int(upper_bound)
  except ValueError:
    raise TypeError('number should be an integer')
  
  if upper_bound <= 0:
    raise ValueError('number must be greater than zero')
  
    
  # If upper_bound == 1, the math_log call will loop infinitely.
  # The only int in [0, 1) is 0 anyway, so return 0 here.
  # Resolves bug #927
  if upper_bound == 1:
    return 0
  
  k = int(1.00001 + math_log(upper_bound - 1, 2.0))   # 2**k > n-1 > 2**(k-2)
  r = random_nbit_int(k)
  while r >= upper_bound:
    r = random_nbit_int(k)
  return r

 

def random_randrange(start, stop=None, step=1):
  """
  <Purpose>
    Choose a random item from range(start, stop[, step]).
    
  <Arguments>
    start:
      The random integer returned will be greater than
      or equal to start. 
  
    stop:
      The random integer returned will be less than stop.
      Results will be integers less than this argument.

    step:
      Determines which elements from the range will be considered.
     
  <Exceptions>
    ValueError:
      Non-integer for start or stop argument
      Empty range, if start < 0 and stop is None
      Empty range
      Zero or non-integer step for range

  <Side Effects>
    This function results in one or more calls to randomfloat 
    which uses a OS source of randomdata which is metered.
  
  <Returns>
    Random item from (start, stop[, step]) 'exclusive'
    
  <Notes on port>
    This fixes the problem with randint() which includes the
    endpoint; in Python this is usually not what you want.
    
    Anthony -I removed these since they do not apply
      int=int, default=None, maxwidth=1L<<BPF
      Do not supply the 'int', 'default', and 'maxwidth' arguments.
  """
  maxwidth = 1L<<53

  # This code is a bit messy to make it fast for the
  # common case while still doing adequate error checking.
  istart = int(start)
  if istart != start:
    raise ValueError, "non-integer arg 1 for randrange()"
  if stop is None:
    if istart > 0:
      if istart >= maxwidth:
        return random_int_below(istart)
      return int(randomfloat() * istart)
    raise ValueError, "empty range for randrange()"

  # stop argument supplied.
  istop = int(stop)
  if istop != stop:
    raise ValueError, "non-integer stop for randrange()"
  width = istop - istart
  if step == 1 and width > 0:
    # Note that
    #     int(istart + self.random()*width)
    # instead would be incorrect.  For example, consider istart
    # = -2 and istop = 0.  Then the guts would be in
    # -2.0 to 0.0 exclusive on both ends (ignoring that random()
    # might return 0.0), and because int() truncates toward 0, the
    # final result would be -1 or 0 (instead of -2 or -1).
    #     istart + int(self.random()*width)
    # would also be incorrect, for a subtler reason:  the RHS
    # can return a long, and then randrange() would also return
    # a long, but we're supposed to return an int (for backward
    # compatibility).

    if width >= maxwidth:
      return int(istart + random_int_below(width))
    return int(istart + int(randomfloat()*width))
  if step == 1:
    raise ValueError, "empty range for randrange() (%d,%d, %d)" % (istart, istop, width)

  # Non-unit step argument supplied.
  istep = int(step)
  if istep != step:
    raise ValueError, "non-integer step for randrange()"
  if istep > 0:
    n = (width + istep - 1) // istep
  elif istep < 0:
    n = (width + istep + 1) // istep
  else:
    raise ValueError, "zero step for randrange()"

  if n <= 0:
    raise ValueError, "empty range for randrange()"

  if n >= maxwidth:
    return istart + istep*random_int_below(n)
  return istart + istep*int(randomfloat() * n)



def random_randint(lower_bound, upper_bound):
  """
  <Purpose>
    Return random integer in range [lower_bound, upper_bound], 
    including both end points.
    
  <Arguments>
    upper_bound:
      The random integer returned will be less than upper_bound.
    lower_bound:
      The random integer returned will be greater than
      or equal to the lower_bound.

  <Exceptions>
    None

  <Side Effects>
    This function results in one or more calls to randomfloat 
    which uses a OS source of randomdata which is metered.
  
  <Returns>
    Random integer from [lower_bound, upper_bound] 'inclusive'  
  """
  return random_randrange(lower_bound, upper_bound+1)



def random_sample(population, k):
  """
  <Purpose>
    To return a list containing a random sample from the population.
    
  <Arguments>
    population:
               The elements to be sampled from.
    k: 
      The number of elements to sample
      
  <Exceptions>
    ValueError is sampler larger than population.
    
  <Side Effects>
    This function results in one or more calls to randomfloat 
    which uses a OS source of randomdata which is metered.
    
  <Returns>
    A list of len(k) with random elements from the population.
    
  """
  
  newpopulation = population[:]
  if len(population) < k:
    raise ValueError, "sample larger than population"

  retlist = []
  populationsize = len(population)-1

  for num in range(k):
    pos = random_randint(0,populationsize-num)
    retlist.append(newpopulation[pos])
    del newpopulation[pos]

  return retlist

### Automatically generated by repyhelper.py ### /Users/wojciech/seattle/demokit/random.repy
