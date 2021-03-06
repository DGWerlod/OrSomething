import media
gameW, gameH, gameIW = 900, 600, 700

# TITLE SCREEN AND INSTRUCTIONS

title, titleRECT = media.centeredText("In Construction", 60, media.blueOG, gameW)
titleRECT.top = gameH/2 - titleRECT.height/2 -40

footer, footerRECT = media.centeredText("Click anywhere to continue", 30, media.blueOG,gameW)
footerRECT.top = gameH/2 - footerRECT.height/2 +200

instructionsHeader, instructionsHeaderRECT = media.centeredText("Instructions", 60, media.blueOG, gameW)
instructionsHeaderRECT.top = instructionsHeaderRECT.height/2 +10

instructionsText = ["1. Drag and drop objects to build your environment","2. Hit GO or Right Click to start moving",
		"3. Use WASD to move and Space to jump", "4. Reach the goal zone to improve your sad life"]
instructions = [[],[],[],[]]

i = 0
for heightChange in range(50,-150,-50):
	now, nowRECT = media.centeredText(instructionsText[i], 30, media.blueOG, gameW)
	instructions[i].append(now)
	instructions[i].append(nowRECT)
	instructions[i][1].top = gameH/2 - instructions[i][1].height/2 - heightChange
	i += 1

# LEVEL SELECTION

global levelText, returnToInstructions, returnToInstructionsRECT
levelText = []
returnToInstructions, returnToInstructionsRECT = media.centeredText("", 0,  (0,0,0), 0)

def buildLevelSelectText(levelRects, returnRect):
	global levelText, returnToInstructions, returnToInstructionsRECT
	levelNum = 1
	for l in levelRects:
		now, nowRECT = media.centeredText("Level " + str(levelNum), int(l.w/5),  media.blueOG, l.w) # size orig. 250 -> 50
		nowRECT.left += l.x
		nowRECT.top = l.y + l.h/2 - nowRECT.h/2 - 3 #-3 aesthetic
		levelText.append([now,nowRECT])
		levelNum += 1
	returnToInstructions, returnToInstructionsRECT = media.centeredText("Return to Instructions", 25,  media.blueOG, returnRect.w)
	returnToInstructionsRECT.left += returnRect.x
	returnToInstructionsRECT.top = returnRect.y + returnRect.h/2 - returnToInstructionsRECT.h/2 - 3 #-3 aesthetic



# LEVEL PROPER

returnToLevels, returnToLevelsRECT = media.centeredText("Select Level", 20, media.lightGrey, 150)
returnToLevelsRECT.left += 725
returnToLevelsRECT.top = 25 + 40 - returnToLevelsRECT.h/2

goButton, goButtonRECT = media.centeredText("GO", 50, media.lightGrey, 150)
goButtonRECT.left += 730-5 
goButtonRECT.top = 475 + 35 - goButtonRECT.h/2

stopButton, stopButtonRECT = media.centeredText("STOP", 50, media.lightGrey, 150)
stopButtonRECT.left += 730-5 
stopButtonRECT.top = 475 + 35 - stopButtonRECT.h/2

counters = [[],[],[]]

i = 0
for heightChange in range(200,425,75):
	now, nowRECT = media.centeredText("x" + str(0), 30, media.mediumBlue, 50)
	counters[i].append(now)
	counters[i].append(nowRECT)
	counters[i][1].right += 825 + 5
	counters[i][1].top = heightChange + 35-2 - counters[i][1].h/2
	i += 1

def refreshCounter(selectionID, newValue):
	new, newRECT = media.centeredText("x" + str(newValue), 30, media.mediumBlue, 50)
	counters[selectionID][0] = new
	counters[selectionID][1] = newRECT
	counters[selectionID][1].right += 825 + 5
	counters[selectionID][1].top = 200+(selectionID*75) + 35-2 - counters[selectionID][1].h/2