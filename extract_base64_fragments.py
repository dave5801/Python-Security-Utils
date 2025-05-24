import re

regex = r"INSERT INTO xQGgYA VALUES \('(.+)'\)"

final_str = ""

with open('output.txt') as f:
    content = f.read()
    matches = re.finditer(regex, content, re.MULTILINE)

    for matchNum, match in enumerate(matches, start=1):
        for groupNum in range(0, len(match.groups())):
            groupNum = groupNum + 1
            final_str = final_str + match.group(groupNum)

print(final_str)
