import glob
fileList = glob.glob('./LanguageFiles/campaign_*.txt')

def translateLoop(lines):
	translatedLines = []
	for l in lines:
		a = l.replace('l', 'w')
		a = a.replace('r', 'w')
		a = a.replace('R', 'W')
		a = a.replace('L', 'W')
		translatedLines.append(a)
		print('translated: \"' + l + '\" resulting in: \"' + a + '\"')
	return translatedLines
for fn in fileList:
	# open file
	file = open(fn, 'r', errors='ignore', encoding='utf-8')
	lines = file.readlines()
	file.close()

	# trim <XXXX> and newlines from lines
	trimmedlines = []
	for line in lines:
		trimmedlines.append(line.strip('\n'))
	cleanedLines = []
	for line in trimmedlines:
		if line.startswith("//"):
			continue
		cleanedLines.append(line)
	while("" in cleanedLines):
		cleanedLines.remove("")
	trimmedlines = []
	for l in cleanedLines:
		trimmedlines.append(l[7:])
	print("translating: " + fn)
	result = translateLoop(trimmedlines)
	translatedfile = open('./translated/' + fn[16:] + '.translated', "w+", errors='ignore', encoding='utf-8')
	count = 0;
	for tln in result:
		translatedfile.write("<" + "{:04d}".format(count) + "> " + tln + "\n")
		count += 1;
	translatedfile.close()
	os.remove(fn)