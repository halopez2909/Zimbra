f = open('zimbra-frontend/src/api/api.ts', 'r', encoding='utf-8')
content = f.read()
f.close()
content = content.replace(
    'export const createFollowup',
    'export const createFollowUp'
).replace(
    'export const getFollowupsByClient',
    'export const getFollowUpsByClient'
)
f = open('zimbra-frontend/src/api/api.ts', 'w', encoding='utf-8')
f.write(content)
f.close()
print('OK')
