
void FUN__text__0046b350(int param_1,undefined4 param_2)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_50 [16];
  int local_10;
  int local_c;
  undefined4 local_8;
  
  puVar2 = local_50;
  for (iVar1 = 0x13; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_c = (int)((*(int *)(param_1 + 0x2ec) >> 0x10) + (*(int *)(param_1 + 0x2ec) >> 0x1f & 0x1fU))
            >> 5;
  local_10 = (int)((*(int *)(param_1 + 0x2f0) >> 0x10) + (*(int *)(param_1 + 0x2f0) >> 0x1f & 0xfU))
             >> 4;
  FUN__text__0043b8b0(local_c,local_10,*(undefined1 *)(*(int *)(param_1 + 600) + 0x30),param_2);
  local_8 = 0x46b3d3;
  FUN__text__0056ce80();
  return;
}

