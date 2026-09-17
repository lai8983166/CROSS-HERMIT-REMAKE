
undefined4 FUN__text__005829d0(int param_1,int param_2)

{
  int iVar1;
  undefined4 uVar2;
  size_t sVar3;
  size_t sVar4;
  undefined1 local_80 [120];
  uint local_8;
  
  local_8 = (uint)((ushort)param_1 & 0x3ff | 0x400);
  iVar1 = (*DAT_0080a688)(local_8,1,local_80,0x78);
  if (iVar1 == 0) {
    uVar2 = 0;
  }
  else {
    iVar1 = FUN__text__00582c40(local_80);
    if ((param_1 != iVar1) && (param_2 != 0)) {
      sVar3 = _GetPrimaryLen(DAT_0080a678);
      sVar4 = _strlen(DAT_0080a678);
      if (sVar3 == sVar4) {
        return 0;
      }
    }
    uVar2 = 1;
  }
  return uVar2;
}

