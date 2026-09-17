
void FUN__text__00457aa0(void)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined8 uVar4;
  undefined4 local_5c [16];
  int local_1c;
  int local_18;
  undefined1 local_14;
  char local_10;
  undefined4 local_c;
  int local_8;
  
  puVar3 = local_5c;
  for (iVar2 = 0x16; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  iVar2 = FUN__text__004577f0();
  if ((iVar2 != 0) && (iVar2 = FUN__text__004263b0(DAT_007a49fc), iVar2 != 0)) {
    iVar2 = FUN__text__00456b20();
    if (iVar2 == 0) {
      local_c = FUN__text__004264d0();
    }
    else {
      local_1c = FUN__text__0041ae70();
      local_10 = FUN__text__0041ad60();
      local_1c = local_1c + local_10 * 0x88;
      local_c = FUN__text__00426500(local_1c + 2,&DAT_005983e0);
    }
    (*API_KERNEL32_DLL_lstrlenA)(local_c);
    local_18 = FUN__text__0056ce80();
    if (local_18 != 0) {
      FUN__text__004254c0(local_c);
      iVar2 = FUN__text__00456b20();
      if (iVar2 != 0) {
        if (*(char *)(local_8 + 0x18c) == '\0') {
          local_14 = 0xff;
        }
        else {
          local_14 = 4;
        }
        local_10 = FUN__text__0041ad60();
        iVar2 = (int)local_10;
        if (iVar2 == -1) {
          uVar4 = FUN__text__00424f80("myno != -1",
                                      "E:\\CrossHermit\\GAME\\src\\yoshida\\TacticsTask.cpp",
                                      DAT_0060cdd0 + 0x1a,0);
          iVar2 = (int)((ulonglong)uVar4 >> 0x20);
          if ((int)uVar4 != 0) {
            pcVar1 = (code *)swi(3);
            (*pcVar1)();
            return;
          }
        }
        FUN__text__00457e00(local_10,CONCAT31((int3)((uint)iVar2 >> 8),local_14),local_c);
      }
      FUN__text__00425a50();
    }
  }
  local_8 = 0x457c36;
  FUN__text__0056ce80();
  return;
}

