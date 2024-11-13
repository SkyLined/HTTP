def fApplyHeaderSettingsToRequest(
  asbRemoveHeadersForLowerNames,
  dtsbReplaceHeaderNameAndValue_by_sLowerName,
  atsbAddHeadersNameAndValue,
  oHTTPRequest,
):
  for sbHeaderLowerName in asbRemoveHeadersForLowerNames:
    oHTTPRequest.oHeaders.fbRemoveHeadersForName(sbHeaderLowerName);
  for (sbHeaderLowerName, (sbHeaderName, sbHeaderValue)) in dtsbReplaceHeaderNameAndValue_by_sLowerName.items():
    oHTTPRequest.oHeaders.fbRemoveHeadersForName(sbHeaderLowerName);
    oHTTPRequest.oHeaders.foAddHeaderForNameAndValue(sbHeaderName, sbHeaderValue);
  for (sbHeaderName, sbHeaderValue) in atsbAddHeadersNameAndValue:
    oHTTPRequest.oHeaders.foAddHeaderForNameAndValue(sbHeaderName, sbHeaderValue);
