
void __thiscall FUN__text__00414f90(int param_1,char param_2)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_48 [16];
  int local_8;
  
  puVar3 = local_48;
  for (iVar2 = 0x11; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_8 = param_1;
  if ((param_2 < '\0') || ('\x03' < param_2)) {
    iVar2 = FUN__text__00424f80("(0<=type)&&(type<=3)",
                                "E:\\CrossHermit\\GAME\\src\\system\\directx\\DxMain.cpp",
                                DAT_005ff544 + 1,0);
    if (iVar2 != 0) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
  }
  *(char *)(local_8 + 0xb17c) = param_2;
  local_8 = 0x414ffb;
  FUN__text__0056ce80();
  return;
}

