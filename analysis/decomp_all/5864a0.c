
undefined4 FUN_005864a0(uint param_1)

{
  undefined4 *puVar1;
  undefined4 uVar2;
  
  if ((param_1 < DAT_0080a900) &&
     ((*(byte *)((&DAT_0080a800)[(int)param_1 >> 5] + 4 + (param_1 & 0x1f) * 0x24) & 1) != 0)) {
    uVar2 = *(undefined4 *)((&DAT_0080a800)[(int)param_1 >> 5] + (param_1 & 0x1f) * 0x24);
  }
  else {
    puVar1 = (undefined4 *)FUN_00576d20();
    *puVar1 = 9;
    puVar1 = (undefined4 *)FUN_00576d30();
    *puVar1 = 0;
    uVar2 = 0xffffffff;
  }
  return uVar2;
}

