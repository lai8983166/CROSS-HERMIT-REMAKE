
void __fastcall FUN__text__00445800(int param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_54 [16];
  int local_14;
  int local_10;
  undefined4 local_c;
  int local_8;
  
  puVar2 = local_54;
  for (iVar1 = 0x14; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_c = 0;
  local_14 = *(int *)(param_1 + 0x1bb4);
  local_8 = param_1;
  if (local_14 == 0) {
    *(undefined4 *)(param_1 + 0x1bc0) = 1;
    *(int *)(param_1 + 0x1bb4) = *(int *)(param_1 + 0x1bb4) + 1;
  }
  else if (local_14 == 1) {
    if (*(int *)(param_1 + 0x1bc0) == 0) {
      *(int *)(param_1 + 0x1bb4) = *(int *)(param_1 + 0x1bb4) + 1;
    }
    else {
      *(int *)(param_1 + 0x1bc0) = *(int *)(param_1 + 0x1bc0) + -1;
    }
  }
  else if (local_14 == 2) {
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
  FUN__text__00446340(0xffffffff,0xff);
  FUN__text__0044ca80();
  FUN__text__0044c9a0(0);
  local_8 = 0x445917;
  FUN__text__0056ce80();
  return;
}

