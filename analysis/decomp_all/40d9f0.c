
void __fastcall FUN__text__0040d9f0(int param_1)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_4c [11];
  undefined4 uStack_20;
  int local_c;
  int local_8;
  
  puVar3 = local_4c;
  for (iVar2 = 0x12; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  *(undefined4 *)(param_1 + 0x28) = 10000;
  *(undefined4 *)(param_1 + 0x2c) = 0;
  local_8 = param_1;
  (**(code **)(**(int **)(param_1 + 4) + 0x5c))
            (*(undefined4 *)(param_1 + 4),*(int *)(param_1 + 0x28) << 7,0x208,0x1c4,0,param_1 + 0x24
            );
  local_c = FUN__text__0056ce80();
  if ((local_c < 0) &&
     (iVar2 = FUN__text__00424f80("((HRESULT)(ret) >= 0)",
                                  "E:\\CrossHermit\\GAME\\src\\system\\directx\\DxDraw.cpp",
                                  DAT_005ff348 + 0xe,0), iVar2 != 0)) {
    pcVar1 = (code *)swi(3);
    (*pcVar1)();
    return;
  }
  uStack_20 = 0x40daa5;
  FUN__text__0056ce80();
  return;
}

