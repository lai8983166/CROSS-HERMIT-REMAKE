
void __thiscall FUN__text__0041ed80(int param_1,int param_2,undefined2 *param_3,undefined2 *param_4)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_4c [16];
  int local_c;
  int local_8;
  
  puVar3 = local_4c;
  for (iVar2 = 0x12; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  *param_4 = 0;
  *param_3 = 0;
  if (*(int *)(param_1 + 4) == 0) {
    local_8 = param_1;
    iVar2 = FUN__text__00424f80(&DAT_005924d4,
                                "E:\\CrossHermit\\GAME\\src\\system\\directx\\DxTexPos.cpp",
                                DAT_005ff5c4 + 4,0);
    if (iVar2 != 0) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
  }
  else {
    local_c = *(int *)(param_1 + 4) + param_2 * 8;
    *param_3 = *(undefined2 *)(local_c + 4);
    *param_4 = *(undefined2 *)(local_c + 6);
  }
  local_8 = 0x41ee1f;
  FUN__text__0056ce80();
  return;
}

