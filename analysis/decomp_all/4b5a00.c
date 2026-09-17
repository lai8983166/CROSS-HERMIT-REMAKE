
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void __fastcall FUN__text__004b5a00(int param_1)

{
  undefined2 extraout_var;
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_48 [16];
  int local_8;
  
  puVar2 = local_48;
  for (iVar1 = 0x11; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  DAT_007d6a31 = 0;
  _DAT_007d6a4a = 0xffff;
  DAT_007d6a58 = 0xffff;
  DAT_007d6a50 = 0;
  DAT_007d6a52 = 0xffff;
  DAT_007d6a56 = 0xffff;
  DAT_007d6a36 = 0;
  DAT_007d6a38 = 0xffff;
  DAT_007d6a3a = 0xffff;
  DAT_007d6a3c = 0xffff;
  _DAT_007d6a3e = 0;
  DAT_007d6f66 = 0;
  *(undefined1 *)(param_1 + 0x62c) = 0;
  local_8 = param_1;
  FUN__text__004b6690(*(undefined2 *)(param_1 + 0x596 + DAT_007d6a34 * 2),0xffffffff,1,2);
  FUN__text__004b6690(CONCAT22(extraout_var,*(undefined2 *)(local_8 + 0x596 + DAT_007d6a34 * 2)),
                      0xffffffff,0,0);
  local_8 = 0x4b5ae9;
  FUN__text__0056ce80();
  return;
}

