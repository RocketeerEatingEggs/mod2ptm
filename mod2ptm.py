# mod2ptm.py
# a (probably) useless tool that converts from ProTracker .mod to Poly Tracker .ptm
# the reason I say useless is because it's obvious it's a converter based on the files it spits out
# by RocketeerEatingEggs

import sys
import math

if (sys.argv[1]=="-h") or (sys.argv[1]=="--help") or (sys.argv[1]==None) or (sys.argv[2]==None):
    docs = """mod2ptm, by RocketeerEatingEggs on Github
Usage: mod2ptm file.mod file.ptm"""
    print(docs)

ModPeriodTable = [
    0, # required by the converter to add no note
    6848,6464,6096,5760,5424,5120,4832,4560,4304,4064,3840,3624, # octave 0
    3424,3232,3048,2880,2712,2560,2416,2280,2152,2032,1920,1812, # octave 1
    1712,1616,1524,1440,1356,1280,1208,1140,1076,1016, 960, 906, # octave 2
     856, 808, 762, 720, 678, 640, 604, 570, 538, 508, 480, 453, # octave 3, amiga
     428, 404, 381, 360, 339, 320, 302, 285, 269, 254, 240, 226, # octave 4, amiga
     214, 202, 190, 180, 170, 160, 151, 143, 135, 127, 120, 113, # octave 5, amiga
     107, 101,  95,  90,  85,  80,  75,  71,  67,  63,  60,  56, # octave 6
      53,  50,  47,  45,  42,  40,  37,  35,  33,  31,  30,  28, # octave 7
      26,  25,  23,  22,  21,  20,  18,  17,  16,  15,  15,  14, # octave 8
    ]

ModFinetunesTable = [
    8272, 8332, 8393, 8453, 8514, 8576, 8638, 8701, 7808, 7864, 7921, 7978, 8037, 8095, 8153, 8213
    ]

ModChannelsTable = [
    "1CHN","2CHN","3CHN","M.K.","5CHN","6CHN","7CHN","8CHN","9CHN","10CH","11CH","12CH","13CH","14CH","15CH","16CH",
    "17CH","18CH","19CH","20CH","21CH","22CH","23CH","24CH","25CH","26CH","27CH","28CH","29CH","30CH","31CH","32CH"
    ]

def compareMagic(magic):
    for i in range(32):
        if magic == ModChannelsTable[i]:
            return i + 1
    return 0

def periodToNote(lower, upper):
    newPeriod = (upper << 4) + lower
    for i in range(len(ModPeriodTable)):
        if ModPeriodTable[i] > newPeriod:
            return i
        if ModPeriodTable[i] == newPeriod:
            return i
    return 0 # oops, no note found!

with open(sys.argv[2], "wb") as PTMfile:
    with open(sys.argv[1], "rb") as MODfile:
        MODfile.seek(1080)
        numChannels = compareMagic(str(MODfile.read(4), encoding="utf-8"))
        if numChannels != 0:
            MODfile.seek(0)
            songName = str(MODfile.read(20), encoding="utf-8").ljust(28, "\x00")
            PTMfile.write(bytes(songName, encoding="utf-8"))
            PTMfile.write(b"\x1A\x07\x02\x00")
            MODfile.seek(950)
            numOrders = int.from_bytes(MODfile.read(1), byteorder="little")
            MODfile.read(1)
            numPatterns = 0
            for i in range(numOrders):
                patternNumber = int.from_bytes(MODfile.read(1), byteorder="little")
                if patternNumber > numPatterns:
                    numPatterns = patternNumber
            numPatterns = numPatterns + 1
            PTMfile.write(numOrders.to_bytes(2, byteorder="big"))
            PTMfile.write((31).to_bytes(2, byteorder="big"))
            PTMfile.write(numPatterns.to_bytes(2, byteorder="big"))
            PTMfile.write(numChannels.to_bytes(2, byteorder="big"))
            PTMfile.write(b"\x00\x00\x00\x00")
            PTMfile.write(b"PTMF")
            PTMfile.write(b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00")
            PTMfile.write(b"\x03\x0C\x03\x0C\x03\x0C\x03\x0C\x03\x0C\x03\x0C\x03\x0C\x03\x0C")
            MODfile.seek(952)
            PTMfile.write(MODfile.read(128))
            PTMfile.write(b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00")
            PTMfile.write(b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00")
            PTMfile.write(b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00")
            PTMfile.write(b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00")
            PTMfile.write(b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00")
            PTMfile.write(b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00")
            PTMfile.write(b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00")
            PTMfile.write(b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00")
            PTMfile.write(b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00")
            PTMfile.write(b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00")
            PTMfile.write(b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00")
            PTMfile.write(b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00")
            PTMfile.write(b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00")
            PTMfile.write(b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00")
            PTMfile.write(b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00")
            PTMfile.write(b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00")
            PatSegStart = PTMfile.tell()
            PTMfile.write(b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00")
            PTMfile.write(b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00")
            PTMfile.write(b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00")
            PTMfile.write(b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00")
            PTMfile.write(b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00")
            PTMfile.write(b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00")
            PTMfile.write(b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00")
            PTMfile.write(b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00")
            PTMfile.write(b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00")
            PTMfile.write(b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00")
            PTMfile.write(b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00")
            PTMfile.write(b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00")
            PTMfile.write(b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00")
            PTMfile.write(b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00")
            PTMfile.write(b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00")
            PTMfile.write(b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00")
            PTMfile.write(b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00")
            PTMfile.write(b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00")
            PTMfile.write(b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00")
            PTMfile.write(b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00")
            PTMfile.write(b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00")
            PTMfile.write(b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00")
            PTMfile.write(b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00")
            PTMfile.write(b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00")
            PTMfile.write(b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00")
            PTMfile.write(b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00")
            PTMfile.write(b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00")
            PTMfile.write(b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00")
            PTMfile.write(b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00")
            PTMfile.write(b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00")
            PTMfile.write(b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00")
            PTMfile.write(b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00")
            MODfile.seek(20)
            smpFileOffs = []
            smpLengths = []
            for i in range(31):
                smpName = str(MODfile.read(22), encoding="utf-8").ljust(28, "\x00")
                smpLength = int.from_bytes(MODfile.read(2), byteorder="little") * 2
                smpLengths.append(smpLength)
                smpLengthBytes = smpLength.to_bytes(4, byteorder="big")
                smpC4Spd = ModFinetunesTable[int.from_bytes(MODfile.read(1), byteorder="little")].to_bytes(2, byteorder="big")
                smpVolume = MODfile.read(1)
                smpRepStart = int.from_bytes(MODfile.read(2), byteorder="little") * 2
                smpRepLength = int.from_bytes(MODfile.read(2), byteorder="little") * 2
                smpRepStartBytes = smpRepStart.to_bytes(4, byteorder="big")
                smpRepEndBytes = (smpRepStart + smpRepLength).to_bytes(4, byteorder="big")
                if smpLength == 0:
                    PTMfile.write(b"\x00")
                else:
                    if smpRepLength > 1:
                        PTMfile.write(b"\x05")
                    else:
                        PTMfile.write(b"\x01")
                PTMfile.write(b"MOD2PTM.PTS\x00")
                PTMfile.write(smpVolume)
                PTMfile.write(smpC4Spd)
                PTMfile.write(b"\x00\x00")
                smpFileOffs.append(PTMfile.tell())
                PTMfile.write(b"\x00\x00\x00\x00")
                PTMfile.write(smpLengthBytes)
                PTMfile.write(smpRepStartBytes)
                PTMfile.write(smpRepEndBytes)
                PTMfile.write(b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00")
                PTMfile.write(bytes(smpName, encoding="utf-8"))
                PTMfile.write(b"PTMS")
            MODfile.seek(1084)
            patFileOffs = []
            for patternNumber in range(numPatterns):
                PTMfile.write(b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00")
                patFileOffs.append(math.floor(PTMfile.tell() / 16))
                currentLoc = PTMfile.tell()
                pnummult = patternNumber * 2
                PTMfile.seek(PatSegStart + pnummult)
                PTMfile.write(patFileOffs[patternNumber].to_bytes(2, byteorder="little"))
                PTMfile.seek(patFileOffs[patternNumber] * 16)
                for rowNumber in range(64):
                    for channelNumber in range(numChannels):
                        byteVal = 0
                        eventPart1 = int.from_bytes(MODfile.read(1), byteorder="little")
                        lowerPeriod = int.from_bytes(MODfile.read(1), byteorder="little")
                        eventPart3 = int.from_bytes(MODfile.read(1), byteorder="little")
                        effectParam = MODfile.read(1)
                        upperPeriod = eventPart1 & 15
                        note = periodToNote(lowerPeriod, upperPeriod)
                        instrument = ((eventPart1 & 240) | (eventPart3 & 240)) >> 4
                        effectNumber = eventPart3 & 15
                        noNote = True
                        if note != 0:
                            noNote = False
                        if instrument != 0:
                            noNote = False
                        noEffect = False
                        if effectNumber == 0:
                            noEffect = True # we don't do one for parameter because that would be incredibly stupid
                        byteVal = byteVal + channelNumber + 1
                        if noNote == False:
                            byteVal = byteVal + 32
                        if noEffect == False:
                            byteVal = byteVal + 64
                        if byteVal & 224 == 0:
                            PTMfile.write(b"\x00")
                        else:
                            PTMfile.write(byteVal.to_bytes(1, byteorder="big"))
                            if noNote == False:
                                PTMfile.write(note.to_bytes(1, byteorder="big"))
                                PTMfile.write(instrument.to_bytes(1, byteorder="big"))
                            if noEffect == False:
                                PTMfile.write(effectNumber.to_bytes(1, byteorder="big"))
                                PTMfile.write(effectParam)
            # sample time!!!
            PTMfile.seek(1024, 1)
            for i in range(31):
                # write file offsets
                newSampOffs = PTMfile.tell()
                PTMfile.seek(smpFileOffs[i])
                PTMfile.write(newSampOffs.to_bytes(4, byteorder="little"))
                PTMfile.seek(newSampOffs)
                PTMfile.write(MODfile.read(smpLengths[i]))
