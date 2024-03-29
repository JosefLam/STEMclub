import board
import busio
import time
import terminalio
import displayio
import digitalio
import re
from adafruit_display_text import label
from adafruit_st7789 import ST7789
import usb_midi
import adafruit_midi
from adafruit_midi.note_on import NoteOn
from adafruit_midi.note_off import NoteOff

i2c = busio.I2C(board.GP21, board.GP20)

# First set some parameters used for shapes and text
BORDER = 10
FONTSCALE = 2
BACKGROUND_COLOR = 0x00FF00  # Bright Green
FOREGROUND_COLOR = 0xAA0088  # Purple
TEXT_COLOR = 0xFFFF00

OPENHIHAT = 46
CLOSEDHIHAT = 42
PEDALHIHAT = 44

SNARE = 38
ELECTRICSNARE = 40

KICK = 35
ELECTRICKICK = 36

HIGHTOM = 48
MIDTOM = 47
LOWTOM = 45

RIDE = 51
RIDECRASH = 59
RIDEBELL = 53

CRASH1 = 49
CRASH2 = 57



buttonA = digitalio.DigitalInOut(board.GP12)
buttonA.switch_to_input(pull=digitalio.Pull.UP)
buttonB = digitalio.DigitalInOut(board.GP13)
buttonB.switch_to_input(pull=digitalio.Pull.UP)
buttonX = digitalio.DigitalInOut(board.GP14)
buttonX.switch_to_input(pull=digitalio.Pull.UP)
buttonY = digitalio.DigitalInOut(board.GP15)
buttonY.switch_to_input(pull=digitalio.Pull.UP)

btnCd = 0.2

# Release any resources currently in use for the displays
displayio.release_displays()

tft_cs = board.GP17
tft_dc = board.GP16
spi_mosi = board.GP19
spi_clk = board.GP18
spi = busio.SPI(spi_clk, spi_mosi)

display_bus = displayio.FourWire(spi, command=tft_dc, chip_select=tft_cs)
display = ST7789(
    display_bus, rotation=180, width=240, height=240, rowstart=80
)

# Make the display context
splash = displayio.Group()
display.show(splash)

color_bitmap = displayio.Bitmap(display.width, display.height, 1)
color_palette = displayio.Palette(1)
color_palette[0] = BACKGROUND_COLOR

bg_sprite = displayio.TileGrid(color_bitmap, pixel_shader=color_palette, x=0, y=0)
splash.append(bg_sprite)

# Draw a smaller inner rectangle
inner_bitmap = displayio.Bitmap(
    display.width - BORDER * 2, display.height - BORDER * 2, 1
)
inner_palette = displayio.Palette(1)
inner_palette[0] = FOREGROUND_COLOR
inner_sprite = displayio.TileGrid(
    inner_bitmap, pixel_shader=inner_palette, x=BORDER, y=BORDER
)
splash.append(inner_sprite)

# Draw a label
text = "MIDI"
text_area = label.Label(terminalio.FONT, text=text, color=TEXT_COLOR)
text_width = text_area.bounding_box[2] * FONTSCALE
text_group = displayio.Group(
    scale=FONTSCALE,
    x=display.width // 2 - text_width // 2,
    y=(display.height // 2) - 15,
)
text_group.append(text_area)  # Subgroup for text scaling

text_area1 = label.Label(terminalio.FONT, text="", color=TEXT_COLOR)
text_width1 = text_area1.bounding_box[2] * FONTSCALE
text_group1 = displayio.Group(
    scale=FONTSCALE,
    x=display.width // 2 - text_width1 // 2,
    y=(display.height // 2) + 15,
)
text_group1.append(text_area1)  # Subgroup for text scaling

midi_msg_area = label.Label(terminalio.FONT, text="", color=TEXT_COLOR)
midi_msg_width = midi_msg_area.bounding_box[2] * FONTSCALE
midi_msg_group = displayio.Group(
    scale=FONTSCALE,
    x = 10,
    y = display.height - 40
)
midi_msg_group.append(midi_msg_area)

midi_details_area = label.Label(terminalio.FONT, text="", color=TEXT_COLOR)
midi_details_width = midi_msg_area.bounding_box[2] * FONTSCALE
midi_details_group = displayio.Group(
    scale=FONTSCALE,
    x = 10,
    y = display.height - 20
)
midi_details_group.append(midi_details_area)




splash.append(text_group)
splash.append(text_group1)
splash.append(midi_msg_group)
splash.append(midi_details_group)

uart = busio.UART(board.GP0, board.GP1, baudrate=31250, timeout=0.001)

midi_in_channel = 10
midi_out_channel = 10
midi = adafruit_midi.MIDI(
    midi_in=uart,
    midi_out=uart,
    in_channel=(midi_in_channel - 1),
    out_channel=(midi_out_channel - 1),
    debug=False,
)


hiHatCNotes = ""
hiHatONotes = ""
kickNotes = ""
snareNotes = ""
crashNotes = ""





text_area.text = "Custom Notes?"
text_area1.text = "X for yes, A for no"

notesComplete = False

while notesComplete == False:
    if not buttonX.value:
        time.sleep(btnCd)
        noteString = ""
        setNoteNum = 1
        while not (setNoteNum == 9):
            text_area.text = "HiHatClosed"
            text_area1.text = str(setNoteNum)+"/8"
            if not buttonA.value:
                noteString = (noteString)+"0"
                setNoteNum = setNoteNum + 1
                time.sleep(btnCd)
            elif not buttonX.value:
                noteString = (noteString)+"1"
                setNoteNum = setNoteNum + 1
                time.sleep(btnCd)
            
        hiHatCNotes = noteString
        
        noteString = ""
        setNoteNum = 1
        while not (setNoteNum == 9):
            text_area.text = "HiHatOpen"
            text_area1.text = str(setNoteNum)+"/8"
            if not buttonA.value:
                noteString = (noteString)+"0"
                setNoteNum = setNoteNum + 1
                time.sleep(btnCd)
            elif not buttonX.value:
                noteString = (noteString)+"1"
                setNoteNum = setNoteNum + 1
                time.sleep(btnCd)
                
        hiHatONotes = noteString
        
        noteString = ""
        setNoteNum = 1
        while not (setNoteNum == 9):
            text_area.text = "Kick"
            text_area1.text = str(setNoteNum)+"/8"
            if not buttonA.value:
                noteString = (noteString)+"0"
                setNoteNum = setNoteNum + 1
                time.sleep(btnCd)
            elif not buttonX.value:
                noteString = (noteString)+"1"
                setNoteNum = setNoteNum + 1
                time.sleep(btnCd)
                
        kickNotes = noteString
        
        noteString = ""
        setNoteNum = 1
        while not (setNoteNum == 9):
            text_area.text = "Snare"
            text_area1.text = str(setNoteNum)+"/8"
            if not buttonA.value:
                noteString = (noteString)+"0"
                setNoteNum = setNoteNum + 1
                time.sleep(btnCd)
            elif not buttonX.value:
                noteString = (noteString)+"1"
                setNoteNum = setNoteNum + 1
                time.sleep(btnCd)
                
        snareNotes = noteString
        
        noteString = ""
        setNoteNum = 1
        while not (setNoteNum == 9):
            text_area.text = "Crash"
            text_area1.text = str(setNoteNum)+"/8"
            if not buttonA.value:
                noteString = (noteString)+"0"
                setNoteNum = setNoteNum + 1
                time.sleep(btnCd)
            elif not buttonX.value:
                noteString = (noteString)+"1"
                setNoteNum = setNoteNum + 1
                time.sleep(btnCd)
                
        crashNotes = noteString
        
        notesComplete = True

    elif not buttonA.value:
        time.sleep(btnCd)
        notePage = open("notes.txt", "r")
        hiHatCNotes = notePage.readline().split("\t")[0]
        hiHatONotes = notePage.readline().split("\t")[0]
        kickNotes = notePage.readline().split("\t")[0]
        snareNotes = notePage.readline().split("\t")[0]
        crashNotes = notePage.readline().split("\t")[0]
        
        notePage.close()
        
        notesComplete = True













text_area.text = "BPM select"
tempo = 60

  
start = 0

play = False

while True:
    text_area1.text = str(tempo)+"BPM"
    while not buttonA.value:
        if tempo > 50:
            tempo = tempo - 5
            text_area1.text = str(tempo)+"BPM"
            time.sleep(btnCd)
    while not buttonX.value:
        if tempo < 360:
            tempo = tempo + 5
            text_area1.text = str(tempo)+"BPM"
            time.sleep(btnCd)
    if not buttonY.value:
        text_area1.text = "playing"
        play = True
        delay = (1/(tempo/60))/2
        time.sleep(btnCd)
        while (play == True):
            noteNum = 0
            
            while noteNum != 8:
            
                if int(hiHatCNotes[noteNum]) == 1:
                    midi.send(NoteOn(CLOSEDHIHAT, 120))
                
                if int(hiHatONotes[noteNum]) == 1:
                    midi.send(NoteOn(OPENHIHAT, 120))
                
                if int(kickNotes[noteNum]) == 1:
                    midi.send(NoteOn(ELECTRICKICK, 120))
                
                if int(snareNotes[noteNum]) == 1:
                    midi.send(NoteOn(SNARE, 120))
                
                if int(crashNotes[noteNum]) == 1:
                    midi.send(NoteOn(CRASH1, 120))
            
                noteNum = noteNum + 1
                if not buttonY.value:
                    play = False
                    text_area1.text = "stopping"
                    time.sleep(1)
                
                time.sleep(delay)

msg = midi.receive()
if msg != None:
    midi_msg_area.text=type(msg).__name__
    try:
        midi_details_area.text="Cha:{} Not:{} Vel:{}".format(msg.channel, msg.note, msg.velocity)
    except:
        midi_details_area.text = ""

    
    
    #time.sleep(0.1)
    #pass


