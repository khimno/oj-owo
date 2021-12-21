import glob
fileList = glob.glob('./LanguageFiles/charavoice_*.txt')

def translateLoop(lines):
	translatedLines = []
	for l in lines:
		a = l.replace('l', 'w')
		translatedLines.append(a.replace('r', 'w'))
		print('translated: \""' + l + '\" resulting in: \"' + a + '\"')

for fn in fileList:
    # open file
    file = open(fn, 'r', errors='ignore', encoding='utf-8')
    lines = file.readlines()
    file.close()

    # trim <XXXX> and newlines from lines
    trimmedlines = []
    for line in lines:
        trimmedlines.append(line.strip('\n')[7:])

    while("" in trimmedlines):
        trimmedlines.remove("")

    result = translateLoop(trimmedlines)
    translatedfile = open(fn[16:] + '.translated', "w+", errors='ignore', encoding='utf-8')
    count = 0;
    for tln in result:
        translatedfile.write("<" + "{:04d}".format(count) + "> " + tln + "\n")
        count += 1;
    translatedfile.close()
