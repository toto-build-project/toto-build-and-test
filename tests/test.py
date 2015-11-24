import fileinput
i = 0
for line in fileinput.input():
	if line.strip() == "":
		break
	i += int(line.strip())

print i
