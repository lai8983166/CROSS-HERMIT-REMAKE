
void __fastcall FUN__text__00446a80(int param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_54 [16];
  undefined4 local_14;
  int local_10;
  undefined4 local_c;
  int local_8;
  
  puVar2 = local_54;
  for (iVar1 = 0x14; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_c = 0;
  local_14 = *(undefined4 *)(param_1 + 0x1bb4);
  local_8 = param_1;
  switch(local_14) {
  case 0:
    *(undefined4 *)(param_1 + 0x1bc0) = 1;
    *(int *)(param_1 + 0x1bb4) = *(int *)(param_1 + 0x1bb4) + 1;
    break;
  case 1:
    if (*(int *)(param_1 + 0x1bc0) == 0) {
      *(int *)(param_1 + 0x1bb4) = *(int *)(param_1 + 0x1bb4) + 1;
    }
    else {
      *(int *)(param_1 + 0x1bc0) = *(int *)(param_1 + 0x1bc0) + -1;
    }
    break;
  case 2:
    local_10 = FUN__text__004180b0();
    if (local_10 == 0) {
      *(int *)(local_8 + 0x1bb4) = *(int *)(local_8 + 0x1bb4) + 1;
    }
    else {
      *(undefined4 *)(local_8 + 0x1bb0) = 0xff;
      *(undefined4 *)(local_8 + 0x1bc4) = 0;
      *(undefined4 *)(local_8 + 0x1bc8) = 1;
    }
    break;
  case 3:
    iVar1 = FUN__text__004183e0(&DAT_005953ac);
    if (iVar1 == 0) {
      *(int *)(local_8 + 0x1bb4) = *(int *)(local_8 + 0x1bb4) + 1;
    }
    else {
      *(undefined4 *)(local_8 + 0x1bb0) = 0xff;
      *(undefined4 *)(local_8 + 0x1bc4) = 1;
      *(undefined4 *)(local_8 + 0x1bc8) = 1;
    }
    break;
  case 4:
    local_10 = FUN__text__0044c8b0();
    if (local_10 == 0) {
      *(undefined4 *)(local_8 + 0x1a50) = 9;
      local_c = 1;
    }
    else {
      *(undefined4 *)(local_8 + 0x1bb0) = 0xff;
      *(undefined4 *)(local_8 + 0x1bc4) = 3;
    }
  }
  FUN__text__00446c70(0xffffffff,0xff);
  FUN__text__0044ca80();
  FUN__text__0044c9a0(0);
  local_8 = 0x446c51;
  FUN__text__0056ce80();
  return;
}

