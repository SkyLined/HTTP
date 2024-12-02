import base64;
import binascii;
import re;

from mColorsAndChars import (
  COLOR_INFO,
  COLOR_NORMAL,
);
from .faxGetStringOrBytesOutput import faxGetStringOrBytesOutput;

sbBase64EncodedValueRegExp = rb"(?:[A-Za-z0-9+/]{4})+(?:[A-Za-z0-9+/]{2}==|[A-Za-z0-9+/]{3}=)?";
rBase64EncodedValues = re.compile(rb"%s(?:([!#$%%&*\-.:;@^_|~])%s)*" % (sbBase64EncodedValueRegExp, sbBase64EncodedValueRegExp));
rHexadecimalValue = re.compile(rb"([0-9A-Fa-f]{2})+");
rGUID = re.compile(rb"[0-9A-Fa-f]{8}(?:-[0-9A-Fa-f]{4}){4}[0-9A-Fa-f]{8}");

def faxGetDecodedValuesOutput(sbEncodedValues, u0MaxLength = None):
  if len(sbEncodedValues) == 0 or rGUID.match(sbEncodedValues) or rHexadecimalValue.match(sbEncodedValues):
    return [];
  oBase64EncodedDataMatch = rBase64EncodedValues.match(sbEncodedValues);
  if oBase64EncodedDataMatch:
    sb0Separator = oBase64EncodedDataMatch.group(1);
    if sb0Separator is None:
      try:
        sbDecodeValue = base64.b64decode(sbEncodedValues);
      except binascii.Error:
        pass;
      else:
        return [
          [
            COLOR_NORMAL, "└─> Base64 decoded value: ", faxGetStringOrBytesOutput(sbDecodeValue, u0MaxLength),
          ],
        ];
    else:
      try:
        asbDecodedValues = [
          base64.b64decode(sbBase64EncodedValue)
          for sbBase64EncodedValue in sbEncodedValues.split(sb0Separator)
        ];
      except binascii.Error:
        pass;
      else:
        return [
          [
            COLOR_NORMAL, "╘═> ",
            COLOR_INFO, str(len(asbDecodedValues)),
            COLOR_NORMAL, " base64 decoded values separated by '",
            COLOR_INFO, str(sb0Separator, "ascii", "strict"),
            COLOR_NORMAL, "':",
          ],
        ] + [
          [
            COLOR_NORMAL, "  ", faxGetStringOrBytesOutput(sbBase64DecodedValue, u0MaxLength),
          ]
          for sbBase64DecodedValue in asbDecodedValues
        ];
  return [];