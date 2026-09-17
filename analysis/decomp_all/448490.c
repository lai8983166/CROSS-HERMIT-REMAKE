
void FUN__text__00448490(void)

{
  code *pcVar1;
  int iVar2;
  int iVar3;
  undefined4 *puVar4;
  undefined4 local_54 [16];
  undefined1 local_14;
  char local_10;
  undefined4 local_c;
  int local_8;
  
  puVar4 = local_54;
  for (iVar3 = 0x14; iVar3 != 0; iVar3 = iVar3 + -1) {
    *puVar4 = 0xcccccccc;
    puVar4 = puVar4 + 1;
  }
  iVar3 = FUN__text__004263b0(DAT_007a49fc);
  if (iVar3 != 0) {
    local_c = FUN__text__00426500(local_8 + 0x1a60,&DAT_005983e0);
    (*API_KERNEL32_DLL_lstrlenA)(local_c);
    iVar3 = FUN__text__0056ce80();
    if (iVar3 != 0) {
      FUN__text__004254c0(local_c);
      if (*(char *)(local_8 + 0x1aa2) == '\0') {
        local_14 = 0xff;
      }
      else {
        local_14 = 4;
      }
      local_10 = FUN__text__0041ad60();
      iVar3 = (int)local_10;
      if (iVar3 == -1) {
        iVar2 = FUN__text__00424f80("myno != -1","E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\NetTask.cpp",
                                    DAT_00606734 + 0xe,0);
        iVar3 = 0;
        if (iVar2 != 0) {
          pcVar1 = (code *)swi(3);
          (*pcVar1)();
          return;
        }
      }
      FUN__text__004431a0(local_10,CONCAT31((int3)((uint)iVar3 >> 8),local_14),local_c);
      FUN__text__00425a50();
    }
  }
  local_8 = 0x4485a9;
  FUN__text__0056ce80();
  return;
}

