def gmt2json(pathx,hasDescColumn=True,isFuzzy=False):
	wordsAll = []
	# secondColumn = []
	with open(pathx,'r') as gf:
		for line in gf:
			line = line.strip('\r\n\t')
#             if not a empty line
			if line:
				words = []
				i = 0
				for item in line.split('\t'):
					if i==0:
						words.append(item)
					else:
#               a gene symbol cannot be a string of numbers.
						if item!="" and not isNumStr(item):
							words.append(item)
				wordsAll.append(words)
				# secondColumn.append(words[1])
	gmtName = getfilename(pathx)
	print(gmtName)
	gmt = []
	if not isFuzzy and hasDescColumn:
		for words in wordsAll:
			gmt.append({'gmt':gmtName,'desc':words[1],
				'term':words[0],'items':words[2:]})
	return gmt


def getBaseDir():
	currentPath = os.getcwd()
	while currentPath != '/':
		if os.path.isdir(currentPath+'/.git'):
			break
		currentPath = getParDir(currentPath)
	if currentPath == '/':
		raise Exception('Base dir not found because .git directory is not present')
	return currentPath
