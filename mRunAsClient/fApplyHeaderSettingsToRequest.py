def fApplyHeaderSettingsToRequest(
  *,
  asbRemoveHeadersForLowerNames,
  dtsbReplaceHeaderNameAndValue_by_sLowerName,
  atsbAddHeadersNameAndValue,
  oRequest,
):
  for sbHeaderLowerName in asbRemoveHeadersForLowerNames:
    oRequest.oHeaders.fbRemoveHeadersForName(sbHeaderLowerName);
  for (sbHeaderLowerName, (sbHeaderName, sbHeaderValue)) in dtsbReplaceHeaderNameAndValue_by_sLowerName.items():
    oRequest.oHeaders.fbRemoveHeadersForName(sbHeaderLowerName);
    oRequest.oHeaders.foAddHeaderForNameAndValue(sbHeaderName, sbHeaderValue);
  for (sbHeaderName, sbHeaderValue) in atsbAddHeadersNameAndValue:
    oRequest.oHeaders.foAddHeaderForNameAndValue(sbHeaderName, sbHeaderValue);
