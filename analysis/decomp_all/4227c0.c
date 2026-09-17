
void __thiscall
FUN__text__004227c0(int *param_1,undefined4 param_2,undefined4 param_3,undefined4 param_4,
                   undefined4 param_5)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_48 [16];
  int *local_8;
  
  puVar2 = local_48;
  for (iVar1 = 0x11; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_8 = param_1;
  if (*param_1 != 0) {
    FUN__text__00422680();
  }
  iVar1 = FUN__text__00422f20(param_2,param_3,param_4,param_5);
  *local_8 = iVar1;
  local_8 = (int *)0x422828;
  FUN__text__0056ce80();
  return;
}

