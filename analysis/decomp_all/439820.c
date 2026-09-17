
void __thiscall FUN__text__00439820(int param_1,int param_2,int param_3)

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
  if (*(int *)(param_1 + 0x30) <= param_2) {
    iVar2 = FUN__text__00424f80("x<cellw","E:\\CrossHermit\\GAME\\src\\YOSHIDA\\FindPath.CPP",
                                DAT_005ff9c0 + 1,0);
    if (iVar2 != 0) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
  }
  if (*(int *)(local_8 + 0x34) <= param_3) {
    iVar2 = FUN__text__00424f80("y<cellh","E:\\CrossHermit\\GAME\\src\\YOSHIDA\\FindPath.CPP",
                                DAT_005ff9c0 + 2,0);
    if (iVar2 != 0) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
  }
  local_8 = 0x4398c1;
  FUN__text__0056ce80();
  return;
}

