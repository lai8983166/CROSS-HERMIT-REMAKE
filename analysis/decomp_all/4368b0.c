
void __fastcall FUN__text__004368b0(int param_1)

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
  local_8 = param_1;
  FUN__text__004313f0(param_1 + 0x115d14);
  local_c = FUN__text__00431910(local_8 + 0x115d14);
  if (local_c == 0) {
    if (*(int *)(local_8 + 0x2e6f4) == 0) {
      local_14 = FUN__text__00431990(local_8 + 0x115d14,DAT_007f4490);
      if (local_14 == 0) {
        *(undefined4 *)(*(int *)(local_8 + 0x117c38) + 0x174) = 1;
      }
      else if (local_14 == 1) {
        *(undefined4 *)(*(int *)(local_8 + 0x117c38) + 0x174) = 5;
      }
      else {
        *(undefined4 *)(*(int *)(local_8 + 0x117c38) + 0x174) = 3;
      }
      local_c = local_14;
      FUN__text__004549d0(0,0,0,1,0,0,1);
    }
  }
  else {
    local_10 = FUN__text__00431a60(DAT_007f4490);
    if (*(short *)(local_8 + 0x116074 + local_10 * 2) == 0) {
      *(undefined4 *)(*(int *)(local_8 + 0x117c38) + 0x174) = 5;
    }
    else {
      *(undefined4 *)(*(int *)(local_8 + 0x117c38) + 0x174) = 1;
    }
    FUN__text__004549d0(0,0,0,1,0,0,1);
  }
  local_8 = 0x436a17;
  FUN__text__0056ce80();
  return;
}

