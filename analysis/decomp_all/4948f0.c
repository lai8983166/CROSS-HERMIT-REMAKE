
void __fastcall FUN__text__004948f0(int param_1)

{
  int iVar1;
  int iVar2;
  int iVar3;
  int iVar4;
  undefined4 *puVar5;
  undefined4 local_58 [16];
  int local_18;
  int local_14;
  undefined4 local_10;
  int local_c;
  int local_8;
  
  puVar5 = local_58;
  for (iVar2 = 0x15; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar5 = 0xcccccccc;
    puVar5 = puVar5 + 1;
  }
  for (local_c = 0; local_c != *(int *)(param_1 + 0x108b50); local_c = local_c + 1) {
    *(undefined1 *)(*(int *)(param_1 + 0x108b60 + local_c * 4) + 0x28c) = 0;
  }
  local_10 = 0;
  local_8 = param_1;
  for (local_c = 0; local_c != *(int *)(local_8 + 0xdc30c); local_c = local_c + 1) {
    iVar2 = *(int *)(*(int *)(local_8 + 0xdc310 + local_c * 4) + 0x2ec);
    iVar1 = *(int *)(*(int *)(local_8 + 0xdc310 + local_c * 4) + 0x2f0);
    local_18._0_2_ = (short)((uint)iVar1 >> 0x10);
    iVar3 = (int)(short)local_18;
    local_14._0_2_ = (short)((uint)iVar2 >> 0x10);
    iVar4 = (int)(short)local_14;
    local_18 = iVar1 >> 0x10;
    local_14 = iVar2 >> 0x10;
    iVar2 = FUN__text__0046b1a0(iVar4 - *(short *)(local_8 + 0x2a30e),
                                (iVar3 - *(short *)(local_8 + 0x2a310)) + 0x1e);
    if (iVar2 != 0) {
      iVar2 = FUN__text__00468d10(*(undefined4 *)(local_8 + 0xdc310 + local_c * 4));
      if (iVar2 != 0) {
        iVar2 = FUN__text__0046a4c0(*(undefined4 *)(local_8 + 0xdc310 + local_c * 4));
        if (iVar2 != 0) {
          *(undefined1 *)(*(int *)(local_8 + 0xdc310 + local_c * 4) + 0x28c) = 1;
          local_10 = 1;
        }
      }
    }
  }
  FUN__text__0046f170();
  local_8 = 0x494a3f;
  FUN__text__0056ce80();
  return;
}

