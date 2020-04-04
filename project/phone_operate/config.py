# OCR did not recognize any result return parameters
OCR_NO_WORDS = []

# Android key events
KEY={
    'BACK_KEYEVENT' : '4',
    'HOME_KEYEVENT' : '3',
}

# WeChat location information
BTN={
    # 4 buttons at the bottom of WeChat main interface
    'WEIXIN_BTN' : (120,1800,200,1900),
    'TONGXUNLU_BTN' : (380,1800,460,1900),
    'FAXIAN_BTN' : (620,1800,700,1900),
    'WO_BTN' : (920,1800,1000,1900),
    # Public account folder list
    'GZH_FOLDER':(0,640,900,750),
    # Search for the first result of the public number
    'FIRST_GZH_SEARCH_RESULT':(34,225,900,330),
    # 2 buttons in the upper right corner of all public account list
    'SEARCH_BTN' : (800,120,860,200),
    'ADD_BTN' : (950,100,1020,200),
    # Public account details button
    'PROFILE_BTN' : (950,100,1020,200),
    # More buttons
    'MORE_BTN' : (950,100,1020,200),
    'CLAIRE_WEIXIN' : (130,1350,200,1400),
    #Uniform location for each simulator
    'EMU_WEIXIN_ICON':(920,670,1000,750),
    # Search for the first result of the public number based on pinyin
    'FIRST_RESULT':(200,220,800,350),
    # Certificate prompt continue button position
    'CAR_NOTE_CONTINUE':(780,1200,900,1250),
    # Public account all message button
    'ALL_HISTORY_MSG':(34,1720,1024,1800),
    # Allow location confirmation button
    'ASK_FOR_LOCATION':(780,1150,860,1180),
    # Wrote a message button
    'LEAVE_MSG':(480,1770,580,1790),
    # Due to the different number of title lines, the confirmation message location is also different. Simply click three times.
    'CONFIRM_MSG1':(120,760,940,850),
    'CONFIRM_MSG2':(120,830,940,920),
    'CONFIRM_MSG3':(120,900,940,990),
}

CROP_RANGE = {
    'MESSAGE_LIST':(0,220,700,1920),
    'PROFILE_MESSAGE_LIST':(0,820,700,1680),
    'CAR_NOTE':(130,700,950,1270),
    'LEAVE_MSG_BOTTOM':(0,1650,1080,1920),
}

UI_WORDS = {
    'CAR_NOTE':'There is a problem with the siteof security certificate',
    'NO_LEAVING_MSG':'Write a message',
}

PHONE = {
    'PXX':{'phone':'127.0.0.1:62025','phone_model':'SM-G955A'},
    'DRMJ':{'phone':'127.0.0.1:62001','phone_model':'SM-N950W'},
    'Claire':{'phone':'127.0.0.1:62027','phone_model':'SM-G930K'},
    'Frank':{'phone':'127.0.0.1:62026','phone_model':'SM-N9007'},
    'XZP':{'phone':'127.0.0.1:62028','phone_model':'SM-N9089'},
}

