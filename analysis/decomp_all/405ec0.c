
void __thiscall FUN__text__00405ec0(int param_1,int *param_2,int param_3)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_78 [16];
  int local_38;
  int local_34;
  undefined1 local_30 [32];
  undefined4 local_10;
  undefined4 local_c;
  int local_8;
  
  puVar2 = local_78;
  for (iVar1 = 0x1d; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_38 = param_3;
  local_8 = param_1;
  if (param_3 == 0) {
    (**(code **)(**(int **)(param_1 + 0x2c) + 0x38))(*(undefined4 *)(param_1 + 0x2c),0,local_30);
    local_34 = FUN__text__0056ce80();
    if (local_34 < 0) goto LAB__text__00405fd4;
    (**(code **)(**(int **)(local_8 + 0x2c) + 0x3c))(*(undefined4 *)(local_8 + 0x2c),0,&local_c);
    local_34 = FUN__text__0056ce80();
    if (local_34 < 0) goto LAB__text__00405fd4;
  }
  else if (param_3 == 1) {
    if (*(int *)(param_1 + 0x30) == 0) goto LAB__text__00405fd4;
    local_c = *(undefined4 *)(param_1 + 0x30);
  }
  (**(code **)(*param_2 + 0x84))(param_2,&local_10);
  local_34 = FUN__text__0056ce80();
  if (local_34 != 0) {
    local_10 = 0;
  }
  (**(code **)(*param_2 + 0x7c))(param_2,local_c,local_10);
  local_34 = FUN__text__0056ce80();
LAB__text__00405fd4:
  local_8 = 0x405fe1;
  FUN__text__0056ce80();
  return;
}

