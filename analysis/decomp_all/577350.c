
undefined4 __thiscall FUN__text__00577350(undefined4 param_1,uint param_2)

{
  undefined4 *puVar1;
  undefined4 uVar2;
  
  if ((param_2 < DAT_0080a900) &&
     ((*(byte *)((&DAT_0080a800)[(int)param_2 >> 5] + 4 + (param_2 & 0x1f) * 0x24) & 1) != 0)) {
    FUN__text__00586620(param_2,param_1);
    uVar2 = __close_lk(param_2);
    FUN__text__005866b0(param_2);
  }
  else {
    puVar1 = (undefined4 *)FUN__text__00576d20();
    *puVar1 = 9;
    puVar1 = (undefined4 *)FUN__text__00576d30();
    *puVar1 = 0;
    uVar2 = 0xffffffff;
  }
  return uVar2;
}

