
void FUN__text__00480480(undefined4 param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_50 [16];
  undefined4 local_10;
  int local_c;
  undefined4 local_8;
  
  puVar2 = local_50;
  for (iVar1 = 0x13; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_c = FUN__text__0047a8e0(param_1);
  iVar1 = FUN__text__00468d80(param_1);
  if ((((iVar1 == 0) && (iVar1 = FUN__text__00469ad0(param_1), iVar1 == 0)) &&
      (*(int *)(local_c + 0x20) != 0)) &&
     (*(int *)(local_c + 0x34) = *(int *)(local_c + 0x34) + 1,
     *(int *)(local_c + 0x20) <= *(int *)(local_c + 0x34))) {
    *(undefined4 *)(local_c + 0x34) = 0;
    local_10 = FUN__text__00480740(param_1);
  }
  local_8 = 0x480533;
  FUN__text__0056ce80();
  return;
}

