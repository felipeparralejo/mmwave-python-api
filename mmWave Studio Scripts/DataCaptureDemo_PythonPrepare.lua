--Based on the original DataCaptureDemo_xWR.lua
--Place this in C:\ti\mmwave_studio_XX_XX_XX_XX\mmWaveStudio\Scripts

-- CONNECTION
COM_PORT = 4

-------- RADAR PARAMETERS --------

-- General
TX0_EN = 1
TX1_EN = 1
TX2_EN = 1

NUM_TX = TX0_EN + TX1_EN + TX2_EN
NUM_RX = 4

-- ProfileConfig
START_FREQ = 60 -- GHz
IDLE_TIME = 7 -- us
RAMP_END_TIME = 24 -- us
ADC_START_TIME = 3 --us
FREQ_SLOPE = 166 -- MHz/us
ADC_SAMPLES = 256
SAMPLE_RATE = 12500 -- ksps
RX_GAIN = 30 -- dB

-- ChirpConfig
-- The setup is such that we receive Rx information in the order of TX0->TX2->TX1
-- This translates to getting all the azimuth information first (indices [0,7]) then getting any elevation information (indices [8,11])
-- TO CHANGE TX ANTENNA ORDER, ACTIVATE OR DEACTIVATE ANTENNA IN CHIRPCONFIG

-- FrameConfig
START_CHIRP_TX = 0
END_CHIRP_TX = NUM_TX - 1
NUM_FRAMES = 0 -- Set this to 0 to continuously stream data
CHIRP_LOOPS = 128 -- Number of chirps per frame
PERIODICITY = 70 -- ms

-----------------------------------------------------------

ar1.FullReset()
ar1.SOPControl(2)
ar1.Connect(COM_PORT,921600,1000)

--BSS and MSS firmware download
info = debug.getinfo(1,'S');
file_path = (info.source);
file_path = string.gsub(file_path, "@","");
file_path = string.gsub(file_path, "DataCaptureDemo_PythonPrepare.lua","");
fw_path   = file_path.."..\\..\\rf_eval_firmware"

--Export bit operation file
bitopfile = file_path.."\\".."bitoperations.lua"
dofile(bitopfile)

--Read part ID
--This register address used to find part number for ES2 and ES3 devices
res, efusedevice = ar1.ReadRegister(0xFFFFE214, 0, 31)
res, efuseES1device = ar1.ReadRegister(0xFFFFE210, 0, 31)
efuseES2ES3Device = bit_and(efusedevice, 0x03FC0000)
efuseES2ES3Device = bit_rshift(efuseES2ES3Device, 18)

--if part number is zero then those are ES1 devices 
if(efuseES2ES3Device == 0) then
	if (bit_and(efuseES1device, 3) == 0) then
		partId = 1243
	elseif (bit_and(efuseES1device, 3) == 1) then
		partId = 1443
	else
		partId = 1642
	end
elseif(efuseES2ES3Device == 0xE0 and (bit_and(efuseES1device, 3) == 2)) then
		partId = 6843
		ar1.frequencyBandSelection("60G")
--if part number is non-zero then those are ES12 and ES3 devices
else
   if(efuseES2ES3Device == 0x20 or efuseES2ES3Device == 0x21 or efuseES2ES3Device == 0x80) then
		partId = 1243
	elseif(efuseES2ES3Device == 0xA0 or efuseES2ES3Device == 0x40)then
		partId = 1443
	elseif(efuseES2ES3Device == 0x60 or efuseES2ES3Device == 0x61 or efuseES2ES3Device == 0x04 or efuseES2ES3Device == 0x62 or efuseES2ES3Device == 0x67) then
		partId = 1642
	elseif(efuseES2ES3Device == 0x66 or efuseES2ES3Device == 0x01 or efuseES2ES3Device == 0xC0 or efuseES2ES3Device == 0xC1) then
		partId = 1642
	elseif(efuseES2ES3Device == 0x70 or efuseES2ES3Device == 0x71 or efuseES2ES3Device == 0xD0 or efuseES2ES3Device == 0x05) then
		partId = 1843
	elseif(efuseES2ES3Device == 0xE0 or efuseES2ES3Device == 0xE1 or efuseES2ES3Device == 0xE2 or efuseES2ES3Device == 0xE3 or efuseES2ES3Device == 0xE4) then
		partId = 6843
		ar1.frequencyBandSelection("60G")
	else
		WriteToLog("Inavlid Device part number in ES2 and ES3 devices\n" ..partId)
    end
end 

--ES version
res, ESVersion = ar1.ReadRegister(0xFFFFE218, 0, 31)
ESVersion = bit_and(ESVersion, 15)

--ADC_Data file path
data_path     = file_path.."..\\PostProc"
adc_data_path = data_path.."\\adc_data.bin"

-- Download Firmware
if(partId == 1642) then
    BSS_FW    = fw_path.."\\radarss\\xwr16xx_radarss.bin"
    MSS_FW    = fw_path.."\\masterss\\xwr16xx_masterss.bin"
elseif(partId == 1243) then
    BSS_FW    = fw_path.."\\radarss\\xwr12xx_xwr14xx_radarss.bin"
    MSS_FW    = fw_path.."\\masterss\\xwr12xx_xwr14xx_masterss.bin"
elseif(partId == 1443) then
    BSS_FW    = fw_path.."\\radarss\\xwr12xx_xwr14xx_radarss.bin"
    MSS_FW    = fw_path.."\\masterss\\xwr12xx_xwr14xx_masterss.bin"
elseif(partId == 1843) then
    BSS_FW    = fw_path.."\\radarss\\xwr18xx_radarss.bin"
    MSS_FW    = fw_path.."\\masterss\\xwr18xx_masterss.bin"
elseif(partId == 6843) then
    BSS_FW    = fw_path.."\\radarss\\xwr68xx_radarss.bin"
    MSS_FW    = fw_path.."\\masterss\\xwr68xx_masterss.bin"
else
    WriteToLog("Invalid Device partId FW\n" ..partId)
    WriteToLog("Invalid Device ESVersion\n" ..ESVersion)
end

-- Download BSS Firmware
if (ar1.DownloadBSSFw(BSS_FW) == 0) then
    WriteToLog("BSS FW Download Success\n", "green")
else
    WriteToLog("BSS FW Download failure\n", "red")
end

-- Download MSS Firmware
if (ar1.DownloadMSSFw(MSS_FW) == 0) then
    WriteToLog("MSS FW Download Success\n", "green")
else
    WriteToLog("MSS FW Download failure\n", "red")
end

-- SPI Connect
if (ar1.PowerOn(1, 1000, 0, 0) == 0) then
    WriteToLog("Power On Success\n", "green")
else
   WriteToLog("Power On failure\n", "red")
end

-- RF Power UP
if (ar1.RfEnable() == 0) then
    WriteToLog("RF Enable Success\n", "green")
else
    WriteToLog("RF Enable failure\n", "red")
end

-- (TX0, TX1, TX2, RX0, RX1, RX2, RX3, Bits=16, Format=Complex1x, IQSwap=I first)
if (ar1.ChanNAdcConfig(TX0_EN, TX1_EN, TX2_EN, 1, 1, 1, 1, 2, 1, 0) == 0) then
    WriteToLog("ChanNAdcConfig Success\n", "green")
else
    WriteToLog("ChanNAdcConfig failure\n", "red")
end

if (partId == 1642) then
    if (ar1.LPModConfig(0, 1) == 0) then
        WriteToLog("LPModConfig Success\n", "green")
    else
        WriteToLog("LPModConfig failure\n", "red")
    end
else
    if (ar1.LPModConfig(0, 0) == 0) then
        WriteToLog("Regualar mode Cfg Success\n", "green")
    else
        WriteToLog("Regualar mode Cfg failure\n", "red")
    end
end

--For XWR1843 LDO Bypass is required to support the third transmitter
if ((partId == 1843) and (TX2_EN == 1)) then
    if(ar1.RfLdoBypassConfig(0x3) == 0) then
        WriteToLog("RfLdoBypassConfig Success\n", "green")
    else
        WriteToLog("RfLdoBypassConfig failure\n", "red")
    end
end

if (ar1.RfInit() == 0) then
    WriteToLog("RfInit Success\n", "green")
else
    WriteToLog("RfInit failure\n", "red")
end

RSTD.Sleep(1000)

if (ar1.DataPathConfig(1, 1, 0) == 0) then
    WriteToLog("DataPathConfig Success\n", "green")
else
    WriteToLog("DataPathConfig failure\n", "red")
end

if (ar1.LvdsClkConfig(1, 1) == 0) then
    WriteToLog("LvdsClkConfig Success\n", "green")
else
    WriteToLog("LvdsClkConfig failure\n", "red")
end

if((partId == 1642) or (partId == 1843) or (partId == 6843)) then
    if (ar1.LVDSLaneConfig(0, 1, 1, 0, 0, 1, 0, 0) == 0) then
        WriteToLog("LVDSLaneConfig Success\n", "green")
    else
        WriteToLog("LVDSLaneConfig failure\n", "red")
    end
elseif ((partId == 1243) or (partId == 1443)) then
    if (ar1.LVDSLaneConfig(0, 1, 1, 1, 1, 1, 0, 0) == 0) then
        WriteToLog("LVDSLaneConfig Success\n", "green")
    else
        WriteToLog("LVDSLaneConfig failure\n", "red")
    end
end

if((partId == 1642) or (partId == 1843) or (partId == 1243) or (partId == 1443)) then
    if(ar1.ProfileConfig(0, START_FREQ, IDLE_TIME, ADC_START_TIME, RAMP_END_TIME, 0, 0, 0, 0, 0, 0, FREQ_SLOPE, 0, ADC_SAMPLES, SAMPLE_RATE, 0, 0, RX_GAIN) == 0) then
        WriteToLog("ProfileConfig Success\n", "green")
    else
        WriteToLog("ProfileConfig failure\n", "red")
    end
elseif(partId == 6843) then
    if(ar1.ProfileConfig(0, START_FREQ, IDLE_TIME, ADC_START_TIME, RAMP_END_TIME, 0, 0, 0, 0, 0, 0, FREQ_SLOPE, 0, ADC_SAMPLES, SAMPLE_RATE, 0, 131072, RX_GAIN) == 0) then
		WriteToLog("ProfileConfig Success\n", "green")
    else
        WriteToLog("ProfileConfig failure\n", "red")
    end
end

if (NUM_TX >= 1) then
    -- (CHIRP_START_IDX, CHIRP_END_IDX, PROFILE_ID, START_FREQ_VAR, FREQ_SLOP_VAR, IDLE_TIME_VAR, ADC_START_VAR, TX0_ENABLE, TX1_ENABLE, TX2_ENABLE)
    -- TO CHANGE TX ANTENNA ORDER, ACTIVATE OR DEACTIVATE ANTENNA IN CHIRPCONFIG BELOW
    if (ar1.ChirpConfig(0, 0, 0, 0, 0, 0, 0, 1, 0, 0) == 0) then
        WriteToLog("ChirpConfig 0 Success\n", "green")
    else
        WriteToLog("ChirpConfig 0 failure\n", "red")
    end
end

if (NUM_TX >= 2) then
    if (ar1.ChirpConfig(1, 1, 0, 0, 0, 0, 0, 0, 0, 1) == 0) then
        WriteToLog("ChirpConfig 1 Success\n", "green")
    else
        WriteToLog("ChirpConfig 1 failure\n", "red")
    end
end

if (NUM_TX >= 3) then
    if (ar1.ChirpConfig(2, 2, 0, 0, 0, 0, 0, 0, 1, 0) == 0) then
        WriteToLog("ChirpConfig 2 Success\n", "green")
    else
        WriteToLog("ChirpConfig 2 failure\n", "red")
    end
end

if (ar1.FrameConfig(START_CHIRP_TX, END_CHIRP_TX, NUM_FRAMES, CHIRP_LOOPS, PERIODICITY, 0, 0, 1) == 0) then
    WriteToLog("FrameConfig Success\n", "green")
else
    WriteToLog("FrameConfig failure\n", "red")
end

-- select Device type
if (ar1.SelectCaptureDevice("DCA1000") == 0) then
    WriteToLog("SelectCaptureDevice Success\n", "green")
else
    WriteToLog("SelectCaptureDevice failure\n", "red")
end

--DATA CAPTURE CARD API
if (ar1.CaptureCardConfig_EthInit("192.168.33.30", "192.168.33.180", "12:34:56:78:90:12", 4096, 4098) == 0) then
    WriteToLog("CaptureCardConfig_EthInit Success\n", "green")
else
    WriteToLog("CaptureCardConfig_EthInit failure\n", "red")
end

--AWR12xx or xWR14xx-1, xWR16xx or xWR18xx or xWR68xx- 2 (second parameter indicates the device type)
if ((partId == 1642) or (partId == 1843) or (partId == 6843)) then
    if (ar1.CaptureCardConfig_Mode(1, 2, 1, 2, 3, 30) == 0) then
        WriteToLog("CaptureCardConfig_Mode Success\n", "green")
    else
        WriteToLog("CaptureCardConfig_Mode failure\n", "red")
    end
elseif ((partId == 1243) or (partId == 1443)) then
    if (ar1.CaptureCardConfig_Mode(1, 1, 1, 2, 3, 30) == 0) then
        WriteToLog("CaptureCardConfig_Mode Success\n", "green")
    else
        WriteToLog("CaptureCardConfig_Mode failure\n", "red")
    end
end

if (ar1.CaptureCardConfig_PacketDelay(25) == 0) then
    WriteToLog("CaptureCardConfig_PacketDelay Success\n", "green")
else
    WriteToLog("CaptureCardConfig_PacketDelay failure\n", "red")
end

-------- CALCULATED PARAMETERS --------
-- MinPeriodicity (minimum time per frame to receive all chirps)
MIN_PERIODICITY = (IDLE_TIME + RAMP_END_TIME)*CHIRP_LOOPS*NUM_TX/1000 -- ms
CHIRPS_PER_FRAME = (END_CHIRP_TX - START_CHIRP_TX + 1) * CHIRP_LOOPS
NUM_DOPPLER_BINS = CHIRPS_PER_FRAME / NUM_TX
NUM_RANGE_BINS = ADC_SAMPLES
RANGE_RESOLUTION = (3e8 * SAMPLE_RATE * 1e3) / (2 * FREQ_SLOPE * 1e12 * ADC_SAMPLES)
MAX_RANGE = (300 * 0.9 * SAMPLE_RATE) / (2 * FREQ_SLOPE * 1e3)
DOPPLER_RESOLUTION = 3e8 / (2 * START_FREQ * 1e9 * (IDLE_TIME + RAMP_END_TIME) * 1e-6 * NUM_DOPPLER_BINS * NUM_TX)
MAX_DOPPLER = 3e8 / (4 * START_FREQ * 1e9 * (IDLE_TIME + RAMP_END_TIME) * 1e-6 * NUM_TX)


print("Minimum Frame Periodicity:", MIN_PERIODICITY)
print("Chirps Per Frame:", CHIRPS_PER_FRAME)
print("Num Doppler Bins:", NUM_DOPPLER_BINS)
print("Num Range Bins:", NUM_RANGE_BINS)
print("Range Resolution:", RANGE_RESOLUTION)
print("Max Unambiguous Range:", MAX_RANGE)
print("Doppler Resolution:", DOPPLER_RESOLUTION)
print("Max Doppler:", MAX_DOPPLER)

---------------------------------------------------------------

--Start Record ADC data
ar1.CaptureCardConfig_StartRecord(adc_data_path, 1)
RSTD.Sleep(1000)

--Trigger frame
ar1.StartFrame()
RSTD.Sleep(1000)
WriteToLog("You can now start your Python script to acquire data .....!!!! \n", "green")

--Post process the Capture RAW ADC data
--ar1.StartMatlabPostProc(adc_data_path)
--WriteToLog("Please wait for a few seconds for matlab post processing .....!!!! \n", "green")
--RSTD.Sleep(10000)
