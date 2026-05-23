f = open('sql/04_triggers_procedures.sql', 'r', encoding='utf-8')
content = f.read()
f.close()

# Remove conflict markers keeping all content
import re
# Remove <<<<<<, ======= and >>>>>>> lines
content = re.sub(r'<<<<<<< HEAD\n', '', content)
content = re.sub(r'=======\n', '', content)
content = re.sub(r'>>>>>>> origin/feature/jenn\n', '', content)

f = open('sql/04_triggers_procedures.sql', 'w', encoding='utf-8')
f.write(content)
f.close()
print('OK - lines:', len(content.split('\n')))
