
void __fastcall FUN__text__00414c30(int param_1)

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
  if (*(int *)(param_1 + 0xb210) != 0) {
    *(undefined4 *)(param_1 + 0xb200) = 0;
    *(int *)(param_1 + 0xb1c0) = *(int *)(param_1 + 0xb1c0) + 1;
    local_8 = param_1;
    FUN__text__004155d0();
    (**(code **)(**(int **)(local_8 + 0xb210) + 0x88))(*(undefined4 *)(local_8 + 0xb210));
    local_c = FUN__text__0056ce80();
    if ((local_c != 0) && (local_c == -0x7789fe3e)) {
      iVar2 = FUN__text__00413f00();
      if (iVar2 != 0) goto LAB__text__00414dc1;
      *(undefined4 *)(local_8 + 0xb280) = 1;
      (**(code **)(**(int **)(local_8 + 0xb210) + 0x88))(*(undefined4 *)(local_8 + 0xb210));
      local_c = FUN__text__0056ce80();
    }
    if ((local_c != 0) &&
       (iVar2 = FUN__text__00424f80("ret==((HRESULT)0x00000000L)",
                                    "E:\\CrossHermit\\GAME\\src\\system\\directx\\DxMain.cpp",
                                    DAT_005ff53c + 0x26,0), iVar2 != 0)) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
    *(undefined4 *)(local_8 + 0xb200) = 1;
    (**(code **)(**(int **)(local_8 + 0xb210) + 0x90))
              (*(undefined4 *)(local_8 + 0xb210),0,0,1,
               (uint)*(byte *)(local_8 + 0xb276) << 0x10 | 0xff000000 |
               (uint)*(byte *)(local_8 + 0xb275) << 8 | (uint)*(byte *)(local_8 + 0xb274),0,0);
    local_c = FUN__text__0056ce80();
    FUN__text__00414610();
  }
LAB__text__00414dc1:
  local_8 = 0x414dce;
  FUN__text__0056ce80();
  return;
}

