import os
import glob
# These are all the files like game_*, error.txt, eventnames.txt, discord.txt, unitgames.txt, shop.txt, profile.txt etc.
# cards_misc.txt is valid for this, but not the translate-cards.py script.
# This is because misc has no flavor=, name= or descr= tags.
# You will know because they all follow < SOME_KEYWORD > then the line and use // for comments.
# Some will use [EOF], others will not.
# Artists and VA names (voiceactors.txt and cardartists.txt) are not translated.
# When using this script, you can add them below if you want to translate them. Otherwise, just leave them out and copy them over untouched.
# A fix must be applied to menuscreens.txt due to a block that contains extraneous newlines.
fileList = glob.glob('./LanguageFiles/game_*.txt')
fileList.append('./LanguageFiles/cards_misc.txt')
fileList.append('./LanguageFiles/error.txt')
fileList.append('./LanguageFiles/eventnames.txt')
fileList.append('./LanguageFiles/discord.txt')
fileList.append('./LanguageFiles/unitgames.txt')
fileList.append('./LanguageFiles/shop.txt')
fileList.append('./LanguageFiles/profile.txt')
fileList.append('./LanguageFiles/arcade_rules.txt')
fileList.append('./LanguageFiles/arcade.txt')
fileList.append('./LanguageFiles/campaign.txt')
fileList.append('./LanguageFiles/challenges.txt')
fileList.append('./LanguageFiles/characterselect.txt')
fileList.append('./LanguageFiles/comment.txt')
fileList.append('./LanguageFiles/config.txt')
fileList.append('./LanguageFiles/fieldnames.txt')
fileList.append('./LanguageFiles/launcher.txt')
fileList.append('./LanguageFiles/menuscreens.txt')
fileList.append('./LanguageFiles/multiplayer.txt')
fileList.append('./LanguageFiles/result.txt')

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
		# Some files from the game start with the \ufeff encoding character.
		# This is a workaround for that. I'm not sure why it's there in some but not others.
		if line.startswith("<") or line.startswith("\ufeff<") and line.endswith(">"):
			# Workaround for a bug where the <empty> placeholder text
			if line.equals("<empty>"):
				cleanedLines.append(line)
				continue
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