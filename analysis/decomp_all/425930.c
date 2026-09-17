
void __thiscall FUN__text__00425930(undefined4 *param_1,undefined4 param_2)

{
  undefined4 uVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_54 [16];
  undefined4 local_14;
  undefined4 local_10;
  int local_c;
  undefined4 *local_8;
  
  puVar3 = local_54;
  for (iVar2 = 0x14; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  *param_1 = param_2;
  local_8 = param_1;
  uVar1 = FUN__text__0056cd3e(*param_1);
  local_8[1] = uVar1;
  if (local_8[1] != 0) {
    uVar1 = FUN__text__0056cd38(local_8[1]);
    local_8[2] = uVar1;
    if (local_8[2] != 0) {
      (*API_USER32_DLL_GetKeyboardLayout)(0);
      uVar1 = FUN__text__0056ce80();
      local_8[3] = uVar1;
      local_c = FUN__text__0056cd32(local_8[3]);
      if (local_c != 0) {
        local_14 = 0;
        local_10 = 0;
        iVar2 = FUN__text__00425ac0();
        if (iVar2 == 0) goto LAB__text__004259f6;
      }
    }
  }
  FUN__text__004258c0();
LAB__text__004259f6:
  local_c = 0x425a03;
  FUN__text__0056ce80();
  return;
}

