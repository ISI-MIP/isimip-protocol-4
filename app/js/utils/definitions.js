import { castArray, isNil } from 'lodash'

export const getSpecifierList = (row) => {
  const specifier = row.specifier
  const specifierAlias = row.specifier_alias
  const specifierList = isNil(specifierAlias) ? [specifier] : castArray(specifierAlias)

  return specifierList
}
