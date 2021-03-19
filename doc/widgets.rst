Widget Mappings
###############

This is a quick reference of mappings of EDM to Qt widget types.

=============== ========================== ============================== ======================== ======
Name in EDM UI   EDM Class                 EpicsQt                        caQtDM                   Notes
=============== ========================== ============================== ======================== ======
Arc             activeArcClass             QEShape                        caGraphics
Bar             activeBarClass             QEAnalogProgressBar            caLinearGauge
Button          activeButtonClass          QEPushButton                   caMessageButton          when buttonType == "push"
Button          activeButtonClass          QECheckBox                     caToggleButton           for toggle buttonType
Choice Button   activeChoiceButtonClass    QERadioGroup                   caChoice
Circle          activeCircleClass          QESimpleShape or QSimpleShape  caGraphics               QESimpleShape when alarm colors aren't used
Exit Button     activeExitButtonClass                                                              No mapping
Group           activeGroupClass           QWidget                        QWidget                  Size is adjusted to hold all children
Line            activeLineClass            QSimpleShape or QEShape        caPolyLine               Straight lines become QLine if no alarm colors
Menu Button     activeMenuButtonClass      QEComboBox                     [1]
Message Button  activeMessageButtonClass   QEPushButton                   [1]
Meter           activeMeterClass           QEAnalogProgressBar            [1]
Motif Slider    activeMotifSliderClass     QESlider or QEAnalogSlider     [1]                      QESlider if vertical, or if showLabel, showLimits, showSaveValue, and showValue are not set
Radio Box       activeRadioButtonClass     QERadioGroup                   [1]
Rectangle       activeRectangleClass       QESimpleShape or QSimpleShape  caGraphics               QESimpleShape if alarmPv is set
Slider          activeSliderClass          QEAnalogSlider                 [1]
Updown Button   activeUpdownButtonClass    QESpinBox                      [1]
(display)       activeWindowClass          QEPvFrame or QEFrame           QFrame                   This is the top-level widget
Static Text     activeXTextClass           QESubstitutedLabel or QLabel   caLabel                  QLabel if macros are not in value
Text Control    activeXTextDspClass        QELineEdit                     [1]
Text Monitor    activeXTextDspClass:noedit QELabel                        [1]
Byte            ByteClass                  QEBitStatus                    [1]
Related Display relatedDisplayClass        QEMenuButton or QEPushButton   caRelatedDisplay         QEPushButton if numDsps property is 1
Shell Command   shellCmdClass              QEMenuButton or QEPushButton   caRelatedDisplay         QEPushButton if numDsps property is 1
Text Update     TextupdateClass            QELabel                        [1]
X-Y Graph       xyGraphClass               QEPlot                         [1]
=============== ========================== ============================== ======================== ======

[1] No caQtDM implementation provided as of this writing.

