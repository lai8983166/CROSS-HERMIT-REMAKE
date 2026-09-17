
void FUN__text__00428a40(int param_1)

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
  local_8 = __malloc_dbg(param_1,1,"E:\\CrossHermit\\GAME\\src\\system\\SysMem.cpp",DAT_005ff6d8 + 3
                        );
  DAT_0079fc74 = DAT_0079fc74 + param_1;
  if (local_8 == 0) {
    iVar2 = FUN__text__00424f80("addr!=0","E:\\CrossHermit\\GAME\\src\\system\\SysMem.cpp",
                                DAT_005ff6d8 + 10,0);
    if (iVar2 != 0) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
  }
  local_8 = 0x428ac2;
  FUN__text__0056ce80();
  return;
}

