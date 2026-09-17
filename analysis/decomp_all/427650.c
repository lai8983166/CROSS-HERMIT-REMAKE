
void __thiscall FUN__text__00427650(int *param_1,int param_2)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_50 [16];
  int local_10;
  int local_c;
  int *local_8;
  
  puVar3 = local_50;
  for (iVar2 = 0x13; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_8 = param_1;
  if ((param_2 < 1) &&
     (iVar2 = FUN__text__00424f80("0<cnt","e:\\crosshermit\\game\\src\\system\\syslinklist.cpp",
                                  DAT_005ff6a4 + 4,0), iVar2 != 0)) {
    pcVar1 = (code *)swi(3);
    (*pcVar1)();
    return;
  }
  if ((*local_8 != 0) &&
     (iVar2 = FUN__text__00424f80("ListCnt==0","e:\\crosshermit\\game\\src\\system\\syslinklist.cpp"
                                  ,DAT_005ff6a4 + 6,0), iVar2 != 0)) {
    pcVar1 = (code *)swi(3);
    (*pcVar1)();
    return;
  }
  if (*local_8 == 0) {
    local_10 = FUN__text__00428a40(param_2 * 0xc);
    local_8[1] = local_10;
    if ((local_8[1] == 0) &&
       (iVar2 = FUN__text__00424f80("ListWork!=0",
                                    "e:\\crosshermit\\game\\src\\system\\syslinklist.cpp",
                                    DAT_005ff6a4 + 10,0), iVar2 != 0)) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
    if (local_8[1] != 0) {
      *local_8 = param_2;
      _memset((void *)local_8[1],0,*local_8 * 0xc);
      for (local_c = 0; local_c != *local_8; local_c = local_c + 1) {
        FUN__text__00427cd0(local_8[1] + local_c * 0xc);
      }
    }
  }
  local_8 = (int *)0x427793;
  FUN__text__0056ce80();
  return;
}

