
void __thiscall FUN__text__0040e210(int param_1,undefined4 param_2)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_4c [14];
  undefined4 uStack_14;
  int local_c;
  int local_8;
  
  puVar3 = local_4c;
  for (iVar2 = 0x12; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_8 = param_1;
  (**(code **)(**(int **)(param_1 + 4) + 0xf4))(*(undefined4 *)(param_1 + 4),0,param_2);
  local_c = FUN__text__0056ce80();
  if (local_c != 0) {
    iVar2 = FUN__text__00424f80("ret==((HRESULT)0x00000000L)",
                                "E:\\CrossHermit\\GAME\\src\\system\\directx\\DxDraw.cpp",
                                DAT_005ff354 + 0xb,0);
    if (iVar2 != 0) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
  }
  *(undefined4 *)(local_8 + 0x34) = param_2;
  uStack_14 = 0x40e294;
  FUN__text__0056ce80();
  return;
}

