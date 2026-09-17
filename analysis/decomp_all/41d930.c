
void FUN__text__0041d930(undefined4 param_1,undefined4 param_2)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_54 [16];
  undefined1 local_14 [8];
  int local_c;
  int local_8;
  
  puVar2 = local_54;
  for (iVar1 = 0x14; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  iVar1 = FUN__text__0041d790();
  if (iVar1 != 0) {
    (**(code **)(**(int **)(local_8 + 0xc) + 0x3c))(*(undefined4 *)(local_8 + 0xc),local_14);
    local_c = FUN__text__0056ce80();
    if (local_c < 0) {
      FUN__text__0041d040(local_c);
    }
    else {
      *(undefined4 *)(local_8 + 600) = param_1;
      *(undefined4 *)(local_8 + 0x25c) = param_2;
      (**(code **)(**(int **)(local_8 + 0xc) + 0x38))
                (*(undefined4 *)(local_8 + 0xc),*(undefined4 *)(local_8 + 600),
                 *(undefined4 *)(local_8 + 0x25c));
      local_c = FUN__text__0056ce80();
      if (local_c < 0) {
        FUN__text__0041d040(local_c);
      }
    }
  }
  local_8 = 0x41da0a;
  FUN__text__0056ce80();
  return;
}

