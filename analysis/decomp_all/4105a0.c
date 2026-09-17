
void FUN__text__004105a0(int param_1,int param_2,undefined2 param_3,undefined4 param_4,
                        undefined1 param_5)

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
  local_c = FUN__text__0040dcd0(7);
  *(undefined4 *)(local_c + 4) = 7;
  *(undefined1 *)(local_c + 8) = param_5;
  *(undefined4 *)(local_c + 0xc) = param_4;
  *(undefined2 *)(local_c + 10) = param_3;
  for (local_10 = 0; local_10 != param_2; local_10 = local_10 + 1) {
    *(undefined2 *)(local_c + 0x10 + local_10 * 4) = *(undefined2 *)(param_1 + local_10 * 4);
    *(undefined2 *)(local_c + 0x12 + local_10 * 4) = *(undefined2 *)(param_1 + 2 + local_10 * 4);
  }
  *(undefined1 *)(local_c + 9) = (undefined1)param_2;
  FUN__text__0040df20(local_c,param_3);
  local_8 = 0x41066d;
  FUN__text__0056ce80();
  return;
}

