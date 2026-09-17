
void __thiscall FUN__text__004940b0(int param_1,int param_2)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_54 [16];
  int local_14;
  int local_10;
  int local_c;
  int local_8;
  
  puVar2 = local_54;
  for (iVar1 = 0x14; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  if (*(int *)(param_1 + 0x108b50) != 0) {
    local_c = param_1 + 0x116098 + param_2 * 0x2c;
    local_8 = param_1;
    FUN__text__00493fe0(local_c);
    local_14 = *(int *)(local_8 + 0x108b50);
    while (local_14 = local_14 + -1, -1 < local_14) {
      iVar1 = FUN__text__0046a4c0(*(undefined4 *)(local_8 + 0x108b60 + local_14 * 4));
      if (iVar1 != 0) {
        local_10 = FUN__text__00427d60();
        *(undefined4 *)(local_10 + 8) = *(undefined4 *)(local_8 + 0x108b60 + local_14 * 4);
        FUN__text__00427e30(local_10);
        *(undefined1 *)(*(int *)(*(int *)(local_8 + 0x108b60 + local_14 * 4) + 600) + 0x98) =
             (undefined1)param_2;
      }
    }
  }
  local_8 = 0x494192;
  FUN__text__0056ce80();
  return;
}

