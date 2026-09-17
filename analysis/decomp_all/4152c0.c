
void __thiscall FUN__text__004152c0(int param_1,int param_2)

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
  if (((param_2 < 0) || (0x34bc0 < param_2)) &&
     (iVar2 = FUN__text__00424f80("(0<=cnt)&&(cnt<=60*60*60)",
                                  "E:\\CrossHermit\\GAME\\src\\system\\directx\\DxMain.cpp",
                                  DAT_005ff548 + 1,0), iVar2 != 0)) {
    pcVar1 = (code *)swi(3);
    (*pcVar1)();
    return;
  }
  if (*(int *)(local_8 + 0xb180) == 1) {
    if (param_2 == 0) {
      param_2 = 1;
    }
    do {
      do {
        iVar2 = FUN__text__004150e0();
      } while (iVar2 != 1);
      param_2 = param_2 + -1;
    } while (param_2 != 0);
  }
  local_8 = 0x41535f;
  FUN__text__0056ce80();
  return;
}

