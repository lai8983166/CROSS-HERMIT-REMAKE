
void FUN__text__0040bbd0(void *param_1)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_50 [16];
  int local_10;
  int local_c;
  undefined4 local_8;
  
  puVar3 = local_50;
  for (iVar2 = 0x13; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  _memset(param_1,0,0x1828);
  local_10 = FUN__text__00427650(0x200);
  if (local_10 != 0) {
    iVar2 = FUN__text__00424f80("ret==0",
                                "E:\\CrossHermit\\GAME\\SRC\\System\\DIRECTX\\DxAnimDataCtrl.cpp",
                                DAT_005ff110 + 6,0);
    if (iVar2 != 0) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
  }
  for (local_c = 0; local_c != 0x200; local_c = local_c + 1) {
    FUN__text__00427890(local_c,(int)param_1 + local_c * 0xc + 0x28);
  }
  local_8 = 0x40bc80;
  FUN__text__0056ce80();
  return;
}

