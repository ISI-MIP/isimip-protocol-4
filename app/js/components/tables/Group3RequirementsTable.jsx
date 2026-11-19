import React from 'react'
import PropTypes from 'prop-types'
import ReactMarkdown from 'react-markdown'
import { isEmpty } from 'lodash'

import { filterRows } from '../../utils/filter'

import Sectors from '../badges/Sectors'

const Group3RequirementsTable = function({ config, caption, rows }) {
  const filteredRows = filterRows(config, rows)

  return (
    <table className="table table-bordered table-fixed">
      <caption>
        <ReactMarkdown components={{p: 'span'}}>{caption}</ReactMarkdown>
      </caption>
      <thead className="table-dark">
        <tr>
          <th style={{width: '25%'}}>Forcing</th>
          <th style={{width: '25%'}}>Harmonized dataset</th>
          <th style={{width: '50%'}}>Required for</th>
        </tr>
      </thead>
      <tbody>
        {
          filterRows(config, rows).map((row, index) => {
            return (
              <tr key={index}>
                <td>{row.title}</td>
                <td>
                  {
                    row.datasets && (
                      <ul className="list-unstyled">
                        {
                          row.datasets.map((d, i) => <li key={i}>{d}</li>)
                        }
                      </ul>
                    )
                  }
                </td>
                <td>
                  <Sectors config={config} sectors={row.required} />
                  {
                    !isEmpty(row.comment) && (
                      <div className="mt-2">
                        <ReactMarkdown>{row.comment}</ReactMarkdown>
                      </div>
                    )
                  }
                </td>
              </tr>
            )
          })
        }
        {
          isEmpty(filteredRows) && <tr>
            <td colSpan={config.simulation_round.endsWith('a') ? 4 : 5}>
              No Group III requirements have been defined for this selection of sectors, yet.
            </td>
          </tr>
        }
      </tbody>
    </table>
  )
}

Group3RequirementsTable.propTypes = {
  config: PropTypes.object.isRequired,
  caption: PropTypes.string.isRequired,
  rows: PropTypes.array.isRequired
}

export default Group3RequirementsTable
