
void FUN__text__004d73c0(undefined4 param_1,undefined4 *param_2)

{
  uint uVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 auStack_30760 [16];
  int iStack_30720;
  int iStack_3071c;
  short sStack_30718;
  uint uStack_30714;
  int iStack_306ec;
  undefined2 uStack_30574;
  short sStack_30572;
  undefined2 uStack_30570;
  undefined4 local_2c;
  undefined4 uStack_28;
  undefined4 local_24;
  undefined4 local_20;
  undefined4 local_1c;
  undefined4 local_18;
  undefined4 *local_14;
  
  FUN__text__0056e230();
  puVar3 = auStack_30760;
  for (iVar2 = 0xc1d7; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_14 = (undefined4 *)0x0;
  local_18 = 0x80;
  local_1c = 3;
  local_20 = 0;
  local_24 = 1;
  uStack_28 = 0x80000000;
  local_2c = param_1;
  (*DAT_005921ec)();
  local_24 = FUN__text__0056ce80();
  (*API_KERNEL32_DLL_GetFileTime)();
  FUN__text__0056ce80();
  (*API_KERNEL32_DLL_FileTimeToLocalFileTime)();
  FUN__text__0056ce80();
  (*API_KERNEL32_DLL_FileTimeToSystemTime)();
  FUN__text__0056ce80();
  (*DAT_00592270)();
  FUN__text__0056ce80();
  FUN__text__004d75a0();
  if ((sStack_30718 == 7) && (uVar1 = FUN__text__004e2c30(), uStack_30714 <= uVar1)) {
    iStack_3071c = 0;
    iStack_30720 = iStack_306ec;
    iStack_306ec = 0;
    iStack_3071c = FUN__text__004d76b0();
    if (iStack_3071c == iStack_30720) {
      local_1c = CONCAT22(uStack_30574,1);
      if (0xc < sStack_30572) {
        sStack_30572 = sStack_30572 + -0xc;
      }
      local_18 = CONCAT22(uStack_30570,sStack_30572);
      local_14 = &local_2c;
      puVar3 = &local_1c;
      for (iVar2 = 5; iVar2 != 0; iVar2 = iVar2 + -1) {
        *param_2 = *puVar3;
        puVar3 = puVar3 + 1;
        param_2 = param_2 + 1;
      }
    }
  }
  FUN__text__0056ce80();
  return;
}

