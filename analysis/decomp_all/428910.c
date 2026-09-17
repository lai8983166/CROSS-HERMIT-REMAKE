
void FUN__text__00428910(void)

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
  FUN__text__0042b2d0(&DAT_00594e54,DAT_0079fc74);
  local_8 = FUN__text__005709d0();
  if (local_8 != 0) {
    iVar2 = FUN__text__00424f80("ret==0","E:\\CrossHermit\\GAME\\src\\system\\SysMem.cpp",
                                DAT_005ff6d4 + 6,0);
    if (iVar2 != 0) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
  }
  local_8 = 0x42897a;
  FUN__text__0056ce80();
  return;
}

