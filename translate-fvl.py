import os
import glob
# This script translates the files with the flavor= tag.
# WARNING: This script will not work on cards_bounty.txt by default.
# cards_bounty.txt MUST be modified to have flavor= tags.
# The applicable fixes have been applied if you are using the source files in this repo.
fileList = glob.glob('./LanguageFiles/cards_*.txt')
fileList.append('./LanguageFiles/cards.txt')
# Remove this one file from the list.
# This file is a special case and has to be handled on its own.
fileList.remove('./LanguageFiles/cards_mushroom.txt')
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

	sysids = []
	# trim <XXXX> and newlines from lines
	trimmedlines = []
	for line in lines:
		nospace = line.strip()
		trimmedlines.append(nospace.strip('\n'))
	while("" in trimmedlines):
		trimmedlines.remove("")
	cleanedLines = []
	usesEOF = False
	for line in trimmedlines:
		if line.startswith("//"):
			continue
		# Some files from the game start with the \ufeff encoding character.
		# This is a workaround for that. I'm not sure why it's there in some but not others.
		if line.startswith("<") or line.startswith("\ufeff<") and line.endswith(">"):
			sysids.append(line)
			continue
		if line.startswith("[EOF]"):
			usesEOF = True
			continue
		if line.startswith("name="):
			cleanedLines.append(line[5:])
		if line.startswith("descr="):
			cleanedLines.append(line[6:])
		if line.startswith("flavor="):
			cleanedLines.append(line[7:])

	trimmedlines = []
	for l in cleanedLines:
		trimmedlines.append(l)

	print("translating: " + fn)
	print(trimmedlines)
	print(sysids)
	result = translateLoop(trimmedlines)

	translatedfile = open('./translated/' + fn[16:] + '.translated', "w+", errors='ignore', encoding='utf-8')
	count = 0;
	lineIndex = 0;
	for tln in result:
		if lineIndex == 0:
			if sysids:
				translatedfile.write(sysids.pop(0))
				translatedfile.write("\n")
			translatedfile.write("name=" + tln + "\n")
			lineIndex += 1;
			continue
		if lineIndex == 1:
			translatedfile.write("descr=" + tln + "\n")
			lineIndex += 1;
			continue
		if lineIndex == 2:
			translatedfile.write("flavor=" + tln + "\n\n")
			lineIndex = 0;
			continue
		count += 1;

	if usesEOF:
		translatedfile.write("[EOF]")
	translatedfile.close()
	os.remove(fn)