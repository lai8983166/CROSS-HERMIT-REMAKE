
void FUN__text__0041e590(void)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_4c [16];
  int local_c;
  int local_8;
  
  puVar2 = local_4c;
  for (iVar1 = 0x12; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  iVar1 = FUN__text__0041d790();
  if ((iVar1 != 0) && (iVar1 = FUN__text__0041d7c0(), iVar1 == 0)) {
    (**(code **)(**(int **)(local_8 + 4) + 0x20))(*(undefined4 *)(local_8 + 4));
    local_c = FUN__text__0056ce80();
    if (-1 < local_c) {
      *(undefined1 *)(local_8 + 0x21) = 1;
    }
  }
  local_8 = 0x41e614;
  FUN__text__0056ce80();
  return;
}

