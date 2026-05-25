f = open('src/pages/ProposalsPage.tsx', 'r', encoding='utf-8')
lines = f.readlines()
f.close()

# Fix amount en linea 140
lines[140] = "                    <td style={{ padding: '8px', fontWeight: 'bold' }}>{'$' + Number(p.proposed_amount).toLocaleString()}</td>\n"

# Agregar columna Action en headers - despues de Close Date
lines[130] = "                  <th style={{ padding: '10px', textAlign: 'left' }}>Close Date</th>\n                  <th style={{ padding: '10px', textAlign: 'left' }}>Action</th>\n"

# Agregar celda Action en filas - despues de close date
lines[146] = """                    <td style={{ padding: '8px', fontSize: '13px' }}>{p.estimated_close_date || '-'}</td>
                    <td style={{ padding: '8px' }}>
                      {p.status !== 'accepted' && p.status !== 'rejected' && (
                        <select
                          value={p.status}
                          onChange={async e => {
                            try {
                              await fetch('http://localhost:9000/proposals/' + p.proposal_id + '/status', {
                                method: 'PATCH',
                                headers: { 'Content-Type': 'application/json' },
                                body: JSON.stringify({ status: e.target.value })
                              });
                              setProposals(await getProposals());
                              setPipeline(await getPipeline());
                            } catch {}
                          }}
                          style={{ padding: '4px 8px', borderRadius: '4px', border: '1px solid #ccc', fontSize: '12px' }}
                        >
                          <option value="draft">Draft</option>
                          <option value="sent">Sent</option>
                          <option value="negotiation">Negotiation</option>
                          <option value="accepted">Accept</option>
                          <option value="rejected">Reject</option>
                        </select>
                      )}
                      {(p.status === 'accepted' || p.status === 'rejected') && (
                        <span style={{ fontSize: '12px', color: '#888' }}>{p.status}</span>
                      )}
                    </td>\n"""

f = open('src/pages/ProposalsPage.tsx', 'w', encoding='utf-8')
f.writelines(lines)
f.close()
print('OK')
