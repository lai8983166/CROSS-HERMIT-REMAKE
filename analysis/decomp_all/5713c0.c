
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN__text__005713c0(void)

{
  uint uVar1;
  int iVar2;
  undefined4 uVar3;
  undefined4 uVar4;
  undefined4 uVar5;
  undefined4 uVar6;
  uint local_70;
  undefined1 local_60 [44];
  uint local_34;
  uint local_30;
  undefined1 *local_1c;
  _EXCEPTION_POINTERS *local_18;
  void *pvStack_14;
  undefined1 *puStack_10;
  undefined *puStack_c;
  undefined4 local_8;
  
  local_8 = 0xffffffff;
  puStack_c = &DAT_005f9d48;
  puStack_10 = &LAB__text__00576b9c;
  pvStack_14 = ExceptionList;
  local_1c = &stack0xffffff84;
  ExceptionList = &pvStack_14;
  uVar1 = (*DAT_005922e8)();
  _DAT_0080a3f8 = uVar1 >> 8 & 0xff;
  DAT_0080a3f4 = uVar1 & 0xff;
  _DAT_0080a3f0 = DAT_0080a3f4 * 0x100 + _DAT_0080a3f8;
  DAT_0080a3ec = uVar1 >> 0x10;
  iVar2 = FUN__text__0057b9d0(1);
  if (iVar2 == 0) {
    FUN__text__00571560(0x1c);
  }
  iVar2 = FUN__text__005752d0();
  if (iVar2 == 0) {
    FUN__text__00571560(0x10);
  }
  local_8 = 0;
  FUN__text__0057d5b0();
  DAT_0080bb74 = (*DAT_0059217c)();
  DAT_0080a460 = FUN__text__0057d390();
  FUN__text__0057ce80();
  FUN__text__0057cd30();
  FUN__text__0056e2a0();
  local_34 = 0;
  (*DAT_00592180)(local_60);
  uVar3 = FUN__text__0057cc70();
  if ((local_34 & 1) == 0) {
    local_70 = 10;
  }
  else {
    local_70 = local_30 & 0xffff;
  }
  uVar6 = 0;
  uVar5 = 0;
  uVar4 = (*DAT_005922c8)(0,0,uVar3,local_70);
  uVar3 = FUN__text__0049dd70(uVar4,uVar5,uVar6,uVar3);
  FUN__text__0056e2e0(uVar3);
  __XcptFilter(local_18->ExceptionRecord->ExceptionCode,local_18);
  return;
}

