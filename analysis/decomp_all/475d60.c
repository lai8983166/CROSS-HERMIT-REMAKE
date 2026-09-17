
void FUN__text__00475d60(int param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_58 [16];
  int local_18;
  int local_14;
  char *local_10;
  char *local_c;
  undefined4 local_8;
  
  puVar2 = local_58;
  for (iVar1 = 0x15; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_c = (char *)(param_1 + 0x290);
  local_10 = (char *)(param_1 + 0x293);
  local_18 = (int)*local_10;
  switch(local_18) {
  case 0:
    FUN__text__0046c040(param_1,2);
    FUN__text__0046bcc0(param_1,0x12);
    iVar1 = FUN__text__00468eb0(param_1);
    if (iVar1 != 0) {
      FUN__text__0046be50(param_1,0x80f,0,0);
      iVar1 = FUN__text__00468eb0(param_1);
      if (iVar1 != 0) {
        FUN__text__0046be50(param_1,*(ushort *)(*(int *)(param_1 + 600) + 2) + 0x834,0,0);
      }
    }
    local_14 = FUN__text__0047a8e0(param_1);
    *(char *)(local_14 + 0x3c) =
         (char)((int)((*(int *)(param_1 + 0x2ec) >> 0x10) +
                     (*(int *)(param_1 + 0x2ec) >> 0x1f & 0x1fU)) >> 5);
    *(char *)(local_14 + 0x3d) =
         (char)((int)((*(int *)(param_1 + 0x2f0) >> 0x10) +
                     (*(int *)(param_1 + 0x2f0) >> 0x1f & 0xfU)) >> 4);
    *local_10 = *local_10 + '\x01';
    break;
  case 1:
    if (*(char *)(param_1 + 4) != '\0') {
      if (*local_c == '\x01') {
        FUN__text__0049ad90(param_1,0x65);
      }
      if (*local_c == '\x19') {
        FUN__text__0049ad90(param_1,0x7d);
      }
      *(short *)(param_1 + 10) = *(short *)(param_1 + 10) + 1;
      *local_10 = *local_10 + '\x01';
    }
    break;
  case 2:
    if (0x3b < *(short *)(param_1 + 10)) {
      *(undefined2 *)(param_1 + 10) = 0;
      *local_10 = *local_10 + '\x01';
    }
    break;
  case 3:
    if (0 < *(short *)(param_1 + 10)) {
      FUN__text__00475270(param_1,2);
      FUN__text__0046b0b0(param_1,0);
      FUN__text__0046b0f0(param_1,0);
    }
  }
  local_8 = 0x475f40;
  FUN__text__0056ce80();
  return;
}

