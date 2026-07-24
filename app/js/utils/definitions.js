import { castArray } from 'lodash'

export const getSpecifierList = (row) => {
  const specifier = row.specifier
  const specifierAlias = row.specifier_alias

  if (specifierAlias) {
    return castArray(specifierAlias)
  } else {
    return [specifier]
  }
}
