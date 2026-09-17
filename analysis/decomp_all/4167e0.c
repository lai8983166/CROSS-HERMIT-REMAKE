
void __thiscall FUN__text__004167e0(int param_1,int param_2,undefined4 param_3,undefined4 param_4)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_4c [16];
  undefined4 local_c;
  int local_8;
  
  puVar3 = local_4c;
  for (iVar2 = 0x12; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_8 = param_1;
  if (param_2 == 0) {
    iVar2 = FUN__text__00424f80("addr!=0","E:\\CrossHermit\\GAME\\src\\system\\directx\\DxMain.cpp",
                                DAT_005ff54c + 2,0);
    if (iVar2 != 0) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
  }
  local_c = FUN__text__0041f090(*(undefined4 *)(local_8 + 0xb210),param_2,param_3,param_4);
  local_8 = 0x41685e;
  FUN__text__0056ce80();
  return;
}

