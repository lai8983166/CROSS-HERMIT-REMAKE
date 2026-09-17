
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void __thiscall
FUN__text__00459350(int param_1,undefined4 param_2,uint param_3,undefined4 param_4,
                   undefined4 param_5)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_4c [16];
  uint local_c;
  int local_8;
  
  puVar2 = local_4c;
  for (iVar1 = 0x12; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  _DAT_007a4188 = *(undefined4 *)(param_1 + 0x10);
  local_c = param_3;
  if (param_3 < 0x1d) {
    if ((param_3 == 0x1c) || ((param_3 == 2 || (param_3 == 0x10)))) goto LAB__text__004593da;
  }
  else if ((param_3 == 0x110) || (param_3 == 0x111)) goto LAB__text__004593da;
  local_8 = param_1;
  FUN__text__00424a90(param_2,param_3,param_4,param_5);
LAB__text__004593da:
  local_8 = 0x4593e7;
  FUN__text__0056ce80();
  return;
}

