
void FUN__text__0040ec50(undefined4 param_1,undefined4 param_2,undefined2 param_3,undefined4 param_4
                        ,undefined1 param_5,undefined4 param_6)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_4c [16];
  int local_c;
  undefined4 local_8;
  
  puVar2 = local_4c;
  for (iVar1 = 0x12; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  iVar1 = FUN__text__0040e2a0(param_1,param_2,0x200,0x80);
  if (iVar1 == 0) {
    local_c = FUN__text__0040dcd0(3);
    *(undefined4 *)(local_c + 4) = 3;
    *(undefined2 *)(local_c + 8) = (undefined2)param_1;
    *(undefined2 *)(local_c + 10) = (undefined2)param_2;
    *(undefined4 *)(local_c + 0xc) = param_4;
    *(undefined1 *)(local_c + 0x10) = param_5;
    (*API_KERNEL32_DLL_lstrcpyA)(local_c + 0x11,param_6);
    FUN__text__0056ce80();
    FUN__text__0040df20(local_c,param_3);
  }
  local_8 = 0x40ed15;
  FUN__text__0056ce80();
  return;
}

