
uint FUN__text__00586510(intptr_t param_1,uint param_2)

{
  int iVar1;
  ulong uVar2;
  uint uVar3;
  undefined4 *puVar4;
  byte local_10;
  
  local_10 = 0;
  if ((param_2 & 8) != 0) {
    local_10 = 0x20;
  }
  if ((param_2 & 0x4000) != 0) {
    local_10 = local_10 | 0x80;
  }
  if ((param_2 & 0x80) != 0) {
    local_10 = local_10 | 0x10;
  }
  iVar1 = (*DAT_00592104)(param_1);
  if (iVar1 == 0) {
    uVar2 = (*API_KERNEL32_DLL_GetLastError)();
    __dosmaperr(uVar2);
    uVar3 = 0xffffffff;
  }
  else {
    if (iVar1 == 2) {
      local_10 = local_10 | 0x40;
    }
    else if (iVar1 == 3) {
      local_10 = local_10 | 8;
    }
    uVar3 = FUN__text__00586110();
    if (uVar3 == 0xffffffff) {
      puVar4 = (undefined4 *)FUN__text__00576d20();
      *puVar4 = 0x18;
      puVar4 = (undefined4 *)FUN__text__00576d30();
      *puVar4 = 0;
      uVar3 = 0xffffffff;
    }
    else {
      __set_osfhnd(uVar3,param_1);
      *(byte *)((&DAT_0080a800)[(int)uVar3 >> 5] + 4 + (uVar3 & 0x1f) * 0x24) = local_10 | 1;
      FUN__text__005866b0(uVar3);
    }
  }
  return uVar3;
}

