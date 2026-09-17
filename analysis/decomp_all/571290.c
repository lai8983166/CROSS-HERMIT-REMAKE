
undefined4 __thiscall FUN__text__00571290(undefined4 param_1,undefined4 param_2)

{
  uint uVar1;
  int iVar2;
  
  FUN__text__0056e450(param_1);
  uVar1 = FUN__text__0056f830(DAT_0080bb88,2);
  if (uVar1 < (uint)((int)DAT_0080bb84 + (4 - DAT_0080bb88))) {
    iVar2 = FUN__text__0056f830(DAT_0080bb88,2,2,"onexit.c",0x68);
    iVar2 = FID_conflict___realloc_dbg(DAT_0080bb88,iVar2 + 0x10);
    if (iVar2 == 0) {
      FUN__text__0056e460();
      return 0;
    }
    DAT_0080bb84 = (undefined4 *)(iVar2 + ((int)DAT_0080bb84 - DAT_0080bb88 >> 2) * 4);
    DAT_0080bb88 = iVar2;
  }
  *DAT_0080bb84 = param_2;
  DAT_0080bb84 = DAT_0080bb84 + 1;
  FUN__text__0056e460();
  return param_2;
}

