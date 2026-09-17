
void __thiscall
FUN__text__0046beb0(int param_1,int param_2,int param_3,undefined4 param_4,undefined4 param_5,
                   int param_6,undefined4 *param_7)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_48 [16];
  int local_8;
  
  puVar2 = local_48;
  for (iVar1 = 0x11; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_8 = param_1;
  if (param_6 != 0) {
    FUN__text__0040ad20(param_2 + 0xa0 + param_6 * 0x58);
  }
  if (param_3 != -1) {
    if ((param_6 == 0) && (param_7 != (undefined4 *)0x0)) {
      *(undefined4 *)(param_2 + 0xe8) = *param_7;
      *(undefined4 *)(param_2 + 0xec) = param_7[1];
      *(undefined4 *)(param_2 + 0xf0) = param_7[2];
    }
    FUN__text__00465140(param_2 + 0xa0 + param_6 * 0x58,*(undefined4 *)(local_8 + 0x2a6e8),param_3,
                        param_4,param_5,7);
  }
  local_8 = 0x46bf65;
  FUN__text__0056ce80();
  return;
}

