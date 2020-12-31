"""Generate test for github issue."""
import sys
import requests

URL = "https://api.github.com/repos/ludeeus/awesomeversion/issues/{number}"

ISSUE_CONTENT = """\"\"\"Test for issue #{number}.\"\"\"
# https://github.com/ludeeus/awesomeversion/issues/{number}
{imports}

def test():
    \"\"\"Test for issue #{number}.\"\"\"
    {content}
"""
issue_number = sys.argv[1]
imports = []
content = []
request = requests.get(URL.format(number=issue_number))
body = request.json()["body"].split("```python")[1].split("```")[0]

for line in body.split("\r\n"):
    if "from " and " import " in line:
        imports.append(line)
    elif not line:
        continue
    else:
        content.append(line)

with open(f"./tests/issues/test_issue{issue_number}.py", "w") as target:
    target.write(
        ISSUE_CONTENT.format(
            number=issue_number,
            imports="\n".join(imports),
            content="\n    ".join(content),
        )
    )
