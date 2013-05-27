from Adafruit_I2C import Adafruit_I2C
from time import sleep

class TSL2561 :
   i2c = None
   
   
   TSL2561_ADDR_LOW = 0x29
   TSL2561_ADDR_FLOAT = 0x39
   TSL2561_ADDR_HIGH = 0x49

   TSL2561_REGISTER_CONTROL          = 0x00
   TSL2561_REGISTER_TIMING           = 0x01
   TSL2561_REGISTER_THRESHHOLDL_LOW  = 0x02
   TSL2561_REGISTER_THRESHHOLDL_HIGH = 0x03
   TSL2561_REGISTER_THRESHHOLDH_LOW  = 0x04
   TSL2561_REGISTER_THRESHHOLDH_HIGH = 0x05
   TSL2561_REGISTER_INTERRUPT        = 0x06
   TSL2561_REGISTER_CRC              = 0x08
   TSL2561_REGISTER_ID               = 0x0A
   TSL2561_REGISTER_CHAN0_LOW        = 0x0C
   TSL2561_REGISTER_CHAN0_HIGH       = 0x0D
   TSL2561_REGISTER_CHAN1_LOW        = 0x0E
   TSL2561_REGISTER_CHAN1_HIGH       = 0x0F

   TSL2561_INTEGRATIONTIME_13MS      = 0x00   # // 13.7ms
   TSL2561_INTEGRATIONTIME_101MS     = 0x01   # // 101ms
   TSL2561_INTEGRATIONTIME_402MS     = 0x02   # // 402ms
   
   TSL2561_GAIN_0X                   = 0x00  #  // No gain
   TSL2561_GAIN_16X                  = 0x10  #  // 16x gain
     
   TSL2561_COMMAND_BIT       = (0x80)
   TSL2561_CLEAR_BIT         = (0x40)    #// Clears any pending interrupt (write 1 to clear)
   TSL2561_WORD_BIT          = (0x20)    #// 1 = read/write word (rather than byte)
   TSL2561_BLOCK_BIT         = (0x10)    #// 1 = using block read/write
   
   TSL2561_CONTROL_POWERON   = (0x03)
   TSL2561_CONTROL_POWEROFF  = (0x00)
   

   TSL2561_LUX_LUXSCALE      = (14)      #// Scale by 2^14
   TSL2561_LUX_RATIOSCALE    = (9)       #// Scale ratio by 2^9
   TSL2561_LUX_CHSCALE       = (10)      #// Scale channel values by 2^10
   TSL2561_LUX_CHSCALE_TINT0 = (0x7517)  #// 322/11 * 2^TSL2561_LUX_CHSCALE
   TSL2561_LUX_CHSCALE_TINT1 = (0x0FE7)  #// 322/81 * 2^TSL2561_LUX_CHSCALE

   _initialized = False
   
   _integration = TSL2561_INTEGRATIONTIME_13MS
   _gain = TSL2561_GAIN_16X
   
   def __init__(self, debug = False, address=TSL2561_ADDR_FLOAT):
      self.i2c = Adafruit_I2C(address)
      self.address = address
      self.debug = debug
      
      self.setParams()
     
#return to footcandles
   def getOutput(self):
      lum = self.getFullLuminosity()
      ir = lum >> 16
      full = lum & 0xFFFF

      return self.calculateLux(full, ir) /  10.763910417 ;
   
   def calculateLux(self, ch0, ch1):
      chScale = (1 << self.TSL2561_LUX_CHSCALE)
      if (self._integration == self.TSL2561_INTEGRATIONTIME_13MS):
         chScale = self.TSL2561_LUX_CHSCALE_TINT0
      elif (self._integration == TSL2561_INTEGRATIONTIME_101MS):
         chScale = self.TSL2561_LUX_CHSCALE_TINT1
         
      if (not self._gain):
         chScale = chScale << 4;
         
      channel0 = (ch0 * chScale) >> self.TSL2561_LUX_CHSCALE
      channel1 = (ch1 * chScale) >> self.TSL2561_LUX_CHSCALE
      
      print "IR: %d" % channel0
      print "Full: %d" % channel1
         
      return ch0
      

   def getFullLuminosity(self):
     self.enable()

     if (self._integration == self.TSL2561_INTEGRATIONTIME_13MS):
        sleep(1e-3 * 14)
     elif (self._integration == self.TSL2561_INTEGRATIONTIME_101MS):
        sleep(1e-3 * 102)
     else:
        sleep(1e-3 * 400)
      
     x = self.i2c.readU16(self.TSL2561_COMMAND_BIT | self.TSL2561_WORD_BIT | 
           self.TSL2561_REGISTER_CHAN1_LOW)
     x = x << 16
     x = x | self.i2c.readU16(self.TSL2561_COMMAND_BIT | self.TSL2561_WORD_BIT | 
           self.TSL2561_REGISTER_CHAN0_LOW)
 
     self.disable()
     return x  

   def setParams(self, integration = TSL2561_INTEGRATIONTIME_13MS, 
                       gain = TSL2561_GAIN_16X):
      self.enable()
      
      self._integration = integration
      self._gain = gain
      self.i2c.write8(self.TSL2561_COMMAND_BIT | self.TSL2561_REGISTER_TIMING, 
            integration | gain) 

      self.disable()

   def enable(self):
      if (not self._initialized):
         self.begin()
         
      self.i2c.write8(self.TSL2561_COMMAND_BIT | self.TSL2561_REGISTER_CONTROL, 
            self.TSL2561_CONTROL_POWERON)
   def disable(self):
      if (not self._initialized):
         self.begin()
         
      self.i2c.write8(self.TSL2561_COMMAND_BIT | self.TSL2561_REGISTER_CONTROL, 
            self.TSL2561_CONTROL_POWEROFF)
      
   def begin(self):
      self.i2c.write8(self.address, self.TSL2561_REGISTER_ID);
      ret = self.i2c.readU8(self.address)
      if (not ret & 0x0A ):
         print "PROBLEM !!!! %d" % ret
         return False
      else:
         self._initialized = True
         return True

