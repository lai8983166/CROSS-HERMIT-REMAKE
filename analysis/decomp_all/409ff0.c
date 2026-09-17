
void __thiscall
FUN__text__00409ff0(int *param_1,int param_2,int param_3,int param_4,undefined1 param_5)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_54 [16];
  int local_14;
  int local_10;
  int local_c;
  int *local_8;
  
  puVar2 = local_54;
  for (iVar1 = 0x14; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_c = *(int *)(param_2 + 0x20);
  local_8 = param_1;
  while (local_c != 0) {
    local_10 = *(int *)(local_c + 0x20);
    if (*(char *)(local_c + 2) == '\0') {
      FUN__text__0040ab80(local_c);
    }
    local_c = local_10;
  }
  local_10 = 0;
  local_14 = FUN__text__00409f70(param_2,param_3);
  if (((*local_8 != 0) && (param_3 < 4)) && (param_4 < *(int *)(local_14 + 4))) {
    *(undefined1 *)(param_2 + 3) = param_5;
    *(undefined1 *)(param_2 + 8) = 0;
    *(undefined4 *)(param_2 + 0x18) = 7;
    *(undefined2 *)(param_2 + 0x12) = 0;
    *(undefined2 *)(param_2 + 0x14) = 0;
    *(int *)(param_2 + 0x24) = param_2;
    *(undefined1 *)(param_2 + 0xb) = 0;
    *(undefined2 *)(param_2 + 0x10) = 0;
    FUN__text__0040a400(param_2,param_3,param_4);
  }
  local_8 = (int *)0x40a0f7;
  FUN__text__0056ce80();
  return;
}

