
void __fastcall FUN__text__00414de0(int param_1)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_50 [16];
  int local_10;
  int local_c;
  int local_8;
  
  puVar3 = local_50;
  for (iVar2 = 0x13; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  if (*(int *)(param_1 + 0xb210) != 0) {
    local_8 = param_1;
    if ((*(int *)(param_1 + 0xb200) != 1) &&
       (iVar2 = FUN__text__00424f80("DrawEnable==1",
                                    "E:\\CrossHermit\\GAME\\src\\system\\directx\\DxMain.cpp",
                                    DAT_005ff540 + 5,0), iVar2 != 0)) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
    if (*(int *)(local_8 + 0xb200) == 1) {
      (**(code **)(**(int **)(local_8 + 0xb210) + 0x8c))(*(undefined4 *)(local_8 + 0xb210));
      local_c = FUN__text__0056ce80();
      if ((local_c < 0) &&
         (iVar2 = FUN__text__00424f80("((HRESULT)(ret) >= 0)",
                                      "E:\\CrossHermit\\GAME\\src\\system\\directx\\DxMain.cpp",
                                      DAT_005ff540 + 0x2a,0), iVar2 != 0)) {
        pcVar1 = (code *)swi(3);
        (*pcVar1)();
        return;
      }
      (**(code **)(**(int **)(local_8 + 0xb210) + 0x3c))(*(undefined4 *)(local_8 + 0xb210),0,0,0,0);
      local_c = FUN__text__0056ce80();
      if ((-1 < local_c) ||
         ((local_10 = local_c, local_c == -0x7789f798 && (iVar2 = FUN__text__00413f00(), iVar2 == 0)
          ))) {
        *(undefined4 *)(local_8 + 0xb200) = 0;
      }
    }
  }
  local_8 = 0x414f25;
  FUN__text__0056ce80();
  return;
}

