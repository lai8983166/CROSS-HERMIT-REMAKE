
void FUN__text__004396e0(void)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_4c [16];
  int local_c;
  undefined4 local_8;
  
  puVar3 = local_4c;
  for (iVar2 = 0x12; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_c = FUN__text__00427d60();
  if (local_c == 0) {
    iVar2 = FUN__text__00424f80("list!=0","E:\\CrossHermit\\GAME\\src\\YOSHIDA\\FindPath.CPP",
                                DAT_005ff9b8 + 4,0);
    if (iVar2 != 0) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
  }
  local_8 = 0x439745;
  FUN__text__0056ce80();
  return;
}

