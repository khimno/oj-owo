import glob
# You will have to just replace these with the correct file names.
# I would enumerate the files valid for this folder but I am lazy.
# They are all the files like game_*, error.txt, eventnames.txt, discord.txt, unitgames.txt, shop.txt, profile.txt etc.
# cards_misc.txt is valid for this, but not the translate-cards.py script.
# This is because misc has no flavor=, name= or descr= tags.
# You will know because they all follow < SOME_KEYWORD > then the line and use // for comments.
# Some will use [EOF], others will not.
fileList = glob.glob('./LanguageFiles/game_*.txt')

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
	cleanedLines = []
	usesEOF = False
	for line in trimmedlines:
		if line.startswith("//"):
			continue
		if line.startswith("<") and line.endswith(">"):
			sysids.append(line)
			continue
		if line.startswith("[EOF]"):
			usesEOF = True
			continue
		cleanedLines.append(line)
	while("" in cleanedLines):
		cleanedLines.remove("")
	trimmedlines = []
	for l in cleanedLines:
		trimmedlines.append(l)

	print("translating: " + fn)
	result = translateLoop(trimmedlines)

	translatedfile = open('./translated/' + fn[16:] + '.translated', "w+", errors='ignore', encoding='utf-8')
	count = 0;

	for tln in result:
		if sysids:
			translatedfile.write(sysids.pop(0))
			translatedfile.write("\n")
		translatedfile.write(tln)
		translatedfile.write("\n")
		count += 1;

	if usesEOF:
		translatedfile.write("[EOF]")
	translatedfile.close()
	os.remove(fn)