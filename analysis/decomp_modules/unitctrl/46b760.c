
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void __thiscall FUN__text__0046b760(int param_1,int param_2,undefined4 param_3)

{
  undefined1 uVar1;
  char cVar2;
  int iVar3;
  undefined4 *puVar4;
  undefined4 local_54 [16];
  int local_14;
  int local_10;
  int local_c;
  int local_8;
  
  puVar4 = local_54;
  for (iVar3 = 0x14; iVar3 != 0; iVar3 = iVar3 + -1) {
    *puVar4 = 0xcccccccc;
    puVar4 = puVar4 + 1;
  }
  _DAT_007a49e0 = param_2;
  local_8 = param_1;
  if ((*(short *)(param_1 + 0x108b32) != 0) && (*(char *)(param_1 + 0x108b34) != '\0')) {
    *(byte *)(param_2 + 8) = *(byte *)(param_2 + 8) & 0x7f;
    FUN__text__0048d720(param_2,param_3);
    FUN__text__0048e2a0(param_2);
    iVar3 = FUN__text__00475700(param_2);
    if (iVar3 != 0) goto LAB__text__0046b9f7;
    FUN__text__00490350(param_2,param_3);
    uVar1 = FUN__text__0040a100(param_2 + 0x48);
    *(undefined1 *)(param_2 + 4) = uVar1;
    *(short *)(param_2 + 10) = *(short *)(param_2 + 10) + 1;
    for (local_c = 0; local_c != 5; local_c = local_c + 1) {
      FUN__text__0040a100(param_2 + 0xa0 + local_c * 0x58);
    }
    FUN__text__00482a30(param_2,param_3);
    FUN__text__004918d0(param_2,param_3);
    FUN__text__00493450(param_2);
    FUN__text__00472370(param_2);
    if (*(char *)(local_8 + 0x108b39) != '\0') {
      FUN__text__0046bc20(param_2,param_3);
    }
    FUN__text__00472770(param_2);
    FUN__text__00430400(param_2);
  }
  iVar3 = FUN__text__00469480(param_2);
  if (iVar3 != 0) {
    iVar3 = FUN__text__0046a430(param_2);
    if ((iVar3 != 0) || (iVar3 = FUN__text__0046a5e0(param_2), iVar3 != 0)) {
      iVar3 = (int)(short)((uint)*(undefined4 *)(param_2 + 0x2ec) >> 0x10);
      local_10 = (int)(iVar3 + (iVar3 >> 0x1f & 0x1fU)) >> 5;
      iVar3 = (int)(short)((uint)*(undefined4 *)(param_2 + 0x2f0) >> 0x10);
      local_14 = (int)(iVar3 + (iVar3 >> 0x1f & 0xfU)) >> 4;
      cVar2 = FUN__text__004ddbb0(param_2);
      FUN__text__0043d270(local_10,local_14,(int)cVar2);
    }
    FUN__text__0046b2c0(param_2);
    if ((*(char *)(param_2 + 0x4e7) != *(char *)(param_2 + 0x4e9)) ||
       (*(char *)(param_2 + 0x4e8) != *(char *)(param_2 + 0x4ea))) {
      FUN__text__0043c470(*(undefined1 *)(param_2 + 0x4e9),*(undefined1 *)(param_2 + 0x4ea),0);
      FUN__text__0043c470(*(undefined1 *)(param_2 + 0x4e7),*(undefined1 *)(param_2 + 0x4e8),1);
    }
  }
LAB__text__0046b9f7:
  local_8 = 0x46ba04;
  FUN__text__0056ce80();
  return;
}

