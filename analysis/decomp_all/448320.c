
void __fastcall FUN__text__00448320(int param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_58 [16];
  int local_18;
  int local_14;
  uint local_10;
  int local_c;
  int local_8;
  
  puVar2 = local_58;
  for (iVar1 = 0x15; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_14 = param_1 + 0x1a54;
  local_10 = *(uint *)(DAT_007a49fc + 0x199c) & 1;
  local_8 = param_1;
  local_c = FUN__text__0044c710(&DAT_00605cf8,2);
  if ((local_c != -1) && (local_10 != 0)) {
    if (local_c == 0) {
      *(undefined1 *)(local_14 + 0x4e) = 0;
    }
    else if (local_c == 1) {
      *(undefined1 *)(local_14 + 0x4e) = 1;
    }
    local_18 = local_c;
    FUN__text__004db2b0(5);
  }
  local_8 = 0x4483bc;
  FUN__text__0056ce80();
  return;
}

