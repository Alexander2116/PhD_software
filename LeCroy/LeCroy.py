from lecroydso import LeCroyDSO, LeCroyVISA

transport = LeCroyVISA('GPIB::0::INSTR')
dso = LeCroyDSO(transport)

print(dso.query('*IDN?'))
print(dso.get_instrument_model())
print(dso.get_trigger_mode())
print(dso.get_trigger_type())