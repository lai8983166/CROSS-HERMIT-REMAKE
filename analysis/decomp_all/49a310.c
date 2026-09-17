
void __fastcall FUN__text__0049a310(int param_1)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_6c [16];
  undefined1 local_2c [4];
  undefined1 local_28 [4];
  undefined2 local_24;
  undefined2 local_20;
  int local_1c;
  undefined1 *local_18;
  int local_14;
  int local_10;
  int local_c;
  int local_8;
  
  puVar3 = local_6c;
  for (iVar2 = 0x1a; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_c = param_1 + 0x108b3e;
  local_20 = *(undefined2 *)(param_1 + 0x108b40);
  local_24 = *(undefined2 *)(param_1 + 0x108b42);
  local_8 = param_1;
  FUN__text__0043d4e0();
  local_10 = 0;
  do {
    if (local_10 == *(int *)(local_8 + 0x108b50)) {
      local_8 = 0x49a473;
      FUN__text__0056ce80();
      return;
    }
    iVar2 = FUN__text__0043d660(local_20,local_24,(int)*(char *)(local_c + 6),
                                *(undefined1 *)
                                 (*(int *)(*(int *)(local_8 + 0x108b60 + local_10 * 4) + 600) + 0x30
                                 ),local_28,local_2c);
    if (iVar2 != 0) {
      local_14 = FUN__text__00427d60();
      if (local_14 == 0) {
        iVar2 = FUN__text__00424f80("list!=0",
                                    "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlStMem.cpp",
                                    DAT_0061a068 + 0x16,0);
        if (iVar2 != 0) {
          pcVar1 = (code *)swi(3);
          (*pcVar1)();
          return;
        }
      }
      local_18 = *(undefined1 **)(local_14 + 8);
      local_1c = *(int *)(local_8 + 0x108b60 + local_10 * 4);
      *local_18 = 4;
      local_18[1] = *(undefined1 *)(local_1c + 2);
      local_18[2] = *(undefined1 *)(local_1c + 2);
      local_18[3] = local_28[0];
      local_18[4] = local_2c[0];
      FUN__text__00427e30(local_14);
    }
    local_10 = local_10 + 1;
  } while( true );
}

