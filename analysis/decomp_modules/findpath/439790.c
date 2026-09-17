
void __fastcall FUN__text__00439790(int param_1)

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
  if (*(int *)(param_1 + 0x88) == 0) {
    iVar2 = FUN__text__00424f80("NodePos!=0","E:\\CrossHermit\\GAME\\src\\YOSHIDA\\FindPath.CPP",
                                DAT_005ff9bc + 2,0);
    if (iVar2 != 0) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
  }
  _memset(*(void **)(local_8 + 0x88),0,*(int *)(local_8 + 0x30) * 4 * *(int *)(local_8 + 0x34));
  local_8 = 0x43980f;
  FUN__text__0056ce80();
  return;
}

