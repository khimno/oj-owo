import glob
import os
# This script is used to translate the files that ONLY have name= and descr= tags.
# Do not use this on files with flavor= tags because it will not work.
# The applicable files have been enumerated here.
fileList = glob.glob('./LanguageFiles/bounty*.txt')
fileList.append('./LanguageFiles/abilities.txt')
# cards_effect.txt has flavor= tags in some cards but not others.
# As such, there is a workaround for it.
fileList.append('./LanguageFiles/cards_effect.txt')
fileList.append('./LanguageFiles/cards_effect_coop.txt')
fileList.append('./LanguageFiles/consumables.txt')
fileList.append('./LanguageFiles/fieldevents.txt')
fileList.append('./LanguageFiles/mixers.txt')
fileList.append('./LanguageFiles/pets.txt')
fileList.append('./LanguageFiles/units.txt')

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
			continue
		if line.startswith("descr="):
			cleanedLines.append(line[6:])
			continue
		# Workaround for cards_effect.txt
		# Seriously, if anyone from fbf is reading this, please be consistent in that file.
		# Does the game even use the flavor text in that file?
		# Why am I asking questions like this?
		# Why am I expecting the void to respond?
		# The FitnessGram™ Pacer Test is a multistage aerobic capacity test that progressively gets more difficult as it continues.
		if line.startswith("flavor="):
			continue

	trimmedlines = []
	for l in cleanedLines:
		trimmedlines.append(l)

	print("translating: " + fn)
	print(trimmedlines)
	print(sysids)
	result = translateLoop(trimmedlines)

	translatedfile = open('./translated/' + fn[16:] + '.translated', "w+", errors='ignore', encoding='utf-8')
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
			lineIndex = 0;
			continue

	if usesEOF:
		translatedfile.write("[EOF]")
	translatedfile.close()
	os.remove(fn)