
void __thiscall FUN__text__00472a70(int param_1,undefined2 param_2)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_50 [16];
  short local_10;
  short local_c;
  int local_8;
  
  puVar2 = local_50;
  for (iVar1 = 0x13; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  if ((*(short *)(param_1 + 0x10f9c0) != -1) && (*(short *)(param_1 + 0x10f9c2) != -1)) {
    local_c = *(short *)(param_1 + 0x10f9c0) - *(short *)(param_1 + 0x2a30e);
    iVar1 = ((int)*(short *)(param_1 + 0x10f9c2) - (int)*(short *)(param_1 + 0x2a310)) + 0x1e;
    local_10 = (short)iVar1;
    local_8 = param_1;
    FUN__text__0040a330(param_1 + 0x109dc8,param_1 + 0xde4b0,(int)local_c,(int)local_10,
                        CONCAT22((short)((uint)iVar1 >> 0x10),param_2));
  }
  local_8 = 0x472b21;
  FUN__text__0056ce80();
  return;
}

