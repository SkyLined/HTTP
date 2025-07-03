def fApplyHeaderSettingsToRequest(
  *,
  asbRemoveHeadersForLowerNames,
  dtsbReplaceHeaderNameAndValue_by_sLowerName,
  atsbAddHeadersNameAndValue,
  oRequest,
):
  for sbHeaderLowerName in asbRemoveHeadersForLowerNames:
    oRequest.oHeaders.fbRemoveForNormalizedName(sbHeaderLowerName);
  for (sbHeaderLowerName, (sbHeaderName, sbHeaderValue)) in dtsbReplaceHeaderNameAndValue_by_sLowerName.items():
    oRequest.oHeaders.foReplaceOrAddUniqueNameAndValue(sbHeaderName, sbHeaderValue);
  for (sbHeaderName, sbHeaderValue) in atsbAddHeadersNameAndValue:
    oRequest.oHeaders.foAddNameAndValue(sbHeaderName, sbHeaderValue);
