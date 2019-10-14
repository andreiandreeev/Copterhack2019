rollInt = 180

if   rollInt < -99:
        rollStr =         str(rollInt)
elif rollInt < -9:
        rollStr = '0'   + str(rollInt)
elif rollInt < 0:
        rollStr = '00 ' + str(rollInt) 
elif rollInt < 10:
        rollStr = '+00' + str(rollInt)
elif rollInt < 100:
        rollStr = '+0'  + str(rollInt)
else:
        rollStr = '+'   + str(rollInt)

print(rollStr)
