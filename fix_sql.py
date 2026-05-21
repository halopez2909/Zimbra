content = open('sql/04_triggers_procedures.sql', 'r', encoding='utf-8').read()
content = content.replace('\\$', 'cls')
open('sql/04_triggers_procedures.sql', 'w', encoding='utf-8').write(content)
print('OK')
