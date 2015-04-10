# -*- coding: utf-8 -*-
### Automatically generated by repyhelper.py ### /Users/wojciech/seattle/demokit/xmlparse.repy

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
  xmlparse.repy

<Started>
  April 2009

<Author>
  Conrad Meyer <cemeyer@u.washington.edu>

<Purpose>
  Provide a relatively simplistic but usable xml parsing library for
  RePy.
"""

class xmlparse_XMLParseError(Exception):
  """Exception raised when an error is encountered parsing the XML."""
  pass




class xmlparse_XMLTreeNode:
  """
  <Purpose>
    Provide a simple tree structure for XML data.

  <Exceptions>
    None.

  <Example Use>
    node = xmlparse_parse("<Some><xml><data></data></xml></Some>")
  """   


  def __init__(self, tag_name):
    self.tag_name = tag_name
    self.children = None
    self.content = None
    self.attributes = {}


  def __repr__(self):
    """Provide a pretty representation of an XML tree."""

    if self.content is not None:
      return "%s:\"%s\"" % (self.tag_name, self.content)
    else:
      return "%s:%s" % (self.tag_name, str(self.children))


  def to_string(self):
    result = "<" + self.tag_name
    for attribute_name in self.attributes.keys():
      attribute_value_escaped = \
          self.attributes[attribute_name].replace("\"", "\\\"")
      result += " " + attribute_name + "=\"" + attribute_value_escaped + "\""
    
    if self.content is None:
      result += ">"
      for childnode in self.children:
        result += childnode.to_string()
      result += "</" + self.tag_name + ">"
    else:
      if len(self.content) == 0:
        result += "/>"
      else:
        result += ">" + self.content + "</" + self.tag_name + ">"

    return result




def xmlparse_parse(data):
  """
  <Purpose>
    Parses an XML string into an xmlparse_XMLTreeNode containing the root
    item.

  <Arguments>
    data:
           The data to parse.

  <Exceptions>
    xmlparse_XMLParseError if parsing fails.

  <Side Effects>
    None.

  <Returns>
    An xmlparse_XMLTreeNode tree.
  """

  data = data.lstrip()
  if data.startswith("<?xml"):
    data = data[data.find("?>")+2:]
  
  # Well-formed XML Documents have exactly one root node
  parsed_elements = _xmlparse_parse(data)
  if len(parsed_elements) != 1:
    raise xmlparse_XMLParseError("XML response from server contained more than one root node")

  return parsed_elements[0]




def _xmlparse_read_attributes(string):
  # Returns a pair containing the dictionary of attributes and remainder
  # of the string on success; excepts on failure.

  # Q_n corresponds to the state_* constant of the same value. The starting
  # node is Q_1.
  #
  #  [ Done ]
  #     ^
  #     |
  #     | (>, /)
  #     |
  #     \--------\ 
  #              |
  #        ,-.   | v-----------------------------------\
  # space (   [ Q_1 ]                                  |
  #        `->   | ^-----------------------\ (')       |
  #              |                         |           |
  #              |                (')      |   <-.     | (")
  #              | non-space   /------->[ Q_4 ]   )    |
  #              |             |               `-'     |
  #  (space)     v     (=)     |             (other)   |
  #     /-----[ Q_2 ]------>[ Q_3 ]-------->[ Q_5 ]----/
  #     |      ^   )           |      (")    ^   )
  #     |       `-'            |              `-'
  #     |     (other)   (other)|             (other)
  #     |                      |
  #     v                      |
  #[Exception]<----------------/

  # Basically the state machine is used to read a list of attribute-pairs,
  # terminated by a '/' or '>'. Attribute pairs either look like:
  #   name='value'
  # or:
  #   name="value"
  # Single-quoted attributes can contain double-quotes, and vice-versa, but
  # single-quotes in single-quoted attributes must be escaped.
  # 
  # To do this we start in Q_1, which consumes input until we arrive at
  # something that looks like an attribute name. In Q_2 we consume characters
  # for the attribute name until it looks like the attribute name is finished.
  # In Q_3 we read a single character to determine what type of quoting is
  # used for the attribute value. In Q_4 or Q_5, we read the attribute's value
  # until the string is closed, then go back to Q_1 (saving the attribute name
  # and value into the dictionary). We decide we are done when we encounter a
  # '>' or '/' in Q_1.

  # Constant states:
  state_EXPECTING_ATTRNAME = 1
  state_READING_ATTRNAME = 2
  state_EXPECTING_ATTRVALUE = 3
  state_READING_ATTRVALUE_SINGLEQUOTE = 4
  state_READING_ATTRVALUE_DOUBLEQUOTE = 5

  current_position = 0
  current_state = 1
  current_attrname = ""
  current_attrvalue = ""
  attributes = {}

  while True:
    if current_position >= len(string):
      raise xmlparse_XMLParseError(
          "Failed to parse element attribute list -- input ran out " + \
              "before we found a closing '>' or '/'")

    current_character = string[current_position]

    if current_state == state_EXPECTING_ATTRNAME:
      if current_character.isspace():
        pass    # We stay in this state
      elif current_character == '>' or current_character == '/':
        # We're finished reading attributes
        return (attributes, string[current_position:])
      else:
        current_attrname += current_character
        current_state = state_READING_ATTRNAME

    elif current_state == state_READING_ATTRNAME:
      if current_character.isspace():
        raise xmlparse_XMLParseError(
            "Failed to parse element attribute list -- attribute " + \
                "ended unexpectedly with a space")
      elif current_character == "=":
        current_state = state_EXPECTING_ATTRVALUE
      else:
        current_attrname += current_character

    elif current_state == state_EXPECTING_ATTRVALUE:
      if current_character == '\'':
        current_state = state_READING_ATTRVALUE_SINGLEQUOTE
      elif current_character == '"':
        current_state = state_READING_ATTRVALUE_DOUBLEQUOTE
      else:
        raise xmlparse_XMLParseError(
            "Failed to parse element attribute list -- attribute " + \
                "values must be quoted")

    elif current_state == state_READING_ATTRVALUE_SINGLEQUOTE:
      if current_character == '\'':
        attributes[current_attrname] = current_attrvalue
        current_state = state_EXPECTING_ATTRNAME
        current_attrname = ""
        current_attrvalue = ""
      else:
        current_attrvalue += current_character

    elif current_state == state_READING_ATTRVALUE_DOUBLEQUOTE:
      if current_character == '"':
        attributes[current_attrname] = current_attrvalue
        current_state = state_EXPECTING_ATTRNAME
        current_attrname = ""
        current_attrvalue = ""
      else:
        current_attrvalue += current_character

    current_position += 1




def _xmlparse_node_from_string(string):
  # string:
  #   <tag attr1="value" attr2='value'>content</tag>
  # Content may be a string or a list of children nodes depending on if the
  # first non-space character is a '<' or not.

  string = string.lstrip()
  if not string.startswith("<"):
    raise xmlparse_XMLParseError("Error parsing XML -- doesn't " + \
        "start with '<'")

  string = string[1:]

  read_pos = 0
  while True:
    if read_pos >= len(string):
      raise xmlparse_XMLParseError("Error parsing XML -- parser " + \
          "ran out of input trying to read a tag")

    # The tag name is ended with a space or a closing angle-brace or
    # a "/".
    curchar = string[read_pos]
    if curchar.isspace() or curchar == ">" or curchar == "/":
      break

    read_pos += 1

  tag = string[0:read_pos]
  string = string[read_pos:]

  # Get the attribute dictionary and remaining string (which will be
  # "> ... [ inner stuff ] </[tag_name]>" or "/>" for well-formed XML).
  attributes, string = _xmlparse_read_attributes(string)

  # "Empty" elements look like: "<[tag_name] [... maybe attributes] />" and
  # not "Empty" elements look like:
  # "<[tag_name] [... maybe attributes]> [inner content] </[tag_name]>".
  empty_element = False
  if string.startswith(">"):
    string = string[1:]
  elif string.startswith("/>"):
    string = string[2:]
    empty_element = True

  xmlnode = xmlparse_XMLTreeNode(tag)
  xmlnode.attributes = attributes

  if empty_element:
    xmlnode.content = ""

  else:
    # Locate the end-boundary of the inner content of this element.
    ending_tag_position = string.rfind("</")
    if ending_tag_position < 0:
      raise xmlparse_XMLParseError("XML parse error -- could not " + \
          "locate closing tag")

    # If this elements starting and closing tag names do not match, this XML
    # is not well-formed.
    if not string.startswith("</" + tag, ending_tag_position):
      raise xmlparse_XMLParseError("XML parse error -- different " + \
          "opening / closing tags at the same nesting level")

    # If the inner content starts with another element, this element has
    # children.  Otherwise, it has content, which is just a string containing
    # the inner content.
    tag_body = string[:ending_tag_position]
    if tag_body.lstrip().startswith("<"):
      xmlnode.children = _xmlparse_parse(tag_body.lstrip())
    else:
      xmlnode.content = tag_body

  return xmlnode




def _xmlparse_find_next_tag(xmldata):
  # Finds the position of the start of the next same-level tag in this XML
  # document.

  read_position = 0
  nested_depth = 0

  original_length = len(xmldata)
  xmldata = xmldata.lstrip()
  length_difference = original_length - len(xmldata)

  # Seek to another XML tag at the same depth.
  while True:
    if xmldata.startswith("</", read_position) or \
        xmldata.startswith("/>", read_position):
      nested_depth -= 1
    elif xmldata.startswith("<", read_position):
      nested_depth += 1

    read_position += 1

    if read_position >= len(xmldata):
      return read_position + length_difference

    if nested_depth == 0:
      nexttagposition = xmldata.find("<", read_position)

      if nexttagposition < 0:
        return original_length
      else:
        return nexttagposition + length_difference




def _xmlparse_parse(xmldata):
  # Takes a raw XML stream and returns a list of XMLTreeNodes.

  nodelist = []

  while True:
    # Whitespace between tags isn't important to the content of
    # an XML document.
    xmldata = xmldata.strip()

    # Strip out XML comments.
    if xmldata.startswith("<!--"):
      commentendloc = xmldata.find("-->", 4)
      if commentendloc < 0:
        raise xmlparse_XMLParseError("XML parse error -- comment " + \
            "missing close tag ('-->')")
      xmldata = xmldata[commentendloc+3:]
      continue

    # Find the end of the current tag.
    nexttagend = _xmlparse_find_next_tag(xmldata)

    thisnode_str = xmldata[0:nexttagend]
    xmldata = xmldata[nexttagend:]

    # Parse a tag out of the string we just found.
    thisnode = _xmlparse_node_from_string(thisnode_str)
    nodelist.append(thisnode)

    if not xmldata.strip().startswith("<"):
      break

  return nodelist

### Automatically generated by repyhelper.py ### /Users/wojciech/seattle/demokit/xmlparse.repy
