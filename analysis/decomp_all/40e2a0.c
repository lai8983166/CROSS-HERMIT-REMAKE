
void __thiscall FUN__text__0040e2a0(int *param_1,undefined4 param_2,undefined4 param_3,int param_4)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_58 [16];
  undefined4 local_18;
  int local_14;
  undefined4 local_10;
  undefined4 local_c;
  int *local_8;
  
  puVar2 = local_58;
  for (iVar1 = 0x15; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_c = 0;
  local_10 = 0;
  local_14 = *(int *)(*param_1 + 0xb278);
  local_18 = *(undefined4 *)(*param_1 + 0xb27c);
  local_8 = param_1;
  iVar1 = FUN__text__0056db00(param_2);
  if (iVar1 <= local_14 + param_4) {
    FUN__text__0056db00(param_3);
  }
  local_8 = (int *)0x40e329;
  FUN__text__0056ce80();
  return;
}

